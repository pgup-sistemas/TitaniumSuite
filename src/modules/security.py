import os
import base64
import pyzipper
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecurityTools:
    def __init__(self, logger_callback=None):
        self.log = logger_callback if logger_callback else print

    def _gerar_chave_da_senha(self, senha, salt=None):
        """
        Deriva uma chave segura de 32 bytes baseada na senha do usuário.
        Se não houver salt (criptografando), gera um novo.
        Se houver salt (descriptografando), usa o existente.
        """
        if salt is None:
            salt = os.urandom(16) # Gera 16 bytes aleatórios
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000, # 100k voltas para tornar lento para hackers
        )
        chave = base64.urlsafe_b64encode(kdf.derive(senha.encode()))
        return chave, salt

    def criptografar_arquivo(self, caminho_arquivo, senha, apagar_original=False):
        """Lê arquivo -> Gera Salt+Chave -> Criptografa -> Salva .enc"""
        self.log(f"🔒 Trancando: {os.path.basename(caminho_arquivo)}...")
        
        try:
            # 1. Preparar a chave
            chave, salt = self._gerar_chave_da_senha(senha)
            f = Fernet(chave)

            # 2. Ler o conteúdo original
            with open(caminho_arquivo, "rb") as file:
                dados = file.read()

            # 3. Criptografar
            dados_cifrados = f.encrypt(dados)

            # 4. Salvar (O segredo: Escrevemos o SALT nos primeiros 16 bytes)
            novo_nome = caminho_arquivo + ".enc"
            with open(novo_nome, "wb") as file:
                file.write(salt + dados_cifrados)

            # 5. Opcional: Destruir original
            if apagar_original:
                os.remove(caminho_arquivo)
                self.log("🗑️ Arquivo original removido por segurança.")

            self.log(f"✅ Sucesso! Arquivo protegido: {os.path.basename(novo_nome)}")
            return True

        except Exception as e:
            self.log(f"❌ Erro na criptografia: {e}")
            return False

    def descriptografar_arquivo(self, caminho_arquivo_enc, senha):
        """Lê Salt do arquivo -> Recria a Chave -> Destranca"""
        self.log(f"🔓 Destrancando: {os.path.basename(caminho_arquivo_enc)}...")
        
        try:
            with open(caminho_arquivo_enc, "rb") as file:
                conteudo = file.read()

            # 1. Separar o Salt (primeiros 16 bytes) do resto
            salt = conteudo[:16]
            dados_cifrados = conteudo[16:]

            # 2. Recriar a chave exata
            chave, _ = self._gerar_chave_da_senha(senha, salt)
            f = Fernet(chave)

            # 3. Tentar descriptografar (Se a senha for errada, falha aqui)
            dados_originais = f.decrypt(dados_cifrados)

            # 4. Salvar arquivo limpo (Remove o .enc)
            nome_original = caminho_arquivo_enc.replace(".enc", "")
            with open(nome_original, "wb") as file:
                file.write(dados_originais)

            self.log(f"✅ Arquivo restaurado: {os.path.basename(nome_original)}")
            return True

        except Exception:
            self.log("❌ ERRO: Senha incorreta ou arquivo corrompido.")
            return False

    def criar_pasta_cofre(self, pasta_alvo, senha):
        """Compacta uma pasta inteira num ZIP com senha AES-256"""
        nome_zip = f"{pasta_alvo}_COFRE.zip"
        self.log(f"📦 Criando cofre para pasta: {pasta_alvo}")

        try:
            with pyzipper.AESZipFile(nome_zip, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(senha.encode('utf-8'))
                
                for folder, _, files in os.walk(pasta_alvo):
                    for file in files:
                        caminho_abs = os.path.join(folder, file)
                        caminho_rel = os.path.relpath(caminho_abs, os.path.dirname(pasta_alvo))
                        zf.write(caminho_abs, arcname=caminho_rel)
            
            self.log(f"✅ Cofre criado com sucesso: {nome_zip}")
            return True
        except Exception as e:
            self.log(f"❌ Erro ao criar cofre: {e}")
            return False