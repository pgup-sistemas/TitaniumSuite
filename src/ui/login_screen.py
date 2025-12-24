import customtkinter as ctk
from tkinter import messagebox
from src.modules.auth import AuthManager

class LoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.auth = AuthManager()
        
        # Configuração da Janela
        self.title("Login - Titanium Suite")
        self.geometry("400x500")
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")

        # Verifica Licença/Trial antes de tudo
        if not self.auth.verificar_licenca_completa():
            self._mostrar_tela_ativacao_profissional()
        else:
            self._mostrar_tela_login()

    def _mostrar_tela_ativacao_profissional(self):
        self.geometry("600x500")
        
        # Título principal
        ctk.CTkLabel(self, text="🚀 TITANIUM SUITE PROFESSIONAL", 
                     font=("Arial", 24, "bold"), text_color="#4cc9f0").pack(pady=20)
        
        # Verifica status do trial
        trial_status = self.auth.verificar_trial_status()
        
        if trial_status["status"] == "trial_ativo":
            self._mostrar_tela_trial(trial_status)
        elif trial_status["status"] == "trial_expirado":
            self._mostrar_tela_ativacao_completa()
        else:
            self._mostrar_tela_ativacao_completa()
    
    def _mostrar_tela_trial(self, trial_status):
        """Tela para período de trial"""
        ctk.CTkLabel(self, text="✨ PERÍODO DE TRIAL ATIVO", 
                     font=("Arial", 20, "bold"), text_color="#06d6a0").pack(pady=10)
        
        ctk.CTkLabel(self, text=f"Você tem {trial_status['dias_restantes']} dias restantes", 
                     font=("Arial", 16)).pack(pady=5)
        
        ctk.CTkLabel(self, text=f"Trial expira em: {trial_status['data_fim']}", 
                     text_color="gray").pack(pady=5)
        
        # Benefícios do trial
        beneficios_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        beneficios_frame.pack(pady=20, padx=40, fill="x")
        
        ctk.CTkLabel(beneficios_frame, text="🎁 BENEFÍCIOS DO TRIAL:", 
                     font=("Arial", 14, "bold")).pack(pady=10)
        
        beneficios = [
            "✅ Todas as funcionalidades liberadas",
            "✅ Dashboard completo com estatísticas", 
            "✅ Criptografia AES-256 ilimitada",
            "✅ Backup na nuvem Google Drive",
            "✅ Suporte prioritário"
        ]
        
        for beneficio in beneficios:
            ctk.CTkLabel(beneficios_frame, text=beneficio, anchor="w").pack(pady=2, padx=20, fill="x")
        
        # Botão para ativar versão completa
        ctk.CTkButton(self, text="💳 ATIVAR VERSÃO COMPLETA", 
                      fg_color="#4cc9f0", hover_color="#3a7bc8",
                      height=40, command=self._mostrar_tela_ativacao_completa).pack(pady=20)
        
        # Botão para continuar trial
        ctk.CTkButton(self, text="🚀 CONTINUAR TRIAL", 
                      fg_color="#06d6a0", hover_color="#05c28a",
                      height=40, command=self._continuar_trial).pack(pady=10)
    
    def _mostrar_tela_ativacao_completa(self):
        """Tela de ativação da versão completa"""
        # Limpa a tela
        for widget in self.winfo_children():
            widget.destroy()
        
        self.geometry("600x500")
        
        # Título
        ctk.CTkLabel(self, text="🔐 ATIVAÇÃO PROFISSIONAL", 
                     font=("Arial", 22, "bold"), text_color="#ef233c").pack(pady=20)
        
        # Gera chave automaticamente
        chave_gerada = self.auth.gerar_chave_ativacao_profissional()
        
        # Frame da chave
        chave_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        chave_frame.pack(pady=20, padx=40, fill="x")
        
        ctk.CTkLabel(chave_frame, text="🔑 SUA CHAVE DE ATIVAÇÃO:", 
                     font=("Arial", 14, "bold")).pack(pady=10)
        
        self.entry_chave = ctk.CTkEntry(chave_frame, width=400, justify="center",
                                       font=("Arial", 12, "bold"))
        self.entry_chave.pack(pady=10)
        self.entry_chave.insert(0, chave_gerada)
        self.entry_chave.configure(state="readonly")
        
        # Instruções
        instrucoes_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        instrucoes_frame.pack(pady=20, padx=40, fill="x")
        
        ctk.CTkLabel(instrucoes_frame, text="📋 INSTRUÇÕES DE ATIVAÇÃO:", 
                     font=("Arial", 14, "bold")).pack(pady=10)
        
        instrucoes = [
            "1️⃣ Sua chave única foi gerada automaticamente",
            "2️⃣ Clique em 'Copiar Chave' para copiar",
            "3️⃣ Acesse: www.titanium.com.br/ativar",
            "4️⃣ Cole sua chave ecomplete o pagamento",
            "5️⃣ Após pagamento, sua licença será ativada"
        ]
        
        for instrucao in instrucoes:
            ctk.CTkLabel(instrucoes_frame, text=instrucao, anchor="w").pack(pady=2, padx=20, fill="x")
        
        # Botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="📋 Copiar Chave", 
                      command=self._copiar_chave).grid(row=0, column=0, padx=10)
        
        ctk.CTkButton(btn_frame, text="🌐 Abrir Site de Ativação", 
                      fg_color="#4cc9f0", command=self._abrir_site_ativacao).grid(row=0, column=1, padx=10)
        
        # Campo para chave ativada
        ctk.CTkLabel(self, text="💳 Digite sua chave ativada:").pack(pady=(20, 5))
        self.entry_key_ativada = ctk.CTkEntry(self, width=400, placeholder_text="Cole aqui sua chave ativada")
        self.entry_key_ativada.pack(pady=5)
        
        ctk.CTkButton(self, text="🚀 ATIVAR SISTEMA", 
                      fg_color="#06d6a0", height=40,
                      command=self.acao_ativar_profissional).pack(pady=20)
    
    def _continuar_trial(self):
        """Permite continuar usando o trial"""
        self.destroy()
        self.abrir_app_principal()

    def acao_ativar_profissional(self):
        """Ativação profissional do sistema"""
        chave_ativada = self.entry_key_ativada.get().strip()
        
        if not chave_ativada:
            messagebox.showwarning("Aviso", "Digite sua chave ativada.")
            return
        
        sucesso, mensagem = self.auth.ativar_sistema_profissional(chave_ativada)
        
        if sucesso:
            messagebox.showinfo("✅ Sucesso", f"{mensagem}\n\nReinicie o aplicativo para usar a versão completa!")
            self.destroy()
        else:
            messagebox.showerror("❌ Erro", mensagem)
    
    def _copiar_chave(self):
        """Copia a chave para a área de transferência"""
        import pyperclip
        try:
            chave = self.entry_chave.get()
            pyperclip.copy(chave)
            messagebox.showinfo("Copiado!", "Chave copiada para a área de transferência!")
        except:
            messagebox.showwarning("Aviso", "Não foi possível copiar. Copie manualmente.")
    
    def _abrir_site_ativacao(self):
        """Abre o site de ativação no navegador"""
        import webbrowser
        webbrowser.open("https://www.titanium.com.br/ativar")
    
    # Método legacy mantido para compatibilidade
    def acao_ativar(self):
        chave_digitada = self.entry_key.get().strip()
        
        # Salva o arquivo para tentar validar
        with open("license.key", "w") as f:
            f.write(chave_digitada)
            
        if self.auth.verificar_licenca():
            messagebox.showinfo("Sucesso", "Sistema ativado! Reinicie o aplicativo.")
            self.destroy() # Fecha para o usuário abrir de novo
        else:
            messagebox.showerror("Erro", "Chave inválida para este computador.")
            import os
            os.remove("license.key") # Remove a chave inválida

    def _mostrar_tela_login(self):
        # Logo / Título
        ctk.CTkLabel(self, text="TITANIUM SUITE", font=("Impact", 30)).pack(pady=(60, 10))
        ctk.CTkLabel(self, text="Enterprise Edition", text_color="#3a86ff").pack(pady=(0, 40))

        # Inputs
        self.entry_user = ctk.CTkEntry(self, width=250, placeholder_text="Usuário")
        self.entry_user.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self, width=250, placeholder_text="Senha", show="*")
        self.entry_pass.pack(pady=10)

        # Botão Entrar
        ctk.CTkButton(self, text="ENTRAR", width=250, height=40, 
                      command=self.acao_login).pack(pady=20)
        
        # Link para redefinir senha
        btn_esquecer = ctk.CTkButton(self, text="🔑 Esqueci minha senha", 
                                     fg_color="transparent", hover_color="#2b2b2b",
                                     command=self._abrir_redefinir_senha)
        btn_esquecer.pack(pady=5)
        
        ctk.CTkLabel(self, text="Suporte: contato@titanium.com", font=("Arial", 10)).pack(side="bottom", pady=20)

    def acao_login(self):
        user = self.entry_user.get()
        senha = self.entry_pass.get()
        
        sucesso, role = self.auth.verificar_login(user, senha)
        
        if sucesso:
            print(f"Login efetuado como: {role}")
            self.destroy() # Fecha tela de login
            # Aqui vamos abrir o App Principal (ver main.py)
            self.abrir_app_principal()
        else:
            messagebox.showerror("Acesso Negado", "Usuário ou senha incorretos.")

    def abrir_app_principal(self):
        # Esta função será sobrescrita no main.py ou chamada via callback
        pass
    
    def _abrir_redefinir_senha(self):
        """Abre a tela de redefinição de senha"""
        from src.ui.redifinir_senha_screen import RedefinirSenhaScreen
        redefinir = RedefinirSenhaScreen()
        redefinir.focus()  # Garante que fica em foco