import os
from PIL import Image
from pypdf import PdfWriter
from reportlab.pdfgen import canvas
import pandas as pd
import numpy as np

TEMP_DIR = "tests/temp_files"

def create_dummy_image(filename="test_image.png"):
    """Cria uma imagem PNG simples."""
    path = os.path.join(TEMP_DIR, filename)
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save(path)
    return path

def create_dummy_pdf(filename="test_pdf.pdf", num_pages=2):
    """Cria um PDF simples com texto."""
    path = os.path.join(TEMP_DIR, filename)
    c = canvas.Canvas(path)
    for i in range(num_pages):
        c.drawString(100, 750, f"Pagina {i+1} de teste.")
        c.showPage()
    c.save()
    return path

def create_dummy_excel(filename="test_excel.xlsx", num_rows=10, with_duplicates=False):
    """Cria um arquivo Excel simples."""
    path = os.path.join(TEMP_DIR, filename)
    
    data = {
        'ID': np.arange(num_rows),
        'Nome': [f'Nome_{i}' for i in range(num_rows)],
        'Valor': np.random.randint(10, 100, num_rows)
    }
    df = pd.DataFrame(data)
    
    if with_duplicates:
        # Adiciona 2 linhas duplicadas
        df.loc[num_rows] = df.iloc[0]
        df.loc[num_rows+1] = df.iloc[1]
        
    df.to_excel(path, index=False)
    return path

def create_dummy_files():
    """Cria todos os arquivos de teste necessários."""
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    print("Criando arquivos de teste...")
    
    # Imagens
    create_dummy_image("img1.png")
    create_dummy_image("img2.jpg")
    
    # PDFs
    create_dummy_pdf("doc1.pdf", 3)
    create_dummy_pdf("doc2.pdf", 1)
    
    # Excel
    create_dummy_excel("data1.xlsx", 5)
    create_dummy_excel("data2.xlsx", 5, with_duplicates=True)
    
    # Arquivos para duplicados (SystemTools)
    with open(os.path.join(TEMP_DIR, "file_a.txt"), "w") as f: f.write("conteudo duplicado")
    with open(os.path.join(TEMP_DIR, "file_b.txt"), "w") as f: f.write("conteudo duplicado")
    with open(os.path.join(TEMP_DIR, "file_c.txt"), "w") as f: f.write("conteudo unico")
    
    print("Arquivos de teste criados com sucesso.")

if __name__ == "__main__":
    create_dummy_files()
