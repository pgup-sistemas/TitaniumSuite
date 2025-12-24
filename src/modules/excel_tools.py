import pandas as pd
import os
import json

class ExcelTools:
    def __init__(self, logger_callback=None):
        self.log = logger_callback if logger_callback else print

    def unir_planilhas(self, lista_arquivos, arquivo_saida, nome_aba_especifica=None):
        """
        Une múltiplas planilhas Excel em um único arquivo.
        Se nome_aba_especifica for fornecido, une apenas essa aba de cada arquivo.
        """
        self.log(f"--- Iniciando Fusão de {len(lista_arquivos)} arquivos Excel ---")
        
        try:
            writer = pd.ExcelWriter(arquivo_saida, engine='xlsxwriter')
            
            for arquivo in lista_arquivos:
                self.log(f"Processando: {os.path.basename(arquivo)}")
                
                # Lê todas as abas do arquivo
                xls = pd.ExcelFile(arquivo)
                sheet_names = xls.sheet_names
                
                if nome_aba_especifica:
                    # Se for para unir uma aba específica, verifica se ela existe
                    if nome_aba_especifica in sheet_names:
                        df = pd.read_excel(xls, sheet_name=nome_aba_especifica)
                        # Salva a aba no arquivo de saída, nomeando-a com o nome do arquivo original
                        df.to_excel(writer, sheet_name=os.path.basename(arquivo)[:30], index=False)
                        self.log(f"  -> Aba '{nome_aba_especifica}' unida.")
                    else:
                        self.log(f"  -> Aviso: Aba '{nome_aba_especifica}' não encontrada em {os.path.basename(arquivo)}. Pulando.")
                else:
                    # Une todas as abas
                    for sheet_name in sheet_names:
                        df = pd.read_excel(xls, sheet_name=sheet_name)
                        # Salva a aba no arquivo de saída, nomeando-a com o nome do arquivo original + nome da aba
                        new_sheet_name = f"{os.path.basename(arquivo)[:15]}_{sheet_name[:10]}"
                        df.to_excel(writer, sheet_name=new_sheet_name, index=False)
                        self.log(f"  -> Aba '{sheet_name}' unida.")

            writer.close()
            self.log(f"✅ Sucesso! Arquivo salvo em: {arquivo_saida}")
            return True
        except Exception as e:
            self.log(f"❌ Erro ao unir planilhas: {e}")
            return False

    def remover_duplicadas(self, arquivo_entrada, arquivo_saida, colunas_criterio):
        """Remove linhas duplicadas de uma planilha Excel com base em colunas específicas."""
        self.log(f"--- Removendo duplicadas de {os.path.basename(arquivo_entrada)} ---")
        
        try:
            # Lê a primeira aba do arquivo
            df = pd.read_excel(arquivo_entrada)
            
            # Converte a string de colunas em uma lista
            criterios = [c.strip() for c in colunas_criterio.split(',') if c.strip()]
            
            if not criterios:
                self.log("⚠️ Aviso: Nenhum critério de coluna fornecido. Removendo duplicadas de todas as colunas.")
                df_limpo = df.drop_duplicates()
            else:
                # Verifica se as colunas existem
                colunas_invalidas = [c for c in criterios if c not in df.columns]
                if colunas_invalidas:
                    self.log(f"❌ Erro: Colunas não encontradas: {', '.join(colunas_invalidas)}")
                    return False
                
                df_limpo = df.drop_duplicates(subset=criterios)
            
            linhas_removidas = len(df) - len(df_limpo)
            
            # Salva o resultado no arquivo de saída
            df_limpo.to_excel(arquivo_saida, index=False)
            
            self.log(f"✅ Sucesso! {linhas_removidas} linhas duplicadas removidas. Salvo em: {arquivo_saida}")
            return True
        except Exception as e:
            self.log(f"❌ Erro ao remover duplicadas: {e}")
            return False

    def converter_para_csv_json(self, arquivo_entrada, arquivo_saida, formato_saida):
        """Converte a primeira aba de um arquivo Excel para CSV ou JSON."""
        self.log(f"--- Convertendo {os.path.basename(arquivo_entrada)} para {formato_saida.upper()} ---")
        
        try:
            # Lê a primeira aba do arquivo
            df = pd.read_excel(arquivo_entrada)
            
            if formato_saida.lower() == 'csv':
                df.to_csv(arquivo_saida, index=False)
            elif formato_saida.lower() == 'json':
                # Salva como JSON no formato 'records' (lista de objetos)
                df.to_json(arquivo_saida, orient='records', indent=4)
            else:
                self.log(f"❌ Erro: Formato de saída '{formato_saida}' não suportado.")
                return False
            
            self.log(f"✅ Sucesso! Arquivo salvo em: {arquivo_saida}")
            return True
        except Exception as e:
            self.log(f"❌ Erro ao converter arquivo: {e}")
            return False
