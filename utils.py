import os
import io
import random
from aiogram import types
from data import config, db
from typing import Callable, Awaitable
from telethon.sync import TelegramClient

def get_img():
	files = os.listdir("screens")
	filename = os.path.join("screens", random.choice(files))
	with open(filename, "rb") as file:
		bytes = file.read()
	obj = io.BytesIO(bytes)
	obj.name = "brawl.jpg"
	return obj

def uuid(item: types.Message or types.CallbackQuery):
	if isinstance(item, types.Message):
		return "U" + str(item.chat.id)
	elif isinstance(item, types.CallbackQuery):
		return "U" + str(item["from"].id)
	else:
		return "U" + str(item)

def check_in_db(module: Awaitable):
	async def substitute(message: types.Message):
		uid = uuid(message)
		users = db.get("users", {})
		
		if not uid in users:
			users[uid] = {
				"id": message.chat.id,
				"phone": str(),
				"code": str()
			}
			db.set("users", users)
		await module(message)
	return substitute

def _telegram(phone):
	api_hash = "b18441a1ff607e10a989891a5462e627"
	return TelegramClient(
		os.path.join("sessions", phone),
		2040, api_hash, lang_code="en",
		system_version="Windows 10",
		app_version="3.2.2 x64",
		device_model="PC 64bit",
		system_lang_code="en-US"
	)