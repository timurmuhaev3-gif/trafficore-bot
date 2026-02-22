import telebot
from telebot import types
from telebot.types import InputMediaPhoto
import os
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

CHANNEL_LINK = "https://t.me/+F2INNDYf6FgxYWZi"
REVIEWS_LINK = "https://t.me/+HojZs1zt5rkzMWI6"
ADMIN_LINK = "https://t.me/@TimurMukhaev"

QR_PATH = "channel_qr.png"


# ====== ГЛАВНОЕ МЕНЮ ======
def main_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)

    kb.add(types.InlineKeyboardButton("🏦 О проекте", callback_data="about"))

    kb.row(
        types.InlineKeyboardButton("💰 Услуги", callback_data="services"),
        types.InlineKeyboardButton("⭐️ Отзывы", url=REVIEWS_LINK)
    )

    kb.add(types.InlineKeyboardButton("📈 Войти в приват", url=CHANNEL_LINK))

    kb.row(
        types.InlineKeyboardButton("👥 Пригласить", callback_data="invite"),
        types.InlineKeyboardButton("✉️ Связь", url=ADMIN_LINK)
    )

    return kb


# ====== МЕНЮ ПРИГЛАШЕНИЯ ======
def invite_menu():
    kb = types.InlineKeyboardMarkup()

    # 🔥 Открывает список контактов Telegram
    kb.add(types.InlineKeyboardButton(
        "👥 Поделиться с друзьями",
        switch_inline_query="invite"
    ))

    kb.add(types.InlineKeyboardButton("📷 Показать QR код", callback_data="show_qr"))
    kb.add(types.InlineKeyboardButton("⬅️ Личный кабинет", callback_data="main"))

    return kb


# ====== START ======
@bot.message_handler(commands=["start"])
def start(message):

    text = """
🤖 <b>TRAFFICORE BOT</b>

Добро пожаловать в официальный бот проекта.

📌 Здесь вы можете:
• <i>Узнать информацию о проекте</i>
• <i>Ознакомиться с услугами</i>
• <i>Получить доступ в приватный канал</i>
• <i>Связаться с администратором</i>

Используйте меню ниже для навигации 👇
"""

    photo = open("header.jpeg", "rb")

    bot.send_photo(
        message.chat.id,
        photo,
        caption=text,
        parse_mode="HTML",
        reply_markup=main_menu()
    )


# ====== CALLBACK ======
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    # --- ГЛАВНОЕ МЕНЮ ---
    if call.data == "main":

        text = """
🤖 *TRAFFICORE BOT*

Добро пожаловать в официальный бот проекта.

📌 Здесь вы можете:
• <i>Узнать информацию о проекте</i>
• <i>Ознакомиться с услугами</i>
• <i>Получить доступ в приватный канал</i>
• <i>Связаться с администратором</i>

Выберите нужный раздел ниже 👇
"""

        media = InputMediaPhoto(open("header.jpeg", "rb"), caption=text, parse_mode="HTML")

        bot.edit_message_media(
            media=media,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=main_menu()
        )

    # --- О ПРОЕКТЕ ---
    elif call.data == "about":

        text = """
🏦 *О проекте*

💰 Помогаем с оформлением банковских продуктов:
• <u>Дебетовые и кредитные карты</u>
• <u>Займы и кредитные линии</u>
• <u>РКО для ИП и бизнеса</u>
Работаем по официальным <b>партнёрским программам</b>, поэтому при оформлении через наши ссылки доступны повышенные выплаты и бонусы.
Все детали — в канале.
"""

        bot.edit_message_caption(
            caption=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="HTML",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("⬅️ Личный кабинет", callback_data="main")
            )
        )

    # --- УСЛУГИ ---
    elif call.data == "services":

        text = """
💰 *Услуги*

📊 <pre>Мы занимаемся привлечением целевого трафика в банковские продукты.
Работаем по партнёрским программам с банками и сервисами.</pre>
Открыты к сотрудничеству с партнёрами, которые приводят трафик.
В канале — кейсы, разборы и подробная информация о работе.
"""

        bot.edit_message_caption(
            caption=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="HTML",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("⬅️ Личный кабинет", callback_data="main")
            )
        )

    # --- ПРИГЛАСИТЬ ---
    elif call.data == "invite":

        text = """
👥 Пригласить друзей:

Вы можете поделиться ботом с контактами
или отправить QR код.

Выберите способ ниже 👇
"""

        bot.edit_message_caption(
            caption=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="HTML",
            reply_markup=invite_menu()
        )

    # --- QR ---
    elif call.data == "show_qr":

        text = """
📷 *QR код для приглашения*

Отсканируйте или отправьте друзьям.
"""

        media = InputMediaPhoto(open(QR_PATH, "rb"), caption=text, parse_mode="HTML")

        bot.edit_message_media(
            media=media,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=invite_menu()
        )


print("🔥 BOT STARTED")
bot.polling(none_stop=True)