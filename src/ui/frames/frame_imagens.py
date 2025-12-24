import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from src.modules.image_tools import ImageTools
from src.utils.task_queue import TaskQueue
from src.ui.components.tooltip import add_tooltip
from src.ui.components.unified_console import UnifiedConsole

class FrameImagens(ctk.CTkFrame):
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
        ctk.CTkLabel(self.frame_conteudo, text="Ferramentas de Imagem em Lote", 
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20, anchor="w")

        # --- Sistema de Abas ---
        self.tabview = ctk.CTkTabview(self.frame_conteudo, width=800, height=400)
        self.tabview.pack(fill="both", expand=True)

        self.tab_resize = self.tabview.add("Redimensionar")
        self.tab_convert = self.tabview.add("Converter Formato")
        self.tab_compress = self.tabview.add("Comprimir")

        # Configura as abas
        self._setup_aba_resize()
        self._setup_aba_convert()
        self._setup_aba_compress()

        # === CONSOLE UNIFICADO (criar primeiro) ===
        self.console = UnifiedConsole(self, height=100, title="📋 Console de Execução")
        self.console.grid(row=1, column=0, sticky="ew")
        self.console.log("Ferramentas de imagem prontas. Selecione uma operação acima.", "info")
        
        # === ImageTool (depois do console) ===
        self.image_tool = ImageTools(logger_callback=self.console.log)

    def _selecionar_arquivos(self):
        """Abre a caixa de diálogo para selecionar arquivos de imagem."""
        arquivos = filedialog.askopenfilenames(filetypes=[("Arquivos de Imagem", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff")])
        if arquivos:
            self.arquivos_selecionados = list(arquivos)
            return True
        return False

    # ==========================
    # LÓGICA DA ABA REDIMENSIONAR
    # ==========================
    def _setup_aba_resize(self):
        frame = self.tab_resize
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        # --- Seleção de Arquivos ---
        ctk.CTkLabel(frame, text="1. Selecione as Imagens para Redimensionar:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.lbl_resize_files = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado.")
        self.lbl_resize_files.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        btn_select = ctk.CTkButton(frame, text="📁 Selecionar Imagens", command=lambda: self._acao_selecionar_e_atualizar(self.lbl_resize_files))
        btn_select.grid(row=1, column=1, padx=20, pady=5, sticky="e")
        
        # --- Opções de Redimensionamento ---
        ctk.CTkLabel(frame, text="2. Defina as Dimensões:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        # Opção 1: Largura e Altura Fixas
        frame_fixed = ctk.CTkFrame(frame)
        frame_fixed.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(frame_fixed, text="Largura (px):").pack(side="left", padx=5)
        self.entry_width = ctk.CTkEntry(frame_fixed, width=80, placeholder_text="1920")
        self.entry_width.pack(side="left", padx=5)
        ctk.CTkLabel(frame_fixed, text="Altura (px):").pack(side="left", padx=5)
        self.entry_height = ctk.CTkEntry(frame_fixed, width=80, placeholder_text="1080")
        self.entry_height.pack(side="left", padx=5)
        
        # Opção 2: Porcentagem
        frame_percent = ctk.CTkFrame(frame)
        frame_percent.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(frame_percent, text="Porcentagem (%):").pack(side="left", padx=5)
        self.entry_percent = ctk.CTkEntry(frame_percent, width=80, placeholder_text="50")
        self.entry_percent.pack(side="left", padx=5)
        
        # --- Botão Executar ---
        btn_run = ctk.CTkButton(frame, text="🚀 Iniciar Redimensionamento em Lote", fg_color="green", command=self._acao_redimensionar)
        btn_run.grid(row=4, column=0, columnspan=2, padx=20, pady=30)

    def _acao_selecionar_e_atualizar(self, label):
        if self._selecionar_arquivos():
            label.configure(text=f"{len(self.arquivos_selecionados)} arquivos selecionados.")
            self.console.log(f"{len(self.arquivos_selecionados)} imagens selecionadas", "info")
        else:
            label.configure(text="Nenhum arquivo selecionado.")

    def _acao_redimensionar(self):
        if not self.arquivos_selecionados:
            messagebox.showerror("Erro", "Selecione os arquivos primeiro.")
            return
            
        output_dir = filedialog.askdirectory(title="Selecione a Pasta de Saída")
        if not output_dir:
            return

        # Lógica para determinar o modo de redimensionamento
        width = self.entry_width.get()
        height = self.entry_height.get()
        percent = self.entry_percent.get()
        
        try:
            width = int(width) if width else None
            height = int(height) if height else None
            percent = int(percent) if percent else None
        except ValueError:
            messagebox.showerror("Erro", "Largura, Altura e Porcentagem devem ser números inteiros.")
            return

        if not (width or height or percent):
            messagebox.showerror("Erro", "Defina pelo menos Largura/Altura ou Porcentagem.")
            return

        # Submete cada arquivo para a fila de tarefas
        for arquivo in self.arquivos_selecionados:
            task_name = f"Redimensionar {os.path.basename(arquivo)}"
            self.task_queue.submit_task(
                self.image_tool.redimensionar_imagem,
                arquivo,
                output_dir,
                width=width,
                height=height,
                percent=percent,
                task_name=task_name
            )
        
        messagebox.showinfo("Sucesso", f"{len(self.arquivos_selecionados)} tarefas de redimensionamento adicionadas à fila.")
        self.console.log(f"{len(self.arquivos_selecionados)} tarefas adicionadas à fila", "process")
        self.arquivos_selecionados = []
        self.lbl_resize_files.configure(text="Nenhum arquivo selecionado.")

    # ==========================
    # LÓGICA DA ABA CONVERTER
    # ==========================
    def _setup_aba_convert(self):
        frame = self.tab_convert
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        # --- Seleção de Arquivos ---
        ctk.CTkLabel(frame, text="1. Selecione as Imagens para Converter:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.lbl_convert_files = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado.")
        self.lbl_convert_files.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        btn_select = ctk.CTkButton(frame, text="📁 Selecionar Imagens", command=lambda: self._acao_selecionar_e_atualizar(self.lbl_convert_files))
        btn_select.grid(row=1, column=1, padx=20, pady=5, sticky="e")
        
        # --- Opções de Conversão ---
        ctk.CTkLabel(frame, text="2. Escolha o Formato de Saída:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.option_format = ctk.CTkOptionMenu(frame, values=["JPG", "PNG", "WEBP", "BMP", "TIFF"])
        self.option_format.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        # --- Botão Executar ---
        btn_run = ctk.CTkButton(frame, text="🚀 Iniciar Conversão em Lote", fg_color="green", command=self._acao_converter)
        btn_run.grid(row=4, column=0, columnspan=2, padx=20, pady=30)

    def _acao_converter(self):
        if not self.arquivos_selecionados:
            messagebox.showerror("Erro", "Selecione os arquivos primeiro.")
            return
            
        output_dir = filedialog.askdirectory(title="Selecione a Pasta de Saída")
        if not output_dir:
            return
            
        target_format = self.option_format.get()

        # Submete cada arquivo para a fila de tarefas
        for arquivo in self.arquivos_selecionados:
            task_name = f"Converter {os.path.basename(arquivo)} para {target_format}"
            self.task_queue.submit_task(
                self.image_tool.converter_imagem,
                arquivo,
                output_dir,
                target_format,
                task_name=task_name
            )
        
        messagebox.showinfo("Sucesso", f"{len(self.arquivos_selecionados)} tarefas de conversão adicionadas à fila.")
        self.console.log(f"{len(self.arquivos_selecionados)} tarefas de conversão adicionadas à fila", "process")
        self.arquivos_selecionados = []
        self.lbl_convert_files.configure(text="Nenhum arquivo selecionado.")

    # ==========================
    # LÓGICA DA ABA COMPRIMIR
    # ==========================
    def _setup_aba_compress(self):
        frame = self.tab_compress
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        # --- Seleção de Arquivos ---
        ctk.CTkLabel(frame, text="1. Selecione as Imagens para Comprimir:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.lbl_compress_files = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado.")
        self.lbl_compress_files.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        btn_select = ctk.CTkButton(frame, text="📁 Selecionar Imagens", command=lambda: self._acao_selecionar_e_atualizar(self.lbl_compress_files))
        btn_select.grid(row=1, column=1, padx=20, pady=5, sticky="e")
        
        # --- Opções de Compressão ---
        ctk.CTkLabel(frame, text="2. Nível de Compressão (Qualidade JPG):", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.slider_quality = ctk.CTkSlider(frame, from_=10, to=100, number_of_steps=90, command=self._update_quality_label)
        self.slider_quality.set(70) # Padrão de compressão balanceada
        self.slider_quality.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_quality_value = ctk.CTkLabel(frame, text="Qualidade: 70/100 (Balanceado)")
        self.lbl_quality_value.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        
        # --- Botão Executar ---
        btn_run = ctk.CTkButton(frame, text="🚀 Iniciar Compressão em Lote", fg_color="green", command=self._acao_comprimir)
        btn_run.grid(row=4, column=0, columnspan=2, padx=20, pady=30)

    def _update_quality_label(self, value):
        quality = int(value)
        status = ""
        if quality >= 90:
            status = "(Máxima Qualidade)"
        elif quality >= 70:
            status = "(Balanceado)"
        else:
            status = "(Máxima Compressão)"
            
        self.lbl_quality_value.configure(text=f"Qualidade: {quality}/100 {status}")

    def _acao_comprimir(self):
        if not self.arquivos_selecionados:
            messagebox.showerror("Erro", "Selecione os arquivos primeiro.")
            return
            
        output_dir = filedialog.askdirectory(title="Selecione a Pasta de Saída")
        if not output_dir:
            return
            
        quality = int(self.slider_quality.get())

        # Submete cada arquivo para a fila de tarefas
        for arquivo in self.arquivos_selecionados:
            task_name = f"Comprimir {os.path.basename(arquivo)} (Q={quality})"
            self.task_queue.submit_task(
                self.image_tool.comprimir_imagem,
                arquivo,
                output_dir,
                quality,
                task_name=task_name
            )
        
        messagebox.showinfo("Sucesso", f"{len(self.arquivos_selecionados)} tarefas de compressão adicionadas à fila.")
        self.console.log(f"{len(self.arquivos_selecionados)} tarefas de compressão adicionadas à fila", "process")
        self.arquivos_selecionados = []
        self.lbl_compress_files.configure(text="Nenhum arquivo selecionado.")
