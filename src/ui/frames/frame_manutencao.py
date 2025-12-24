import customtkinter as ctk
import threading
from src.modules.maintenance import SystemCleaner, NetworkTools
from src.ui.components.tooltip import add_tooltip
from src.ui.components.unified_console import UnifiedConsole

class FrameManutencao(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Layout: Grid 2 linhas (conteúdo + console)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)  # Console fixo na parte inferior
        self.grid_columnconfigure(0, weight=1)

        # === ÁREA DE CONTEÚDO ===
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        # Layout: Grid 2 colunas
        self.frame_conteudo.grid_columnconfigure(0, weight=1)
        self.frame_conteudo.grid_columnconfigure(1, weight=1)

        # --- Título ---
        self.lbl_titulo = ctk.CTkLabel(self.frame_conteudo, text="Manutenção do Sistema", 
                                       font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_titulo.grid(row=0, column=0, columnspan=2, pady=20, sticky="w")

        # --- Painel Esquerdo: Limpeza ---
        self.frame_clean = ctk.CTkFrame(self.frame_conteudo, width=400)
        self.frame_clean.grid(row=1, column=0, padx=10, pady=10, sticky="n")
        
        ctk.CTkLabel(self.frame_clean, text="Limpeza de Disco", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        self.chk_temp = ctk.CTkCheckBox(self.frame_clean, text="Arquivos Temporários (%TEMP%)")
        self.chk_temp.pack(pady=5, padx=20, anchor="w")
        self.chk_temp.select() # Marcado por padrão

        self.chk_dns = ctk.CTkCheckBox(self.frame_clean, text="Cache DNS (Internet)")
        self.chk_dns.pack(pady=5, padx=20, anchor="w")
        self.chk_dns.select()

        self.btn_limpar = ctk.CTkButton(self.frame_clean, text="🗑️ EXECUTAR LIMPEZA", 
                                        fg_color="#e63946", hover_color="#d62828",
                                        command=self.iniciar_limpeza_thread)
        self.btn_limpar.pack(pady=20)
        
        # Adicionar tooltips
        add_tooltip(self.btn_limpar, "btn_limpar_temp")
        add_tooltip(self.chk_temp, "Arquivos temporários ocupam espaço desnecessário.\nRecomendado executar semanalmente.")
        add_tooltip(self.chk_dns, "Limpa cache de DNS que pode causar problemas de navegação.\nÚtil quando sites não carregam corretamente.")

        # --- Painel Direito: Rede ---
        self.frame_net = ctk.CTkFrame(self.frame_conteudo, width=400)
        self.frame_net.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        ctk.CTkLabel(self.frame_net, text="Diagnóstico de Rede", font=ctk.CTkFont(weight="bold")).pack(pady=10)

        self.btn_ping = ctk.CTkButton(self.frame_net, text="📡 TESTAR CONEXÃO", 
                                      command=self.iniciar_ping_thread)
        self.btn_ping.pack(pady=10)
        
        # Adicionar tooltip
        add_tooltip(self.btn_ping, "btn_ping")

        # === CONSOLE UNIFICADO ===
        self.console = UnifiedConsole(self, height=100, title="📋 Console de Execução")
        self.console.grid(row=1, column=0, sticky="ew")
        self.console.log("Sistema de manutenção pronto. Selecione uma opção acima.", "info")

    # --- Funções de Controle ---
    
    def iniciar_limpeza_thread(self):
        """Roda em thread separada para não travar a tela"""
        threading.Thread(target=self._executar_limpeza).start()

    def _executar_limpeza(self):
        self.btn_limpar.configure(state="disabled")
        cleaner = SystemCleaner(logger_callback=self.console.log)
        
        if self.chk_temp.get():
            cleaner.limpar_temporarios()
        
        if self.chk_dns.get():
            cleaner.limpar_dns()
            
        self.console.log("--- Processo Finalizado ---", "info")
        self.btn_limpar.configure(state="normal")

    def iniciar_ping_thread(self):
        threading.Thread(target=self._executar_ping).start()

    def _executar_ping(self):
        net = NetworkTools(logger_callback=self.console.log)
        net.verificar_internet()
