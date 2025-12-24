#!/usr/bin/env python3
# teste_onboarding.py - Teste do sistema de onboarding

import customtkinter as ctk
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def testar_onboarding():
    """Testa o funcionamento do onboarding wizard"""
    print("🧪 TESTANDO SISTEMA DE ONBOARDING")
    print("=" * 50)
    
    # Teste 1: Importações
    try:
        from ui.onboarding_wizard import OnboardingWizard
        print("✅ Importação do OnboardingWizard: OK")
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return False
    
    # Teste 2: Criação da interface
    try:
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        root = ctk.CTk()
        root.title("Teste Onboarding")
        root.geometry("400x300")
        
        def abrir_onboarding():
            wizard = OnboardingWizard(root)
            wizard.focus_force()
        
        # Botão para abrir onboarding
        btn_test = ctk.CTkButton(
            root,
            text="🚀 Testar Onboarding Wizard",
            command=abrir_onboarding,
            width=200,
            height=50,
            font=("Arial", 14, "bold")
        )
        btn_test.pack(expand=True)
        
        # Instruções
        lbl_instrucoes = ctk.CTkLabel(
            root,
            text="Clique no botão para testar o onboarding\nVerifique se os botões aparecem corretamente",
            font=("Arial", 12)
        )
        lbl_instrucoes.pack(pady=20)
        
        print("✅ Interface de teste criada")
        print("📝 INSTRUÇÕES:")
        print("1. Clique no botão 'Testar Onboarding Wizard'")
        print("2. Verifique se a janela do onboarding abre")
        print("3. Teste os botões: Voltar, Pular, Continuar")
        print("4. Navegue pelas etapas")
        print("5. Feche a janela para encerrar o teste")
        
        root.mainloop()
        
        print("✅ Teste concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    testar_onboarding()
