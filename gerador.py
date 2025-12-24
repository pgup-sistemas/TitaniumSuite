import hashlib
id_cliente = "E153FE56F9B4354D" # <--- Cole o ID que apareceu na tela
segredo = "TITANIUM_2025_SECRET_KEY"
chave = hashlib.sha256((id_cliente + segredo).encode()).hexdigest()[:20].upper()
print(chave)