import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from src.modules.cloud import DriveManager
from src.ui.components.tooltip import add_tooltip
from src.ui.components.unified_console import UnifiedConsole

class FrameNuvem(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        # Layout: Grid 2 linhas (conteúdo + console)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # === ÁREA DE CONTEÚDO ===
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        # Título
        ctk.CTkLabel(self.frame_conteudo, text="Backup em Nuvem (Google Drive)", 
                     font=ctk.CTkFont(size=24, weight="bold"), text_color="#3a86ff").pack(pady=20, anchor="w")

        # Abas
        self.tabview = ctk.CTkTabview(self.frame_conteudo, width=800, height=400)
        self.tabview.pack(fill="both", expand=True)

        self.tab_backup = self.tabview.add("Executar Backup")
        self.tab_config = self.tabview.add("Configuração")

        self._setup_config()
        self._setup_backup()
        
        # === CONSOLE UNIFICADO (criar primeiro para evitar erro) ===
        self.console = UnifiedConsole(self, height=100, title="📋 Console de Execução")
        self.console.grid(row=1, column=0, sticky="ew")
        self.console.log("Sistema de backup pronto. Configure suas credenciais para começar.", "info")
        
        # === Gerenciador (depois do console) ===
        self.drive = DriveManager(logger_callback=self.console.log)

    # ==========================
    # ABA CONFIGURAÇÃO
    # ==========================
    def _setup_config(self):
        tab = self.tab_config
        
        ctk.CTkLabel(tab, text="Passo 1: Cole abaixo o conteúdo do arquivo 'credentials.json':").pack(pady=10)
        
        self.txt_json = ctk.CTkTextbox(tab, height=150, width=600)
        self.txt_json.pack(pady=10)
        
        btn_salvar = ctk.CTkButton(tab, text="💾 Salvar Credenciais", command=self.acao_salvar_json)
        btn_salvar.pack(pady=10)
        add_tooltip(btn_salvar, "Salva as credenciais do Google Drive para autenticação futura.")

        ctk.CTkLabel(tab, text="Passo 2: Testar conexão (Abrirá o navegador na 1ª vez)").pack(pady=(20, 5))
        
        self.btn_conectar = ctk.CTkButton(tab, text="🔗 CONECTAR COM GOOGLE", fg_color="green", 
                                          command=self.acao_conectar)
        self.btn_conectar.pack(pady=5)
        add_tooltip(self.btn_conectar, "btn_conectar_drive")

    def acao_salvar_json(self):
        texto = self.txt_json.get("0.0", "end").strip()
        if not texto:
            messagebox.showwarning("Aviso", "A caixa de texto está vazia.")
            return

        sucesso, msg = self.drive.configurar_json_texto(texto)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.console.log("Credenciais salvas com sucesso!", "success")
        else:
            messagebox.showerror("Erro", msg)
            self.console.log(f"Erro ao salvar credenciais: {msg}", "error")

    def acao_conectar(self):
        threading.Thread(target=self.drive.conectar).start()

    # ==========================
    # ABA BACKUP
    # ==========================
    def _setup_backup(self):
        tab = self.tab_backup
        
        # Seleção de Origem
        frame_sel = ctk.CTkFrame(tab, fg_color="transparent")
        frame_sel.pack(pady=20)
        
        btn_select_pasta = ctk.CTkButton(frame_sel, text="📁 Selecionar Pasta Local", command=self.acao_select_pasta)
        btn_select_pasta.grid(row=0, column=0, padx=10)
        add_tooltip(btn_select_pasta, "btn_select_pasta")
        
        self.lbl_pasta = ctk.CTkLabel(frame_sel, text="Nenhuma pasta selecionada", text_color="gray")
        self.lbl_pasta.grid(row=0, column=1, padx=10)

        # Nome Destino
        ctk.CTkLabel(tab, text="Nome da Pasta no Google Drive:").pack(pady=(20, 5))
        self.entry_nome_drive = ctk.CTkEntry(tab, width=300, placeholder_text="Ex: Backup_Financeiro_2024")
        self.entry_nome_drive.pack()

        # Botão Ação
        self.btn_upload = ctk.CTkButton(tab, text="☁️ INICIAR UPLOAD", height=50, 
                                        font=("Arial", 16, "bold"),
                                        command=self.acao_upload)
        self.btn_upload.pack(pady=30)
        add_tooltip(self.btn_upload, "btn_upload")
        
        self.pasta_selecionada = None

    def acao_select_pasta(self):
        p = filedialog.askdirectory()
        if p:
            self.pasta_selecionada = p
            self.lbl_pasta.configure(text=p, text_color="white")

    def acao_upload(self):
        nome_destino = self.entry_nome_drive.get()
        
        if not self.pasta_selecionada or not nome_destino:
            messagebox.showwarning("Atenção", "Selecione uma pasta e defina um nome para o destino.")
            return

        # Desabilita botão
        self.btn_upload.configure(state="disabled", text="Enviando...")
        
        def task():
            self.drive.fazer_backup_pasta(self.pasta_selecionada, nome_destino)
            # Reabilita botão
            self.btn_upload.configure(state="normal", text="☁️ INICIAR UPLOAD")

        threading.Thread(target=task).start()