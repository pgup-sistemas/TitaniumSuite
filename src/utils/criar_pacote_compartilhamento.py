#!/usr/bin/env python
"""
Cria um pacote compartilhável com:
1. O arquivo criptografado
2. Um descriptografador executável

Uso: python criar_pacote_compartilhamento.py arquivo.enc
"""

import os
import sys
import shutil
import zipfile

def criar_pacote(arquivo_enc):
    """Cria um pacote compartilhável"""
    
    if not os.path.exists(arquivo_enc):
        print(f"❌ Arquivo não encontrado: {arquivo_enc}")
        return False
    
    nome_base = arquivo_enc.rsplit('.enc', 1)[0]
    
    # Criar diretório temporário
    pasta_temp = "pacote_compartilhamento"
    if os.path.exists(pasta_temp):
        shutil.rmtree(pasta_temp)
    os.makedirs(pasta_temp)
    
    # Copiar arquivo criptografado
    shutil.copy(arquivo_enc, pasta_temp)
    
    # Copiar script descriptografador
    shutil.copy("src/utils/descriptografar_arquivo.py", pasta_temp)
    
    # Criar arquivo de instruções
    instrucoes = f"""
INSTRUÇÕES DE DESCRIPTOGRAFIA
=============================

1. Dê um duplo clique no arquivo "descriptografar.bat".
2. Uma tela preta aparecerá pedindo a senha.
3. Digite a senha que você recebeu e pressione Enter.
   (A senha não aparecerá enquanto você digita, por segurança).
4. Se a senha estiver correta, o arquivo original será restaurado nesta pasta.

ARQUIVO INCLUÍDO:
- {os.path.basename(arquivo_enc)} (arquivo criptografado)
- descriptografar_arquivo.py (script Python)
- descriptografar.bat (atalho para Windows)
"""
    
    with open(os.path.join(pasta_temp, "LEIA-ME.txt"), "w", encoding="utf-8") as f:
        f.write(instrucoes)
    
    # Criar batch file para Windows
    batch_content = f"""@echo off
chcp 65001 > nul
echo ========================================
echo  Descriptografador Titanium Suite
echo ========================================
echo.
echo Este script ira pedir a senha para restaurar o arquivo seguro.

python descriptografar_arquivo.py "{os.path.basename(arquivo_enc)}"

echo.
echo Processo finalizado.
pause
"""
    with open(os.path.join(pasta_temp, "descriptografar.bat"), "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    # Criar ZIP do pacote
    nome_zip = f"{nome_base}_PARA_COMPARTILHAR.zip"
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for raiz, dirs, arquivos in os.walk(pasta_temp):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                caminho_rel = os.path.relpath(caminho_completo, pasta_temp)
                zipf.write(caminho_completo, caminho_rel)
    
    # Limpar pasta temporária
    shutil.rmtree(pasta_temp)
    
    print(f"✅ Pacote criado: {nome_zip}")
    print(f"📧 Envie este arquivo ZIP para o destinatário!")
    return True

def main():
    if len(sys.argv) < 2:
        print("=" * 50)
        print("📦 CRIADOR DE PACOTE PARA COMPARTILHAMENTO")
        print("=" * 50)
        print("\\nUso:")
        print("  python criar_pacote_compartilhamento.py arquivo.enc")
        print("\\nExemplo:")
        print("  python criar_pacote_compartilhamento.py documento.pdf.enc")
        print("\\nIsso criará um arquivo ZIP que você pode enviar por email.")
        print("A senha deverá ser informada ao destinatário por um canal seguro.")
    else:
        arquivo = sys.argv[1]
        criar_pacote(arquivo)

if __name__ == "__main__":
    main()
