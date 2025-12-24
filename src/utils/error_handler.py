# src/utils/error_handler.py
"""
Sistema Universal de Tratamento de Erros
Converte exceções técnicas em mensagens compreensíveis com soluções práticas
"""
import customtkinter as ctk
from tkinter import messagebox
import traceback
import webbrowser

class ErrorHandler:
    """Gerenciador central de erros com interface humanizada"""
    
    # Dicionário de erros conhecidos e suas soluções
    ERROR_SOLUTIONS = {
        "FileNotFoundError": {
            "title": "📁 Arquivo Não Encontrado",
            "friendly": "O sistema não conseguiu localizar o arquivo ou pasta que você selecionou.",
            "causes": [
                "O arquivo foi movido ou deletado",
                "O HD externo foi desconectado",
                "A pasta foi renomeada"
            ],
            "solutions": [
                ("Verificar se o arquivo ainda existe", "check_file"),
                ("Selecionar outro arquivo/pasta", "select_new"),
                ("Reconectar HD externo", "reconnect_drive")
            ]
        },
        
        "PermissionError": {
            "title": "🔒 Sem Permissão de Acesso",
            "friendly": "O Windows bloqueou o acesso a este arquivo. Ele pode estar em uso ou protegido.",
            "causes": [
                "Arquivo aberto em outro programa",
                "Pasta protegida pelo sistema",
                "Necessita privilégios de administrador"
            ],
            "solutions": [
                ("Fechar programas que possam estar usando o arquivo", "close_apps"),
                ("Executar como Administrador", "run_as_admin"),
                ("Escolher outra pasta", "select_new")
            ]
        },
        
        "ConnectionError": {
            "title": "🌐 Problema de Conexão",
            "friendly": "Não foi possível conectar com o Google Drive ou serviço externo.",
            "causes": [
                "Internet desconectada",
                "Token do Google Drive expirado",
                "Firewall bloqueando conexão"
            ],
            "solutions": [
                ("Verificar conexão com Internet", "check_internet"),
                ("Renovar autenticação do Google Drive", "renew_auth"),
                ("Tentar novamente em alguns segundos", "retry")
            ]
        },
        
        "JSONDecodeError": {
            "title": "📄 Arquivo de Configuração Inválido",
            "friendly": "O arquivo credentials.json está corrompido ou incompleto.",
            "causes": [
                "Arquivo copiado incorretamente",
                "Faltam informações necessárias",
                "Formato JSON inválido"
            ],
            "solutions": [
                ("Baixar novamente do Google Cloud Console", "redownload"),
                ("Verificar se copiou o arquivo completo", "check_content"),
                ("Ver tutorial de configuração", "show_tutorial")
            ]
        },
        
        "InvalidToken": {
            "title": "🔑 Autenticação Expirada",
            "friendly": "Sua conexão com o Google Drive expirou e precisa ser renovada.",
            "causes": [
                "Token de acesso válido por tempo limitado",
                "Senha do Google foi alterada"
            ],
            "solutions": [
                ("Renovar autenticação agora", "renew_auth"),
                ("Fazer logout e entrar novamente", "reauth")
            ]
        }
    }
    
    @staticmethod
    def show_friendly_error(parent, exception, context=""):
        """
        Mostra erro em linguagem clara com soluções práticas
        
        Args:
            parent: Widget pai (para centralizar diálogo)
            exception: Exceção capturada
            context: Contexto adicional (ex: "ao fazer backup")
        """
        error_type = type(exception).__name__
        error_msg = str(exception)
        
        # Busca solução predefinida ou usa genérica
        error_info = ErrorHandler.ERROR_SOLUTIONS.get(
            error_type,
            ErrorHandler._get_generic_error()
        )
        
        # Cria janela customizada
        dialog = ErrorDialog(parent, error_info, context, error_msg)
        dialog.wait_window()
        
        return dialog.selected_action
    
    @staticmethod
    def _get_generic_error():
        """Erro genérico para exceções desconhecidas"""
        return {
            "title": "⚠️ Erro Inesperado",
            "friendly": "Ocorreu um problema que o sistema não esperava.",
            "causes": [
                "Possível incompatibilidade com seu Windows",
                "Arquivo corrompido",
                "Problema temporário"
            ],
            "solutions": [
                ("Tentar novamente", "retry"),
                ("Reiniciar o programa", "restart"),
                ("Reportar erro ao suporte", "report")
            ]
        }
    
    @staticmethod
    def log_error(exception, context=""):
        """Salva erro em arquivo de log para análise posterior"""
        from datetime import datetime
        import os
        
        log_dir = "logs/errors"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = f"{log_dir}/error_{datetime.now().strftime('%Y%m%d')}.log"
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"[{datetime.now().isoformat()}] {context}\n")
            f.write(f"Tipo: {type(exception).__name__}\n")
            f.write(f"Mensagem: {str(exception)}\n")
            f.write(f"Traceback:\n{traceback.format_exc()}\n")


class ErrorDialog(ctk.CTkToplevel):
    """Janela de erro customizada e amigável"""
    
    def __init__(self, parent, error_info, context, technical_msg):
        super().__init__(parent)
        
        self.selected_action = None
        self.error_info = error_info
        
        # Configuração da janela
        self.title("Atenção")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # Centraliza na tela
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"+{x}+{y}")
        
        # Força modal
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui(context, technical_msg)
    
    def setup_ui(self, context, technical_msg):
        """Monta interface do diálogo"""
        
        # HEADER (Ícone + Título)
        frame_header = ctk.CTkFrame(self, fg_color="#ef233c", height=80)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        ctk.CTkLabel(
            frame_header,
            text=self.error_info["title"],
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=25)
        
        # BODY (Scrollable)
        frame_body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        frame_body.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Contexto (se fornecido)
        if context:
            ctk.CTkLabel(
                frame_body,
                text=f"Durante: {context}",
                font=ctk.CTkFont(size=12, slant="italic"),
                text_color="gray"
            ).pack(anchor="w", pady=(0, 10))
        
        # Explicação amigável
        ctk.CTkLabel(
            frame_body,
            text="O que aconteceu:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        
        ctk.CTkLabel(
            frame_body,
            text=self.error_info["friendly"],
            font=ctk.CTkFont(size=12),
            wraplength=520,
            justify="left"
        ).pack(anchor="w", pady=(0, 15))
        
        # Possíveis causas
        ctk.CTkLabel(
            frame_body,
            text="Possíveis causas:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        
        for cause in self.error_info["causes"]:
            frame_cause = ctk.CTkFrame(frame_body, fg_color="transparent")
            frame_cause.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                frame_cause,
                text=f"• {cause}",
                font=ctk.CTkFont(size=11),
                text_color="gray"
            ).pack(anchor="w", padx=10)
        
        # Soluções
        ctk.CTkLabel(
            frame_body,
            text="Como resolver:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(15, 10))
        
        for solution_text, action_code in self.error_info["solutions"]:
            btn = ctk.CTkButton(
                frame_body,
                text=solution_text,
                command=lambda code=action_code: self.handle_action(code),
                height=35,
                anchor="w",
                fg_color="#2b2b2b",
                hover_color="#3a3a3a"
            )
            btn.pack(fill="x", pady=3)
        
        # Detalhes técnicos (colapsável)
        self.create_technical_details(frame_body, technical_msg)
        
        # FOOTER (Botão Fechar)
        frame_footer = ctk.CTkFrame(self, fg_color="transparent")
        frame_footer.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkButton(
            frame_footer,
            text="Fechar",
            width=120,
            fg_color="gray",
            hover_color="#555",
            command=self.destroy
        ).pack(side="right")
    
    def create_technical_details(self, parent, technical_msg):
        """Área expansível com detalhes técnicos"""
        self.show_technical = False
        
        frame_tech = ctk.CTkFrame(parent, fg_color="transparent")
        frame_tech.pack(fill="x", pady=(20, 0))
        
        self.btn_toggle = ctk.CTkButton(
            frame_tech,
            text="▶ Mostrar Detalhes Técnicos",
            command=lambda: self.toggle_technical(technical_msg, frame_tech),
            fg_color="transparent",
            hover_color="#2b2b2b",
            anchor="w",
            font=ctk.CTkFont(size=11)
        )
        self.btn_toggle.pack(fill="x")
        
        self.frame_tech_content = ctk.CTkFrame(frame_tech, fg_color="#1a1a1a")
        # Não empacota ainda (só quando expandir)
        
        self.lbl_technical = ctk.CTkLabel(
            self.frame_tech_content,
            text=technical_msg,
            font=ctk.CTkFont(family="Courier", size=10),
            text_color="#aaa",
            justify="left",
            anchor="w"
        )
        self.lbl_technical.pack(padx=10, pady=10)
    
    def toggle_technical(self, technical_msg, parent):
        """Expande/colapsa detalhes técnicos"""
        self.show_technical = not self.show_technical
        
        if self.show_technical:
            self.btn_toggle.configure(text="▼ Ocultar Detalhes Técnicos")
            self.frame_tech_content.pack(fill="x", pady=(5, 0))
        else:
            self.btn_toggle.configure(text="▶ Mostrar Detalhes Técnicos")
            self.frame_tech_content.pack_forget()
    
    def handle_action(self, action_code):
        """Executa ação selecionada pelo usuário"""
        self.selected_action = action_code
        
        # Ações específicas
        if action_code == "check_internet":
            messagebox.showinfo("Dica", "Verifique se:\n• Wi-Fi está conectado\n• Cabo de rede está plugado\n• Abra google.com no navegador para testar")
        
        elif action_code == "show_tutorial":
            webbrowser.open("https://docs.google.com/document/tutorial")  # Substitua pelo seu link
        
        elif action_code == "retry":
            self.destroy()  # Fecha e retorna para tentar novamente
        
        elif action_code == "run_as_admin":
            messagebox.showinfo("Como executar como Admin", "1. Feche o programa\n2. Clique com botão direito no ícone\n3. Escolha 'Executar como administrador'")
        
        # Adicione mais ações conforme necessário
        else:
            self.destroy()


# ===== EXEMPLO DE USO NOS SEUS FRAMES =====

class ExemploIntegracao:
    """Exemplo de como usar em qualquer frame"""
    
    def executar_operacao_arriscada(self):
        """Qualquer operação que possa dar erro"""
        try:
            # Seu código aqui
            arquivo = open("arquivo_inexistente.txt")
            
        except Exception as e:
            # Log automático
            ErrorHandler.log_error(e, context="ao abrir arquivo de configuração")
            
            # Mostra erro amigável
            action = ErrorHandler.show_friendly_error(
                parent=self,
                exception=e,
                context="ao abrir arquivo de configuração"
            )
            
            # Trata ação escolhida pelo usuário
            if action == "retry":
                self.executar_operacao_arriscada()  # Tenta novamente
            elif action == "select_new":
                self.selecionar_novo_arquivo()


# ===== INTEGRAÇÃO NO CLOUD.PY (Exemplo) =====
"""
No seu cloud.py, substitua:

def conectar(self):
    if not os.path.exists(self.arquivo_credenciais):
        self.log("❌ Erro: Credenciais não encontradas.")
        return False

Por:

def conectar(self):
    try:
        if not os.path.exists(self.arquivo_credenciais):
            raise FileNotFoundError("Arquivo credentials.json não encontrado")
        
        # ... resto do código ...
        
    except Exception as e:
        from utils.error_handler import ErrorHandler
        ErrorHandler.log_error(e, "ao conectar com Google Drive")
        ErrorHandler.show_friendly_error(None, e, "ao conectar com Google Drive")
        return False
"""