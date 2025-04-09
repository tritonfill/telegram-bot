
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from googletrans import Translator

TOKEN = "7947093952:AAE_m-QQSANfvnR3Fbk-4SVIrz_MqbPXSIM"
translator = Translator()
user_last_text = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне текст, и я помогу перевести его.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    user_last_text[user_id] = text

    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 Английский", callback_data='en'),
            InlineKeyboardButton("🇷🇺 Русский", callback_data='ru'),
        ],
        [
            InlineKeyboardButton("🇩🇪 Немецкий", callback_data='de'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выбери язык для перевода:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if user_id not in user_last_text:
        await query.edit_message_text("Сначала отправь текст.")
        return

    original_text = user_last_text[user_id]
    dest_lang = query.data
    translated = translator.translate(original_text, dest=dest_lang)

    src_lang = translated.src.upper()
    translated_text = translated.text
    dest_lang_upper = dest_lang.upper()

    response = f"Исходный язык: {src_lang}\nПеревод ({dest_lang_upper}):\n{translated_text}"
    await query.edit_message_text(response)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
