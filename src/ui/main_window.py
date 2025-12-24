'''
Janela principal da aplicação Titanium Suite.
'''
import customtkinter as ctk
from src.ui.frames.frame_manutencao import FrameManutencao
from src.ui.frames.frame_produtividade import FrameProdutividade
from src.ui.frames.frame_seguranca import FrameSeguranca
from src.ui.frames.frame_nuvem import FrameNuvem
from src.ui.frames.frame_imagens import FrameImagens
from src.ui.frames.frame_excel import FrameExcel
from src.ui.frames.frame_sistema import FrameSistema
from src.ui.frames.frame_dashboard import FrameDashboard

# Importa sistema de tooltips
try:
    from src.ui.components.tooltip import add_tooltip
    TOOLTIPS_ENABLED = True
except ImportError:
    TOOLTIPS_ENABLED = False
    print("⚠️ Sistema de tooltips nao encontrado. Execute sem tooltips.")

class TitaniumApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.logout_acionado = False

        # --- Configurações da Janela ---
        self.title("Titanium Suite Enterprise")
        self.geometry("1100x700")  # Janela mais estreita, sem painel lateral
        
        ctk.set_appearance_mode("Dark") 
        ctk.set_default_color_theme("blue")

        # --- Layout Principal (Grid 1x2) ---
        # Coluna 0 = Menu Lateral (Pequena)
        # Coluna 1 = Área de Conteúdo (Grande)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._criar_menu_lateral()
        self._criar_area_conteudo()
        
        self._adicionar_tooltips_menu()

        self.selecionar_menu("dashboard")

    def _criar_menu_lateral(self):
        self.frame_menu = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nsew")
        self.frame_menu.grid_rowconfigure(9, weight=1) # Espaço vazio no final (era 6)

        self.lbl_logo = ctk.CTkLabel(self.frame_menu, text="TITANIUM\nSUITE", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botões do Menu
        self.btn_dash = self._criar_botao_menu("🏠 Dashboard", "dashboard", 1)
        self.btn_manu = self._criar_botao_menu("🧹 Manutenção", "manutencao", 2)
        self.btn_prod = self._criar_botao_menu("⚡ Produtividade", "produtividade", 3)
        self.btn_secu = self._criar_botao_menu("🔒 Segurança", "seguranca", 4)
        self.btn_cloud = self._criar_botao_menu("☁️ Backup Nuvem", "nuvem", 5)
        self.btn_image = self._criar_botao_menu("🖼️ Imagens", "imagens", 6)
        self.btn_excel = self._criar_botao_menu("📊 Excel", "excel", 7)
        self.btn_sistema = self._criar_botao_menu("⚙️ Sistema", "sistema", 8)

        self.frame_menu.grid_rowconfigure(7, weight=1)

        self.btn_sair = ctk.CTkButton(self.frame_menu, text="🚪 Sair / Logout", fg_color="#ef233c", hover_color="#d90429", height=40, anchor="w", command=self.acao_logout)
        self.btn_sair.grid(row=10, column=0, padx=10, pady=10, sticky="ew")

        self.lbl_versao = ctk.CTkLabel(self.frame_menu, text="v2.1.0", text_color="gray")
        self.lbl_versao.grid(row=11, column=0, pady=10)
        
        self.btn_help = ctk.CTkButton(self.frame_menu, text="❓ Refazer Tutorial", fg_color="transparent", hover_color="#2b2b2b", height=30, command=self.refazer_tutorial)
        self.btn_help.grid(row=12, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        self.btn_seguranca = ctk.CTkButton(self.frame_menu, text="🛡️ Configurar Segurança", fg_color="transparent", hover_color="#2b2b2b", height=30, command=self.abrir_configuracao_seguranca)
        self.btn_seguranca.grid(row=13, column=0, padx=10, pady=(0, 10), sticky="ew")

    def _criar_botao_menu(self, texto, nome_comando, linha):
        btn = ctk.CTkButton(self.frame_menu, text=texto, height=40, corner_radius=5, fg_color="transparent", text_color=("gray10", "gray90"), anchor="w", font=ctk.CTkFont(size=14), command=lambda: self.selecionar_menu(nome_comando))
        btn.grid(row=linha, column=0, sticky="ew", padx=10, pady=5)
        return btn

    def _criar_area_conteudo(self):
        self.frame_conteudo = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_conteudo.grid(row=0, column=1, sticky="nsew", padx=(20, 10), pady=20) # Padding ajustado

        self.frames = {}

        self.frames["dashboard"] = FrameDashboard(self.frame_conteudo, master_app=self)
        self.frames["manutencao"] = FrameManutencao(self.frame_conteudo)
        self.frames["produtividade"] = FrameProdutividade(self.frame_conteudo)
        self.frames["seguranca"] = FrameSeguranca(self.frame_conteudo)
        self.frames["nuvem"] = FrameNuvem(self.frame_conteudo)
        self.frames["imagens"] = FrameImagens(self.frame_conteudo) # NOVO
        self.frames["excel"] = FrameExcel(self.frame_conteudo)
        self.frames["sistema"] = FrameSistema(self.frame_conteudo)

    def _adicionar_tooltips_menu(self):
        if not TOOLTIPS_ENABLED:
            return
        
        tooltips_menu = {
            self.btn_dash: "📊 Visão geral da saúde do sistema\nEstatísticas e ações rápidas",
            self.btn_manu: "🧹 Limpeza de arquivos temporários\nDiagnóstico de rede",
            self.btn_prod: "📄 Ferramentas para PDFs e QR Codes\nAumente sua produtividade",
            self.btn_secu: "🔒 Criptografia militar AES-256\nProteja seus documentos sensíveis",
            self.btn_cloud: "☁️ Backup automático no Google Drive\nSeus dados seguros na nuvem",
            self.btn_image: "🖼️ Ferramentas de Imagem em Lote\nRedimensionar, Converter e Comprimir",
            self.btn_excel: "📊 Automação de Planilhas Excel\nUnir, Converter e Limpar Dados",
            self.btn_sistema: "⚙️ Ferramentas de Organização e Sistema\nDuplicados, Renomeação e Organização de Pastas",
            self.btn_sair: "🚪 Volta para tela de login\nNão encerra o programa",
            self.btn_help: "❓ Refaz o tutorial de primeira execução\nÚtil se você pulou algum passo"
        }
        
        for widget, texto in tooltips_menu.items():
            add_tooltip(widget, texto)

    def selecionar_menu(self, nome):
        for frame in self.frames.values():
            frame.grid_forget()

        self.frames[nome].grid(row=0, column=0, sticky="nsew")

        botoes = {
            "dashboard": self.btn_dash,
            "manutencao": self.btn_manu,
            "produtividade": self.btn_prod,
            "seguranca": self.btn_secu,
            "nuvem": self.btn_cloud,
            "imagens": self.btn_image, # NOVO
            "excel": self.btn_excel, # NOVO
            "sistema": self.btn_sistema # NOVO
        }

        for nome_btn, btn in botoes.items():
            if nome_btn == nome:
                btn.configure(fg_color=('gray75', 'gray25'))
            else:
                btn.configure(fg_color="transparent")

    def acao_logout(self):
        self.logout_acionado = True
        self.destroy()

    def refazer_tutorial(self):
        from src.ui.onboarding_wizard import OnboardingWizard
        wizard = OnboardingWizard(self)
        wizard.focus_force()
        wizard.wait_window()

    def abrir_configuracao_seguranca(self):
        from src.ui.configurar_seguranca_screen import ConfigurarSegurancaScreen
        config_screen = ConfigurarSegurancaScreen(self)
        config_screen.focus_force()
        config_screen.wait_window()
