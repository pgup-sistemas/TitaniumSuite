# frame_dashboard.py - VERSÃO CORRIGIDA
import customtkinter as ctk
import os
import json
import psutil
from datetime import datetime, timedelta
from pathlib import Path
from src.ui.components.tooltip import add_tooltip

class FrameDashboard(ctk.CTkFrame):
    def __init__(self, parent, master_app=None):
        super().__init__(parent, fg_color="transparent")
        self.configure(width=1000, height=500)
        self.master_app = master_app
        
        # Grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Título com horário
        self.setup_header()
        
        # Cards de Status (2 colunas)
        self.setup_health_card()      # Esquerda: Saúde do Sistema
        self.setup_activity_card()    # Direita: Últimas Atividades
        
        # Alertas e Ações Rápidas
        self.setup_alerts_section()
        
        # Sistema de logs
        self.ensure_logs_exist()
        
        # Atualiza dados a cada 30 segundos (inteligente)
        self.update_dashboard_smart()
        
    def setup_header(self):
        """Cabeçalho com saudação personalizada"""
        frame_header = ctk.CTkFrame(self, fg_color="transparent")
        frame_header.grid(row=0, column=0, columnspan=2, pady=20, sticky="ew")
        
        # Saudação inteligente
        hora = datetime.now().hour
        if hora < 12:
            saudacao = "☀️ Bom dia"
        elif hora < 18:
            saudacao = "☀️ Boa tarde"
        else:
            saudacao = "🌙 Boa noite"
        
        usuario = os.getenv('USERNAME', 'Usuário')
        
        ctk.CTkLabel(
            frame_header, 
            text=f"{saudacao}, {usuario}!",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w")
        
        data_atual = datetime.now().strftime("%A, %d de %B de %Y")
        ctk.CTkLabel(
            frame_header,
            text=data_atual.replace("Monday", "Segunda").replace("Tuesday", "Terça"),
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w")
        
    def setup_health_card(self):
        """Card de Saúde do Sistema (Score 0-100)"""
        self.card_health = ctk.CTkFrame(self, corner_radius=15, width=400)
        self.card_health.grid(row=1, column=0, padx=10, pady=10, sticky="n")
        
        # Título do Card
        lbl_health_title = ctk.CTkLabel(
            self.card_health,
            text="🛡️ Saúde do Sistema",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        lbl_health_title.pack(pady=(15, 10))
        add_tooltip(lbl_health_title, "card_health")
        
        # Score Visual (Grande e Chamativo)
        self.lbl_score = ctk.CTkLabel(
            self.card_health,
            text="--",
            font=ctk.CTkFont(size=64, weight="bold"),
            text_color="#06d6a0"
        )
        self.lbl_score.pack(pady=10)
        
        self.lbl_status = ctk.CTkLabel(
            self.card_health,
            text="Analisando...",
            font=ctk.CTkFont(size=14)
        )
        self.lbl_status.pack()
        
        # Barra de progresso visual
        self.progress_health = ctk.CTkProgressBar(self.card_health, height=15)
        self.progress_health.pack(fill="x", pady=15)
        self.progress_health.set(0)
        
        # Indicadores Detalhados
        self.frame_indicators = ctk.CTkFrame(self.card_health, fg_color="transparent")
        self.frame_indicators.pack(pady=10, fill="x", padx=20)
        
        self.indicators = {}
        indicadores = [
            ("disco", "💾 Espaço em Disco"),
            ("backup", "☁️ Status Backup"),
            ("temp", "🗑️ Arquivos Temp"),
            ("licenca", "🔑 Licença")
        ]
        
        for key, label in indicadores:
            frame = ctk.CTkFrame(self.frame_indicators, fg_color="transparent")
            frame.pack(fill="x", pady=2)
            
            lbl = ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=11), anchor="w")
            lbl.pack(side="left")
            
            status = ctk.CTkLabel(frame, text="⏳", font=ctk.CTkFont(size=11))
            status.pack(side="right")
            
            self.indicators[key] = status
            
    def setup_activity_card(self):
        """Card de Últimas Atividades"""
        self.card_activity = ctk.CTkFrame(self, corner_radius=15, width=400)
        self.card_activity.grid(row=1, column=1, padx=10, pady=10, sticky="n")
        
        ctk.CTkLabel(
            self.card_activity,
            text="📊 Resumo do Sistema",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 10))
        
        # Frame rolável para estatísticas
        self.scroll_stats = ctk.CTkScrollableFrame(self.card_activity, height=250)
        self.scroll_stats.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Estatísticas (serão populadas dinamicamente)
        self.stats_labels = {}
        
    def setup_alerts_section(self):
        """Seção de Alertas e Ações Rápidas"""
        self.frame_alerts = ctk.CTkFrame(self, corner_radius=15)
        self.frame_alerts.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            self.frame_alerts,
            text="⚡ Ações Recomendadas",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 5), anchor="w", padx=15)
        
        # Container de alertas (dinâmico)
        self.container_alerts = ctk.CTkFrame(self.frame_alerts, fg_color="transparent")
        self.container_alerts.pack(fill="both", expand=True, padx=15, pady=10)
        
    def ensure_logs_exist(self):
        """Garante que os logs necessários existam"""
        # Cria diretório de logs
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Cria log de backup se não existir
        backup_log = logs_dir / "backup_history.json"
        if not backup_log.exists():
            initial_log = {
                "history": [],
                "last_check": datetime.now().isoformat()
            }
            with open(backup_log, "w") as f:
                json.dump(initial_log, f, indent=2)
        
        # Cria log de manutenção se não existir
        maintenance_log = logs_dir / "maintenance_history.json"
        if not maintenance_log.exists():
            initial_maintenance = {
                "history": [],
                "last_clean": datetime.now().isoformat()
            }
            with open(maintenance_log, "w") as f:
                json.dump(initial_maintenance, f, indent=2)
        
        # Garante que os logs estejam no formato correto
        self._validate_backup_log_format(backup_log)
        self._validate_maintenance_log_format(maintenance_log)
    
    def _validate_backup_log_format(self, backup_log):
        """Valida e corrige o formato do log de backup"""
        try:
            with open(backup_log, "r") as f:
                data = json.load(f)
            
            # Se for uma lista (formato antigo), converte para dicionário
            if isinstance(data, list):
                corrected_data = {
                    "history": data,
                    "last_check": datetime.now().isoformat()
                }
                with open(backup_log, "w") as f:
                    json.dump(corrected_data, f, indent=2)
        except:
            # Se houver erro, cria log padrão
            initial_log = {
                "history": [],
                "last_check": datetime.now().isoformat()
            }
            with open(backup_log, "w") as f:
                json.dump(initial_log, f, indent=2)
    
    def _validate_maintenance_log_format(self, maintenance_log):
        """Valida e corrige o formato do log de manutenção"""
        try:
            with open(maintenance_log, "r") as f:
                data = json.load(f)
            
            # Se for uma lista (formato antigo), converte para dicionário
            if isinstance(data, list):
                corrected_data = {
                    "history": data,
                    "last_clean": datetime.now().isoformat()
                }
                with open(maintenance_log, "w") as f:
                    json.dump(corrected_data, f, indent=2)
        except:
            # Se houver erro, cria log padrão
            initial_maintenance = {
                "history": [],
                "last_clean": datetime.now().isoformat()
            }
            with open(maintenance_log, "w") as f:
                json.dump(initial_maintenance, f, indent=2)
    
    def update_dashboard_smart(self):
        """Atualiza dashboard baseado em necessidade real"""
        try:
            # Calcula saúde do sistema
            score, status_text, color = self.calculate_health_score()
            
            # Atualiza UI
            self.lbl_score.configure(text=f"{score}", text_color=color)
            self.lbl_status.configure(text=status_text)
            self.progress_health.set(score / 100)
            
            # Atualiza estatísticas reais
            self.update_real_statistics()
            
            # Atualiza alertas
            self.update_alerts()
            
            # Define intervalo baseado no score
            if score < 50:  # Sistema crítico
                interval = 10000  # Atualiza a cada 10s
            elif score < 70:  # Sistema com atenção
                interval = 20000  # Atualiza a cada 20s
            else:  # Sistema saudável
                interval = 60000  # Atualiza a cada 60s
            
            # Reagenda
            self.after(interval, self.update_dashboard_smart)
            
        except Exception as e:
            self.log_error(f"Erro na atualização do dashboard: {e}")
            # Reagenda mesmo com erro
            self.after(30000, self.update_dashboard_smart)
        
    def calculate_health_score(self):
        """Calcula pontuação de saúde (0-100) - VERSÃO CORRIGIDA"""
        score = 100
        issues = []
        
        # 1. ESPAÇO EM DISCO (30 pontos) - CORRIGIDO PARA MULTIPLATAFORMA
        try:
            disk_percent, disk_free_gb, disk_total_gb = self.get_disk_usage()
            
            if disk_percent > 95:
                score -= 30
                self.indicators["disco"].configure(text=f"🔴 {disk_percent:.0f}%", text_color="#ef233c")
                issues.append("Disco quase cheio")
            elif disk_percent > 85:
                score -= 15
                self.indicators["disco"].configure(text=f"⚠️ {disk_percent:.0f}%", text_color="#ffd60a")
            else:
                self.indicators["disco"].configure(text=f"✅ {disk_percent:.0f}%", text_color="#06d6a0")
        except Exception as e:
            score -= 10
            self.indicators["disco"].configure(text="❓ Erro", text_color="gray")
            self.log_error(f"Erro ao capturar disco: {e}")
        
        # 2. STATUS BACKUP (30 pontos) - MELHORADO
        try:
            backup_status, backup_info = self.get_backup_status()
            if backup_status == "critical":
                score -= 30
                self.indicators["backup"].configure(text=f"🔴 {backup_info}", text_color="#ef233c")
                issues.append("Backup desatualizado")
            elif backup_status == "warning":
                score -= 15
                self.indicators["backup"].configure(text=f"⚠️ {backup_info}", text_color="#ffd60a")
            else:
                self.indicators["backup"].configure(text=f"✅ {backup_info}", text_color="#06d6a0")
        except Exception as e:
            score -= 20
            self.indicators["backup"].configure(text="❓ Erro", text_color="gray")
            self.log_error(f"Erro ao capturar backup: {e}")
        
        # 3. ARQUIVOS TEMPORÁRIOS (20 pontos) - CORRIGIDO
        try:
            temp_size_gb, temp_count = self.get_temp_files_info()
            
            if temp_size_gb > 5:
                score -= 20
                self.indicators["temp"].configure(text=f"🔴 {temp_size_gb:.1f}GB", text_color="#ef233c")
                issues.append("Muitos arquivos temporários")
            elif temp_size_gb > 2:
                score -= 10
                self.indicators["temp"].configure(text=f"⚠️ {temp_size_gb:.1f}GB", text_color="#ffd60a")
            else:
                self.indicators["temp"].configure(text=f"✅ {temp_size_gb:.1f}GB", text_color="#06d6a0")
        except Exception as e:
            self.indicators["temp"].configure(text="❓ Erro", text_color="gray")
            self.log_error(f"Erro ao capturar arquivos temp: {e}")
        
        # 4. LICENÇA (20 pontos) - MELHORADO
        try:
            license_status = self.get_license_status()
            if license_status == "valid":
                self.indicators["licenca"].configure(text="✅ Ativa", text_color="#06d6a0")
            elif license_status == "trial":
                self.indicators["licenca"].configure(text="⏱️ Trial", text_color="#ffd60a")
            else:
                score -= 20
                self.indicators["licenca"].configure(text="🔴 Inválida", text_color="#ef233c")
                issues.append("Licença expirada")
        except Exception as e:
            score -= 10
            self.indicators["licenca"].configure(text="❓ Erro", text_color="gray")
            self.log_error(f"Erro ao capturar licença: {e}")
        
        # Define texto e cor baseado no score
        if score >= 90:
            status = "Excelente"
            color = "#06d6a0"
        elif score >= 70:
            status = "Bom"
            color = "#4cc9f0"
        elif score >= 50:
            status = "Atenção Necessária"
            color = "#ffd60a"
        else:
            status = "Crítico"
            color = "#ef233c"
        
        return score, status, color
    
    def get_disk_usage(self):
        """Captura uso de disco multiplataforma - CORREÇÃO CRÍTICA"""
        try:
            if os.name == 'nt':  # Windows
                disk = psutil.disk_usage('C:')
            else:  # Linux/Mac
                disk = psutil.disk_usage('/')
            
            percent_used = (disk.total - disk.free) / disk.total * 100
            free_gb = disk.free / (1024**3)
            total_gb = disk.total / (1024**3)
            
            return percent_used, free_gb, total_gb
        except Exception as e:
            self.log_error(f"Erro ao capturar disco: {e}")
            return 0, 0, 0
    
    def get_temp_files_info(self):
        """Captura informações de arquivos temporários de forma segura - CORREÇÃO CRÍTICA"""
        temp_paths = self._get_temp_paths()
        total_size = 0
        file_count = 0
        
        for temp_path in temp_paths:
            if temp_path.exists():
                try:
                    # Usa generator para economizar memória e evitar bloqueios
                    for item in self._safe_iterdir(temp_path):
                        if item.is_file():
                            try:
                                # Verifica se é realmente um arquivo temporário
                                if self._is_temp_file(item):
                                    stat = item.stat()
                                    total_size += stat.st_size
                                    file_count += 1
                            except (PermissionError, OSError):
                                continue  # Pula arquivos sem permissão
                except Exception as e:
                    self.log_error(f"Erro ao ler {temp_path}: {e}")
        
        return total_size / (1024**3), file_count  # Retorna em GB
    
    def _get_temp_paths(self):
        """Obtém caminhos de arquivos temporários baseados no sistema"""
        temp_paths = []
        
        # Caminho TEMP padrão
        temp_env = os.environ.get('TEMP', '')
        if temp_env:
            temp_paths.append(Path(temp_env))
        
        # Caminho Windows Temp
        if os.name == 'nt':
            windir = os.environ.get('WINDIR', '')
            if windir:
                temp_paths.append(Path(windir) / "Temp")
        
        # Caminho Linux/Mac Temp
        else:
            temp_paths.append(Path("/tmp"))
        
        return temp_paths
    
    def _safe_iterdir(self, path):
        """Itera sobre diretório de forma segura"""
        try:
            return path.iterdir()
        except PermissionError:
            return []
    
    def _is_temp_file(self, file_path):
        """Verifica se é realmente um arquivo temporário"""
        temp_extensions = ['.tmp', '.temp', '.cache', '.log']
        temp_names = ['temp', 'tmp', 'cache']
        
        # Verifica extensão
        if file_path.suffix.lower() in temp_extensions:
            return True
        
        # Verifica nome
        name_lower = file_path.stem.lower()
        if any(temp_name in name_lower for temp_name in temp_names):
            return True
        
        # Verifica data de modificação (arquivos muito antigos não são temporários)
        try:
            stat = file_path.stat()
            age_days = (datetime.now().timestamp() - stat.st_mtime) / (24 * 3600)
            if age_days > 30:  # Mais de 30 dias
                return False
        except:
            pass
        
        return False
    
    def get_backup_status(self):
        """Obtém status do backup - MELHORADO"""
        backup_log = Path("logs/backup_history.json")
        
        if not backup_log.exists():
            return "critical", "Nunca feito"
        
        try:
            with open(backup_log, "r", encoding="utf-8") as f:
                history_data = json.load(f)
            
            # Valida se é dicionário
            if not isinstance(history_data, dict):
                # Se for lista, converte
                history_data = {"history": history_data, "last_check": datetime.now().isoformat()}
                with open(backup_log, "w") as f:
                    json.dump(history_data, f, indent=2)
            
            if not history_data.get("history"):
                return "warning", "Sem histórico"
            
            last_backup_str = history_data["history"][-1]["timestamp"]
            last_backup = datetime.fromisoformat(last_backup_str)
            days_ago = (datetime.now() - last_backup).days
            
            if days_ago > 14:
                return "critical", f"Há {days_ago}d"
            elif days_ago > 7:
                return "warning", f"Há {days_ago}d"
            else:
                return "ok", f"Há {days_ago}d"
                
        except Exception as e:
            self.log_error(f"Erro ao ler log de backup: {e}")
            return "error", "Erro de leitura"
    
    def get_license_status(self):
        """Obtém status da licença - MELHORADO"""
        license_file = Path("license.key")
        
        if not license_file.exists():
            # Verifica trial
            trial_status = self._check_trial_status()
            if trial_status["status"] == "trial_ativo":
                return "trial"
            return "invalid"
        
        try:
            from src.modules.auth import AuthManager
            auth = AuthManager()
            
            if auth.verificar_licenca_completa():
                return "valid"
            else:
                return "expired"
        except Exception as e:
            self.log_error(f"Erro ao verificar licença: {e}")
            return "error"
    
    def _check_trial_status(self):
        """Verifica status do trial"""
        trial_config = Path("config/trial.json")
        
        if not trial_config.exists():
            return {"status": "trial_ativo", "dias_restantes": 30}
        
        try:
            with open(trial_config, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            data_inicio = datetime.fromisoformat(data["data_inicio"])
            data_fim = data_inicio + timedelta(days=data["trial_dias"])
            agora = datetime.now()
            
            if agora <= data_fim:
                dias_restantes = (data_fim - agora).days
                return {"status": "trial_ativo", "dias_restantes": dias_restantes}
            else:
                return {"status": "trial_expirado", "dias_restantes": 0}
        except:
            return {"status": "erro", "dias_restantes": 0}
    
    def update_real_statistics(self):
        """Atualiza estatísticas reais do sistema - SUBSTITUI DADOS FICTÍCIOS"""
        # Limpa stats anteriores
        for widget in self.scroll_stats.winfo_children():
            widget.destroy()
        
        # Carrega dados reais
        stats_data = self.load_real_stats()
        
        for stat in stats_data:
            frame = ctk.CTkFrame(self.scroll_stats, fg_color="#2b2b2b", corner_radius=10)
            frame.pack(fill="x", pady=5)
            
            # Ícone + Label
            ctk.CTkLabel(
                frame,
                text=f"{stat['icon']} {stat['label']}",
                font=ctk.CTkFont(size=12),
                anchor="w"
            ).pack(side="left", padx=10, pady=8)
            
            # Valor
            ctk.CTkLabel(
                frame,
                text=stat['value'],
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#4cc9f0"
            ).pack(side="right", padx=10, pady=8)
    
    def load_real_stats(self):
        """Carrega estatísticas reais do sistema - SUBSTITUIÇÃO CRÍTICA"""
        stats = []
        
        # 1. Espaço em Disco (REAL)
        try:
            disk_percent, disk_free_gb, disk_total_gb = self.get_disk_usage()
            stats.append({
                "icon": "💾", 
                "label": "Espaço em Disco", 
                "value": f"{disk_free_gb:.1f} GB livre"
            })
        except:
            stats.append({
                "icon": "❓", 
                "label": "Espaço em Disco", 
                "value": "Erro ao capturar"
            })
        
        # 2. Arquivos Temporários (REAL)
        try:
            temp_size_gb, temp_count = self.get_temp_files_info()
            stats.append({
                "icon": "🗑️", 
                "label": "Arquivos Temp", 
                "value": f"{temp_count:,} arquivos ({temp_size_gb:.1f}GB)"
            })
        except:
            stats.append({
                "icon": "❓", 
                "label": "Arquivos Temp", 
                "value": "Erro ao capturar"
            })
        
        # 3. Status da Licença (REAL)
        try:
            license_status = self.get_license_status()
            if license_status == "valid":
                stats.append({
                    "icon": "✅", 
                    "label": "Licença", 
                    "value": "Ativa"
                })
            elif license_status == "trial":
                trial_info = self._check_trial_status()
                stats.append({
                    "icon": "⏱️", 
                    "label": "Licença", 
                    "value": f"Trial ({trial_info['dias_restantes']} dias)"
                })
            else:
                stats.append({
                    "icon": "⚠️", 
                    "label": "Licença", 
                    "value": "Expirada"
                })
        except:
            stats.append({
                "icon": "❓", 
                "label": "Licença", 
                "value": "Erro ao verificar"
            })
        
        # 4. Status do Backup (REAL)
        try:
            backup_status, backup_info = self.get_backup_status()
            stats.append({
                "icon": "☁️", 
                "label": "Backup", 
                "value": backup_info
            })
        except:
            stats.append({
                "icon": "❓", 
                "label": "Backup", 
                "value": "Erro ao verificar"
            })
        
        # 5. Uso de Memória (ADICIONAL)
        try:
            memory = psutil.virtual_memory()
            stats.append({
                "icon": "🧠", 
                "label": "Memória RAM", 
                "value": f"{memory.percent}% usado"
            })
        except:
            stats.append({
                "icon": "❓", 
                "label": "Memória RAM", 
                "value": "Erro ao capturar"
            })
        
        # 6. CPU (ADICIONAL)
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            stats.append({
                "icon": "⚡", 
                "label": "CPU", 
                "value": f"{cpu_percent:.1f}% uso"
            })
        except:
            stats.append({
                "icon": "❓", 
                "label": "CPU", 
                "value": "Erro ao capturar"
            })
        
        return stats
    
    def update_alerts(self):
        """Atualiza alertas e ações recomendadas - MELHORADO"""
        # Limpa alertas anteriores
        for widget in self.container_alerts.winfo_children():
            widget.destroy()
        
        # Coleta alertas baseado no score
        score, _, _ = self.calculate_health_score()
        
        if score < 70:
            # Mostra botão de ação rápida
            btn_action = ctk.CTkButton(
                self.container_alerts,
                text="🚀 Executar Manutenção Completa",
                font=ctk.CTkFont(size=14, weight="bold"),
                height=50,
                fg_color="#06d6a0",
                hover_color="#05c28a",
                command=self.run_quick_maintenance
            )
            btn_action.pack(fill="x", pady=5)
        
        # Alertas específicos baseados em dados reais
        self._add_specific_alerts()
    
    def _add_specific_alerts(self):
        """Adiciona alertas específicos baseados em dados reais"""
        
        # Alerta de Backup
        backup_status, backup_info = self.get_backup_status()
        if backup_status in ["critical", "error"]:
            self.create_alert_card(
                "☁️ Backup Pendente",
                f"Status: {backup_info}. Proteja seus dados agora!",
                "Criar Backup",
                self.open_backup_tab
            )
        
        # Alerta de Espaço em Disco
        try:
            disk_percent, _, _ = self.get_disk_usage()
            if disk_percent > 85:
                self.create_alert_card(
                    "💾 Espaço em Disco Baixo",
                    f"Seu disco está {disk_percent:.0f}% cheio. Libere espaço.",
                    "Limpar Agora",
                    self.open_maintenance_tab
                )
        except:
            pass
        
        # Alerta de Arquivos Temporários
        try:
            temp_size_gb, temp_count = self.get_temp_files_info()
            if temp_size_gb > 2:
                self.create_alert_card(
                    "🗑️ Muitos Arquivos Temp",
                    f"{temp_count:,} arquivos temporários ocupando {temp_size_gb:.1f}GB.",
                    "Limpar Temp",
                    self.open_maintenance_tab
                )
        except:
            pass
        
        # Alerta de Licença
        license_status = self.get_license_status()
        if license_status in ["expired", "invalid"]:
            self.create_alert_card(
                "🔑 Licença Expirada",
                "Sua licença expirou. Ative para continuar usando.",
                "Ativar Agora",
                self.open_license_tab
            )
    
    def create_alert_card(self, title, description, btn_text, btn_action):
        """Cria um card de alerta com botão de ação"""
        frame = ctk.CTkFrame(self.container_alerts, fg_color="#2b2b2b", corner_radius=10)
        frame.pack(fill="x", pady=5)
        
        # Grid para layout
        frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 2))
        
        ctk.CTkLabel(
            frame,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w",
            wraplength=600
        ).grid(row=1, column=0, sticky="w", padx=15, pady=(0, 10))
        
        ctk.CTkButton(
            frame,
            text=btn_text,
            width=150,
            height=30,
            command=btn_action
        ).grid(row=0, column=1, rowspan=2, padx=15, pady=10)
    
    def run_quick_maintenance(self):
        """Executa manutenção rápida - INTEGRADO"""
        if self.master_app:
            self.master_app.executar_manutencao_completa()
        else:
            print("Executando manutenção rápida...")
    
    def open_backup_tab(self):
        """Abre aba de backup - INTEGRADO"""
        if self.master_app:
            self.master_app.selecionar_menu("nuvem")
        else:
            print("Abrindo aba de backup...")
    
    def open_maintenance_tab(self):
        """Abre aba de manutenção - INTEGRADO"""
        if self.master_app:
            self.master_app.selecionar_menu("manutencao")
        else:
            print("Abrindo aba de manutenção...")
    
    def open_license_tab(self):
        """Abre aba de configuração de segurança/licença"""
        if self.master_app:
            self.master_app.selecionar_menu("dashboard")  # Ou criar aba específica
            # Poderia abrir configuração de segurança
        else:
            print("Abrindo configuração de licença...")
    
    def log_error(self, message):
        """Registra erro e informa usuário - SISTEMA DE LOGS"""
        # Registra no console
        print(f"[DASHBOARD ERROR] {datetime.now().strftime('%H:%M:%S')} - {message}")
        
        # Registra em arquivo de log
        try:
            error_log = Path("logs/dashboard_errors.log")
            with open(error_log, "a") as f:
                f.write(f"{datetime.now().isoformat()} - {message}\n")
        except:
            pass
        
        # Mostra notificação ao usuário (se houver label de status)
        if hasattr(self, 'lbl_status'):
            self.lbl_status.configure(
                text=f"⚠️ Erro: {message[:50]}...",
                text_color="red"
            )