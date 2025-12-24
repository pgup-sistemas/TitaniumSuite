import os
import shutil
import subprocess
import platform

class SystemCleaner:
    def __init__(self, logger_callback=None):
        """
        logger_callback: Função para enviar mensagens de texto para a interface (GUI)
        """
        self.log = logger_callback if logger_callback else print

    def limpar_temporarios(self):
        self.log("--- Iniciando Limpeza de Temporários ---")
        
        # Lista de pastas para limpar
        pastas = [
            os.environ.get('TEMP'), # Pasta %TEMP% do usuário
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp'), # C:\Windows\Temp
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch') # Prefetch
        ]

        bytes_removidos = 0

        for pasta in pastas:
            if not os.path.exists(pasta):
                continue
            
            self.log(f"Varrendo: {pasta}")
            for root, dirs, files in os.walk(pasta):
                for file in files:
                    caminho_completo = os.path.join(root, file)
                    try:
                        tamanho = os.path.getsize(caminho_completo)
                        os.remove(caminho_completo)
                        bytes_removidos += tamanho
                    except Exception:
                        # Arquivo em uso pelo Windows, ignora silenciosamente
                        pass
        
        mb_total = bytes_removidos / (1024 * 1024)
        self.log(f"✅ Concluído. Liberado: {mb_total:.2f} MB")

    def limpar_dns(self):
        self.log("--- Limpando Cache DNS ---")
        try:
            subprocess.run(["ipconfig", "/flushdns"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log("✅ Cache DNS limpo com sucesso.")
        except Exception as e:
            self.log(f"❌ Erro ao limpar DNS: {e}")

class NetworkTools:
    def __init__(self, logger_callback=None):
        self.log = logger_callback if logger_callback else print

    def verificar_internet(self):
        self.log("--- Testando Conectividade ---")
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        comando = ['ping', param, '1', '8.8.8.8']
        
        try:
            # creationflags=0x08000000 evita abrir tela preta do CMD
            subprocess.run(comando, check=True, creationflags=0x08000000) 
            self.log("✅ Conexão com Internet: ONLINE (Google DNS respondeu)")
            return True
        except subprocess.CalledProcessError:
            self.log("⚠️ Conexão com Internet: OFFLINE")
            return False
        except Exception as e:
            self.log(f"❌ Erro no teste de ping: {e}")
            return False