import sqlite3
import hashlib
import uuid
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

class AuthManager:
    def __init__(self):
        self.db_path = "database/titanium.db"
        self._inicializar_db()

    def _inicializar_db(self):
        """Cria a tabela de usuários se não existir"""
        os.makedirs("database", exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de Usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                security_question TEXT,
                security_answer_hash TEXT
            )
        ''')
        
        # Migração: Adiciona colunas de segurança se não existirem
        self._migrar_tabela_seguranca(cursor)
        
        # Cria um usuário Admin padrão se o banco estiver vazio
        cursor.execute("SELECT count(*) FROM users")
        if cursor.fetchone()[0] == 0:
            self._criar_usuario_admin(cursor)
            
        conn.commit()
        conn.close()
    
    def _migrar_tabela_seguranca(self, cursor):
        """Migra a tabela existente para adicionar colunas de segurança"""
        try:
            # Verifica se as colunas já existem
            cursor.execute("PRAGMA table_info(users)")
            colunas_existentes = [coluna[1] for coluna in cursor.fetchall()]
            
            # Adiciona coluna security_question se não existir
            if "security_question" not in colunas_existentes:
                cursor.execute("ALTER TABLE users ADD COLUMN security_question TEXT")
                print(">> Coluna security_question adicionada")
            
            # Adiciona coluna security_answer_hash se não existir
            if "security_answer_hash" not in colunas_existentes:
                cursor.execute("ALTER TABLE users ADD COLUMN security_answer_hash TEXT")
                print(">> Coluna security_answer_hash adicionada")
                
        except sqlite3.Error as e:
            print(f">> Erro na migração: {e}")
    
    def _criar_usuario_admin(self, cursor):
        """Cria usuário admin padrão"""
        # Senha padrão: admin123
        senha_hash = self._hash_senha("admin123")
        # Pergunta de segurança padrão
        pergunta = "Qual é o nome do seu primeiro pet?"
        resposta = "rex"  # Resposta padrão
        resposta_hash = self._hash_senha(resposta)
        
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", 
                     ("admin", senha_hash, "superadmin", pergunta, resposta_hash))
        print(">> Usuário 'admin' criado com senha 'admin123'")
        print(">> Pergunta de segurança configurada")

    def _hash_senha(self, senha):
        """Gera SHA-256 da senha"""
        return hashlib.sha256(senha.encode()).hexdigest()

    def verificar_login(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            hash_salvo, role = resultado
            if self._hash_senha(password) == hash_salvo:
                return True, role
        
        return False, None

    # --- SISTEMA DE LICENÇA (Hardware ID) ---
    
    def pegar_id_maquina(self):
        """Gera um ID único baseado na máquina"""
        mac = hex(uuid.getnode()).replace('0x', '').upper()
        return hashlib.md5(mac.encode()).hexdigest()[:16].upper() # Retorna 16 caracteres

    def verificar_licenca(self):
        """
        Verifica se existe um arquivo 'license.key' válido.
        Lógica Simplificada: A licença deve ser o Hash do ID da Máquina + Segredo.
        """
        if not os.path.exists("license.key"):
            return False
            
        with open("license.key", "r") as f:
            chave_arquivo = f.read().strip()
            
        id_maquina = self.pegar_id_maquina()
        # SEGREDO DO DESENVOLVEDOR (Só você sabe isso)
        segredo = "TITANIUM_2025_SECRET_KEY" 
        
        # Recalcula o que deveria ser a chave
        chave_esperada = hashlib.sha256((id_maquina + segredo).encode()).hexdigest()[:20].upper()
        
        return chave_arquivo == chave_esperada

    def gerar_licenca_para_cliente(self, id_cliente):
        """
        VOCÊ USA ISSO: Função para gerar a chave que você enviará ao cliente.
        Coloque isso num script separado 'gerador_keys.py' que fica SÓ COM VOCÊ.
        """
        segredo = "TITANIUM_2025_SECRET_KEY"
        return hashlib.sha256((id_cliente + segredo).encode()).hexdigest()[:20].upper()

    # ===== SISTEMA DE TRIAL PROFISSIONAL =====
    
    def verificar_trial_status(self):
        """
        Verifica se o usuário está em período de trial
        Returns: dict com status do trial
        """
        trial_config = Path("config/trial.json")
        
        if not trial_config.exists():
            # Primeiro uso - cria trial de 30 dias
            self._inicializar_trial()
            return self._get_trial_status()
        
        try:
            with open(trial_config, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            data_inicio = datetime.fromisoformat(data["data_inicio"])
            data_fim = data_inicio + timedelta(days=30)
            agora = datetime.now()
            
            if agora <= data_fim:
                dias_restantes = (data_fim - agora).days
                return {
                    "status": "trial_ativo",
                    "dias_restantes": dias_restantes,
                    "data_fim": data_fim.strftime("%d/%m/%Y"),
                    "ativado": False
                }
            else:
                return {
                    "status": "trial_expirado",
                    "dias_restantes": 0,
                    "ativado": False
                }
        except:
            return {"status": "erro", "dias_restantes": 0, "ativado": False}
    
    def _inicializar_trial(self):
        """Inicia período de trial de 30 dias"""
        os.makedirs("config", exist_ok=True)
        trial_data = {
            "data_inicio": datetime.now().isoformat(),
            "trial_dias": 30,
            "versao": "2.0"
        }
        
        with open("config/trial.json", "w", encoding="utf-8") as f:
            json.dump(trial_data, f, indent=2, ensure_ascii=False)
    
    def _get_trial_status(self):
        """Retorna status atual do trial"""
        trial_config = Path("config/trial.json")
        
        try:
            with open(trial_config, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            data_inicio = datetime.fromisoformat(data["data_inicio"])
            data_fim = data_inicio + timedelta(days=data["trial_dias"])
            agora = datetime.now()
            
            if agora <= data_fim:
                dias_restantes = (data_fim - agora).days
                return {
                    "status": "trial_ativo",
                    "dias_restantes": dias_restantes,
                    "data_fim": data_fim.strftime("%d/%m/%Y"),
                    "ativado": False
                }
            else:
                return {
                    "status": "trial_expirado",
                    "dias_restantes": 0,
                    "ativado": False
                }
        except:
            return {"status": "erro", "dias_restantes": 0, "ativado": False}
    
    def verificar_licenca_completa(self):
        """
        Verifica licença incluindo trial - VERSÃO PROFISSIONAL
        """
        # 1. Verifica trial ativo
        trial_status = self.verificar_trial_status()
        if trial_status["status"] == "trial_ativo":
            return True  # Trial ativo permite uso
        
        # 2. Verifica licença comprada
        if self.verificar_licenca():
            return True
        
        return False
    
    def gerar_chave_ativacao_profissional(self):
        """
        Gera chave de ativação profissional automaticamente
        """
        id_maquina = self.pegar_id_maquina()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        segredo = "TITANIUM_PRO_2025_SECRET"
        
        # Gera chave única para esta máquina e momento
        chave = hashlib.sha256((id_maquina + timestamp + segredo).encode()).hexdigest()[:24].upper()
        
        return chave
    
    def ativar_sistema_profissional(self, chave_digitada):
        """
        Ativa o sistema profissionalmente
        """
        # Verifica se é chave válida
        chave_esperada = self.gerar_chave_ativacao_profissional()
        
        if chave_digitada.strip().upper() == chave_esperada:
            # Chave válida - salva licença
            with open("license.key", "w") as f:
                f.write(chave_digitada.strip())
            
            # Registra ativação
            ativacao_data = {
                "chave": chave_digitada.strip(),
                "data_ativacao": datetime.now().isoformat(),
                "id_maquina": self.pegar_id_maquina(),
                "versao": "2.0_profissional"
            }
            
            with open("config/ativacao_profissional.json", "w", encoding="utf-8") as f:
                json.dump(ativacao_data, f, indent=2, ensure_ascii=False)
            
            return True, "Sistema ativado com sucesso!"
        else:
            return False, "Chave de ativação inválida."

    # ===== SISTEMA DE REDEFINIÇÃO DE SENHA =====
    
    def obter_pergunta_seguranca(self, username):
        """
        Obtém a pergunta de segurança de um usuário
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT security_question FROM users WHERE username = ?", (username,))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado and resultado[0]:
            return resultado[0]
        return None
    
    def verificar_resposta_seguranca(self, username, resposta):
        """
        Verifica se a resposta de segurança está correta
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT security_answer_hash FROM users WHERE username = ?", (username,))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado and resultado[0]:
            resposta_hash = self._hash_senha(resposta)
            return resposta_hash == resultado[0]
        return False
    
    def redefinir_senha(self, username, nova_senha, resposta_seguranca):
        """
        Redefine a senha de um usuário após verificar resposta de segurança
        """
        # Verifica se a resposta está correta
        if not self.verificar_resposta_seguranca(username, resposta_seguranca):
            return False, "Resposta de segurança incorreta."
        
        # Atualiza a senha
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        nova_senha_hash = self._hash_senha(nova_senha)
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", 
                     (nova_senha_hash, username))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return True, "Senha redefinida com sucesso!"
        else:
            conn.close()
            return False, "Usuário não encontrado."
    
    def redefinir_usuario_senha(self, username_atual, nova_senha, resposta_seguranca):
        """
        Redefine tanto o nome de usuário quanto a senha
        """
        # Verifica se a resposta está correta
        if not self.verificar_resposta_seguranca(username_atual, resposta_seguranca):
            return False, "Resposta de segurança incorreta."
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Solicita novo nome de usuário
        novo_username = input("Digite o novo nome de usuário: ").strip()
        if not novo_username:
            conn.close()
            return False, "Nome de usuário não pode estar vazio."
        
        # Verifica se o novo nome já existe
        cursor.execute("SELECT username FROM users WHERE username = ?", (novo_username,))
        if cursor.fetchone():
            conn.close()
            return False, "Este nome de usuário já existe."
        
        # Atualiza usuário e senha
        nova_senha_hash = self._hash_senha(nova_senha)
        cursor.execute("UPDATE users SET username = ?, password_hash = ? WHERE username = ?", 
                     (novo_username, nova_senha_hash, username_atual))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return True, f"Usuário alterado para '{novo_username}' e senha redefinida!"
        else:
            conn.close()
            return False, "Usuário não encontrado."
    
    def listar_perguntas_seguranca(self):
        """
        Retorna lista de perguntas de segurança disponíveis
        """
        return [
            "Qual é o nome do seu primeiro pet?",
            "Qual foi o nome da sua primeira escola?",
            "Qual é o nome da sua cidade natal?",
            "Qual foi o modelo do seu primeiro carro?",
            "Qual é o nome do seu melhor amigo de infância?",
            "Qual foi o seu primeiro emprego?",
            "Qual é o nome da sua mãe?",
            "Qual é o seu filme favorito?",
            "Qual é a sua comida favorita?",
            "Qual é o nome do seu personagem de ficção favorito?"
        ]
    
    def configurar_pergunta_seguranca(self, username, pergunta, resposta):
        """
        Configura uma nova pergunta e resposta de segurança
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        resposta_hash = self._hash_senha(resposta)
        cursor.execute("UPDATE users SET security_question = ?, security_answer_hash = ? WHERE username = ?", 
                     (pergunta, resposta_hash, username))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return True, "Pergunta de segurança configurada!"
        else:
            conn.close()
            return False, "Usuário não encontrado."