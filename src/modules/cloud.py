import os
import json
import pickle
import hashlib
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

class DriveManager:
    def __init__(self, logger_callback=None):
        self.log = logger_callback if logger_callback else print
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.creds = None
        self.service = None
        self.arquivo_credenciais = "credentials.json"
        self.arquivo_token = "token.pickle"
        self.metadata_path = "logs/backup_history.json"

    # --- HASHING E METADATA ---
    def _hash_file(self, filepath: str) -> str:
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return None

    def _carregar_metadata(self) -> dict:
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _salvar_metadata(self, data: dict):
        os.makedirs(os.path.dirname(self.metadata_path), exist_ok=True)
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    # --- SETUP E CONEXÃO ---
    def configurar_json_texto(self, texto_json):
        try:
            dados = json.loads(texto_json)
            if 'installed' not in dados and 'web' not in dados:
                return False, "JSON inválido."
            with open(self.arquivo_credenciais, "w") as f:
                json.dump(dados, f)
            return True, "Credenciais salvas!"
        except Exception as e:
            return False, str(e)

    def conectar(self):
        if not os.path.exists(self.arquivo_credenciais):
            self.log("❌ Erro: Credenciais 'credentials.json' não encontradas.")
            return False
        try:
            if os.path.exists(self.arquivo_token):
                with open(self.arquivo_token, 'rb') as token:
                    self.creds = pickle.load(token)
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(self.arquivo_credenciais, self.SCOPES)
                    self.creds = flow.run_local_server(port=0)
                with open(self.arquivo_token, 'wb') as token:
                    pickle.dump(self.creds, token)
            self.service = build('drive', 'v3', credentials=self.creds)
            self.log("✅ Conectado ao Google Drive.")
            return True
        except Exception as e:
            self.log(f"❌ Falha na conexão: {e}")
            return False

    # --- LÓGICA DE PASTAS E ARQUIVOS NO DRIVE ---
    def _get_item_id(self, name, parent_id, is_folder=False):
        mime_query = "mimeType = 'application/vnd.google-apps.folder'" if is_folder else ""
        query = f"name = '{name}' and '{parent_id}' in parents and trashed = false"
        if mime_query:
            query += f" and {mime_query}"
        
        results = self.service.files().list(q=query, fields="files(id)").execute()
        items = results.get('files', [])
        return items[0]['id'] if items else None

    def _criar_pasta_se_nao_existe(self, nome, parent_id):
        existente_id = self._get_item_id(nome, parent_id, is_folder=True)
        if existente_id:
            return existente_id
        metadata = {'name': nome, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [parent_id]}
        file = self.service.files().create(body=metadata, fields='id').execute()
        return file.get('id')

    # --- FUNCIONALIDADES PRINCIPAIS ---
    def fazer_backup_pasta(self, pasta_local, nome_destino_drive):
        if not self.service and not self.conectar():
            return

        self.log(f"🚀 Iniciando Backup Incremental de: {pasta_local}")
        
        metadata = self._carregar_metadata()
        backup_job_metadata = metadata.get(nome_destino_drive, {})
        
        root_drive_id = self._criar_pasta_se_nao_existe(nome_destino_drive, 'root')
        mapa_pastas = {pasta_local: root_drive_id}

        total_enviados = 0
        total_atualizados = 0
        total_pulados = 0

        for root, dirs, files in os.walk(pasta_local):
            parent_id_atual = mapa_pastas.get(root)
            if not parent_id_atual:
                continue

            for d in sorted(dirs):
                caminho_local_subpasta = os.path.join(root, d)
                novo_id = self._criar_pasta_se_nao_existe(d, parent_id_atual)
                mapa_pastas[caminho_local_subpasta] = novo_id

            for f in sorted(files):
                caminho_abs = os.path.join(root, f)
                try:
                    file_hash = self._hash_file(caminho_abs)
                    file_mtime = os.path.getmtime(caminho_abs)
                    
                    metadata_arquivo = backup_job_metadata.get(caminho_abs)
                    
                    if metadata_arquivo and metadata_arquivo['hash'] == file_hash and metadata_arquivo['mtime'] == file_mtime:
                        total_pulados += 1
                        continue

                    drive_file_id = self._get_item_id(f, parent_id_atual)
                    media = MediaFileUpload(caminho_abs, resumable=True)

                    if drive_file_id:
                        self.log(f"🔄 Atualizando: {f}...")
                        self.service.files().update(fileId=drive_file_id, media_body=media).execute()
                        total_atualizados += 1
                    else:
                        self.log(f"⬆️ Enviando: {f}...")
                        file_metadata = {'name': f, 'parents': [parent_id_atual]}
                        self.service.files().create(body=file_metadata, media_body=media).execute()
                        total_enviados += 1
                    
                    backup_job_metadata[caminho_abs] = {'hash': file_hash, 'mtime': file_mtime}
                except Exception as e:
                    self.log(f"❌ Erro com o arquivo {f}: {e}")
        
        metadata[nome_destino_drive] = backup_job_metadata
        self._salvar_metadata(metadata)

        self.log(f"✅ FIM DO BACKUP. Enviados: {total_enviados} | Atualizados: {total_atualizados} | Pulados: {total_pulados}")

    def listar_backups_raizes(self):
        """Lista todas as pastas na raiz do Google Drive."""
        if not self.service and not self.conectar():
            return []
        try:
            query = "mimeType = 'application/vnd.google-apps.folder' and 'root' in parents and trashed = false"
            results = self.service.files().list(q=query, fields="files(id, name)").execute()
            return results.get('files', [])
        except Exception as e:
            self.log(f"❌ Erro ao listar pastas da raiz: {e}")
            return []

    def listar_arquivos_backup(self, folder_id):
        """Lista todos os arquivos recursivamente a partir de um folder_id."""
        if not self.service and not self.conectar():
            return []
        
        arquivos_encontrados = []
        page_token = None
        while True:
            try:
                response = self.service.files().list(q=f"'{folder_id}' in parents and trashed=false",
                                                     spaces='drive',
                                                     fields='nextPageToken, files(id, name, mimeType)',
                                                     pageToken=page_token).execute()
                for file in response.get('files', []):
                    if file.get('mimeType') == 'application/vnd.google-apps.folder':
                        arquivos_encontrados.extend(self.listar_arquivos_backup(file.get('id')))
                    else:
                        arquivos_encontrados.append(file)
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
            except Exception as e:
                self.log(f"❌ Erro ao listar arquivos: {e}")
                break
        return arquivos_encontrados

    def restaurar_arquivos(self, arquivos, pasta_destino_local):
        """Baixa uma lista de arquivos do Drive para uma pasta local."""
        if not self.service and not self.conectar():
            return
        
        self.log(f"Restaurando {len(arquivos)} arquivos para: {pasta_destino_local}")
        for arquivo in arquivos:
            file_id = arquivo['id']
            file_name = arquivo['name']
            caminho_local = os.path.join(pasta_destino_local, file_name)
            
            try:
                self.log(f"⬇️ Baixando: {file_name}...")
                request = self.service.files().get_media(fileId=file_id)
                with open(caminho_local, "wb") as f:
                    downloader = MediaIoBaseDownload(f, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        self.log(f"   Progresso: {int(status.progress() * 100)}%")
                self.log(f"✅ Salvo em: {caminho_local}")
            except Exception as e:
                self.log(f"❌ Erro ao baixar {file_name}: {e}")
        self.log("✅ Restauração Concluída.")