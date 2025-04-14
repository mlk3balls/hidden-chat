# main.py

import telebot
from telebot import types
from config import BOT_TOKEN, ADMINS
from database import init_db, save_message, get_all_messages, get_message_by_id

bot = telebot.TeleBot(BOT_TOKEN)
init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! پیام ناشناست رو برام بفرست، من بدون اسم نشونش می‌دم.")

@bot.message_handler(commands=['messages'])
def show_messages(message):
    username = message.from_user.username
    if username not in ADMINS:
        bot.reply_to(message, "دسترسی نداری.")
        return

    messages = get_all_messages()
    if not messages:
        bot.reply_to(message, "هیچ پیامی نیست.")
        return

    for msg in messages:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("مشاهده فرستنده", callback_data=f"view_{msg[0]}")
        markup.add(btn)
        bot.send_message(message.chat.id, f"پیام: {msg[1]}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("view_"))
def callback_view_sender(call):
    msg_id = int(call.data.split("_")[1])
    msg = get_message_by_id(msg_id)
    if not msg:
        bot.answer_callback_query(call.id, "پیام پیدا نشد.")
        return

    user_info = f"آیدی عددی: {msg[1]}
یوزرنیم: @{msg[2]}" if msg[2] else "یوزرنیم ثبت نشده"
    bot.send_message(call.message.chat.id, f"فرستنده:
{user_info}")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username
    msg = message.text

    save_message(user_id, username, msg)
    bot.reply_to(message, "پیامت ناشناس ذخیره شد!")

bot.infinity_polling()
