# 🚀 COMANDOS PARA UPLOAD NO GIT

## 📋 **Preparação para Upload**

### **1. Verifique o Status Atual**
```bash
# Verifique arquivos modificados
git status

# Veja diferenças
git diff

# Liste arquivos para commit
git ls-files --others --exclude-standard
```

### **2. Adicione Arquivos ao Staging**
```bash
# Adicione todos os arquivos relevantes
git add .

# Ou adicione seletivamente (recomendado)
git add main.py
git add requirements.txt
git add README.md
git add VERSION.md
git add .gitignore
git add src/
git add config/
git add logs/
git add database/
```

### **3. Faça o Primeiro Commit**
```bash
# Commit inicial
git commit -m "🚀 Versão 2.0.0 - Corporate Edition

✨ Principais Features:
- Dashboard inteligente com monitoramento em tempo real
- Sistema de segurança profissional com criptografia AES-256
- Manutenção automática inteligente
- Backup corporativo com Google Drive
- Redefinição de senha local sem internet
- Interface profissional com tooltips contextuais
- Sistema de ativação trial + profissional
- Arquitetura modular e escalável

🔧 Melhorias Técnicas:
- Performance otimizada (CPU < 5%, RAM < 100MB)
- Tratamento completo de erros e exceções
- Compatibilidade multiplataforma (Windows/Linux/Mac)
- Sistema de logs detalhado e organizado
- Segurança robusta com criptografia militar

🎯 Impacto:
- Transformação completa de protótipo para sistema corporativo
- Qualidade enterprise com padrões industriais
- Pronto para deploy em ambiente empresarial
- Escalável para milhares de usuários"
```

## 🌐 **Configuração do Repositório Remoto**

### **1. Crie Repositório no GitHub/GitLab**
- Acesse github.com ou gitlab.com
- Crie novo repositório (ex: TitaniumSuite)
- Copie a URL do repositório

### **2. Configure Remote**
```bash
# Adicione remote (substitua <URL> pela URL do seu repositório)
git remote add origin <URL>

# Verifique remote
git remote -v
```

### **3. Primeiro Push**
```bash
# Force push inicial (se necessário)
git push -u origin main --force

# Ou push normal
git push -u origin main
```

## 🏷️ **Criação de Tags e Releases**

### **1. Crie Tag de Versão**
```bash
# Crie tag anotada
git tag -a v2.0.0 -m "🚀 Versão 2.0.0 - Corporate Edition"

# Envie tag para remote
git push origin v2.0.0
```

### **2. Crie Release no GitHub**
```bash
# Se usar GitHub CLI
gh release create v2.0.0 --title "🚀 Versão 2.0.0 - Corporate Edition" --notes "Release completa com todas as funcionalidades corporativas"
```

## 🔄 **Comandos Diários de Git**

### **1. Verificação Diária**
```bash
# Verifique status
git status

# Veja commits recentes
git log --oneline -5

# Verifique branches
git branch -a
```

### **2. Fluxo de Trabalho**
```bash
# Atualize repositório
git pull origin main

# Faça suas alterações
# ... edição de arquivos ...

# Adicione alterações
git add .

# Commit suas alterações
git commit -m "feat: descrição da funcionalidade"

# Envie para remote
git push origin main
```

### **3. Gerenciamento de Branches**
```bash
# Crie nova branch
git checkout -b feature/nova-funcionalidade

# Liste branches
git branch

# Mude de branch
git checkout main

# Merge de branch
git merge feature/nova-funcionalidade

# Delete branch local
git branch -d feature/nova-funcionalidade

# Delete branch remote
git push origin --delete feature/nova-funcionalidade
```

## 📊 **Comandos de Análise**

### **1. Estatísticas do Projeto**
```bash
# Estatísticas de commits
git shortlog -sn

# Estatísticas de código
git log --stat

# Tamanho do repositório
du -sh .git
```

### **2. Histórico e Diferenças**
```bash
# Histórico detalhado
git log --graph --oneline --all

# Diferenças entre commits
git diff commit1..commit2

# Diferenças para próximo commit
git diff HEAD
```

## 🛠️ **Comandos de Manutenção**

### **1. Limpeza**
```bash
# Limpe arquivos não rastreados
git clean -fd

# Verifique integridade
git fsck

# Compacte repositório
git gc --aggressive
```

### **2. Recuperação**
```bash
# Desfaça último commit (mantendo alterações)
git reset --soft HEAD~1

# Desfaça alterações não commitadas
git checkout -- nome_do_arquivo

# Recupere arquivo de commit específico
git checkout commit_hash -- nome_do_arquivo
```

## 🚨 **Problemas Comuns e Soluções**

### **1. Conflitos de Merge**
```bash
# Resolva conflitos manualmente
# Edite arquivos com conflitos
git add arquivo_resolvido
git commit
```

### **2. Push Rejeitado**
```bash
# Se houver commits remotos
git pull --rebase origin main
git push origin main
```

### **3. Arquivo Sensível no Git**
```bash
# Remova do histórico (se necessário)
git filter-branch --tree-filter 'rm -f senha.txt' HEAD
git push origin --force --all
```

## 📋 **Checklist de Upload**

### **✅ Pré-Upload**
- [ ] Verifique `.gitignore` está correto
- [ ] Remova arquivos sensíveis (senhas, chaves)
- [ ] Teste o sistema localmente
- [ ] Atualize documentação
- [ ] Crie mensagem de commit clara

### **✅ Upload**
- [ ] Adicione arquivos ao staging
- [ ] Faça commit com mensagem descritiva
- [ ] Configure remote corretamente
- [ ] Faça push para o repositório
- [ ] Crie tag de versão

### **✅ Pós-Upload**
- [ ] Verifique repositório online
- [ ] Crie release (se aplicável)
- [ ] Atualize documentação do repositório
- [ ] Compartilhe URL do repositório
- [ ] Teste clone em ambiente limpo

## 🎯 **Comandos Rápidos**

### **Upload Completo (1 comando)**
```bash
git add . && git commit -m "🚀 Versão 2.0.0 - Corporate Edition" && git push -u origin main
```

### **Status Rápido**
```bash
git status && git diff --stat
```

### **Pull com Rebase**
```bash
git pull --rebase origin main
```

### **Tag e Push**
```bash
git tag -a v2.0.0 -m "Corporate Edition" && git push origin v2.0.0
```

---

**Pronto para upload! 🚀** O Titanium Suite está configurado para versionamento profissional no Git.