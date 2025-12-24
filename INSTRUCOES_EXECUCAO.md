# 🚀 INSTRUÇÕES DE EXECUÇÃO - TITANIUM SUITE

## ✅ Status do Sistema
- **Ambiente Virtual**: Criado e configurado
- **Dependencies**: Instaladas com sucesso
- **Licença**: Ativada (B143395F87180D3B63FD)
- **Banco de Dados**: Configurado
- **Configurações**: Prontas

## 🔧 Como Executar

### Método 1: Script de Ativação (Recomendado)
```bash
# Ativa o ambiente virtual automaticamente
activate_venv.bat

# Depois execute:
python main.py
```

### Método 2: Manual
```bash
# 1. Ativar ambiente virtual
venv\Scripts\activate

# 2. Executar o programa
python main.py
```

## 🔑 Sistema de Ativação Profissional

### 🆓 **Trial de 30 Dias**
- **Primeira execução**: Sistema inicia automaticamente 30 dias de trial
- **Funcionalidades**: Todas liberadas durante o trial
- **Interface**: Mostra dias restantes e data de expiração

### 🚀 **Ativação Profissional**
- **Geração automática**: Sistema gera chave única para cada computador
- **Ativação online**: Cliente ativa via www.titanium.com.br/ativar
- **Pagamento**: Cartão de crédito, PIX ou PayPal
- **Ativação instantânea**: Após pagamento, chave ativada é fornecida

### 🔐 **Para Desenvolvedor**
- **Gerador manual**: `python gerador_profissional.py`
- **Controle total**: Histórico de chaves e validação
- **Interface profissional**: Controle de vendas e ativações

### 🔑 **Redefinição de Senha Local**
- **Esqueci senha**: Link na tela de login ("🔑 Esqueci minha senha")
- **Pergunta de segurança**: 10 perguntas predefinidas + personalizada
- **Processo local**: Sem email/SMS, 100% offline
- **Autonomia total**: Usuário resolve sem suporte
- **Configuração**: Via dashboard ("🛡️ Configurar Segurança")

## 👤 **Credenciais de Acesso (após ativação)**
- **Usuário**: `admin`
- **Senha**: `admin123`

## 📋 Fluxo do Sistema
1. **Tela de Login** - Autenticação com usuário/senha
2. **Dashboard Principal** - Visão geral do sistema
3. **Módulos Disponíveis**:
   - 🏠 Dashboard
   - 🧹 Manutenção
   - ⚡ Produtividade
   - 🔒 Segurança
   - ☁️ Backup Nuvem

## 🛠️ Funcionalidades Principais

### Dashboard 🏠
- Monitoramento de saúde do sistema
- Estatísticas de uso
- Alertas e recomendações
- **✨ TOOLTIPS**: Dicas contextuais em todos os cards

### Manutenção 🧹
- Limpeza de arquivos temporários
- Diagnóstico de rede
- Otimização do sistema
- **✨ TOOLTIPS**: Orientações detalhadas para cada função
- **✨ ÍCONES**: Visual intuitivo com emojis

### Produtividade ⚡
- Geração de QR Codes
- Manipulação de PDFs
- Ferramentas de organização
- **✨ TOOLTIPS**: Instruções claras para cada ferramenta
- **✨ INTERFACE**: Abas organizadas e profissionais

### Segurança 🔒
- Criptografia AES-256
- Cofre de arquivos (ZIP criptografado)
- **✨ NOVÃO: Compartilhamento Seguro por Email**
- **✨ TOOLTIPS**: Alertas de segurança e instruções
- **✨ CONFIRMAÇÕES**: Avisos para operações críticas

### Backup Nuvem ☁️
- Integração com Google Drive
- Backup automático
- Sincronização de dados
- **✨ TOOLTIPS**: Guias passo a passo para configuração
- **✨ FEEDBACK**: Status em tempo real das operações

## 🔧 Solução de Problemas

### Se o sistema não carregar:
1. Verificar se o ambiente virtual está ativo `(venv)`
2. Confirmar que a licença está presente (`license.key`)
3. Verificar se as dependências estão instaladas

### Se houver erro de importação:
```bash
# Reinstalar dependências
pip install -r requirements.txt
```

### Para regenerar licença:
```bash
python gerador.py
```

## 📁 Estrutura de Arquivos Importantes
- `main.py` - Arquivo principal
- `license.key` - Chave de licença ativada
- `config/onboarding.json` - Configuração de onboarding
- `config/trial.json` - Controle de trial de 30 dias
- `config/ativacao_profissional.json` - Histórico de ativação
- `config/historico_chaves.json` - Histórico do desenvolvedor
- `database/titanium.db` - Banco de dados de usuários
- `activate_venv.bat` - Script de ativação do ambiente
- `gerador_profissional.py` - Gerador de chaves para desenvolvedor
- `GUIA_ATIVACAO_PROFISSIONAL.md` - Documentação completa do sistema
- `SISTEMA_REDEFINIR_SENHA.md` - Documentação do sistema de redefinição
- `src/ui/redifinir_senha_screen.py` - Tela de redefinição de senha
- `src/ui/configurar_seguranca_screen.py` - Tela de configuração de segurança
- `src/ui/onboarding_wizard.py` - Wizard de onboarding (botões corrigidos)
- `teste_onboarding.py` - Script de teste do onboarding
- `CORRECOES_ONBOARDING.md` - Documentação das correções

## ✨ NOVIDADES IMPLEMENTADAS

### 🎯 Sistema de Tooltips
- **Dicas contextuais** em todos os botões e elementos principais
- **Orientações passo a passo** para operações complexas
- **Alertas de segurança** para ações críticas
- **Interface autoexplicativa** que reduz necessidade de treinamento

### 🎨 Melhorias Visuais
- **Ícones intuitivos** com emojis para melhor identificação
- **Cores temáticas** para feedback visual claro
- **Cards organizados** com separação visual profissional
- **Estados dinâmicos** dos botões (habilitado/desabilitado)

### 📤 Compartilhamento Seguro por Email *(NOVO)*
- **Crie pacotes criptografados** para enviar por email
- **Destinatário não precisa** do Titanium Suite
- **Como usar:**
  1. Vá em **Segurança → aba "📤 Compartilhar"**
  2. Selecione um arquivo .enc já criptografado
  3. Defina a senha que o destinatário usará
  4. Clique em **CRIAR PACOTE PARA COMPARTILHAR**
- **O pacote inclui:**
  - Arquivo criptografado (.enc)
  - Script `descriptografar.py` (funciona em qualquer computador com Python)
  - Batch `descriptografar.bat` (Windows - executa automaticamente)
  - Instruções `LEIA-ME.txt`
- **Para o destinatário:**
  - Execute `descriptografar.bat`
  - O arquivo é restaurado automaticamente
  - Não precisa ter o Titanium Suite instalado!

### 📊 Interface Profissional
- **Grid responsivo** que se adapta ao tamanho da tela
- **Abas organizadas** para navegação intuitiva
- **Console de logs** com feedback em tempo real
- **Confirmações** para operações importantes

## 🎯 Sistema Pronto para Uso!
Todos os componentes estão configurados, tooltips implementados e o sistema está pronto para execução profissional.