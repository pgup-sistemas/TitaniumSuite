# 🛡️ Titanium Suite - Sistema de Segurança Corporativo

## 📋 **Visão Geral**

O Titanium Suite é um **sistema de segurança corporativo completo** desenvolvido em Python com interface moderna CustomTkinter. O sistema oferece ferramentas avançadas de manutenção, segurança, produtividade e backup para empresas e usuários avançados.

## 🚀 **Principais Funcionalidades**

### 🏠 **Dashboard Inteligente**
- **Monitoramento em tempo real** da saúde do sistema
- **Indicadores de performance** (CPU, RAM, Disco)
- **Alertas inteligentes** baseados em métricas reais
- **Estatísticas semanais** de uso e manutenção
- **Sistema de scoring** de saúde (0-100)

### 🧹 **Manutenção Automática**
- **Limpeza de arquivos temporários** inteligente
- **Diagnóstico de rede** (ping, conexão)
- **Otimização de disco** e performance
- **Relatórios detalhados** de operações
- **Agendamento automático** de tarefas

### 🔒 **Segurança Avançada**
- **Criptografia AES-256** militar
- **Cofres de arquivos** (ZIP criptografado)
- **Pacotes compartilháveis** para email (criptografa + descriptografador)
- **Gerenciamento de senhas** seguro
- **Perguntas de segurança** para recuperação
- **Sistema de redefinição** local sem internet

### 📤 **Compartilhamento Seguro** *(NOVO)*
- **Crie pacotes criptografados** para enviar por email
- **Destinatário não precisa** do Titanium Suite
- **Script independente** para descriptografia
- **Suporte a qualquer tipo** de arquivo (PDF, imagens, etc.)
- **Senha personalizada** para cada destinatário

### ⚡ **Produtividade**
- **Gerador de QR Codes** avançado
- **Manipulação de PDFs** (unir, comprimir)
- **Organização automática** de arquivos
- **Ferramentas de otimização** de workflow

### ☁️ **Backup Corporativo**
- **Integração Google Drive** automática
- **Backup incremental** inteligente
- **Sincronização em tempo real**
- **Histórico de versões** completo
- **Restauração fácil** de arquivos

## 🛠️ **Tecnologias Utilizadas**

### **Frontend**
- **CustomTkinter** - Interface gráfica moderna
- **Tooltips inteligentes** - Ajuda contextual
- **Design responsivo** - Layout adaptável
- **Temas profissionais** - Dark/Light mode

### **Backend**
- **Python 3.13+** - Linguagem principal
- **SQLite3** - Banco de dados local
- **psutil** - Monitoramento de sistema
- **psycopg2** - Conexão PostgreSQL (opcional)

### **Segurança**
- **SHA-256** - Hashing de senhas
- **AES-256** - Criptografia de arquivos
- **Sistema de licenciamento** - Ativação profissional
- **Perguntas de segurança** - Recuperação local

### **Cloud**
- **Google Drive API** - Backup na nuvem
- **OAuth 2.0** - Autenticação segura
- **Upload/Download** - Transferência inteligente

## 📦 **Instalação**

### **1. Requisitos**
- Python 3.13+
- Conexão com internet (para dependências)

### **2. Clone e Configuração**
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd TitaniumSuite

# Crie ambiente virtual
python -m venv venv

# Ative ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### **3. Execução**
```bash
# Execute o sistema
python main.py
```

## 🔐 **Sistema de Ativação**

### **Trial Profissional**
- **30 dias gratuitos** com todas as funcionalidades
- **Ativação automática** via chave única
- **Sem necessidade de contato** com suporte

### **Ativação Permanente**
- **Chave de ativação** gerada automaticamente
- **Pagamento online** (cartão, PIX, PayPal)
- **Ativação instantânea** após pagamento

### **Redefinição de Senha Local**
- **Sem email/SMS** - 100% offline
- **Perguntas de segurança** pré-configuradas
- **Autonomia total** do usuário

## 🎨 **Interface do Usuário**

### **Design Profissional**
- **Tooltips contextuais** em todos os elementos
- **Cores temáticas** para feedback visual
- **Ícones intuitivos** com emojis
- **Layout organizado** e responsivo

### **Navegação**
- **Menu lateral** com acesso rápido
- **Abas organizadas** por funcionalidade
- **Dashboard central** com visão geral
- **Console de logs** em tempo real

## 📊 **Monitoramento**

### **Indicadores de Saúde**
- **Espaço em disco** (multiplataforma)
- **Status de backup** automático
- **Arquivos temporários** acumulados
- **Validade da licença** (trial/ativa)

### **Alertas Inteligentes**
- **Sistema crítico** (< 50 pontos)
- **Atenção necessária** (50-70 pontos)
- **Sistema saudável** (> 70 pontos)
- **Ações recomendadas** específicas

## 🔧 **Configuração Avançada**

### **Arquivos de Configuração**
- `config/onboarding.json` - Configurações iniciais
- `config/trial.json` - Controle de trial
- `config/ativacao_profissional.json` - Histórico de ativação
- `database/titanium.db` - Banco de dados de usuários

### **Logs do Sistema**
- `logs/backup_history.json` - Histórico de backups
- `logs/maintenance_history.json` - Histórico de manutenção
- `logs/dashboard_errors.log` - Erros do dashboard

## 🚀 **Deploy Corporativo**

### **Para Empresas**
```bash
# Crie pacote executável
pip install pyinstaller
pyinstaller --onefile --windowed main.py

# Distribua o executável
# O sistema cria ambiente virtual automaticamente
```

### **Para Desenvolvedores**
```bash
# Ambiente de desenvolvimento
python -m venv dev-env
source dev-env/bin/activate  # Linux/Mac
dev-env\Scripts\activate     # Windows

# Instale dependências de desenvolvimento
pip install -r requirements-dev.txt
```

## 📈 **Métricas de Performance**

### **Tempo de Resposta**
- **Dashboard**: Atualização inteligente (10s-60s)
- **Criptografia**: Processamento paralelo
- **Backup**: Upload em chunks
- **Interface**: Renderização otimizada

### **Uso de Recursos**
- **CPU**: < 5% em modo idle
- **Memória**: < 100MB base
- **Disco**: Logs rotativos (1MB máximo)
- **Rede**: Conexões eficientes

## 🛡️ **Segurança**

### **Proteção de Dados**
- **Criptografia AES-256** para arquivos sensíveis
- **Hashing SHA-256** para senhas
- **Armazenamento seguro** de credenciais
- **Isolamento de processos** críticos

### **Compartilhamento Seguro por Email** *(NOVO)*
O Titanium Suite agora permite criar **pacotes compartilháveis** que podem ser enviados por email de forma segura:

```
1. Criptografe qualquer arquivo (PDF, imagem, etc.)
2. Vá em Segurança → aba "📤 Compartilhar"
3. Selecione o arquivo .enc e defina uma senha para o destinatário
4. O sistema cria um ZIP com:
   - Arquivo criptografado (.enc)
   - Script descriptografar.py
   - Batch descriptografar.bat (Windows)
   - Instruções LEIA-ME.txt
```

**Para o destinatário:**
- Execute `descriptografar.bat` (Windows)
- O arquivo é restaurado automaticamente
- Não precisa do Titanium Suite instalado!

### **Privacidade**
- **Zero coleta** de dados pessoais
- **Processamento local** (sem upload não autorizado)
- **Controle total** do usuário sobre seus dados
- **Compliance** com LGPD/GDPR

## 📞 **Suporte**

### **Documentação**
- `INSTRUCOES_EXECUCAO.md` - Guia completo de uso
- `GUIA_ATIVACAO_PROFISSIONAL.md` - Sistema de ativação
- `SISTEMA_REDEFINIR_SENHA.md` - Sistema de segurança
- `CORRECOES_ONBOARDING.md` - Onboarding wizard

### **Contato**
- **Email**: contato@titanium.com
- **Site**: www.titanium.com.br
- **Documentação**: docs.titanium.com.br

## 🎯 **Roadmap**

### **Versão 2.1 (Próximo)**
- [ ] **Integração Active Directory**
- [ ] **Relatórios PDF** avançados
- [ ] **API REST** para integração
- [ ] **Multi-usuário** avançado

### **Versão 3.0 (Futuro)**
- [ ] **IA para diagnósticos**
- [ ] **Dashboard web** remoto
- [ ] **Mobile app** de monitoramento
- [ ] **Blockchain** para auditoria

## 📄 **Licença**

Este projeto está licenciado sob a licença **MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 **Contribuição**

Contribuições são bem-vindas! Por favor, siga estas etapas:

1. **Fork** o projeto
2. Crie uma **branch** (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um **Pull Request**

---

**Titanium Suite** - Segurança Corporativa com Excelência Tecnológica 🛡️