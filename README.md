
# Discord Audit Bot

A complete audit bot for Discord servers. It logs messages, files, changes, voice channel actions, and much more. Logs are saved in a text channel and sent daily in PDF format.

✅ Works with or without a MySQL database.

---

## 🔍 Features

- Real-time logging of:
  - Sent, edited, and deleted messages  
  - Uploaded and deleted files (with name, size, type)  
  - Server joins and leaves  
  - Voice channel joins, leaves, and switches  
  - Mute/unmute and headphone usage  
  - AFK actions  
  - Channel and role creation/removal  
  - Nickname and avatar changes  
  - Bans and unbans  
- Dedicated audit channel (e.g. `#audit`)  
- Daily **PDF report summarizing all events**  
- **MySQL database integration (optional)**:
  - Structured history
  - Filtering by user, event type, date

---

## 🚀 Installation

### 1. Clone the project

```bash
git clone https://github.com/youruser/discord-audit-bot.git
cd discord-audit-bot
```

### 2. Install dependencies

Create a virtual environment (optional) and install:

```bash
pip install -r requirements.txt
```

### 3. Set up your bot on Discord

1. Go to [https://discord.com/developers/applications](https://discord.com/developers/applications)  
2. Click **New Application** and give it a name  
3. Go to **Bot** > click **Add Bot**  
4. Go to **OAuth2 > URL Generator**
   - Scopes: `bot`
   - Permissions: select:
     - View Audit Log  
     - Manage Messages  
     - Read/Send Messages  
     - Manage Channels  
     - Ban Members  
     - And any other permissions needed  
5. Generate the URL, paste it in your browser, and add the bot to your server  
6. Copy the **Token** and paste it into the `bot.py` file on the line:
   ```python
   TOKEN = "YOUR_TOKEN_HERE"
   ```
7. Create a text channel in your server called `#audit`

---

## 💾 Database (optional)

To store logs in a MySQL database, configure as follows:

- In `bot.py`, set:
  ```python
  SAVE_TO_DATABASE = True
  ```
- Fill in the connection credentials in `DB_CONFIG`

### SQL Script:

```sql
CREATE DATABASE IF NOT EXISTS discord_audit;
USE discord_audit;

CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    type VARCHAR(50),
    timestamp DATETIME NOT NULL,
    message TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 📝 Logs

- All events are sent in real-time to the `#audit` channel  
- At 8:00 PM, a **daily PDF summary** is automatically generated and sent

---

## ⚙️ Settings

In the `bot.py` file, you can configure:

- `TOKEN`: your bot’s token  
- `LOG_CHANNEL_ID`: name of the channel where logs will be sent  
- `SAVE_TO_DATABASE`: if `True`, enables database logging  
- `RESTRICTED_USERS`: list of user IDs with limited access time (7:00 AM to 8:00 PM)

---

## 🤝 Contributions

Pull requests are welcome! If you have suggestions, improvements, or want to integrate with other platforms (like dashboards, Notion, or Google Sheets), feel free to contribute.

---

## 📄 License

MIT License.
