from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from openai import OpenAI

TELEGRAM_TOKEN = "8569708146:AAGduSsoHtUINOU2qB26rwjHjS2JyreRcSc"
OPENAI_API_KEY = "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"


client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- ฟังก์ชันแปล ----------
async def translate_text(update: Update, target_lang: str, text: str):
    prompt = f"""
ตรวจจับภาษา และแปลข้อความต่อไปนี้เป็น {target_lang}
ข้อความ:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "คุณคือผู้ช่วยแปลภาษาอย่างมืออาชีพ"},
            {"role": "user", "content": prompt}
        ]
    )
    await update.message.reply_text(
        response.choices[0].message.content.strip()
    )

# ---------- คำสั่ง ----------
async def th(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await translate_text(update, "ภาษาไทย", " ".join(context.args))

async def en(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await translate_text(update, "ภาษาอังกฤษ", " ".join(context.args))

async def cn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await translate_text(update, "ภาษาจีน", " ".join(context.args))

# ---------- แปลอัตโนมัติ ----------
async def auto_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await translate_text(update, "ภาษาไทย", update.message.text)

# ---------- main ----------
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("th", th))
app.add_handler(CommandHandler("en", en))
app.add_handler(CommandHandler("cn", cn))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_translate))

print("🤖 Bot is running 24/7 ready...")
app.run_polling()
