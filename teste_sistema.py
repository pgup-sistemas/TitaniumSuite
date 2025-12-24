#!/usr/bin/env python3
# teste_sistema.py - Script de verificação do Titanium Suite

print("=== VERIFICAÇÃO DO SISTEMA TITANIUM SUITE ===")

# Teste 1: Importações principais
try:
    from src.ui.login_screen import LoginScreen
    from src.ui.main_window import TitaniumApp
    from src.modules.auth import AuthManager
    print("✅ Todas as importações OK")
except Exception as e:
    print(f"❌ Erro nas importações: {e}")
    exit(1)

# Teste 2: Verificação de licença
try:
    auth = AuthManager()
    licenca_ok = auth.verificar_licenca()
    if licenca_ok:
        print("✅ Licença válida")
    else:
        print("❌ Licença inválida")
        exit(1)
except Exception as e:
    print(f"❌ Erro na verificação de licença: {e}")
    exit(1)

# Teste 3: Login teste
try:
    sucesso, role = auth.verificar_login("admin", "admin123")
    if sucesso:
        print(f"✅ Login teste OK - Usuário: {role}")
    else:
        print("❌ Login teste falhou")
        exit(1)
except Exception as e:
    print(f"❌ Erro no login teste: {e}")
    exit(1)

# Teste 4: Dependências
try:
    import customtkinter as ctk
    import qrcode
    import PIL
    import cryptography
    import pyzipper
    import psutil
    print("✅ Todas as dependências OK")
except Exception as e:
    print(f"❌ Erro nas dependências: {e}")
    exit(1)

print("=== SISTEMA PRONTO PARA USO ===")
print("Para executar: python main.py")