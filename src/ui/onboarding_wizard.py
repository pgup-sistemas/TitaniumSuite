# ui/onboarding_wizard.py
"""
Wizard de Primeira Execução - Configura tudo em 5 passos
"""
import customtkinter as ctk
from tkinter import filedialog
import json
from pathlib import Path
import threading

class OnboardingWizard(ctk.CTkToplevel):
    """Assistente de Configuração Inicial - Primeira Execução"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("🚀 Configuração Inicial - Titanium Suite")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Centraliza na tela
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.winfo_screenheight() // 2) - (600 // 2)
        self.geometry(f"+{x}+{y}")
        
        # Força modal
        self.transient(parent)
        self.grab_set()
        
        self.current_step = 0
        self.config = {
            "folders_to_organize": [],
            "backup_type": "local",
            "backup_path": "",
            "automation_schedule": "friday_18h",
            "first_run_completed": False
        }
        
        self.steps = [
            self.step_welcome,
            self.step_select_folders,
            self.step_backup_config,
            self.step_automation,
            self.step_final
        ]
        
        self.setup_ui()
        self.show_current_step()
        
    def setup_ui(self):
        """Layout base do wizard"""
        # Header com progresso
        self.header = ctk.CTkFrame(self, height=100, fg_color="#1e3a5f")
        self.header.pack(fill="x", pady=(0, 20))
        self.header.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            self.header, 
            text="",
            font=("Arial", 22, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=(20, 10))
        
        # Indicador de progresso
        self.progress = ctk.CTkProgressBar(self, width=650, height=8)
        self.progress.pack(pady=10)
        self.progress.set(0)
        
        self.lbl_progress = ctk.CTkLabel(self, text="", font=("Arial", 10), text_color="gray")
        self.lbl_progress.pack()
        
        # Container do conteúdo dinâmico
        self.content = ctk.CTkScrollableFrame(self, height=280)
        self.content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Botões de navegação - CORRIGIDO
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        self.nav_frame.pack(fill="x", padx=30, pady=(10, 20))
        self.nav_frame.pack_propagate(False)
        
        # Frame interno para centralizar os botões
        self.buttons_container = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        self.buttons_container.pack(expand=True, fill="both", padx=20)
        
        # Botão Voltar (Esquerda)
        self.btn_prev = ctk.CTkButton(
            self.buttons_container, 
            text="← Voltar",
            width=140,
            height=45,
            command=self.previous_step,
            state="disabled",
            fg_color="#6c757d",
            hover_color="#5a6268",
            text_color="white",
            font=("Arial", 14, "bold"),
            corner_radius=8
        )
        self.btn_prev.grid(row=0, column=0, padx=(0, 15), sticky="w")
        
        # Botão Pular (Centro-Esquerda)
        self.btn_skip = ctk.CTkButton(
            self.buttons_container,
            text="Pular Tutorial",
            width=160,
            height=45,
            fg_color="#6c757d",
            hover_color="#5a6268",
            text_color="white",
            command=self.skip_wizard,
            font=("Arial", 13),
            corner_radius=8
        )
        self.btn_skip.grid(row=0, column=1, padx=15, sticky="w")
        
        # Espaçador central
        self.spacer = ctk.CTkLabel(self.buttons_container, text="", width=200)
        self.spacer.grid(row=0, column=2)
        
        # Botão Continuar (Direita)
        self.btn_next = ctk.CTkButton(
            self.buttons_container,
            text="Continuar →",
            width=160,
            height=45,
            command=self.next_step,
            fg_color="#28a745",
            hover_color="#218838",
            text_color="white",
            font=("Arial", 14, "bold"),
            corner_radius=8
        )
        self.btn_next.grid(row=0, column=3, padx=(15, 0), sticky="e")
        
    def show_current_step(self):
        """Renderiza a tela atual"""
        # Limpa conteúdo anterior
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Atualiza progresso
        progress_value = (self.current_step + 1) / len(self.steps)
        self.progress.set(progress_value)
        self.lbl_progress.configure(text=f"Passo {self.current_step + 1} de {len(self.steps)}")
        
        # Chama a função da etapa
        self.steps[self.current_step]()
        
        # Controla visibilidade dos botões
        self._update_buttons()
    
    def _update_buttons(self):
        """Atualiza estado e visibilidade dos botões"""
        # Garante que o frame de navegação está visível
        self.nav_frame.pack(fill="x", padx=30, pady=(10, 20))
        
        # Botão Voltar
        if self.current_step > 0:
            self.btn_prev.configure(state="normal")
        else:
            self.btn_prev.configure(state="disabled")
        
        # Botão Pular (não mostrar na última etapa)
        if self.current_step < len(self.steps) - 1:
            self.btn_skip.grid(row=0, column=1, padx=15, sticky="w")
        else:
            self.btn_skip.grid_forget()
        
        # Botão Continuar/Finalizar
        if self.current_step == len(self.steps) - 1:
            self.btn_next.configure(
                text="Finalizar ✓",
                fg_color="#28a745",
                hover_color="#218838"
            )
        else:
            self.btn_next.configure(
                text="Continuar →",
                fg_color="#28a745", 
                hover_color="#218838"
            )
        
        # Força atualização da interface
        self.update_idletasks()
        
    def step_welcome(self):
        """Etapa 1: Boas-vindas"""
        self.title_label.configure(text="🎉 Bem-vindo ao Titanium Suite!")
        
        # Logo/Imagem (se tiver)
        frame_hero = ctk.CTkFrame(self.content, fg_color="#2b2b2b", corner_radius=15)
        frame_hero.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            frame_hero,
            text="🛡️",
            font=("Arial", 60)
        ).pack(pady=20)
        
        welcome_text = """Vamos configurar tudo em apenas 5 passos rápidos:

✓ Escolher pastas para organizar automaticamente
✓ Configurar backup (local ou nuvem)
✓ Agendar manutenção automática
✓ Testar tudo funcionando

Leva menos de 3 minutos e você nunca mais precisará se preocupar!"""
        
        ctk.CTkLabel(
            self.content,
            text=welcome_text,
            font=("Arial", 13),
            justify="left"
        ).pack(pady=20)
        
        ctk.CTkLabel(
            self.content,
            text="💡 Você pode refazer esse tutorial a qualquer momento clicando em '❓ Refazer Tutorial' no menu.",
            font=("Arial", 10),
            text_color="gray",
            wraplength=600
        ).pack(pady=10)
        
    def step_select_folders(self):
        """Etapa 2: Selecionar pastas críticas"""
        self.title_label.configure(text="📁 Quais pastas deseja organizar?")
        
        info = ctk.CTkLabel(
            self.content,
            text="Marque as pastas que acumulam arquivos no dia a dia.\nO sistema vai organizá-las automaticamente por tipo de arquivo:",
            font=("Arial", 12),
            justify="left"
        )
        info.pack(pady=(0, 15))
        
        # Sugestões inteligentes
        home = Path.home()
        suggestions = [
            ("📥 Downloads", str(home / "Downloads"), "PDFs, imagens, vídeos que você baixa"),
            ("📄 Documentos", str(home / "Documents"), "Contratos, planilhas, relatórios"),
            ("🖥️ Área de Trabalho", str(home / "Desktop"), "Arquivos que ficam bagunçados na área de trabalho"),
            ("🖼️ Imagens", str(home / "Pictures"), "Fotos e prints de tela")
        ]
        
        self.folder_vars = {}
        for name, path, desc in suggestions:
            # Verifica se pasta existe
            if not Path(path).exists():
                continue
            
            var = ctk.BooleanVar(value=True)  # Marcado por padrão
            self.folder_vars[path] = var
            
            frame = ctk.CTkFrame(self.content, fg_color="#2b2b2b", corner_radius=10)
            frame.pack(fill="x", pady=5)
            
            checkbox = ctk.CTkCheckBox(
                frame,
                text=name,
                variable=var,
                font=("Arial", 12, "bold")
            )
            checkbox.pack(anchor="w", padx=15, pady=(10, 2))
            
            ctk.CTkLabel(
                frame,
                text=f"📂 {path}",
                font=("Arial", 9),
                text_color="gray"
            ).pack(anchor="w", padx=35, pady=0)
            
            ctk.CTkLabel(
                frame,
                text=desc,
                font=("Arial", 9),
                text_color="#aaa"
            ).pack(anchor="w", padx=35, pady=(0, 10))
        
        # Botão para adicionar pasta customizada
        btn_custom = ctk.CTkButton(
            self.content,
            text="+ Adicionar Outra Pasta",
            width=200,
            fg_color="transparent",
            border_width=2,
            command=self.add_custom_folder
        )
        btn_custom.pack(pady=15)
        
    def add_custom_folder(self):
        """Permite adicionar pasta personalizada"""
        folder = filedialog.askdirectory(title="Selecione uma pasta")
        if folder:
            var = ctk.BooleanVar(value=True)
            self.folder_vars[folder] = var
            
            frame = ctk.CTkFrame(self.content, fg_color="#2b2b2b", corner_radius=10)
            frame.pack(fill="x", pady=5)
            
            checkbox = ctk.CTkCheckBox(
                frame,
                text=f"📁 Personalizada",
                variable=var,
                font=("Arial", 12, "bold")
            )
            checkbox.pack(anchor="w", padx=15, pady=(10, 2))
            
            ctk.CTkLabel(
                frame,
                text=folder,
                font=("Arial", 9),
                text_color="gray"
            ).pack(anchor="w", padx=35, pady=(0, 10))
    
    def step_backup_config(self):
        """Etapa 3: Tipo de backup"""
        self.title_label.configure(text="☁️ Como deseja fazer backup?")
        
        info = ctk.CTkLabel(
            self.content,
            text="Escolha onde seus arquivos importantes serão protegidos:",
            font=("Arial", 12)
        )
        info.pack(pady=(0, 20))
        
        self.backup_type = ctk.StringVar(value="local")
        
        # Opção 1: Backup Local
        frame_local = ctk.CTkFrame(self.content, border_width=2, corner_radius=15)
        frame_local.pack(fill="x", pady=10, padx=20)
        
        radio_local = ctk.CTkRadioButton(
            frame_local,
            text="💾 Backup Local (HD Externo / Pendrive)",
            variable=self.backup_type,
            value="local",
            font=("Arial", 14, "bold")
        )
        radio_local.pack(anchor="w", padx=20, pady=(15, 5))
        
        desc_local = ctk.CTkLabel(
            frame_local,
            text="✓ Rápido e simples\n✓ Ideal para começar\n✓ Você controla onde fica\n⚠️ Lembre de conectar o HD/pendrive regularmente",
            font=("Arial", 10),
            text_color="gray",
            justify="left"
        )
        desc_local.pack(anchor="w", padx=40, pady=(0, 15))
        
        # Botão para escolher pasta de backup local
        self.btn_choose_backup = ctk.CTkButton(
            frame_local,
            text="Escolher Pasta de Backup",
            width=200,
            command=self.choose_backup_folder,
            state="normal"
        )
        self.btn_choose_backup.pack(padx=20, pady=(0, 15))
        
        self.lbl_backup_path = ctk.CTkLabel(
            frame_local,
            text="Nenhuma pasta selecionada",
            font=("Arial", 9),
            text_color="gray"
        )
        self.lbl_backup_path.pack(padx=20, pady=(0, 15))
        
        # Opção 2: Google Drive
        frame_drive = ctk.CTkFrame(self.content, border_width=2, corner_radius=15)
        frame_drive.pack(fill="x", pady=10, padx=20)
        
        radio_drive = ctk.CTkRadioButton(
            frame_drive,
            text="☁️ Google Drive (Nuvem)",
            variable=self.backup_type,
            value="google_drive",
            font=("Arial", 14, "bold")
        )
        radio_drive.pack(anchor="w", padx=20, pady=(15, 5))
        
        desc_drive = ctk.CTkLabel(
            frame_drive,
            text="✓ Acessível de qualquer lugar\n✓ Backup automático\n✓ Proteção contra perda física\n📌 Requer configuração (faremos depois na aba Nuvem)",
            font=("Arial", 10),
            text_color="gray",
            justify="left"
        )
        desc_drive.pack(anchor="w", padx=40, pady=(0, 15))
    
    def choose_backup_folder(self):
        """Escolhe pasta para backup local"""
        folder = filedialog.askdirectory(title="Escolha onde salvar os backups")
        if folder:
            self.config["backup_path"] = folder
            self.lbl_backup_path.configure(text=f"✓ {folder}", text_color="green")
        
    def step_automation(self):
        """Etapa 4: Agendamento"""
        self.title_label.configure(text="⏰ Quando executar manutenção automática?")
        
        info = ctk.CTkLabel(
            self.content,
            text="O sistema vai organizar, limpar e fazer backup automaticamente.\nEscolha o melhor horário para você:",
            font=("Arial", 12),
            justify="center"
        )
        info.pack(pady=(0, 20))
        
        self.schedule_var = ctk.StringVar(value="friday_18h")
        
        schedules = [
            ("🌙 Toda noite às 22h", "daily_22h", "Perfeito se você desliga o PC à noite", "#4a4a4a"),
            ("📅 Toda sexta às 18h", "friday_18h", "⭐ Recomendado - Ideal para semana de trabalho", "#06d6a0"),
            ("🗓️ Todo domingo às 10h", "sunday_10h", "Para quem trabalha sábado", "#4a4a4a"),
            ("❌ Não automatizar", "manual", "Você decide quando executar (não recomendado)", "#4a4a4a")
        ]
        
        for label, value, desc, color in schedules:
            frame = ctk.CTkFrame(self.content, fg_color=color, corner_radius=10)
            frame.pack(fill="x", pady=6, padx=20)
            
            radio = ctk.CTkRadioButton(
                frame,
                text=label,
                variable=self.schedule_var,
                value=value,
                font=("Arial", 13, "bold")
            )
            radio.pack(anchor="w", padx=15, pady=(12, 2))
            
            desc_label = ctk.CTkLabel(
                frame,
                text=desc,
                font=("Arial", 10),
                text_color="white" if value == "friday_18h" else "gray"
            )
            desc_label.pack(anchor="w", padx=35, pady=(0, 12))
    
    def step_final(self):
        """Etapa 5: Resumo e finalização"""
        self.title_label.configure(text="✅ Tudo Pronto!")
        
        # Resumo da configuração
        folders_count = len([v for v in self.folder_vars.values() if v.get()])
        backup_text = "Google Drive" if self.backup_type.get() == "google_drive" else f"Local: {self.config.get('backup_path', 'Não configurado')}"
        schedule_map = {
            "daily_22h": "Diariamente às 22h",
            "friday_18h": "Sexta-feira às 18h",
            "sunday_10h": "Domingo às 10h",
            "manual": "Manual (sem agendamento)"
        }
        schedule_text = schedule_map.get(self.schedule_var.get(), "Não definido")
        
        frame_summary = ctk.CTkFrame(self.content, fg_color="#2b2b2b", corner_radius=15)
        frame_summary.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            frame_summary,
            text="📋 Resumo da Configuração",
            font=("Arial", 16, "bold")
        ).pack(pady=(20, 15))
        
        summary_text = f"""
📁 Pastas a organizar: {folders_count} pasta(s) selecionada(s)

☁️ Tipo de Backup: {backup_text}

⏰ Agendamento: {schedule_text}

✨ O Titanium Suite está pronto para proteger seus dados!
        """
        
        ctk.CTkLabel(
            frame_summary,
            text=summary_text,
            font=("Arial", 13),
            justify="left"
        ).pack(pady=10, padx=30)
        
        ctk.CTkLabel(
            frame_summary,
            text="💡 Dica: Explore cada aba para conhecer todas as ferramentas disponíveis!",
            font=("Arial", 11),
            text_color="#4cc9f0",
            wraplength=600
        ).pack(pady=(10, 20))
        
    def next_step(self):
        """Avança para próxima etapa"""
        # Validações antes de avançar
        if self.current_step == 2:  # Página de backup
            if self.backup_type.get() == "local" and not self.config.get("backup_path"):
                from tkinter import messagebox
                messagebox.showwarning("Atenção", "Selecione uma pasta para o backup local ou escolha Google Drive.")
                return
        
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_current_step()
        else:
            self.finalizar_wizard()
    
    def previous_step(self):
        """Volta para etapa anterior"""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()
    
    def skip_wizard(self):
        """Pula wizard (salva configuração mínima)"""
        from tkinter import messagebox
        if messagebox.askyesno("Pular Tutorial", "Tem certeza? Você pode refazer depois no menu '❓ Refazer Tutorial'."):
            self.config["first_run_completed"] = True
            self.salvar_configuracao()
            self.destroy()
    
    def finalizar_wizard(self):
        """Salva configurações e fecha wizard"""
        # Coleta dados finais
        self.config["folders_to_organize"] = [
            path for path, var in self.folder_vars.items() if var.get()
        ]
        self.config["backup_type"] = self.backup_type.get()
        self.config["automation_schedule"] = self.schedule_var.get()
        self.config["first_run_completed"] = True
        
        self.salvar_configuracao()
        
        # Feedback visual
        from tkinter import messagebox
        messagebox.showinfo(
            "Configuração Concluída!",
            "✅ Titanium Suite configurado com sucesso!\n\n"
            "Explore as abas para conhecer todas as ferramentas.\n"
            "Seu sistema está protegido! 🛡️"
        )
        
        self.destroy()
    
    def salvar_configuracao(self):
        """Salva configuração em JSON"""
        config_path = Path("config/onboarding.json")
        config_path.parent.mkdir(exist_ok=True)
        
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)