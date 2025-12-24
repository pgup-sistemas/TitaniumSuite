# main.py - VERSÃO COM ONBOARDING
import customtkinter as ctk
from pathlib import Path
import json
from src.ui.login_screen import LoginScreen
from src.ui.main_window import TitaniumApp

# Variáveis globais de controle
usuario_logado = False

def callback_login_sucesso():
    global usuario_logado
    usuario_logado = True

def verificar_primeira_execucao():
    """Verifica se é a primeira vez que o usuário abre o sistema"""
    config_path = Path("config/onboarding.json")
    
    # Se não existe, é primeira execução
    if not config_path.exists():
        return True
    
    # Se existe, verifica se foi completado
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            return not config.get("first_run_completed", False)
    except:
        return True

def mostrar_onboarding(app_principal):
    """Mostra wizard de primeira execução"""
    from src.ui.onboarding_wizard import OnboardingWizard
    
    wizard = OnboardingWizard(app_principal)
    wizard.focus_force()  # Garante que fica em foco
    wizard.wait_window()  # Bloqueia até finalizar

if __name__ == "__main__":

    while True:
        # 1. Reseta o status
        usuario_logado = False

        # 2. Abre Login
        tela_login = LoginScreen()
        tela_login.abrir_app_principal = callback_login_sucesso
        tela_login.mainloop()

        # 3. Verifica: Se fechou a janela sem logar, encerra o programa de vez
        if not usuario_logado:
            break

        # 4. Se logou, abre o App Principal
        app = TitaniumApp()
        
        # 5. NOVO: Verifica se precisa mostrar onboarding
        if verificar_primeira_execucao():
            # Aguarda a janela renderizar completamente
            app.after(500, lambda: mostrar_onboarding(app))
        
        app.mainloop()

        # 6. Verifica: Se o app fechou, foi Logout ou Fechar (X)?
        if app.logout_acionado:
            print("Logout realizado. Reiniciando ciclo...")
            continue # Volta para o começo do While (Abre Login)
        else:
            print("Aplicativo encerrado pelo usuário.")
            break # Sai do While e encerra o script