import discord
from discord.ext import commands, tasks
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime, time
import mysql.connector

TOKEN = "SEU_TOKEN_AQUI"
ID_CANAL_LOG = "auditoria"
USUARIOS_RESTRITOS = {759112049857999999}
SALVAR_EM_BANCO = False
logs = []
voice_times = {}
afks = {}

DB_CONFIG = {
    'host': 'localhost',
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'database': 'discord_auditoria'
}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

def fora_do_horario():
    agora = datetime.now().time()
    return agora < time(7, 0) or agora > time(20, 0)

def gerar_pdf_log_binario(logs):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setFont("Helvetica", 10)
    c.drawString(50, 800, f"Log de Auditoria - {datetime.now().strftime('%d/%m/%Y')}")
    y = 780
    for log in logs:
        c.drawString(50, y, log)
        y -= 15
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    buffer.seek(0)
    return buffer

def salvar_no_banco(user_id, user_name, tipo, mensagem):
    if not SALVAR_EM_BANCO:
        return
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT IGNORE INTO usuarios (id, nome) VALUES (%s, %s)", (user_id, user_name))
        cursor.execute("""
            INSERT INTO logs (usuario_id, tipo, data_hora, mensagem)
            VALUES (%s, %s, %s, %s)
        """, (user_id, tipo, datetime.now(), mensagem))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    gerar_log_pdf.start()

@bot.event
async def on_member_join(member):
    await logar(f"🟢 {member.name} entrou no servidor.", member.id, member.name, "entrada")

@bot.event
async def on_member_remove(member):
    await logar(f"🔴 {member.name} saiu do servidor.", member.id, member.name, "saida")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id in USUARIOS_RESTRITOS and fora_do_horario():
        await message.channel.send(f"⛔ {message.author.mention}, acesso permitido apenas entre 07h e 20h.")
        return
    if message.attachments:
        for file in message.attachments:
            msg = f"📎 {message.author} enviou arquivo: {file.filename} ({file.size / 1024:.2f} KB) - {file.content_type}"
            await logar(msg, message.author.id, message.author.name, "arquivo", file)
    else:
        msg = f"💬 {message.author} em {message.channel.name}: {message.content}"
        await logar(msg, message.author.id, message.author.name, "mensagem")
    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    msg = f"✏️ {before.author} editou:\nDe: {before.content}\nPara: {after.content}"
    await logar(msg, before.author.id, before.author.name, "edicao")

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    if message.attachments:
        for file in message.attachments:
            msg = f"🗑️ {message.author} apagou arquivo: {file.filename} ({file.size / 1024:.2f} KB) - {file.content_type}"
            await logar(msg, message.author.id, message.author.name, "apagou")
    else:
        msg = f"🗑️ {message.author} apagou: {message.content}"
        await logar(msg, message.author.id, message.author.name, "apagou")

@bot.event
async def on_voice_state_update(member, before, after):
    tipo = "voz"
    if member.id in USUARIOS_RESTRITOS and fora_do_horario():
        if after.channel:
            await member.move_to(None)
            await logar(f"⛔ {member.name} foi removido do canal de voz por estar fora do horário.", member.id, member.name, tipo)
        return
    if before.channel is None and after.channel is not None:
        voice_times[member.id] = datetime.now()
        msg = f"🎙️ {member.name} entrou no canal de voz: {after.channel.name}"
    elif before.channel is not None and after.channel is None:
        entrada = voice_times.pop(member.id, None)
        minutos = round((datetime.now() - entrada).total_seconds() / 60, 1) if entrada else "?"
        msg = f"📴 {member.name} saiu de {before.channel.name} (ficou {minutos} min)"
    elif before.channel != after.channel:
        entrada = voice_times.get(member.id, datetime.now())
        minutos = round((datetime.now() - entrada).total_seconds() / 60, 1)
        voice_times[member.id] = datetime.now()
        msg = f"🔁 {member.name} trocou de canal: {before.channel.name} → {after.channel.name} (ficou {minutos} min)"
    elif before.self_mute != after.self_mute:
        estado = "mutou o microfone" if after.self_mute else "desmutou o microfone"
        msg = f"🎚️ {member.name} {estado}"
    elif before.self_deaf != after.self_deaf:
        estado = "desligou o fone" if after.self_deaf else "ligou o fone"
        msg = f"🎧 {member.name} {estado}"
    elif before.afk != after.afk:
        msg = f"🛌 {member.name} {'foi para AFK' if after.afk else 'voltou do AFK'}"
        if after.afk:
            afks[member.id] = datetime.now()
        else:
            entrada = afks.pop(member.id, None)
            if entrada:
                minutos = round((datetime.now() - entrada).total_seconds() / 60, 1)
                msg += f" (ficou {minutos} min AFK)"
    else:
        return
    await logar(msg, member.id, member.name, tipo)

# Log principal com gravação no canal, lista e banco
async def logar(msg, user_id=0, user_name="", tipo="evento", arquivo=None):
    print(msg)
    logs.append(f"{datetime.now().strftime('%H:%M:%S')} - {msg}")
    salvar_no_banco(user_id, user_name, tipo, msg)
    for guild in bot.guilds:
        canal_log = discord.utils.get(guild.text_channels, name=ID_CANAL_LOG)
        if canal_log:
            if arquivo:
                await canal_log.send(content=msg, file=await arquivo.to_file())
            else:
                await canal_log.send(msg)

@tasks.loop(minutes=1)
async def gerar_log_pdf():
    agora = datetime.now()
    if agora.hour == 20 and agora.minute == 0:
        buffer = gerar_pdf_log_binario(logs)
        arquivo = discord.File(fp=buffer, filename=f"log_{agora.strftime('%Y%m%d')}.pdf")
        for guild in bot.guilds:
            canal_log = discord.utils.get(guild.text_channels, name=ID_CANAL_LOG)
            if canal_log:
                await canal_log.send(content="📄 Log diário em PDF:", file=arquivo)
        logs.clear()

bot.run(TOKEN)
