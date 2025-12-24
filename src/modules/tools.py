import os
import qrcode
import cv2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

class PDFTools:
    def __init__(self, logger_callback=None):
        self.log = logger_callback if logger_callback else print

    def unir_pdfs(self, lista_arquivos, arquivo_saida):
        """Junta vários PDFs em um só."""
        self.log(f"--- Iniciando Fusão de {len(lista_arquivos)} arquivos ---")
        
        merger = PdfMerger()
        try:
            for pdf in lista_arquivos:
                self.log(f"Adicionando: {os.path.basename(pdf)}")
                merger.append(pdf)
            
            merger.write(arquivo_saida)
            merger.close()
            self.log(f"✅ Sucesso! Arquivo salvo em: {arquivo_saida}")
            return True
        except Exception as e:
            self.log(f"❌ Erro ao unir PDFs: {e}")
            return False

    def comprimir_pdf(self, arquivo_entrada, arquivo_saida):
        """
        Remove metadados e comprime streams para reduzir tamanho.
        Nota: A compressão do PyPDF2 é básica. Para compressão forte (tipo Adobe),
        seria necessário Ghostscript, mas vamos manter Python puro.
        """
        self.log(f"Comprimindo: {os.path.basename(arquivo_entrada)}")
        try:
            reader = PdfReader(arquivo_entrada)
            writer = PdfWriter()

            for page in reader.pages:
                page.compress_content_streams() # Nível 1 de compressão
                writer.add_page(page)
            
            # Remove metadados desnecessários
            writer.add_metadata({}) 
            
            with open(arquivo_saida, "wb") as f:
                writer.write(f)
            
            self.log(f"✅ PDF Comprimido salvo em: {arquivo_saida}")
            return True
        except Exception as e:
            self.log(f"❌ Erro na compressão: {e}")
            return False

    def dividir_pdf(self, arquivo_entrada, diretorio_saida, paginas_por_lote):
        """Divide um PDF em vários arquivos menores."""
        self.log(f"--- Iniciando Divisão de PDF ---")
        self.log(f"Arquivo: {os.path.basename(arquivo_entrada)}")
        self.log(f"Páginas por arquivo: {paginas_por_lote}")

        try:
            reader = PdfReader(arquivo_entrada)
            total_paginas = len(reader.pages)
            nome_base = os.path.splitext(os.path.basename(arquivo_entrada))[0]

            for i in range(0, total_paginas, paginas_por_lote):
                writer = PdfWriter()
                inicio = i
                fim = min(i + paginas_por_lote, total_paginas)
                
                for j in range(inicio, fim):
                    writer.add_page(reader.pages[j])

                arquivo_saida = os.path.join(diretorio_saida, f"{nome_base}_parte_{i//paginas_por_lote + 1}.pdf")
                with open(arquivo_saida, "wb") as f:
                    writer.write(f)
                self.log(f"✅ Parte {i//paginas_por_lote + 1} salva em: {arquivo_saida}")

            self.log("--- Divisão Concluída com Sucesso ---")
            return True
        except Exception as e:
            self.log(f"❌ Erro ao dividir PDF: {e}")
            return False

    def rotacionar_pdf(self, arquivo_entrada, arquivo_saida, angulo):
        """Rotaciona todas as páginas de um PDF."""
        self.log(f"--- Iniciando Rotação de PDF ---")
        self.log(f"Arquivo: {os.path.basename(arquivo_entrada)}")
        self.log(f"Ângulo: {angulo} graus")

        try:
            reader = PdfReader(arquivo_entrada)
            writer = PdfWriter()

            for page in reader.pages:
                page.rotate(angulo)
                writer.add_page(page)

            with open(arquivo_saida, "wb") as f:
                writer.write(f)

            self.log(f"✅ PDF Rotacionado salvo em: {arquivo_saida}")
            return True
        except Exception as e:
            self.log(f"❌ Erro ao rotacionar PDF: {e}")
            return False

    def extrair_texto_ocr(self, arquivo_entrada, arquivo_saida):
        """
        Extrai texto de um PDF usando OCR. Requer Tesseract e Poppler.
        - Tesseract: https://github.com/tesseract-ocr/tesseract
        - Poppler: https://poppler.freedesktop.org/
        """
        self.log("--- Iniciando Extração de Texto (OCR) ---")
        self.log(f"Arquivo: {os.path.basename(arquivo_entrada)}")
        
        try:
            # 1. Converter PDF para uma lista de imagens
            self.log("Convertendo PDF para imagens...")
            imagens = convert_from_path(arquivo_entrada)
            
            texto_completo = ""
            for i, img in enumerate(imagens):
                self.log(f"Processando página {i+1}/{len(imagens)}...")
                
                # 2. Usar pytesseract para extrair texto da imagem
                texto_pagina = pytesseract.image_to_string(img, lang='por') # Assumindo português
                texto_completo += f"\n--- Página {i+1} ---\n{texto_pagina}"

            # 3. Salvar o texto extraído em um arquivo .txt
            with open(arquivo_saida, "w", encoding="utf-8") as f:
                f.write(texto_completo)

            self.log(f"✅ Texto extraído salvo em: {arquivo_saida}")
            return True
        except pytesseract.TesseractNotFoundError:
            self.log("❌ ERRO: Tesseract não encontrado. Verifique se ele está instalado e no PATH do sistema.")
            return False
        except Exception as e:
            self.log(f"❌ Erro durante o OCR: {e}")
            return False
        
class QRTools:
    def __init__(self, logger_callback=None):
        self.log = logger_callback if logger_callback else print

    def gerar_qrcode(self, dados, arquivo_saida, cor_fundo="white", cor_frente="black"):
        self.log(f"Gerando QR Code para: {dados}")
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H, # Alta correção (permite sujeira/logo)
                box_size=10,
                border=4,
            )
            qr.add_data(dados)
            qr.make(fit=True)

            img = qr.make_image(fill_color=cor_frente, back_color=cor_fundo)
            img.save(arquivo_saida)
            
            self.log(f"✅ QR Code salvo em: {arquivo_saida}")
            return str(arquivo_saida) # Retorna caminho para exibir na tela
        except Exception as e:
            self.log(f"❌ Erro ao gerar QR: {e}")
            return None