#!/usr/bin/env python
"""
Descriptografador Standalone do Titanium Suite
Este script pode ser enviado junto com o arquivo .enc para que
outra pessoa possa descriptografar sem precisar do Titanium Suite.
"""

import os
import sys
import base64
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def gerar_chave(senha, salt):
    """Gera a chave Fernet a partir da senha"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    chave = base64.urlsafe_b64encode(kdf.derive(senha.encode('utf-8')))
    return Fernet(chave)

def descriptografar(arquivo_enc, senha, pasta_saida=None):
    """Descriptografa um arquivo .enc"""
    try:
        with open(arquivo_enc, "rb") as f:
            conteudo = f.read()
        
        salt = conteudo[:16]
        dados_cifrados = conteudo[16:]
        
        fernet = gerar_chave(senha, salt)
        dados_originais = fernet.decrypt(dados_cifrados)
        
        nome_original = arquivo_enc.rsplit('.enc', 1)[0]
        if pasta_saida:
            nome_original = os.path.join(pasta_saida, os.path.basename(arquivo_enc.rsplit('.enc', 1)[0]))
        
        with open(nome_original, "wb") as f:
            f.write(dados_originais)
        
        return True, nome_original
    except Exception:
        # A exceção mais comum aqui é InvalidToken da biblioteca, que indica senha errada.
        return False, "Senha incorreta ou arquivo corrompido."

def main():
    """Interface de linha de comando"""
    try:
        print("=" * 50)
        print("🔓 DESCRIPTOGRAFADOR TITANIUM SUITE")
        print("=" * 50)

        # Determina o arquivo a ser descriptografado
        if len(sys.argv) > 1:
            arquivo = sys.argv[1]
            print(f"Arquivo alvo: {arquivo}")
        else:
            arquivos_enc = [f for f in os.listdir('.') if f.endswith('.enc')]
            if not arquivos_enc:
                print("\\n[!] Nenhum arquivo .enc encontrado neste diretório.")
                return
            arquivo = arquivos_enc[0]
            print(f"Arquivo encontrado: {arquivo}")

        if not os.path.exists(arquivo):
            print(f"\\n[!] ERRO: Arquivo '{arquivo}' não encontrado!")
            return
        
        # Pede a senha de forma segura
        senha = getpass.getpass("Digite a senha: ")
        
        sucesso, resultado = descriptografar(arquivo, senha)
        
        if sucesso:
            print(f"\\n[SUCCESS] Arquivo restaurado com sucesso: {resultado}")
        else:
            print(f"\\n[!] ERRO: {resultado}")

    except Exception as e:
        print(f"\\n[!] Ocorreu um erro inesperado: {e}")
    finally:
        print("\\n")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
