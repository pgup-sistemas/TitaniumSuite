#!/usr/bin/env python3
# gerador_profissional.py - GERADOR DE CHAVES PROFISSIONAIS
# 
# ESTE ARQUIVO É PARA USO EXCLUSIVO DO DESENVOLVEDOR
# Use este script para gerar chaves de ativação para clientes

import hashlib
import uuid
import os
import json
from datetime import datetime

class GeradorProfissional:
    def __init__(self):
        self.segredo_master = "TITANIUM_PRO_2025_MASTER_SECRET"
        self.chaves_geradas = []
    
    def gerar_chave_cliente(self, id_cliente=None, nome_cliente=None, email=None):
        """
        Gera chave profissional para cliente específico
        
        Args:
            id_cliente: ID único do cliente (opcional)
            nome_cliente: Nome do cliente (opcional)
            email: Email do cliente (opcional)
        
        Returns:
            dict com informações da chave gerada
        """
        if not id_cliente:
            id_cliente = str(uuid.uuid4())[:8].upper()
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Gera chave única
        dados_chave = f"{id_cliente}_{timestamp}_{self.segredo_master}"
        chave = hashlib.sha256(dados_chave.encode()).hexdigest()[:24].upper()
        
        # Informações da chave
        info_chave = {
            "chave": chave,
            "id_cliente": id_cliente,
            "nome_cliente": nome_cliente or "Cliente",
            "email": email or "",
            "data_geracao": datetime.now().isoformat(),
            "timestamp": timestamp,
            "validade": "Permanente",  # Ou defina período específico
            "tipo": "PROFISSIONAL",
            "status": "GERADA"
        }
        
        # Salva histórico
        self._salvar_historico(info_chave)
        
        return info_chave
    
    def _salvar_historico(self, info_chave):
        """Salva histórico das chaves geradas"""
        os.makedirs("config", exist_ok=True)
        arquivo_historico = "config/historico_chaves.json"
        
        try:
            if os.path.exists(arquivo_historico):
                with open(arquivo_historico, "r", encoding="utf-8") as f:
                    historico = json.load(f)
            else:
                historico = []
        except:
            historico = []
        
        historico.append(info_chave)
        
        with open(arquivo_historico, "w", encoding="utf-8") as f:
            json.dump(historico, f, indent=2, ensure_ascii=False)
    
    def validar_chave(self, chave):
        """
        Valida se uma chave é válida
        
        Args:
            chave: Chave para validar
        
        Returns:
            dict com informações de validação
        """
        arquivo_historico = "config/historico_chaves.json"
        
        if not os.path.exists(arquivo_historico):
            return {"valida": False, "motivo": "Histórico não encontrado"}
        
        try:
            with open(arquivo_historico, "r", encoding="utf-8") as f:
                historico = json.load(f)
            
            for item in historico:
                if item["chave"] == chave.upper() and item["status"] == "GERADA":
                    return {
                        "valida": True, 
                        "cliente": item["nome_cliente"],
                        "data_geracao": item["data_geracao"],
                        "info": item
                    }
            
            return {"valida": False, "motivo": "Chave não encontrada ou já utilizada"}
        except:
            return {"valida": False, "motivo": "Erro ao validar"}
    
    def marcar_chave_usada(self, chave):
        """Marca uma chave como usada/ativada"""
        arquivo_historico = "config/historico_chaves.json"
        
        try:
            with open(arquivo_historico, "r", encoding="utf-8") as f:
                historico = json.load(f)
            
            for item in historico:
                if item["chave"] == chave.upper():
                    item["status"] = "USADA"
                    item["data_uso"] = datetime.now().isoformat()
                    break
            
            with open(arquivo_historico, "w", encoding="utf-8") as f:
                json.dump(historico, f, indent=2, ensure_ascii=False)
            
            return True
        except:
            return False

def main():
    print("=" * 60)
    print("🔐 GERADOR DE CHAVES PROFISSIONAIS - TITANIUM SUITE")
    print("=" * 60)
    
    gerador = GeradorProfissional()
    
    while True:
        print("\\n📋 OPÇÕES:")
        print("1. Gerar nova chave para cliente")
        print("2. Validar chave existente")
        print("3. Ver histórico de chaves")
        print("4. Sair")
        
        opcao = input("\\n👉 Escolha uma opção (1-4): ").strip()
        
        if opcao == "1":
            print("\\n--- GERAR NOVA CHAVE ---")
            nome = input("Nome do cliente (opcional): ").strip()
            email = input("Email do cliente (opcional): ").strip()
            
            info = gerador.gerar_chave_cliente(nome_cliente=nome, email=email)
            
            print("\\n✅ CHAVE GERADA COM SUCESSO!")
            print(f"🔑 Chave: {info['chave']}")
            print(f"👤 Cliente: {info['nome_cliente']}")
            print(f"📅 Data: {info['data_geracao']}")
            print(f"📧 Email: {info['email']}")
            
            # Salva em arquivo
            with open(f"chave_{info['id_cliente']}.txt", "w") as f:
                f.write(f"TITANIUM SUITE - CHAVE DE ATIVAÇÃO\\n")
                f.write(f"Cliente: {info['nome_cliente']}\\n")
                f.write(f"Chave: {info['chave']}\\n")
                f.write(f"Data: {info['data_geracao']}\\n")
                f.write(f"\\nPara ativar: Cole esta chave no campo de ativação do software.\\n")
            
            print(f"📁 Chave salva em: chave_{info['id_cliente']}.txt")
        
        elif opcao == "2":
            print("\\n--- VALIDAR CHAVE ---")
            chave = input("Digite a chave para validar: ").strip()
            
            resultado = gerador.validar_chave(chave)
            
            if resultado["valida"]:
                print("\\n✅ CHAVE VÁLIDA!")
                print(f"Cliente: {resultado['cliente']}")
                print(f"Data de geração: {resultado['data_geracao']}")
            else:
                print(f"\\n❌ CHAVE INVÁLIDA: {resultado['motivo']}")
        
        elif opcao == "3":
            print("\\n--- HISTÓRICO DE CHAVES ---")
            arquivo = "config/historico_chaves.json"
            if os.path.exists(arquivo):
                with open(arquivo, "r", encoding="utf-8") as f:
                    historico = json.load(f)
                
                print(f"\\n📊 Total de chaves: {len(historico)}")
                for i, item in enumerate(historico[-5:], 1):  # Mostra últimas 5
                    print(f"{i}. {item['chave']} - {item['nome_cliente']} - {item['status']}")
            else:
                print("Nenhuma chave gerada ainda.")
        
        elif opcao == "4":
            print("\\n👋 Encerrando gerador...")
            break
        
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()
