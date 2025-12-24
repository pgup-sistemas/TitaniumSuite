import os
import hashlib
import shutil
from typing import List, Dict, Tuple

class SystemTools:
    def __init__(self, logger_callback=None):
        self.log = logger_callback if logger_callback else print

    def _hash_file(self, filepath: str, blocksize: int = 65536) -> str:
        """Calcula o hash SHA256 de um arquivo para identificação única."""
        hasher = hashlib.sha256()
        try:
            with open(filepath, 'rb') as afile:
                buf = afile.read(blocksize)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(blocksize)
            return hasher.hexdigest()
        except Exception as e:
            self.log(f"❌ Erro ao calcular hash de {os.path.basename(filepath)}: {e}")
            return None

    def localizar_duplicados(self, diretorio: str) -> Dict[str, List[str]]:
        """
        Localiza arquivos duplicados em um diretório e subdiretórios.
        Retorna um dicionário onde a chave é o hash e o valor é uma lista de caminhos.
        """
        self.log(f"--- Iniciando busca por duplicados em: {diretorio} ---")
        
        hashes: Dict[str, List[str]] = {}
        
        for dirpath, _, filenames in os.walk(diretorio):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                
                # Ignora links simbólicos e arquivos muito pequenos (opcional)
                if not os.path.islink(filepath) and os.path.getsize(filepath) > 1024:
                    file_hash = self._hash_file(filepath)
                    
                    if file_hash:
                        if file_hash in hashes:
                            hashes[file_hash].append(filepath)
                            self.log(f"  -> Duplicado encontrado: {filename}")
                        else:
                            hashes[file_hash] = [filepath]
        
        # Filtra para manter apenas os hashes com mais de um arquivo (os duplicados)
        duplicados = {h: paths for h, paths in hashes.items() if len(paths) > 1}
        
        self.log(f"✅ Busca concluída. {len(duplicados)} grupos de arquivos duplicados encontrados.")
        return duplicados

    def renomear_em_lote(self, lista_arquivos: List[str], prefixo: str = "", sufixo: str = "", numeracao_inicial: int = 1) -> List[Tuple[str, str]]:
        """Renomeia uma lista de arquivos com prefixo, sufixo e numeração."""
        self.log(f"--- Iniciando Renomeação em Lote de {len(lista_arquivos)} arquivos ---")
        
        resultados: List[Tuple[str, str]] = []
        contador = numeracao_inicial
        
        for filepath in lista_arquivos:
            try:
                diretorio = os.path.dirname(filepath)
                nome_original, extensao = os.path.splitext(os.path.basename(filepath))
                
                # Constrói o novo nome
                novo_nome = f"{prefixo}{nome_original}{sufixo}_{contador:03d}{extensao}"
                novo_caminho = os.path.join(diretorio, novo_nome)
                
                # Renomeia o arquivo
                os.rename(filepath, novo_caminho)
                
                self.log(f"  -> Renomeado: {os.path.basename(filepath)} -> {novo_nome}")
                resultados.append((filepath, novo_caminho))
                contador += 1
                
            except Exception as e:
                self.log(f"❌ Erro ao renomear {os.path.basename(filepath)}: {e}")
                resultados.append((filepath, f"ERRO: {e}"))
                
        self.log(f"✅ Renomeação concluída. {len(resultados)} arquivos processados.")
        return resultados

    def organizar_downloads(self, diretorio_origem: str, regras: Dict[str, str], mover: bool = True) -> Dict[str, int]:
        """
        Organiza arquivos em um diretório com base em regras de extensão.
        Regras: {'pdf': 'Documentos/PDFs', 'jpg,png': 'Imagens', '*': 'Outros'}
        """
        self.log(f"--- Iniciando Organização de {diretorio_origem} ---")
        
        extensoes_mapeadas = {}
        for extensoes, pasta in regras.items():
            for ext in extensoes.split(','):
                extensoes_mapeadas[ext.strip().lower()] = pasta
        
        estatisticas = {"total_movidos": 0, "pastas_criadas": 0}
        
        for filename in os.listdir(diretorio_origem):
            filepath = os.path.join(diretorio_origem, filename)
            
            if os.path.isfile(filepath):
                _, ext = os.path.splitext(filename)
                ext = ext.lstrip('.').lower()
                
                pasta_destino_relativa = extensoes_mapeadas.get(ext) or extensoes_mapeadas.get('*')
                
                if pasta_destino_relativa:
                    pasta_destino_absoluta = os.path.join(diretorio_origem, pasta_destino_relativa)
                    
                    if not os.path.exists(pasta_destino_absoluta):
                        os.makedirs(pasta_destino_absoluta)
                        estatisticas["pastas_criadas"] += 1
                        self.log(f"  -> Pasta criada: {pasta_destino_relativa}")
                        
                    novo_caminho = os.path.join(pasta_destino_absoluta, filename)
                    
                    try:
                        if mover:
                            shutil.move(filepath, novo_caminho)
                            self.log(f"  -> Movido: {filename} para {pasta_destino_relativa}")
                        else:
                            shutil.copy2(filepath, novo_caminho)
                            self.log(f"  -> Copiado: {filename} para {pasta_destino_relativa}")
                            
                        estatisticas["total_movidos"] += 1
                        
                    except Exception as e:
                        self.log(f"❌ Erro ao mover/copiar {filename}: {e}")
        
        self.log(f"✅ Organização concluída. {estatisticas['total_movidos']} arquivos movidos/copiados.")
        return estatisticas

    def deletar_arquivos(self, lista_arquivos: List[str]) -> int:
        """Deleta uma lista de arquivos do sistema."""
        self.log(f"--- Iniciando Deleção de {len(lista_arquivos)} arquivos ---")
        
        arquivos_deletados = 0
        for filepath in lista_arquivos:
            try:
                os.remove(filepath)
                self.log(f"  -> Deletado: {filepath}")
                arquivos_deletados += 1
            except Exception as e:
                self.log(f"❌ Erro ao deletar {filepath}: {e}")
                
        self.log(f"✅ Deleção concluída. {arquivos_deletados} arquivos removidos.")
        return arquivos_deletados
