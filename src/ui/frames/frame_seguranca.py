import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from src.modules.security import SecurityTools
from src.ui.components.tooltip import add_tooltip
from src.ui.components.unified_console import UnifiedConsole

class FrameSeguranca(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        # Layout: Grid 2 linhas (conteúdo + console)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)  # Console fixo na parte inferior
        self.grid_columnconfigure(0, weight=1)

        # === ÁREA DE CONTEÚDO ===
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        # Título
        ctk.CTkLabel(self.frame_conteudo, text="Cofre de Segurança (AES-256)", 
                     font=ctk.CTkFont(size=24, weight="bold"), text_color="#4cc9f0").pack(pady=20, anchor="w")

        # Abas
        self.tabview = ctk.CTkTabview(self.frame_conteudo, width=800, height=400)
        self.tabview.pack(fill="both", expand=True)

        self.tab_arquivo = self.tabview.add("Criptografar Arquivo")
        self.tab_pasta = self.tabview.add("Cofre de Pasta (Zip)")
        self.tab_compartilhar = self.tabview.add("📤 Compartilhar")

        self._setup_tab_arquivo()
        self._setup_tab_pasta()
        self._setup_tab_compartilhar()

        # === CONSOLE UNIFICADO ===
        self.console = UnifiedConsole(self, height=100, title="📋 Console de Execução")
        self.console.grid(row=1, column=0, sticky="ew")
        self.console.log("Sistema de segurança pronto. Selecione uma opção acima.", "info")

    # ==========================
    # ABA 1: ARQUIVO ÚNICO
    # ==========================
    def _setup_tab_arquivo(self):
        tab = self.tab_arquivo
        
        # Seleção
        btn_select = ctk.CTkButton(tab, text="📁 Selecionar Arquivo", command=self.acao_select_file)
        btn_select.pack(pady=20)
        add_tooltip(btn_select, "Escolha o arquivo que deseja criptografar ou descriptografar.")
        self.lbl_file = ctk.CTkLabel(tab, text="Nenhum arquivo selecionado", text_color="gray")
        self.lbl_file.pack()
        
        # Senha
        ctk.CTkLabel(tab, text="Senha de Proteção:").pack(pady=(20, 5))
        self.entry_senha_file = ctk.CTkEntry(tab, show="*", width=300)
        self.entry_senha_file.pack()

        # Opções
        self.switch_delete = ctk.CTkSwitch(tab, text="⚠️ Deletar arquivo original após criptografar")
        self.switch_delete.pack(pady=15)
        add_tooltip(self.switch_delete, "switch_delete_original")

        # Ações
        frame_btns = ctk.CTkFrame(tab, fg_color="transparent")
        frame_btns.pack(pady=10)

        btn_encrypt = ctk.CTkButton(frame_btns, text="🔒 CRIPTOGRAFAR", fg_color="#ef233c", 
                      command=self.acao_encrypt)
        btn_encrypt.grid(row=0, column=0, padx=10)
        add_tooltip(btn_encrypt, "btn_criptografar")
        
        btn_decrypt = ctk.CTkButton(frame_btns, text="🔓 DESCRIPTOGRAFAR", fg_color="#06d6a0", 
                      command=self.acao_decrypt)
        btn_decrypt.grid(row=0, column=1, padx=10)
        add_tooltip(btn_decrypt, "btn_descriptografar")

        self.arquivo_alvo = None

    def acao_select_file(self):
        f = filedialog.askopenfilename()
        if f:
            self.arquivo_alvo = f
            self.lbl_file.configure(text=os.path.basename(f), text_color="white")
            self.console.log(f"Arquivo selecionado: {os.path.basename(f)}", "info")

    def acao_encrypt(self):
        self._executar_crypto(modo="encrypt")

    def acao_decrypt(self):
        self._executar_crypto(modo="decrypt")

    def _executar_crypto(self, modo):
        senha = self.entry_senha_file.get()
        if not self.arquivo_alvo or not senha:
            messagebox.showwarning("Atenção", "Selecione um arquivo e digite uma senha.")
            return

        tool = SecurityTools(logger_callback=self.console.log)
        
        # Roda em thread para não travar a interface
        def task():
            try:
                if modo == "encrypt":
                    self.console.log(f"🔒 Criptografando: {self.arquivo_alvo}", "process")
                    apagar = (self.switch_delete.get() == 1)
                    result = tool.criptografar_arquivo(self.arquivo_alvo, senha, apagar)
                    if result:
                        self.console.log("✅ Criptografia concluída com sucesso!", "success")
                    else:
                        self.console.log("❌ Erro na criptografia - Verifique se o arquivo existe", "error")
                else:
                    self.console.log(f"🔓 Descriptografando: {self.arquivo_alvo}", "process")
                    result = tool.descriptografar_arquivo(self.arquivo_alvo, senha)
                    if result:
                        self.console.log("✅ Descriptografia concluída com sucesso!", "success")
                    else:
                        self.console.log("❌ Erro na descriptografia - Senha incorreta?", "error")
            except Exception as e:
                self.console.log(f"❌ ERRO: {str(e)}", "error")
                messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
                
        threading.Thread(target=task).start()

    # ==========================
    # ABA 2: PASTA SEGURA
    # ==========================
    def _setup_tab_pasta(self):
        tab = self.tab_pasta
        
        ctk.CTkLabel(tab, text="Cria um arquivo .ZIP blindado com senha").pack(pady=10)

        btn_select_folder = ctk.CTkButton(tab, text="📁 Selecionar Pasta para o Cofre", command=self.acao_select_folder)
        btn_select_folder.pack(pady=10)
        add_tooltip(btn_select_folder, "Escolha a pasta que será compactada e criptografada no cofre.")
        
        self.lbl_folder = ctk.CTkLabel(tab, text="Nenhuma pasta", text_color="gray")
        self.lbl_folder.pack()

        ctk.CTkLabel(tab, text="🔐 Senha do Cofre:").pack(pady=(20, 5))
        self.entry_senha_folder = ctk.CTkEntry(tab, show="*", width=300)
        self.entry_senha_folder.pack()

        btn_create_cofre = ctk.CTkButton(tab, text="📦 CRIAR COFRE AGORA", height=50, font=("Arial", 16, "bold"),
                      command=self.acao_zip_folder)
        btn_create_cofre.pack(pady=30)
        add_tooltip(btn_create_cofre, "btn_criar_cofre")
        
        self.pasta_alvo = None

    def acao_select_folder(self):
        d = filedialog.askdirectory()
        if d:
            self.pasta_alvo = d
            self.lbl_folder.configure(text=d, text_color="white")
            self.console.log(f"Pasta selecionada: {d}", "info")

    def acao_zip_folder(self):
        senha = self.entry_senha_folder.get()
        if not self.pasta_alvo or not senha:
            messagebox.showwarning("Atenção", "Selecione uma pasta e digite uma senha.")
            return
        
        tool = SecurityTools(logger_callback=self.console.log)
        
        def task():
            try:
                self.console.log(f"📦 Criando cofre para: {self.pasta_alvo}", "process")
                result = tool.criar_pasta_cofre(self.pasta_alvo, senha)
                if result:
                    self.console.log("✅ Cofre criado com sucesso!", "success")
                    messagebox.showinfo("Sucesso", f"Cofre criado: {self.pasta_alvo}_COFRE.zip")
                else:
                    self.console.log("❌ Erro ao criar cofre", "error")
            except Exception as e:
                self.console.log(f"❌ ERRO: {str(e)}", "error")
                messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        
        threading.Thread(target=task).start()

    # ==========================
    # ABA 3: COMPARTILHAR
    # ==========================
    def _setup_tab_compartilhar(self):
        tab = self.tab_compartilhar
        
        # Info
        info = ctk.CTkFrame(tab, fg_color="#1a1a2e")
        info.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(info, text="📤 Crie pacotes seguros para enviar por email", 
                    font=("Arial", 14, "bold"), text_color="#4cc9f0").pack(pady=10)
        ctk.CTkLabel(info, text="O destinatário receberá um arquivo ZIP com o arquivo criptografado\n" +
                    "e um programa para descriptografar sem precisar do Titanium Suite.", 
                    text_color="gray").pack(pady=(0, 10))
        
        # Seleção do arquivo .enc
        ctk.CTkLabel(tab, text="Selecione o arquivo .enc já criptografado:", 
                    font=("Arial", 12, "bold")).pack(pady=(10, 5))
        
        btn_select_enc = ctk.CTkButton(tab, text="📁 Selecionar Arquivo Criptografado (.enc)", 
                                       command=self.acao_select_enc)
        btn_select_enc.pack(pady=5)
        
        self.lbl_enc = ctk.CTkLabel(tab, text="Nenhum arquivo selecionado", text_color="gray")
        self.lbl_enc.pack()
        
        # Senha para o destinatário
        ctk.CTkLabel(tab, text="Senha para o destinatário:", 
                    font=("Arial", 12, "bold")).pack(pady=(20, 5))
        self.entry_senha_compartilhar = ctk.CTkEntry(tab, show="*", width=300)
        self.entry_senha_compartilhar.pack()
        
        ctk.CTkLabel(tab, text="⚠️ Esta será a senha que o destinatário deve usar", 
                    text_color="gray", font=("Arial", 10)).pack()
        
        # Criar pacote
        btn_criar_pacote = ctk.CTkButton(tab, text="📦 CRIAR PACOTE PARA COMPARTILHAR", 
                                         height=50, fg_color="#7209b7",
                                         command=self.acao_criar_pacote)
        btn_criar_pacote.pack(pady=30)
        
        self.arquivo_enc_selecionado = None
    
    def acao_select_enc(self):
        f = filedialog.askopenfilename(filetypes=[("Arquivos criptografados", "*.enc")])
        if f:
            self.arquivo_enc_selecionado = f
            self.lbl_enc.configure(text=os.path.basename(f), text_color="#4cc9f0")
            self.console.log(f"Arquivo selecionado: {os.path.basename(f)}", "info")
    
    def acao_criar_pacote(self):
        if not self.arquivo_enc_selecionado:
            messagebox.showwarning("Aviso", "Selecione um arquivo .enc primeiro.")
            return
        
        senha_destinatario = self.entry_senha_compartilhar.get()
        if not senha_destinatario:
            messagebox.showwarning("Aviso", "Digite uma senha para o destinatário.")
            return
        
        self.console.log(f"📦 Criando pacote para: {self.arquivo_enc_selecionado}", "process")
        
        def task():
            try:
                import shutil
                import zipfile
                
                pasta_temp = "pacote_temp"
                if os.path.exists(pasta_temp):
                    shutil.rmtree(pasta_temp)
                os.makedirs(pasta_temp)
                
                shutil.copy(self.arquivo_enc_selecionado, pasta_temp)
                
                # SCRIPT PYTHON EMBUTIDO - MODIFICADO PARA SEGURANÇA
                script_py = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, base64, getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def gerar_chave(senha, salt):
    """Gera uma chave de criptografia a partir da senha e do salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000
    )
    return Fernet(base64.urlsafe_b64encode(kdf.derive(senha.encode('utf-8'))))

def main():
    """Função principal para descriptografar o arquivo."""
    try:
        # Pega o nome do arquivo do argumento da linha de comando
        if len(sys.argv) > 1:
            arquivo_enc = sys.argv[1]
        else:
            # Se nenhum argumento for passado, procura por um arquivo .enc no diretório
            arquivos_enc = [f for f in os.listdir('.') if f.endswith('.enc')]
            if not arquivos_enc:
                print("\\n[!] Nenhum arquivo .enc encontrado no diretório.")
                input("Pressione Enter para sair...")
                return
            arquivo_enc = arquivos_enc[0]
        
        print(f"Arquivo a ser descriptografado: {arquivo_enc}")
        if not os.path.exists(arquivo_enc):
            print(f"\\n[!] ERRO: Arquivo '{arquivo_enc}' não encontrado!")
            input("Pressione Enter para sair...")
            return

        # Pede a senha de forma segura
        senha = getpass.getpass("Digite a senha de descriptografia: ")
        
        with open(arquivo_enc, "rb") as f:
            conteudo = f.read()
        
        salt = conteudo[:16]
        dados_criptografados = conteudo[16:]
        
        fernet = gerar_chave(senha, salt)
        dados_originais = fernet.decrypt(dados_criptografados)
        
        nome_original = arquivo_enc.rsplit('.enc', 1)[0]
        with open(nome_original, "wb") as f:
            f.write(dados_originais)
            
        print(f"\\n[SUCCESS] Arquivo '{nome_original}' descriptografado com sucesso!")
        
    except Exception as e:
        print(f"\\n[!] ERRO: Falha ao descriptografar. Verifique a senha ou a integridade do arquivo.")
        # print(f"Detalhes do erro: {e}") # Descomente para depuração
        
    finally:
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
'''
                with open(os.path.join(pasta_temp, "descriptografar.py"), "w", encoding="utf-8") as f:
                    f.write(script_py)
                
                # BATCH SCRIPT - MODIFICADO PARA NÃO INCLUIR A SENHA
                batch = f"""@echo off
chcp 65001 > nul
echo.
echo ========================================
echo  Descriptografador Titanium Suite
echo ========================================
echo.
echo Este script ira pedir a senha para restaurar o arquivo seguro.

python descriptografar.py "{os.path.basename(self.arquivo_enc_selecionado)}"

echo.
echo Processo finalizado.
pause"""
                with open(os.path.join(pasta_temp, "descriptografar.bat"), "w", encoding="utf-8") as f:
                    f.write(batch)
                
                instr = f"""INSTRUCOES DE DESCRIPTOGRAFIA
================================
1. Dê um duplo clique no arquivo "descriptografar.bat".
2. Uma tela preta aparecerá pedindo a senha.
3. Digite a senha que você recebeu e pressione Enter.
   (A senha não aparecerá enquanto você digita, por segurança).
4. Se a senha estiver correta, o arquivo original será restaurado nesta pasta.

Arquivo a ser restaurado: {os.path.basename(self.arquivo_enc_selecionado).replace('.enc', '')}
"""
                with open(os.path.join(pasta_temp, "LEIA-ME.txt"), "w", encoding="utf-8") as f:
                    f.write(instr)
                
                nome_zip = self.arquivo_enc_selecionado.replace(".enc", "_PARA_ENVIAR.zip")
                with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for raiz, dirs, arquivos in os.walk(pasta_temp):
                        for arq in arquivos:
                            caminho = os.path.join(raiz, arq)
                            zf.write(caminho, os.path.relpath(caminho, pasta_temp))
                
                shutil.rmtree(pasta_temp)
                
                self.console.log(f"✅ Pacote seguro criado: {nome_zip}", "success")
                messagebox.showinfo("Sucesso", f"Pacote criado com sucesso!\n\nEnvie o arquivo: {os.path.basename(nome_zip)}")
                
            except Exception as e:
                self.console.log(f"❌ ERRO ao criar pacote: {str(e)}", "error")
                messagebox.showerror("Erro", str(e))
        
        threading.Thread(target=task).start()
