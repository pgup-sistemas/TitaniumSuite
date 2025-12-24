import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from src.modules.excel_tools import ExcelTools
from src.utils.task_queue import TaskQueue
from src.ui.components.tooltip import add_tooltip
from src.ui.components.unified_console import UnifiedConsole

class FrameExcel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.task_queue = TaskQueue()
        self.arquivos_selecionados = []
        
        # Layout: Grid 2 linhas (conteúdo + console)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # === ÁREA DE CONTEÚDO ===
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        # Título
        ctk.CTkLabel(self.frame_conteudo, text="Ferramentas de Automação Excel", 
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20, anchor="w")

        # --- Sistema de Abas ---
        self.tabview = ctk.CTkTabview(self.frame_conteudo, width=800, height=400)
        self.tabview.pack(fill="both", expand=True)

        self.tab_merge = self.tabview.add("Unir Planilhas")
        self.tab_convert = self.tabview.add("Converter Formato")
        self.tab_dedupe = self.tabview.add("Remover Duplicadas")

        # Configura as abas
        self._setup_aba_merge()
        self._setup_aba_convert()
        self._setup_aba_dedupe()

        # === CONSOLE UNIFICADO (criar primeiro) ===
        self.console = UnifiedConsole(self, height=100, title="📋 Console de Execução")
        self.console.grid(row=1, column=0, sticky="ew")
        self.console.log("Ferramentas Excel prontas. Selecione uma operação acima.", "info")
        
        # === ExcelTool (depois do console) ===
        self.excel_tool = ExcelTools(logger_callback=self.console.log)

    def console_log(self, msg):
        """Função auxiliar para enviar mensagens para o console."""
        self.console.log(msg, "info")

    def _selecionar_arquivos(self):
        """Abre a caixa de diálogo para selecionar arquivos Excel."""
        arquivos = filedialog.askopenfilenames(filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
        if arquivos:
            self.arquivos_selecionados = list(arquivos)
            return True
        return False

    def _acao_selecionar_e_atualizar(self, label):
        if self._selecionar_arquivos():
            label.configure(text=f"{len(self.arquivos_selecionados)} arquivos selecionados.")
            self.console.log(f"{len(self.arquivos_selecionados)} arquivos selecionados", "info")
        else:
            label.configure(text="Nenhum arquivo selecionado.")

    # ==========================
    # LÓGICA DA ABA UNIR PLANILHAS
    # ==========================
    def _setup_aba_merge(self):
        frame = self.tab_merge
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        # --- Seleção de Arquivos ---
        ctk.CTkLabel(frame, text="1. Selecione os Arquivos Excel para Unir:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.lbl_merge_files = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado.")
        self.lbl_merge_files.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        btn_select = ctk.CTkButton(frame, text="📁 Selecionar Arquivos", command=lambda: self._acao_selecionar_e_atualizar(self.lbl_merge_files))
        btn_select.grid(row=1, column=1, padx=20, pady=5, sticky="e")
        
        # --- Opções de União ---
        ctk.CTkLabel(frame, text="2. Opções de União:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.radio_var_merge = ctk.StringVar(value="all")
        
        radio_all = ctk.CTkRadioButton(frame, text="Unir TODAS as abas (cada aba vira uma nova aba no arquivo final)", variable=self.radio_var_merge, value="all")
        radio_all.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="w")
        
        radio_specific = ctk.CTkRadioButton(frame, text="Unir apenas a aba com o nome:", variable=self.radio_var_merge, value="specific")
        radio_specific.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        
        self.entry_sheet_name = ctk.CTkEntry(frame, width=150, placeholder_text="Ex: 'Dados'")
        self.entry_sheet_name.grid(row=4, column=1, padx=20, pady=5, sticky="w")
        
        # --- Botão Executar ---
        btn_run = ctk.CTkButton(frame, text="🚀 Iniciar Fusão de Planilhas", fg_color="green", command=self._acao_unir_planilhas)
        btn_run.grid(row=5, column=0, columnspan=2, padx=20, pady=30)

    def _acao_unir_planilhas(self):
        if not self.arquivos_selecionados:
            messagebox.showerror("Erro", "Selecione os arquivos primeiro.")
            return
            
        caminho_salvar = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")], initialfile="Planilha_Consolidada.xlsx")
        if not caminho_salvar:
            return

        aba_especifica = None
        if self.radio_var_merge.get() == "specific":
            aba_especifica = self.entry_sheet_name.get().strip()
            if not aba_especifica:
                messagebox.showerror("Erro", "Por favor, insira o nome da aba específica.")
                return

        task_name = "Unir Planilhas Excel"
        self.console.log(f"Adicionando à fila: {task_name}", "process")
        self.task_queue.submit_task(
            self.excel_tool.unir_planilhas,
            self.arquivos_selecionados,
            caminho_salvar,
            aba_especifica,
            task_name=task_name
        )
        
        messagebox.showinfo("Sucesso", f"Tarefa '{task_name}' adicionada à fila.")
        self.arquivos_selecionados = []
        self.lbl_merge_files.configure(text="Nenhum arquivo selecionado.")

    # ==========================
    # LÓGICA DA ABA CONVERTER FORMATO
    # ==========================
    def _setup_aba_convert(self):
        frame = self.tab_convert
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        # --- Seleção de Arquivo ---
        ctk.CTkLabel(frame, text="1. Selecione o Arquivo Excel para Converter:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.lbl_convert_file = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado.")
        self.lbl_convert_file.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        btn_select = ctk.CTkButton(frame, text="📁 Selecionar Arquivo", command=self._acao_selecionar_arquivo_convert)
        btn_select.grid(row=1, column=1, padx=20, pady=5, sticky="e")
        
        # --- Opções de Conversão ---
        ctk.CTkLabel(frame, text="2. Escolha o Formato de Saída:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.option_format_convert = ctk.CTkOptionMenu(frame, values=["CSV", "JSON"])
        self.option_format_convert.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        # --- Botão Executar ---
        btn_run = ctk.CTkButton(frame, text="🚀 Iniciar Conversão", fg_color="green", command=self._acao_converter_formato)
        btn_run.grid(row=4, column=0, columnspan=2, padx=20, pady=30)
        
        self.arquivo_conversao = None

    def _acao_selecionar_arquivo_convert(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
        if arquivo:
            self.arquivo_conversao = arquivo
            self.lbl_convert_file.configure(text=os.path.basename(arquivo))
            self.console.log(f"Arquivo selecionado: {os.path.basename(arquivo)}", "info")
        else:
            self.lbl_convert_file.configure(text="Nenhum arquivo selecionado.")
            self.arquivo_conversao = None

    def _acao_converter_formato(self):
        if not self.arquivo_conversao:
            messagebox.showerror("Erro", "Selecione o arquivo primeiro.")
            return
            
        formato = self.option_format_convert.get().lower()
        extensao = f".{formato}"
        
        caminho_salvar = filedialog.asksaveasfilename(defaultextension=extensao, filetypes=[(formato.upper(), f"*{extensao}")], initialfile=f"{os.path.splitext(os.path.basename(self.arquivo_conversao))[0]}.{formato}")
        if not caminho_salvar:
            return

        task_name = f"Converter Excel para {formato.upper()}"
        self.console.log(f"Adicionando à fila: {task_name}", "process")
        self.task_queue.submit_task(
            self.excel_tool.converter_para_csv_json,
            self.arquivo_conversao,
            caminho_salvar,
            formato,
            task_name=task_name
        )
        
        messagebox.showinfo("Sucesso", f"Tarefa '{task_name}' adicionada à fila.")
        self.arquivo_conversao = None
        self.lbl_convert_file.configure(text="Nenhum arquivo selecionado.")

    # ==========================
    # LÓGICA DA ABA REMOVER DUPLICADAS
    # ==========================
    def _setup_aba_dedupe(self):
        frame = self.tab_dedupe
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        # --- Seleção de Arquivo ---
        ctk.CTkLabel(frame, text="1. Selecione o Arquivo Excel para Limpar:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.lbl_dedupe_file = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado.")
        self.lbl_dedupe_file.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        btn_select = ctk.CTkButton(frame, text="📁 Selecionar Arquivo", command=self._acao_selecionar_arquivo_dedupe)
        btn_select.grid(row=1, column=1, padx=20, pady=5, sticky="e")
        
        # --- Opções de Critério ---
        ctk.CTkLabel(frame, text="2. Colunas Critério (separadas por vírgula):", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.entry_dedupe_columns = ctk.CTkEntry(frame, width=300, placeholder_text="Ex: 'Nome', 'Email', 'Telefone'")
        self.entry_dedupe_columns.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # --- Botão Executar ---
        btn_run = ctk.CTkButton(frame, text="🚀 Remover Duplicadas", fg_color="green", command=self._acao_remover_duplicadas)
        btn_run.grid(row=4, column=0, columnspan=2, padx=20, pady=30)
        
        self.arquivo_dedupe = None

    def _acao_selecionar_arquivo_dedupe(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
        if arquivo:
            self.arquivo_dedupe = arquivo
            self.lbl_dedupe_file.configure(text=os.path.basename(arquivo))
            self.console.log(f"Arquivo selecionado: {os.path.basename(arquivo)}", "info")
        else:
            self.lbl_dedupe_file.configure(text="Nenhum arquivo selecionado.")
            self.arquivo_dedupe = None

    def _acao_remover_duplicadas(self):
        if not self.arquivo_dedupe:
            messagebox.showerror("Erro", "Selecione o arquivo primeiro.")
            return
            
        colunas_criterio = self.entry_dedupe_columns.get().strip()
        
        caminho_salvar = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")], initialfile=f"{os.path.splitext(os.path.basename(self.arquivo_dedupe))[0]}_limpo.xlsx")
        if not caminho_salvar:
            return

        task_name = "Remover Duplicadas Excel"
        self.console.log(f"Adicionando à fila: {task_name}", "process")
        self.task_queue.submit_task(
            self.excel_tool.remover_duplicadas,
            self.arquivo_dedupe,
            caminho_salvar,
            colunas_criterio,
            task_name=task_name
        )
        
        messagebox.showinfo("Sucesso", f"Tarefa '{task_name}' adicionada à fila.")
        self.arquivo_dedupe = None
        self.lbl_dedupe_file.configure(text="Nenhum arquivo selecionado.")
