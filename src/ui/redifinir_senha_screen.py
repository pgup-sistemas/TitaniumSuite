# src/ui/redifinir_senha_screen.py
"""
Tela de Redefinição de Senha - Sistema Local
Permite redefinir usuário e senha sem necessidade de email/SMS
"""

import customtkinter as ctk
from tkinter import messagebox
from src.modules.auth import AuthManager

class RedefinirSenhaScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.auth = AuthManager()
        
        # Configuração da Janela
        self.title("Redefinir Senha - Titanium Suite")
        self.geometry("500x400")
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        
        self._criar_interface()
    
    def _criar_interface(self):
        """Cria a interface da tela de redefinição"""
        
        # Título
        ctk.CTkLabel(self, text="🔐 REDEFINIR SENHA", 
                     font=("Arial", 24, "bold"), text_color="#4cc9f0").pack(pady=20)
        
        ctk.CTkLabel(self, text="Recuperação Local - Sem Email/SMS", 
                     text_color="gray").pack(pady=(0, 20))
        
        # Frame principal
        self.frame_main = ctk.CTkFrame(self)
        self.frame_main.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Etapa 1: Nome de usuário
        ctk.CTkLabel(self.frame_main, text="1️⃣ Digite seu nome de usuário atual:", 
                     font=("Arial", 14, "bold")).pack(pady=(20, 10))
        
        self.entry_username = ctk.CTkEntry(self.frame_main, width=300, 
                                           placeholder_text="Ex: admin")
        self.entry_username.pack(pady=5)
        
        # Botão para buscar pergunta
        self.btn_buscar = ctk.CTkButton(self.frame_main, text="🔍 Buscar Pergunta de Segurança", 
                                        command=self._buscar_pergunta)
        self.btn_buscar.pack(pady=10)
        
        # Frame para pergunta de segurança (será mostrado dinamicamente)
        self.frame_pergunta = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        
        ctk.CTkLabel(self.frame_pergunta, text="2️⃣ Responda sua pergunta de segurança:", 
                     font=("Arial", 14, "bold")).pack(pady=(20, 10))
        
        self.lbl_pergunta = ctk.CTkLabel(self.frame_pergunta, text="", 
                                         font=("Arial", 12), text_color="#ffd60a",
                                         wraplength=350)
        self.lbl_pergunta.pack(pady=5)
        
        self.entry_resposta = ctk.CTkEntry(self.frame_pergunta, width=300, 
                                           placeholder_text="Digite sua resposta")
        self.entry_resposta.pack(pady=5)
        
        # Frame para nova senha (será mostrado dinamicamente)
        self.frame_nova_senha = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        
        ctk.CTkLabel(self.frame_nova_senha, text="3️⃣ Digite sua nova senha:", 
                     font=("Arial", 14, "bold")).pack(pady=(20, 10))
        
        self.entry_nova_senha = ctk.CTkEntry(self.frame_nova_senha, width=300, 
                                             show="*", placeholder_text="Nova senha")
        self.entry_nova_senha.pack(pady=5)
        
        self.entry_confirmar_senha = ctk.CTkEntry(self.frame_nova_senha, width=300, 
                                                  show="*", placeholder_text="Confirmar nova senha")
        self.entry_confirmar_senha.pack(pady=5)
        
        # Checkbox para alterar usuário também
        self.chk_alterar_usuario = ctk.CTkCheckBox(self.frame_nova_senha, 
                                                   text="✏️ Alterar também o nome de usuário")
        self.chk_alterar_usuario.pack(pady=10)
        
        # Botões de ação
        self.frame_botoes = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        
        self.btn_redefinir = ctk.CTkButton(self.frame_botoes, text="🔄 REDEFINIR SENHA", 
                                           fg_color="#06d6a0", hover_color="#05c28a",
                                           height=40, command=self._redefinir_senha)
        self.btn_redefinir.pack(pady=20)
        
        self.btn_voltar = ctk.CTkButton(self.frame_botoes, text="⬅️ Voltar ao Login", 
                                        command=self._voltar_login)
        self.btn_voltar.pack(pady=(0, 10))
        
        self.frame_botoes.pack()
    
    def _buscar_pergunta(self):
        """Busca a pergunta de segurança do usuário"""
        username = self.entry_username.get().strip()
        
        if not username:
            messagebox.showwarning("Aviso", "Digite seu nome de usuário.")
            return
        
        pergunta = self.auth.obter_pergunta_seguranca(username)
        
        if pergunta:
            # Mostra a pergunta
            self.lbl_pergunta.configure(text=f"❓ {pergunta}")
            self.frame_pergunta.pack(pady=10)
            self.entry_resposta.focus()
        else:
            messagebox.showerror("Erro", "Usuário não encontrado ou não possui pergunta de segurança configurada.")
    
    def _redefinir_senha(self):
        """Processa a redefinição de senha"""
        username = self.entry_username.get().strip()
        resposta = self.entry_resposta.get().strip()
        nova_senha = self.entry_nova_senha.get().strip()
        confirmar_senha = self.entry_confirmar_senha.get().strip()
        
        # Validações
        if not all([username, resposta, nova_senha, confirmar_senha]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
            return
        
        if nova_senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
        
        if len(nova_senha) < 4:
            messagebox.showwarning("Aviso", "A senha deve ter pelo menos 4 caracteres.")
            return
        
        # Verifica se quer alterar usuário também
        if self.chk_alterar_usuario.get():
            # Redefine usuário e senha
            sucesso, mensagem = self.auth.redefinir_usuario_senha(username, nova_senha, resposta)
        else:
            # Redefine apenas senha
            sucesso, mensagem = self.auth.redefinir_senha(username, nova_senha, resposta)
        
        if sucesso:
            messagebox.showinfo("✅ Sucesso", f"{mensagem}\\n\\nUse suas novas credenciais para fazer login.")
            self._voltar_login()
        else:
            messagebox.showerror("❌ Erro", mensagem)
    
    def _voltar_login(self):
        """Volta para a tela de login"""
        self.destroy()
        from src.ui.login_screen import LoginScreen
        login = LoginScreen()
        login.mainloop()
