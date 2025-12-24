"""
Console Unificado para o Titanium Suite
Painel de logs e status integrado na parte inferior de cada frame.
"""

import customtkinter as ctk


class UnifiedConsole(ctk.CTkFrame):
    """
    Componente unificado de console para exibir logs e status.
    Usado na parte inferior de cada frame principal.
    """
    
    def __init__(self, parent, height=120, title="📋 Console de Execução"):
        super().__init__(parent, fg_color="transparent")
        
        # Configuração do frame
        self.configure(height=height)
        
        # Título do console
        self.lbl_title = ctk.CTkLabel(self, text=title, 
                                     font=ctk.CTkFont(size=12, weight="bold"),
                                     text_color="#4cc9f0")
        self.lbl_title.pack(anchor="w", padx=10, pady=(5, 0))
        
        # Área de texto com scrollbar
        self.txt_log = ctk.CTkTextbox(self, height=height-30, 
                                     font=ctk.CTkFont(size=11))
        self.txt_log.pack(fill="both", expand=True, padx=10, pady=5)
        self.txt_log.configure(state="disabled")  # Bloqueia digitação
        
        # Contador de mensagens
        self.msg_count = 0
        
        # Cores para diferentes tipos de mensagens
        self.colors = {
            "info": "#4cc9f0",      # Azul claro
            "success": "#06d6a0",   # Verde
            "warning": "#ffd166",   # Amarelo
            "error": "#ef233c",     # Vermelho
            "process": "#7209b7"    # Roxo
        }
    
    def log(self, message, msg_type="info"):
        """
        Adiciona uma mensagem ao console.
        
        Args:
            message: Texto da mensagem
            msg_type: Tipo da mensagem (info, success, warning, error, process)
        """
        self.txt_log.configure(state="normal")
        
        # Adiciona prefixo baseado no tipo
        prefix = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "process": "⚙️"
        }.get(msg_type, "•")
        
        self.txt_log.insert("end", f"{prefix} {message}\n")
        self.txt_log.see("end")  # Rola para o final
        self.txt_log.configure(state="disabled")
        
        self.msg_count += 1
    
    def clear(self):
        """Limpa o console."""
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.configure(state="disabled")
        self.msg_count = 0
    
    def section(self, title):
        """Adiciona um título de seção."""
        self.txt_log.configure(state="normal")
        self.txt_log.insert("end", f"\n─── {title} ───\n")
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")
    
    def info(self, message):
        self.log(message, "info")
    
    def success(self, message):
        self.log(message, "success")
    
    def warning(self, message):
        self.log(message, "warning")
    
    def error(self, message):
        self.log(message, "error")
    
    def process(self, message):
        self.log(message, "process")
