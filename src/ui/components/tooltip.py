# src/ui/components/tooltip.py
"""
Sistema Universal de Tooltips - Adiciona dicas ao passar mouse em qualquer widget
"""
import customtkinter as ctk

class ToolTip:
    """
    Tooltip customizado para CustomTkinter
    Uso: ToolTip(widget, "Texto da dica")
    """
    
    def __init__(self, widget, text, delay=500):
        """
        Args:
            widget: Widget CTk para anexar tooltip
            text: Texto da dica
            delay: Delay em ms antes de mostrar (padrão: 500ms)
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.timer_id = None
        
        # Bind eventos
        self.widget.bind("<Enter>", self.schedule_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Button>", self.hide_tooltip)  # Esconde ao clicar
    
    def schedule_tooltip(self, event=None):
        """Agenda exibição do tooltip após delay"""
        self.cancel_tooltip()
        self.timer_id = self.widget.after(self.delay, self.show_tooltip)
    
    def show_tooltip(self):
        """Mostra o tooltip próximo ao widget"""
        if self.tooltip_window or not self.text:
            return
        
        # Posição: Abaixo do widget + offset
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        # Cria janela tooltip
        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Sem borda
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        # Tenta ficar sempre no topo
        self.tooltip_window.attributes("-topmost", True)
        
        # Frame com cor de fundo
        frame = ctk.CTkFrame(
            self.tooltip_window,
            fg_color="#2b2b2b",
            border_width=1,
            border_color="#4a4a4a",
            corner_radius=8
        )
        frame.pack()
        
        # Texto
        label = ctk.CTkLabel(
            frame,
            text=self.text,
            font=ctk.CTkFont(size=11),
            text_color="white",
            justify="left",
            wraplength=300
        )
        label.pack(padx=10, pady=8)
    
    def hide_tooltip(self, event=None):
        """Esconde e destrói tooltip"""
        self.cancel_tooltip()
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
    
    def cancel_tooltip(self):
        """Cancela timer de exibição"""
        if self.timer_id:
            self.widget.after_cancel(self.timer_id)
            self.timer_id = None


# ===== DICIONÁRIO DE TOOLTIPS DO SISTEMA =====

TOOLTIPS_SYSTEM = {
    # MANUTENÇÃO
    "btn_limpar_temp": "🗑️ Remove arquivos temporários que não são mais necessários.\nLibera espaço e melhora performance.",
    "btn_limpar_dns": "🌐 Limpa cache de DNS da internet.\nÚtil quando sites não abrem corretamente.",
    "btn_ping": "📡 Testa se sua internet está funcionando.\nPinga o servidor do Google (8.8.8.8).",
    
    # NUVEM/BACKUP
    "btn_conectar_drive": "☁️ Autoriza o Titanium Suite a acessar seu Google Drive.\nVocê será redirecionado para o navegador na primeira vez.",
    "btn_upload": "⬆️ Envia a pasta selecionada para o Google Drive.\nApenas arquivos novos ou modificados são enviados.",
    "btn_select_pasta": "📁 Escolhe qual pasta do seu computador será backupeada.\nRecomendamos: Documentos, Downloads ou Área de Trabalho.",
    
    # SEGURANÇA
    "btn_criptografar": "🔒 Protege arquivo com senha militar AES-256.\nIdeal para documentos sensíveis, contratos e dados financeiros.",
    "btn_descriptografar": "🔓 Destranca arquivo .enc usando a senha correta.\nATENÇÃO: Senha incorreta = arquivo irrecuperável.",
    "btn_criar_cofre": "📦 Cria um arquivo .ZIP protegido com senha.\nCompacta e criptografa uma pasta inteira.",
    "switch_delete_original": "⚠️ Se marcado, o arquivo original será DELETADO após criptografar.\nUse quando precisar remover completamente o original.",
    
    # PRODUTIVIDADE
    "btn_unir_pdf": "📄 Junta vários PDFs em um único arquivo.\nMantém ordem dos arquivos selecionados.",
    "btn_gerar_qr": "📱 Cria QR Code escaneável.\nFunciona para links, textos, Wi-Fi e contatos.",
    "btn_comprimir_pdf": "🗜️ Reduz tamanho do PDF removendo metadados.\nIdeal antes de enviar por e-mail.",
    
    # DASHBOARD
    "card_health": "🛡️ Score de Saúde do Sistema (0-100).\nBaseado em: Espaço em disco, status backup, arquivos temp e licença.",
    "btn_manutencao_rapida": "⚡ Executa todas tarefas de manutenção automaticamente:\nLimpeza, organização, backup e relatório.",
}


def add_tooltip(widget, text_key_or_custom):
    """
    Função auxiliar para adicionar tooltip facilmente
    
    Args:
        widget: Widget CTk
        text_key_or_custom: Chave do dicionário TOOLTIPS_SYSTEM ou texto customizado
    
    Exemplo:
        btn = ctk.CTkButton(self, text="Limpar")
        add_tooltip(btn, "btn_limpar_temp")
        
        # Ou texto customizado:
        add_tooltip(btn, "Este botão limpa arquivos temporários")
    """
    # Verifica se é uma chave conhecida
    if text_key_or_custom in TOOLTIPS_SYSTEM:
        tooltip_text = TOOLTIPS_SYSTEM[text_key_or_custom]
    else:
        tooltip_text = text_key_or_custom
    
    ToolTip(widget, tooltip_text)


# ===== FUNÇÃO PARA ADICIONAR TOOLTIPS EM MASSA =====

def auto_add_tooltips(frame):
    """
    Percorre todos widgets de um frame e adiciona tooltips automaticamente
    baseado no texto do botão ou nome do widget
    
    Uso:
        # No final do __init__ de qualquer frame:
        from ui.components.tooltip import auto_add_tooltips
        auto_add_tooltips(self)
    """
    for widget in frame.winfo_children():
        # Se for Frame ou container, processa recursivamente
        if isinstance(widget, (ctk.CTkFrame, ctk.CTkScrollableFrame)):
            auto_add_tooltips(widget)
        
        # Se for botão, tenta encontrar tooltip
        elif isinstance(widget, ctk.CTkButton):
            btn_text = widget.cget("text").lower()
            
            # Mapeamento inteligente
            if "limpar" in btn_text and "temp" in btn_text:
                add_tooltip(widget, "btn_limpar_temp")
            elif "limpar" in btn_text and "dns" in btn_text:
                add_tooltip(widget, "btn_limpar_dns")
            elif "ping" in btn_text or "conexão" in btn_text:
                add_tooltip(widget, "btn_ping")
            elif "conectar" in btn_text and "drive" in btn_text:
                add_tooltip(widget, "btn_conectar_drive")
            elif "upload" in btn_text or "enviar" in btn_text:
                add_tooltip(widget, "btn_upload")
            elif "criptografar" in btn_text:
                add_tooltip(widget, "btn_criptografar")
            elif "descriptografar" in btn_text:
                add_tooltip(widget, "btn_descriptografar")
            elif "cofre" in btn_text:
                add_tooltip(widget, "btn_criar_cofre")
            elif "unir" in btn_text and "pdf" in btn_text:
                add_tooltip(widget, "btn_unir_pdf")
            elif "qr" in btn_text:
                add_tooltip(widget, "btn_gerar_qr")