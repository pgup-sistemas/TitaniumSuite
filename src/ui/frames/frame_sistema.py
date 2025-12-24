import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from src.modules.system_tools import SystemTools
from src.utils.task_queue import TaskQueue
from src.ui.components.tooltip import add_tooltip
from src.ui.components.unified_console import UnifiedConsole

class FrameSistema(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.task_queue = TaskQueue()
        self.system_tool = None  # Inicializado depois
        self.arquivos_selecionados = []
        
        # Layout: Grid 2 linhas (conteúdo + console)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # === ÁREA DE CONTEÚDO ===
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        # Título
        ctk.CTkLabel(self.frame_conteudo, text="Ferramentas de Sistema e Organização", 
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20, anchor="w")

        # --- Sistema de Abas ---
        self.tabview = ctk.CTkTabview(self.frame_conteudo, width=800, height=400)
        self.tabview.pack(fill="both", expand=True)

        self.tab_dedupe = self.tabview.add("Localizar Duplicados")
        self.tab_rename = self.tabview.add("Renomear em Lote")
        self.tab_organize = self.tabview.add("Organizador de Pastas")

        # Configura as abas
        self._setup_aba_dedupe()
        self._setup_aba_rename()
        self._setup_aba_organize()

        # === CONSOLE UNIFICADO (criar primeiro) ===
        self.console = UnifiedConsole(self, height=100, title="📋 Console de Execução")
        self.console.grid(row=1, column=0, sticky="ew")
        self.console.log("Ferramentas de sistema prontas. Selecione uma operação acima.", "info")
        
        # === SystemTool (depois do console) ===
        self.system_tool = SystemTools(logger_callback=self.console.log)

    # ==========================
    # LÓGICA DA ABA LOCALIZAR DUPLICADOS
    # ==========================
    def _setup_aba_dedupe(self):
        frame = self.tab_dedupe
        frame.grid_columnconfigure(0, weight=1)
        # Removido weight 1 da coluna 1 para botões ficarem juntos

        # --- Frame de Ações (Topo) ---
        top_frame = ctk.CTkFrame(frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(10,0))
        top_frame.grid_columnconfigure(0, weight=1)
        
        # --- Seleção de Diretório ---
        ctk.CTkLabel(top_frame, text="1. Selecione o Diretório para Buscar Duplicados:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w")
        
        self.lbl_dedupe_dir = ctk.CTkLabel(top_frame, text="Nenhum diretório selecionado.")
        self.lbl_dedupe_dir.grid(row=1, column=0, sticky="w", pady=(5,10))
        
        btn_select = ctk.CTkButton(top_frame, text="📁 Selecionar Pasta", command=self._acao_selecionar_diretorio_dedupe)
        btn_select.grid(row=1, column=1, sticky="e", padx=(0,10))
        
        btn_run = ctk.CTkButton(top_frame, text="🔍 Iniciar Busca", fg_color="green", command=self._acao_localizar_duplicados)
        btn_run.grid(row=1, column=2, sticky="e")
        
        self.diretorio_dedupe = None
        self.checkboxes_duplicados = [] # Lista para guardar as checkboxes
        self.grupos_duplicados = {} # Dicionário para guardar os grupos de checkboxes

        # --- Frame de Resultados (Interativo) ---
        results_frame = ctk.CTkFrame(frame)
        results_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(results_frame, text="Resultados:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(5,0))
        
        self.scroll_frame_dedupe = ctk.CTkScrollableFrame(results_frame, label_text="Nenhum resultado para exibir.")
        self.scroll_frame_dedupe.pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- Frame de Ações (Baixo) ---
        bottom_frame = ctk.CTkFrame(frame, fg_color="transparent")
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 10))
        
        self.check_var_todos = ctk.StringVar(value="off")
        self.check_selecionar_todos = ctk.CTkCheckBox(bottom_frame, text="Selecionar Todos", variable=self.check_var_todos, onvalue="on", offvalue="off", command=self._selecionar_todos_duplicados)
        self.check_selecionar_todos.pack(side="left", padx=(0, 20))
        
        self.check_var_inteligente = ctk.StringVar(value="off")
        self.check_selecao_inteligente = ctk.CTkCheckBox(bottom_frame, text="Manter 1 por grupo", variable=self.check_var_inteligente, onvalue="on", offvalue="off", command=self._selecionar_inteligente_duplicados)
        self.check_selecao_inteligente.pack(side="left")
        
        self.btn_delete_selected = ctk.CTkButton(bottom_frame, text="🗑️ Deletar Selecionados", fg_color="#D32F2F", hover_color="#B71C1C", command=self._acao_deletar_duplicados, state="disabled")
        self.btn_delete_selected.pack(side="right")


    def _acao_selecionar_diretorio_dedupe(self):
        diretorio = filedialog.askdirectory(title="Selecione a Pasta para Buscar Duplicados")
        if diretorio:
            self.diretorio_dedupe = diretorio
            self.lbl_dedupe_dir.configure(text=diretorio)
            self.console.log(f"Pasta selecionada: {diretorio}", "info")
        else:
            self.lbl_dedupe_dir.configure(text="Nenhum diretório selecionado.")
            self.diretorio_dedupe = None

    def _acao_localizar_duplicados(self):
        if not self.diretorio_dedupe:
            messagebox.showerror("Erro", "Selecione o diretório primeiro.")
            return

        # Limpa resultados anteriores
        for widget in self.scroll_frame_dedupe.winfo_children():
            widget.destroy()
        self.scroll_frame_dedupe.configure(label_text="Buscando duplicados... Aguarde.")
        self.checkboxes_duplicados = []
        self.grupos_duplicados = {}
        self.btn_delete_selected.configure(state="disabled")
        self.check_var_todos.set("off")
        self.check_var_inteligente.set("off")
        
        self.console.log("Iniciando busca de arquivos duplicados...", "process")
        task_name = f"Buscar Duplicados em {os.path.basename(self.diretorio_dedupe)}"
        self.task_queue.submit_task(
            self._run_localizar_duplicados,
            self.diretorio_dedupe,
            task_name=task_name
        )

    def _run_localizar_duplicados(self, diretorio):
        """Função wrapper para rodar a busca e atualizar a UI (via after)"""
        duplicados = self.system_tool.localizar_duplicados(diretorio)
        self.after(0, self._update_dedupe_results, duplicados)
        return f"Busca concluída. {len(duplicados)} grupos encontrados."

    def _update_dedupe_results(self, duplicados):
        # Limpa o frame
        for widget in self.scroll_frame_dedupe.winfo_children():
            widget.destroy()
            
        if not duplicados:
            self.scroll_frame_dedupe.configure(label_text="✅ Nenhum arquivo duplicado encontrado.")
            self.btn_delete_selected.configure(state="disabled")
            return

        self.scroll_frame_dedupe.configure(label_text="")
        self.btn_delete_selected.configure(state="normal")
        
        self.checkboxes_duplicados = []
        self.grupos_duplicados = {}

        for i, (hash_val, paths) in enumerate(duplicados.items()):
            # Frame do grupo
            group_frame = ctk.CTkFrame(self.scroll_frame_dedupe, border_width=1)
            group_frame.pack(fill="x", expand=True, padx=5, pady=(5, 10))
            
            label_text = f"Grupo {i+1} ({len(paths)} arquivos)"
            ctk.CTkLabel(group_frame, text=label_text, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
            
            # Checkboxes do grupo
            self.grupos_duplicados[i] = []
            for path in sorted(paths):
                check_var = ctk.StringVar(value="off")
                checkbox = ctk.CTkCheckBox(group_frame, text=path, variable=check_var, onvalue="on", offvalue="off")
                checkbox.pack(anchor="w", padx=20, pady=2)
                self.checkboxes_duplicados.append(checkbox)
                self.grupos_duplicados[i].append(checkbox)

    def _selecionar_todos_duplicados(self):
        select_all = self.check_var_todos.get() == "on"
        # Desmarcar a outra opção se esta for marcada
        if select_all:
            self.check_var_inteligente.set("off")
            
        for checkbox in self.checkboxes_duplicados:
            checkbox.select() if select_all else checkbox.deselect()
            
    def _selecionar_inteligente_duplicados(self):
        select_intelligent = self.check_var_inteligente.get() == "on"
        # Desmarcar a outra opção se esta for marcada
        if select_intelligent:
            self.check_var_todos.set("off")

        for grupo in self.grupos_duplicados.values():
            # Desmarca todos primeiro
            for cb in grupo:
                cb.deselect()
            # Se a opção inteligente está ativa, marca todos exceto o primeiro
            if select_intelligent:
                for cb in grupo[1:]: # Deixa o primeiro desmarcado
                    cb.select()

    def _acao_deletar_duplicados(self):
        arquivos_para_deletar = [
            cb.cget("text") for cb in self.checkboxes_duplicados if cb.get() == "on"
        ]
        
        if not arquivos_para_deletar:
            messagebox.showwarning("Nenhum Arquivo", "Nenhum arquivo foi selecionado para deleção.")
            return
            
        qtd = len(arquivos_para_deletar)
        msg = f"Você tem certeza que deseja deletar permanentemente {qtd} arquivo(s)?\n\nESTA AÇÃO NÃO PODE SER DESFEITA."
        
        if messagebox.askyesno("Confirmar Deleção", msg, icon='warning'):
            task_name = f"Deletar {qtd} arquivos duplicados"
            self.console.log(f"Adicionando à fila: {task_name}", "process")
            self.task_queue.submit_task(
                self.system_tool.deletar_arquivos,
                arquivos_para_deletar,
                task_name=task_name
            )
            messagebox.showinfo("Sucesso", f"Tarefa '{task_name}' adicionada à fila.")
            
            # Limpa e reinicia a busca para atualizar a lista
            self._acao_localizar_duplicados()

    # ==========================
    # LÓGICA DA ABA RENOMEAR EM LOTE
    # ==========================
    def _setup_aba_rename(self):
        frame = self.tab_rename
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        # --- Seleção de Arquivos ---
        ctk.CTkLabel(frame, text="1. Selecione os Arquivos para Renomear:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.lbl_rename_files = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado.")
        self.lbl_rename_files.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        btn_select = ctk.CTkButton(frame, text="📁 Selecionar Arquivos", command=self._acao_selecionar_arquivos_rename)
        btn_select.grid(row=1, column=1, padx=20, pady=5, sticky="e")
        
        self.arquivos_rename = []
        
        # --- Opções de Renomeação ---
        ctk.CTkLabel(frame, text="2. Defina as Regras de Renomeação:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        # Prefixo
        ctk.CTkLabel(frame, text="Prefixo:").grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.entry_prefix = ctk.CTkEntry(frame, width=200, placeholder_text="Ex: 'Relatorio_'")
        self.entry_prefix.grid(row=3, column=1, padx=20, pady=5, sticky="w")
        
        # Sufixo
        ctk.CTkLabel(frame, text="Sufixo:").grid(row=4, column=0, padx=20, pady=5, sticky="w")
        self.entry_suffix = ctk.CTkEntry(frame, width=200, placeholder_text="Ex: '_Final'")
        self.entry_suffix.grid(row=4, column=1, padx=20, pady=5, sticky="w")
        
        # Numeração Inicial
        ctk.CTkLabel(frame, text="Numeração Inicial:").grid(row=5, column=0, padx=20, pady=5, sticky="w")
        self.entry_start_num = ctk.CTkEntry(frame, width=100, placeholder_text="1")
        self.entry_start_num.grid(row=5, column=1, padx=20, pady=5, sticky="w")
        
        # --- Botão Executar ---
        btn_run = ctk.CTkButton(frame, text="✏️ Iniciar Renomeação em Lote", fg_color="green", command=self._acao_renomear_em_lote)
        btn_run.grid(row=6, column=0, columnspan=2, padx=20, pady=30)

    def _acao_selecionar_arquivos_rename(self):
        arquivos = filedialog.askopenfilenames(title="Selecione os Arquivos para Renomear")
        if arquivos:
            self.arquivos_rename = list(arquivos)
            self.lbl_rename_files.configure(text=f"{len(self.arquivos_rename)} arquivos selecionados.")
            self.console.log(f"{len(self.arquivos_rename)} arquivos selecionados", "info")
        else:
            self.lbl_rename_files.configure(text="Nenhum arquivo selecionado.")
            self.arquivos_rename = []

    def _acao_renomear_em_lote(self):
        if not self.arquivos_rename:
            messagebox.showerror("Erro", "Selecione os arquivos primeiro.")
            return
            
        prefixo = self.entry_prefix.get()
        sufixo = self.entry_suffix.get()
        
        try:
            num_inicial = int(self.entry_start_num.get() or 1)
        except ValueError:
            messagebox.showerror("Erro", "A numeração inicial deve ser um número inteiro.")
            return

        task_name = f"Renomear {len(self.arquivos_rename)} arquivos"
        self.console.log(f"Adicionando à fila: {task_name}", "process")
        self.task_queue.submit_task(
            self.system_tool.renomear_em_lote,
            self.arquivos_rename,
            prefixo,
            sufixo,
            num_inicial,
            task_name=task_name
        )
        
        messagebox.showinfo("Sucesso", f"Tarefa '{task_name}' adicionada à fila.")
        self.arquivos_rename = []
        self.lbl_rename_files.configure(text="Nenhum arquivo selecionado.")

    # ==========================
    # LÓGICA DA ABA ORGANIZADOR DE PASTAS
    # ==========================
    def _setup_aba_organize(self):
        frame = self.tab_organize
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        # --- Seleção de Diretório ---
        ctk.CTkLabel(frame, text="1. Selecione o Diretório para Organizar:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.lbl_organize_dir = ctk.CTkLabel(frame, text="Nenhum diretório selecionado.")
        self.lbl_organize_dir.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        btn_select = ctk.CTkButton(frame, text="📁 Selecionar Pasta", command=self._acao_selecionar_diretorio_organize)
        btn_select.grid(row=1, column=1, padx=20, pady=5, sticky="e")
        
        self.diretorio_organize = None
        
        # --- Regras de Organização ---
        ctk.CTkLabel(frame, text="2. Regras de Organização (Extensão: Pasta):", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.txt_organize_rules = ctk.CTkTextbox(frame, width=700, height=150)
        self.txt_organize_rules.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="nsew")
        self.txt_organize_rules.insert("0.0", "pdf: Documentos/PDFs\njpg,png,gif: Imagens\nzip,rar: Compactados\n*: Outros")
        add_tooltip(self.txt_organize_rules, "Formato: extensão: pasta_destino. Use '*' para todos os outros arquivos.")
        
        # --- Botão Executar ---
        btn_run = ctk.CTkButton(frame, text="🧹 Iniciar Organização de Pasta", fg_color="green", command=self._acao_organizar_pasta)
        btn_run.grid(row=4, column=0, columnspan=2, padx=20, pady=30)

    def _acao_selecionar_diretorio_organize(self):
        diretorio = filedialog.askdirectory(title="Selecione a Pasta para Organizar")
        if diretorio:
            self.diretorio_organize = diretorio
            self.lbl_organize_dir.configure(text=diretorio)
            self.console.log(f"Pasta selecionada: {diretorio}", "info")
        else:
            self.lbl_organize_dir.configure(text="Nenhum diretório selecionado.")
            self.diretorio_organize = None

    def _acao_organizar_pasta(self):
        if not self.diretorio_organize:
            messagebox.showerror("Erro", "Selecione o diretório primeiro.")
            return
            
        regras_texto = self.txt_organize_rules.get("0.0", "end").strip()
        regras = {}
        try:
            for linha in regras_texto.split('\n'):
                if ':' in linha:
                    extensoes, pasta = linha.split(':', 1)
                    regras[extensoes.strip()] = pasta.strip()
        except Exception:
            messagebox.showerror("Erro", "Formato de regras inválido. Use 'extensao: pasta_destino'.")
            return

        if not regras:
            messagebox.showerror("Erro", "Defina pelo menos uma regra de organização.")
            return

        task_name = f"Organizar Pasta: {os.path.basename(self.diretorio_organize)}"
        self.console.log(f"Adicionando à fila: {task_name}", "process")
        self.task_queue.submit_task(
            self.system_tool.organizar_downloads,
            self.diretorio_organize,
            regras,
            task_name=task_name
        )
        
        messagebox.showinfo("Sucesso", f"Tarefa '{task_name}' adicionada à fila.")
        self.diretorio_organize = None
        self.lbl_organize_dir.configure(text="Nenhum diretório selecionado.")
