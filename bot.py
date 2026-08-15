import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise SystemExit("[ERROR] Не задан BOT_TOKEN. Скопируйте .env.example в .env и впишите токен от @BotFather.")

# ID групп через запятую в переменной ALLOWED_CHAT_IDS. Пусто = работать везде.
ALLOWED_CHAT_IDS = [int(x) for x in os.environ.get("ALLOWED_CHAT_IDS", "").replace(" ", "").split(",") if x]
VOICE_FOLDER = "voices"

async def send_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = [f for f in os.listdir(VOICE_FOLDER) if f.endswith(".ogg")]
    if not files:
        print("[LOG] Нет файлов для отправки.")
        await update.message.reply_text("Нет голосовых файлов для отправки.")
        return

    voice_file = random.choice(files)
    voice_path = os.path.join(VOICE_FOLDER, voice_file)
    print(f"[LOG] Отправляем файл: {voice_file}")

    with open(voice_path, "rb") as voice:
        await context.bot.send_voice(chat_id=update.message.chat_id, voice=voice)

async def handle_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[LOG] Получено сообщение: '{update.message.text}' в чате ID: {update.message.chat_id}")

    if ALLOWED_CHAT_IDS and update.message.chat_id not in ALLOWED_CHAT_IDS:
        print(f"[LOG] Сообщение из другого чата ({update.message.chat_id}), игнорируем.")
        return

    bot_username = (await context.bot.get_me()).username
    print(f"[LOG] Имя бота: @{bot_username}")

    if update.message.entities:
        mentions = [entity for entity in update.message.entities if entity.type == "mention"]
        if any(update.message.text[entity.offset:entity.offset + entity.length] == f"@{bot_username}" for entity in mentions):
            print("[LOG] Бот упомянут! Отправляем голосовое сообщение.")
            await send_voice_message(update, context)
            return
    print("[LOG] В сообщении нет упоминания бота.")

async def handle_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[LOG] Проверяем ключевое слово в сообщении: '{update.message.text}'")

    if ALLOWED_CHAT_IDS and update.message.chat_id not in ALLOWED_CHAT_IDS:
        print(f"[LOG] Сообщение из другого чата ({update.message.chat_id}), игнорируем.")
        return

    text = update.message.text or ""
    if text.lstrip().startswith("Шамиль,"):
        print("[LOG] Триггер сработал (ключевое слово). Отправляем голосовое сообщение.")
        await send_voice_message(update, context)

async def log_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username if update.message.from_user else "unknown"
    print(f"[LOG] ВСЕ сообщения: от @{user} в чате {update.message.chat_id}: {update.message.text}")

if __name__ == "__main__":
    print("[LOG] Запускаем бота...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.Entity("mention"), handle_mention))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_keyword))
    # group=1: иначе этот хендлер не срабатывает — в group=0 отрабатывает только первый подходящий.
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), log_all_messages), group=1)

    app.run_polling()