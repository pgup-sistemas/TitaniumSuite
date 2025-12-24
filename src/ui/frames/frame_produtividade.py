import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from PIL import Image
from src.modules.tools import PDFTools, QRTools
from src.ui.components.tooltip import add_tooltip
from src.utils.task_queue import TaskQueue
from src.ui.components.unified_console import UnifiedConsole

class FrameProdutividade(ctk.CTkFrame):
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
        ctk.CTkLabel(self.frame_conteudo, text="Ferramentas de Produtividade", 
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20, anchor="w")

        # --- Sistema de Abas ---
        self.tabview = ctk.CTkTabview(self.frame_conteudo, width=800, height=400)
        self.tabview.pack(fill="both", expand=True)

        self.tab_pdf_merge = self.tabview.add("Unir/Comprimir PDF")
        self.tab_pdf_split = self.tabview.add("Dividir/Rotacionar PDF")
        self.tab_pdf_ocr = self.tabview.add("Extrair Texto (OCR)")
        self.tab_qr = self.tabview.add("Gerador QR Code")
        
        # Configura as abas
        self._setup_aba_pdf_merge()
        self._setup_aba_pdf_split()
        self._setup_aba_pdf_ocr()
        self._setup_aba_qr()

        # === CONSOLE UNIFICADO (criar primeiro) ===
        self.console = UnifiedConsole(self, height=100, title="📋 Console de Execução")
        self.console.grid(row=1, column=0, sticky="ew")
        self.console.log("Ferramentas de produtividade prontas. Selecione uma operação acima.", "info")
        
        # === PDFTool e QRTools (depois do console) ===
        self.pdf_tool = PDFTools(logger_callback=self.console.log)
        self.qr_tool = QRTools(logger_callback=self.console.log)

    # ==========================
    # LÓGICA DA ABA UNIR/COMPRIMIR PDF
    # ==========================
    def _setup_aba_pdf_merge(self):
        frame = self.tab_pdf_merge
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        # --- Unir PDFs ---
        ctk.CTkLabel(frame, text="🔗 Unir Múltiplos PDFs em um só", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        btn_select_pdf = ctk.CTkButton(frame, text="📁 1. Selecionar PDFs", command=self._acao_selecionar_pdfs)
        btn_select_pdf.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        add_tooltip(btn_select_pdf, "Escolha múltiplos arquivos PDF para unir em um só documento.")
        
        self.lbl_arquivos_merge = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado.", text_color="gray")
        self.lbl_arquivos_merge.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        
        self.btn_merge_pdf = ctk.CTkButton(frame, text="🔗 2. Unir e Salvar", fg_color="green", state="disabled", command=self._acao_unir_pdfs)
        self.btn_merge_pdf.grid(row=1, column=1, padx=20, pady=5, sticky="e")
        add_tooltip(self.btn_merge_pdf, "Inicia a fusão dos PDFs selecionados.")
        
        # --- Comprimir PDF ---
        ctk.CTkLabel(frame, text="Compressão de PDF (Reduzir Tamanho)", font=ctk.CTkFont(weight="bold")).grid(row=3, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        btn_select_compress = ctk.CTkButton(frame, text="📁 1. Selecionar PDF", command=self._acao_selecionar_pdf_compress)
        btn_select_compress.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        
        self.lbl_arquivo_compress = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado.", text_color="gray")
        self.lbl_arquivo_compress.grid(row=5, column=0, padx=20, pady=5, sticky="w")
        
        self.btn_compress_pdf = ctk.CTkButton(frame, text="📉 2. Comprimir e Salvar", fg_color="green", state="disabled", command=self._acao_comprimir_pdf)
        self.btn_compress_pdf.grid(row=4, column=1, padx=20, pady=5, sticky="e")
        
        self.arquivo_compressao = None

    def _acao_selecionar_pdfs(self):
        arquivos = filedialog.askopenfilenames(filetypes=[("Arquivos PDF", "*.pdf")])
        if arquivos:
            self.arquivos_selecionados = list(arquivos)
            qtd = len(arquivos)
            self.lbl_arquivos_merge.configure(text=f"{qtd} arquivos selecionados.")
            self.btn_merge_pdf.configure(state="normal")
            self.console.log(f"{qtd} PDFs selecionados", "info")
        else:
            self.lbl_arquivos_merge.configure(text="Nenhum arquivo selecionado.")
            self.btn_merge_pdf.configure(state="disabled")

    def _acao_unir_pdfs(self):
        if not self.arquivos_selecionados:
            return

        # Desabilitar botão para evitar clicks duplos
        self.btn_merge_pdf.configure(state="disabled")
        self.console.log(f"Iniciando união de {len(self.arquivos_selecionados)} PDFs...", "process")

        caminho_salvar = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")], initialfile="Documento_Unificado.pdf")
        if not caminho_salvar:
            self.btn_merge_pdf.configure(state="normal")
            return

        task_name = "Unir PDFs"
        self.console.log(f"Adicionando à fila: {task_name}", "process")
        self.task_queue.submit_task(
            self.pdf_tool.unir_pdfs,
            self.arquivos_selecionados,
            caminho_salvar,
            task_name=task_name
        )
        
        messagebox.showinfo("Sucesso", f"Tarefa '{task_name}' adicionada à fila.")
        self.arquivos_selecionados = []
        self.lbl_arquivos_merge.configure(text="Nenhum arquivo selecionado.")
        self.btn_merge_pdf.configure(state="disabled")

    def _acao_selecionar_pdf_compress(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if arquivo:
            self.arquivo_compressao = arquivo
            self.lbl_arquivo_compress.configure(text=os.path.basename(arquivo))
            self.btn_compress_pdf.configure(state="normal")
            self.console.log(f"Arquivo selecionado: {os.path.basename(arquivo)}", "info")
        else:
            self.lbl_arquivo_compress.configure(text="Nenhum arquivo selecionado.")
            self.btn_compress_pdf.configure(state="disabled")

    def _acao_comprimir_pdf(self):
        if not self.arquivo_compressao:
            return

        # Desabilitar botão para evitar clicks duplos
        self.btn_compress_pdf.configure(state="disabled")
        self.console.log(f"Iniciando compressão: {os.path.basename(self.arquivo_compressao)}...", "process")

        caminho_salvar = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")], initialfile=f"{os.path.splitext(os.path.basename(self.arquivo_compressao))[0]}_comprimido.pdf")
        if not caminho_salvar:
            self.btn_compress_pdf.configure(state="normal")
            return

        task_name = f"Comprimir PDF: {os.path.basename(self.arquivo_compressao)}"
        self.console.log(f"Adicionando à fila: {task_name}", "process")
        self.task_queue.submit_task(
            self.pdf_tool.comprimir_pdf,
            self.arquivo_compressao,
            caminho_salvar,
            task_name=task_name
        )
        
        messagebox.showinfo("Sucesso", f"Tarefa '{task_name}' adicionada à fila.")
        self.arquivo_compressao = None
        self.lbl_arquivo_compress.configure(text="Nenhum arquivo selecionado.")
        self.btn_compress_pdf.configure(state="disabled")

    # ==========================
    # LÓGICA DA ABA DIVIDIR/ROTACIONAR PDF
    # ==========================
    def _setup_aba_pdf_split(self):
        frame = self.tab_pdf_split
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        # --- Divisão ---
        ctk.CTkLabel(frame, text="✂️ Dividir PDF em Múltiplos Arquivos", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        btn_select_split = ctk.CTkButton(frame, text="📁 1. Selecionar PDF", command=self._acao_selecionar_pdf_split)
        btn_select_split.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        self.lbl_arquivo_split = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado.", text_color="gray")
        self.lbl_arquivo_split.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        
        ctk.CTkLabel(frame, text="Páginas por arquivo:").grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.entry_split_pages = ctk.CTkEntry(frame, width=50, placeholder_text="1")
        self.entry_split_pages.grid(row=3, column=0, padx=(150, 0), pady=5, sticky="w")
        
        self.btn_split_pdf = ctk.CTkButton(frame, text="✂️ 2. Dividir e Salvar", fg_color="green", state="disabled", command=self._acao_dividir_pdf)
        self.btn_split_pdf.grid(row=1, column=1, padx=20, pady=5, sticky="e")
        
        self.arquivo_divisao = None

        # --- Rotação ---
        ctk.CTkLabel(frame, text="🔄 Rotacionar PDF", font=ctk.CTkFont(weight="bold")).grid(row=4, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        btn_select_rotate = ctk.CTkButton(frame, text="📁 1. Selecionar PDF", command=self._acao_selecionar_pdf_rotate)
        btn_select_rotate.grid(row=5, column=0, padx=20, pady=5, sticky="w")
        
        self.lbl_arquivo_rotate = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado.", text_color="gray")
        self.lbl_arquivo_rotate.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        
        ctk.CTkLabel(frame, text="Ângulo de Rotação:").grid(row=7, column=0, padx=20, pady=5, sticky="w")
        self.option_rotate_angle = ctk.CTkOptionMenu(frame, values=["90", "180", "270"])
        self.option_rotate_angle.set("90")
        self.option_rotate_angle.grid(row=7, column=0, padx=(150, 0), pady=5, sticky="w")
        
        self.btn_rotate_pdf = ctk.CTkButton(frame, text="🔄 2. Rotacionar e Salvar", fg_color="green", state="disabled", command=self._acao_rotacionar_pdf)
        self.btn_rotate_pdf.grid(row=5, column=1, padx=20, pady=5, sticky="e")
        
        self.arquivo_rotacao = None

    def _acao_selecionar_pdf_split(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if arquivo:
            self.arquivo_divisao = arquivo
            self.lbl_arquivo_split.configure(text=os.path.basename(arquivo))
            self.btn_split_pdf.configure(state="normal")
            self.console.log(f"Arquivo selecionado: {os.path.basename(arquivo)}", "info")
        else:
            self.lbl_arquivo_split.configure(text="Nenhum arquivo selecionado.")
            self.btn_split_pdf.configure(state="disabled")

    def _acao_dividir_pdf(self):
        if not self.arquivo_divisao:
            return
            
        try:
            paginas_por_arquivo = int(self.entry_split_pages.get())
            if paginas_por_arquivo <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "O número de páginas por arquivo deve ser um número inteiro positivo.")
            return

        diretorio_salvar = filedialog.askdirectory(title="Selecione a Pasta para Salvar os Arquivos Divididos")
        if not diretorio_salvar:
            return

        task_name = f"Dividir PDF: {os.path.basename(self.arquivo_divisao)}"
        self.console.log(f"Adicionando à fila: {task_name}", "process")
        self.task_queue.submit_task(
            self.pdf_tool.dividir_pdf,
            self.arquivo_divisao,
            diretorio_salvar,
            paginas_por_arquivo,
            task_name=task_name
        )
        
        messagebox.showinfo("Sucesso", f"Tarefa '{task_name}' adicionada à fila.")
        self.arquivo_divisao = None
        self.lbl_arquivo_split.configure(text="Nenhum arquivo selecionado.")
        self.btn_split_pdf.configure(state="disabled")

    def _acao_selecionar_pdf_rotate(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if arquivo:
            self.arquivo_rotacao = arquivo
            self.lbl_arquivo_rotate.configure(text=os.path.basename(arquivo))
            self.btn_rotate_pdf.configure(state="normal")
            self.console.log(f"Arquivo selecionado: {os.path.basename(arquivo)}", "info")
        else:
            self.lbl_arquivo_rotate.configure(text="Nenhum arquivo selecionado.")
            self.btn_rotate_pdf.configure(state="disabled")

    def _acao_rotacionar_pdf(self):
        if not self.arquivo_rotacao:
            return
            
        angulo = int(self.option_rotate_angle.get())

        caminho_salvar = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")], initialfile=f"{os.path.splitext(os.path.basename(self.arquivo_rotacao))[0]}_rotacionado.pdf")
        if not caminho_salvar:
            return

        task_name = f"Rotacionar PDF: {os.path.basename(self.arquivo_rotacao)}"
        self.console.log(f"Adicionando à fila: {task_name}", "process")
        self.task_queue.submit_task(
            self.pdf_tool.rotacionar_pdf,
            self.arquivo_rotacao,
            caminho_salvar,
            angulo,
            task_name=task_name
        )
        
        messagebox.showinfo("Sucesso", f"Tarefa '{task_name}' adicionada à fila.")
        self.arquivo_rotacao = None
        self.lbl_arquivo_rotate.configure(text="Nenhum arquivo selecionado.")
        self.btn_rotate_pdf.configure(state="disabled")

    # ==========================
    # LÓGICA DA ABA EXTRAIR TEXTO (OCR)
    # ==========================
    def _setup_aba_pdf_ocr(self):
        frame = self.tab_pdf_ocr
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame, text="📝 Extrair Texto de PDF (OCR)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        btn_select_ocr = ctk.CTkButton(frame, text="📁 1. Selecionar PDF", command=self._acao_selecionar_pdf_ocr)
        btn_select_ocr.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        self.lbl_arquivo_ocr = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado.", text_color="gray")
        self.lbl_arquivo_ocr.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        
        self.btn_ocr_pdf = ctk.CTkButton(frame, text="📝 2. Extrair Texto e Salvar", fg_color="green", state="disabled", command=self._acao_extrair_texto_ocr)
        self.btn_ocr_pdf.grid(row=1, column=1, padx=20, pady=5, sticky="e")
        
        self.arquivo_ocr = None

    def _acao_selecionar_pdf_ocr(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if arquivo:
            self.arquivo_ocr = arquivo
            self.lbl_arquivo_ocr.configure(text=os.path.basename(arquivo))
            self.btn_ocr_pdf.configure(state="normal")
            self.console.log(f"Arquivo selecionado: {os.path.basename(arquivo)}", "info")
        else:
            self.lbl_arquivo_ocr.configure(text="Nenhum arquivo selecionado.")
            self.btn_ocr_pdf.configure(state="disabled")

    def _acao_extrair_texto_ocr(self):
        if not self.arquivo_ocr:
            return

        caminho_salvar = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto", "*.txt")], initialfile=f"{os.path.splitext(os.path.basename(self.arquivo_ocr))[0]}_extraido.txt")
        if not caminho_salvar:
            return

        task_name = f"OCR PDF: {os.path.basename(self.arquivo_ocr)}"
        self.console.log(f"Adicionando à fila: {task_name}", "process")
        self.task_queue.submit_task(
            self.pdf_tool.extrair_texto_ocr,
            self.arquivo_ocr,
            caminho_salvar,
            task_name=task_name
        )
        
        messagebox.showinfo("Sucesso", f"Tarefa '{task_name}' adicionada à fila. O resultado será um arquivo de texto.")
        self.arquivo_ocr = None
        self.lbl_arquivo_ocr.configure(text="Nenhum arquivo selecionado.")
        self.btn_ocr_pdf.configure(state="disabled")

    # ==========================
    # LÓGICA DA ABA QR CODE
    # ==========================
    def _setup_aba_qr(self):
        # Grid layout
        self.tab_qr.grid_columnconfigure(0, weight=1)

        # Input
        ctk.CTkLabel(self.tab_qr, text="Digite o Link, Texto ou Wi-Fi:").pack(pady=(20,5))
        self.entry_qr = ctk.CTkEntry(self.tab_qr, width=400, placeholder_text="Ex: https://minhaempresa.com.br")
        self.entry_qr.pack(pady=5)

        # Botão Gerar
        btn_gerar = ctk.CTkButton(self.tab_qr, text="📱 Gerar QR Code", command=self._acao_gerar_qr)
        btn_gerar.pack(pady=20)
        add_tooltip(btn_gerar, "btn_gerar_qr")

        # Área de Preview da Imagem
        self.lbl_preview_img = ctk.CTkLabel(self.tab_qr, text="[Preview da Imagem]")
        self.lbl_preview_img.pack(pady=10)
        
        # Botão Salvar (só aparece depois de gerar)
        self.btn_salvar_qr = ctk.CTkButton(self.tab_qr, text="Salvar Imagem", state="disabled", 
                                           fg_color="green", command=self._acao_salvar_qr)
        self.btn_salvar_qr.pack(pady=10)
        
        self.imagem_qr_temp = None # Guarda o caminho temporário

    def _acao_gerar_qr(self):
        texto = self.entry_qr.get()
        if not texto:
            return
        
        # A geração de QR Code é rápida, não precisa de TaskQueue
        caminho_temp = "temp_qr_preview.png"
        self.qr_tool.gerar_qrcode(texto, caminho_temp)
        self.imagem_qr_temp = caminho_temp

        # Carrega a imagem na interface (usando CTkImage para alta DPI)
        pil_img = Image.open(caminho_temp)
        tk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(200, 200))
        
        self.lbl_preview_img.configure(image=tk_img, text="") # Remove o texto, mostra img
        self.btn_salvar_qr.configure(state="normal")
        self.console.log("QR Code gerado com sucesso", "success")

    def _acao_salvar_qr(self):
        if not self.imagem_qr_temp:
            return
            
        destino = filedialog.asksaveasfilename(defaultextension=".png", 
                                               filetypes=[("Imagem PNG", "*.png")],
                                               initialfile="qrcode.png")
        if destino:
            import shutil
            shutil.copy(self.imagem_qr_temp, destino)
            self.console.log(f"QR Code salvo: {destino}", "success")
            messagebox.showinfo("Sucesso", "QR Code salvo!")

            # Limpar após salvar
            try:
                os.remove(self.imagem_qr_temp)
                self.imagem_qr_temp = None
                self.lbl_preview_img.configure(image=None, text="[Preview da Imagem]")
                self.btn_salvar_qr.configure(state="disabled")
            except Exception as e:
                self.console.log(f"Não foi possível remover o arquivo temporário: {e}", "warning")
