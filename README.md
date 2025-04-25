# Discord Audit Bot

Um bot completo de auditoria para servidores Discord. Ele registra mensagens, arquivos, alterações, ações em canais de voz e muito mais. Os registros são salvos em um canal de texto e enviados diariamente em PDF.

✅ Funciona com ou sem banco de dados MySQL.

---

## 🔍 Funcionalidades

- Log em tempo real de:
  - Mensagens enviadas, editadas e apagadas
  - Arquivos enviados e apagados (com nome, tamanho, tipo)
  - Entradas e saídas do servidor
  - Entrada, saída e troca de canais de voz
  - Mute/desmute e uso do fone
  - Ações AFK
  - Criação/remoção de canais e cargos
  - Alteração de nickname e avatar
  - Banimentos e desbanimentos
- Canal exclusivo para auditoria (ex: `#auditoria`)
- Geração diária de **PDF com resumo de todos os eventos**
- Integração com **banco de dados MySQL (opcional)**:
  - Histórico estruturado
  - Filtragem por usuário, tipo de evento, data

---

## 🚀 Instalação

### 1. Clone o projeto

```bash
git clone https://github.com/seuusuario/discord-audit-bot.git
cd discord-audit-bot
```

### 2. Instale as dependências

Crie um ambiente virtual (opcional) e instale:

```bash
pip install -r requirements.txt
```

### 3. Configure seu bot no Discord

1. Acesse [https://discord.com/developers/applications](https://discord.com/developers/applications)
2. Clique em **New Application** e dê um nome
3. Vá em **Bot** > clique em **Add Bot**
4. Vá em **OAuth2 > URL Generator**
   - Scopes: `bot`
   - Permissions: selecione:
     - View Audit Log
     - Manage Messages
     - Read/Send Messages
     - Manage Channels
     - Ban Members
     - e outras permissões que desejar
5. Gere a URL, cole no navegador e adicione o bot ao seu servidor
6. Copie o **Token** e cole no arquivo `bot.py` na linha:
   ```python
   TOKEN = "SEU_TOKEN_AQUI"
   ```

7. Crie um canal de texto no seu servidor chamado `#auditoria`

---

## 💾 Banco de Dados (opcional)

Se quiser salvar os logs em banco MySQL, configure:

- No `bot.py`, altere:
  ```python
  SALVAR_EM_BANCO = True
  ```
- Preencha as credenciais de conexão em `DB_CONFIG`

### Script SQL:

```sql
CREATE DATABASE IF NOT EXISTS discord_auditoria;
USE discord_auditoria;

CREATE TABLE usuarios (
    id BIGINT PRIMARY KEY,
    nome VARCHAR(100)
);

CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id BIGINT,
    tipo VARCHAR(50),
    data_hora DATETIME NOT NULL,
    mensagem TEXT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

---

## 📝 Logs

- Todos os eventos são enviados em tempo real para o canal `#auditoria`
- Às 20h, um **PDF diário com o resumo** é gerado e enviado automaticamente

---

## ⚙️ Configurações

No arquivo `bot.py`, você pode configurar:

- `TOKEN`: token do seu bot
- `ID_CANAL_LOG`: nome do canal onde serão enviados os logs
- `SALVAR_EM_BANCO`: se `True`, ativa a gravação no banco de dados
- `USUARIOS_RESTRITOS`: lista de IDs com horário de acesso limitado (07h às 20h)

---

## 🤝 Contribuições

Pull requests são bem-vindos! Se tiver sugestões, melhorias ou quiser integrar com outras plataformas (como dashboards, Notion ou Google Sheets), fique à vontade para colaborar.

---

## 📄 Licença

MIT License.

