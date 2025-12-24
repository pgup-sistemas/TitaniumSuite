# src/ui/configurar_seguranca_screen.py
"""
Tela de Configuração de Segurança
Permite configurar/alterar pergunta e resposta de segurança
"""

import customtkinter as ctk
from tkinter import messagebox
from src.modules.auth import AuthManager

class ConfigurarSegurancaScreen(ctk.CTk):
    def __init__(self, username="admin"):
        super().__init__()
        
        self.username = username
        self.auth = AuthManager()
        
        # Configuração da Janela
        self.title("Configurar Segurança - Titanium Suite")
        self.geometry("600x500")
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        
        self._criar_interface()
        self._carregar_configuracao_atual()
    
    def _criar_interface(self):
        """Cria a interface da tela de configuração"""
        
        # Título
        ctk.CTkLabel(self, text="🛡️ CONFIGURAÇÃO DE SEGURANÇA", 
                     font=("Arial", 24, "bold"), text_color="#4cc9f0").pack(pady=20)
        
        ctk.CTkLabel(self, text="Configure sua pergunta de segurança para recuperação de conta", 
                     text_color="gray").pack(pady=(0, 20))
        
        # Frame principal
        self.frame_main = ctk.CTkFrame(self)
        self.frame_main.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Usuário atual
        ctk.CTkLabel(self.frame_main, text=f"👤 Configurando segurança para: {self.username}", 
                     font=("Arial", 14, "bold")).pack(pady=(20, 20))
        
        # Lista de perguntas predefinidas
        ctk.CTkLabel(self.frame_main, text="📝 Escolha uma pergunta de segurança:", 
                     font=("Arial", 14, "bold")).pack(pady=(10, 5))
        
        # Frame scrollável para as perguntas
        self.frame_perguntas = ctk.CTkScrollableFrame(self.frame_main, height=200)
        self.frame_perguntas.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Variável para pergunta selecionada
        self.pergunta_selecionada = ctk.StringVar()
        
        # Carrega perguntas predefinidas
        perguntas = self.auth.listar_perguntas_seguranca()
        for i, pergunta in enumerate(perguntas):
            radio = ctk.CTkRadioButton(self.frame_perguntas, text=pergunta, 
                                       variable=self.pergunta_selecionada, value=pergunta,
                                       font=("Arial", 11))
            radio.pack(anchor="w", pady=5, padx=10)
        
        # Opção de pergunta personalizada
        ctk.CTkLabel(self.frame_perguntas, text="-" * 50, text_color="gray").pack(pady=10)
        
        radio_custom = ctk.CTkRadioButton(self.frame_perguntas, text="Pergunta personalizada", 
                                          variable=self.pergunta_selecionada, value="custom",
                                          font=("Arial", 11, "bold"))
        radio_custom.pack(anchor="w", pady=5, padx=10)
        
        # Campo para pergunta personalizada
        self.entry_pergunta_custom = ctk.CTkEntry(self.frame_perguntas, width=400, 
                                                  placeholder_text="Digite sua pergunta personalizada",
                                                  state="disabled")
        self.entry_pergunta_custom.pack(pady=5, padx=30, fill="x")
        
        # Habilita campo personalizado quando selecionado
        def on_pergunta_change():
            if self.pergunta_selecionada.get() == "custom":
                self.entry_pergunta_custom.configure(state="normal")
                self.entry_pergunta_custom.focus()
            else:
                self.entry_pergunta_custom.configure(state="disabled")
                self.entry_pergunta_custom.delete(0, "end")
        
        self.pergunta_selecionada.trace("w", lambda *args: on_pergunta_change())
        
        # Resposta de segurança
        ctk.CTkLabel(self.frame_main, text="🔐 Sua resposta de segurança:", 
                     font=("Arial", 14, "bold")).pack(pady=(20, 5))
        
        self.entry_resposta = ctk.CTkEntry(self.frame_main, width=400, 
                                           placeholder_text="Digite sua resposta (lembre-se dela!)")
        self.entry_resposta.pack(pady=5)
        
        # Confirmar resposta
        self.entry_confirmar = ctk.CTkEntry(self.frame_main, width=400, 
                                           placeholder_text="Confirme sua resposta")
        self.entry_confirmar.pack(pady=5)
        
        # Dica de segurança
        frame_dica = ctk.CTkFrame(self.frame_main, fg_color="#1a1a1a")
        frame_dica.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(frame_dica, text="💡 DICA DE SEGURANÇA:", 
                     font=("Arial", 12, "bold")).pack(pady=(10, 5))
        
        dicas = [
            "• Use uma resposta que só você conhece",
            "• Evite informações públicas nas redes sociais", 
            "• Sua resposta deve ser fácil de lembrar",
            "• Esta pergunta será usada para redefinir sua senha"
        ]
        
        for dica in dicas:
            ctk.CTkLabel(frame_dica, text=dica, anchor="w", 
                         font=("Arial", 10)).pack(pady=1, padx=15, fill="x")
        
        # Botões de ação
        frame_botoes = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        frame_botoes.pack(pady=20)
        
        btn_salvar = ctk.CTkButton(frame_botoes, text="💾 SALVAR CONFIGURAÇÃO", 
                                   fg_color="#06d6a0", hover_color="#05c28a",
                                   height=40, command=self._salvar_configuracao)
        btn_salvar.grid(row=0, column=0, padx=10)
        
        btn_cancelar = ctk.CTkButton(frame_botoes, text="❌ CANCELAR", 
                                     fg_color="#ef233c", hover_color="#d62828",
                                     height=40, command=self._cancelar)
        btn_cancelar.grid(row=0, column=1, padx=10)
    
    def _carregar_configuracao_atual(self):
        """Carrega a configuração atual do usuário"""
        pergunta_atual = self.auth.obter_pergunta_seguranca(self.username)
        
        if pergunta_atual:
            # Verifica se é uma pergunta predefinida
            perguntas = self.auth.listar_perguntas_seguranca()
            if pergunta_atual in perguntas:
                self.pergunta_selecionada.set(pergunta_atual)
            else:
                # Pergunta personalizada
                self.pergunta_selecionada.set("custom")
                self.entry_pergunta_custom.configure(state="normal")
                self.entry_pergunta_custom.insert(0, pergunta_atual)
    
    def _salvar_configuracao(self):
        """Salva a nova configuração de segurança"""
        pergunta = self.pergunta_selecionada.get()
        resposta = self.entry_resposta.get().strip()
        confirmar = self.entry_confirmar.get().strip()
        
        # Validações
        if not pergunta:
            messagebox.showwarning("Aviso", "Selecione uma pergunta de segurança.")
            return
        
        if pergunta == "custom":
            pergunta = self.entry_pergunta_custom.get().strip()
            if not pergunta:
                messagebox.showwarning("Aviso", "Digite sua pergunta personalizada.")
                return
        
        if not resposta:
            messagebox.showwarning("Aviso", "Digite sua resposta de segurança.")
            return
        
        if resposta != confirmar:
            messagebox.showerror("Erro", "As respostas não coincidem.")
            return
        
        if len(resposta) < 3:
            messagebox.showwarning("Aviso", "A resposta deve ter pelo menos 3 caracteres.")
            return
        
        # Salva configuração
        sucesso, mensagem = self.auth.configurar_pergunta_seguranca(self.username, pergunta, resposta)
        
        if sucesso:
            messagebox.showinfo("✅ Sucesso", mensagem)
            self._cancelar()
        else:
            messagebox.showerror("❌ Erro", mensagem)
    
    def _cancelar(self):
        """Cancela e fecha a tela"""
        self.destroy()
