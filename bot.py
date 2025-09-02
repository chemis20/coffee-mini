# bot.py
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import json

TOKEN = ''

async def start(update: Update, _):
    kb = [['📋 Каталог', '👤 Кабинет', '📦 Мои заказы', '💎 Лояльность', '❓ Поддержка']]
    await update.message.reply_text(
        "🎉 Добро пожаловать в BrewPoint!\n\nВыберите действие:",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
    )

async def handle_order(update: Update, _):
    # принимаем данные от мини-апа
    data = json.loads(update.message.web_app_data.data)
    items = '\n'.join([f"{i['name']} {i['price']}₽ – {i['time']}" for i in data['items']])
    total = data['total']
    await update.message.reply_text(
        f"✅ Заказ оформлен!\n\n📋 Состав:\n{items}\n💰 Сумма: {total}₽\n⏰ Время: {data['time']}"
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_order))
app.run_polling()
