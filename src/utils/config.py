import os
import sys

def resource_path(relative_path):
    """Retorna o caminho absoluto para recursos (imagens/ícones)."""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)