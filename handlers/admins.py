import asyncio
from loader import bot, dp
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from data.functions.models import *
from data.functions import utils_mute

def get_mention(user):
	return f"tg://resolve?domain={user.username}" if user.username else f"tg://openmessage?user_id={user.id}"

def get_rights_keyboard(me_id):
	me_rights = Admins.get(id=me_id).rights
	full_rights = ["ban", "mute", "warn", "purge", "view", "promote"]
	markup = InlineKeyboardMarkup()

	for right in full_rights:
		markup.add(InlineKeyboardButton(text=right , callback_data="n"), InlineKeyboardButton(text="✅" if right in me_rights else "❌", callback_data="n"))
	return markup

strings = {
	"no_reply": "А де реплай?",
	"no_rights": "Немає прав",
	"purging": "Очищаю...",
	"no_msg": "Не знайдено в DB",
	"purged": "Очищення завершено",
	"id": "<a href=\"tg://user?id={0}\">ID:</a> <code>{0}</code>",
	"is_adm": "Він уже адмін",
	"no_adm": "Він не адмін",
}

@dp.message_handler(commands=["admin"])
async def me_info(message: Message):
	if not Admins.get_or_none(id=message.chat.id):
		return

	keyb = InlineKeyboardMarkup().add(InlineKeyboardButton("Можливості", callback_data="rights"))
	await message.reply(f"Твоя посада: <code>{Admins.get(id=message.chat.id).name}</code>", reply_markup=keyb)


@dp.callback_query_handler(text="rights")
async def get_rights(call: CallbackQuery):
	if not Admins.get_or_none(id=call.message.chat.id):
		return

	keyboard = get_rights_keyboard(call.message.chat.id)
	keyboard.add(InlineKeyboardButton("Назад", callback_data="back_in_admin"))
	await call.message.edit_text("Твої можливості:", reply_markup=keyboard)


@dp.callback_query_handler(text="n")
async def n(call: CallbackQuery):
	if not Admins.get_or_none(id=call.message.chat.id):
		return
	await call.answer()


@dp.callback_query_handler(text="s")
async def s(call: CallbackQuery):
	if not Admins.get_or_none(id=call.message.chat.id):
		return
	await call.message.delete()


@dp.callback_query_handler(text="back_in_admin")
async def back_in_admin(call: CallbackQuery):
	if not Admins.get_or_none(id=call.message.chat.id):
		return

	keyb = InlineKeyboardMarkup().add(InlineKeyboardButton("Можливості", callback_data="rights"))
	await call.message.edit_text(f"Твоя посада: <code>{Admins.get(id=call.message.chat.id).name}</code>", reply_markup=keyb)


@dp.message_handler(commands=["purge"])
async def purge(message: Message):
	mj = message
	args = message.get_args().split()
	reason = (None if not args else " ".join(args))

	if not Admins.get_or_none(id=message.chat.id):
		return
	if not "purge" in Admins.get(id=message.chat.id).rights:
		return await message.reply(strings["no_rights"])

	if not message.reply_to_message:
		return await message.reply(strings["no_reply"])
	if message.reply_to_message.reply_markup:
		for row in message.reply_to_message.reply_markup.inline_keyboard:
			for button in row:
				if button["text"] == "DELETED":
					return await message.reply(strings["no_reply"])

	user_id = get_reply_sender(message.chat.id, message.reply_to_message.message_id)
	if message.chat.id == user_id:
		return await message.reply("Свої повідомлення не можна видаляти")

	if not user_id:
		return await message.reply(strings["no_msg"])
	replies = get_reply_data(message.chat.id, message.reply_to_message.message_id)
	if not replies:
		return await message.reply(strings["no_msg"])

	message = await message.reply(strings["purging"])
	reply_msg_id = get_reply_id(replies, user_id)
	keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text=f"{Admins.get(id=message.chat.id).name}: {message.chat.full_name}", url=get_mention(message.chat)))

	await bot.edit_message_reply_markup(mj.chat.id, mj.reply_to_message.message_id, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("DELETED", callback_data="s")))

	await asyncio.gather(*[
		bot.delete_message(data["chat_id"], data["msg_id"])
		for data in replies
		if data["chat_id"] != user_id and data["chat_id"] != message.chat.id
	], return_exceptions=True)

	await message.edit_text(strings["purged"])

	try:
		USER = await bot.get_chat(user_id)
		await bot.send_message(-100nnnnnnnnnn,
			f"#PURGE\n<b>Адмін:</b> <a href='{get_mention(mj.chat)}'>{mj.chat.full_name}</a>\n<b>Причина:</b> {'null' if not reason else reason}\n<b>Юзер:</b> <a href='{get_mention(USER)}'>{USER.full_name}</a>\n<b>Повідомлення:</b>"
		)
		await bot.forward_message(chat_id=-100nnnnnnnnnn, from_chat_id=user_id, message_id=get_reply_id(replies, user_id))
	except: pass

	ims = await bot.send_message(user_id, f"Твоє повідомлення видалено" + (f" через: <code>{reason}</code>" if reason else ""), reply_to_message_id=reply_msg_id, reply_markup=keyboard)

	await bot.pin_chat_message(ims.chat.id, ims.message_id)
	await bot.unpin_chat_message(ims.chat.id, ims.message_id)


@dp.message_handler(commands=["uid"])
async def uid(message: Message):
	if not Admins.get_or_none(id=message.chat.id):
		return
	if not "view" in Admins.get(id=message.chat.id).rights:
		return await message.reply(strings["no_rights"])

	if not message.reply_to_message:
		return await message.reply(strings["no_reply"])
	id = get_reply_sender(message.chat.id, message.reply_to_message.message_id)
	if not id:
		return await message.reply(strings["no_msg"])
	await message.reply(strings["id"].format(str(id)))


@dp.message_handler(commands=["promote"])
async def promote(message: Message):
	if not Admins.get_or_none(id=message.chat.id):
		return
	if not "promote" in Admins.get(id=message.chat.id).rights:
		return await message.reply(strings["no_rights"])
	if not message.reply_to_message:
		return await message.reply(strings["no_reply"])

	args = message.get_args().split()
	if len(args) < 2:
		return await message.reply("Немає аргументів\nПриклад: /promote Адмін mute\;purge")
	name = args[0]
	rights = args[1]
	replies = get_reply_data(message.chat.id, message.reply_to_message.message_id)
	id = get_reply_sender(message.chat.id, message.reply_to_message.message_id)

	if not id:
		return await message.reply(strings["no_msg"])
	if Admins.get_or_none(id=id):
		return await message.reply(strings["is_adm"])
	Admins.create(id=id, name=name, rights=rights)
	await message.reply("Успішно")

	keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text=f"{Admins.get(id=message.chat.id).name}: {message.chat.full_name}", url="tg://openmessage?user_id=%s" % message.chat.id))

	ims = await bot.send_message(id, f"Тебе було поставлено на посаду: <code>{name}</code>\nАдмін-панель: /admin", reply_markup=keyboard, reply_to_message_id=get_reply_id(replies, id))
	await bot.pin_chat_message(ims.chat.id, ims.message_id)
	await bot.unpin_chat_message(ims.chat.id, ims.message_id)


@dp.message_handler(commands=["demote"])
async def demote(message: Message):
	if not Admins.get_or_none(id=message.chat.id):
		return
	if not "promote" in Admins.get(id=message.chat.id).rights:
		return await message.reply(strings["no_rights"])
	if not message.reply_to_message:
		return await message.reply(strings["no_reply"])

	args = message.get_args().split()
	reason = (None if not args else " ".join(args))

	id = get_reply_sender(message.chat.id, message.reply_to_message.message_id)
	if not id:
		return await message.reply(strings["no_msg"])
	if not Admins.get_or_none(id=id):
		return await message.reply(strings["no_adm"])

	dolj = Admins.get(id=id).name
	Admins.delete().where(Admins.id==id).execute()
	await message.reply("Успішно")

	keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text=f"{Admins.get(id=message.chat.id).name}: {message.chat.full_name}", url="tg://openmessage?user_id=%s" % message.chat.id))

	ims = await bot.send_message(id, f"Тебе було знято з посади: <code>{dolj}</code>" + (f" через: <code>{reason}</code>" if reason else ""), reply_markup=keyboard)
	await bot.pin_chat_message(ims.chat.id, ims.message_id)
	await bot.unpin_chat_message(ims.chat.id, ims.message_id)


@dp.message_handler(commands=["mute"])
async def mute(message: Message):
	if not Admins.get_or_none(id=message.chat.id):
		return
	if not "mute" in Admins.get(id=message.chat.id).rights:
		return await message.reply(strings["no_rights"])
	if not message.reply_to_message:
		return await message.reply(strings["no_reply"])

	replies = get_reply_data(message.chat.id, message.reply_to_message.message_id)
	sender_id = get_reply_sender(message.chat.id, message.reply_to_message.message_id)
	if not sender_id:
		return await message.reply(strings["no_msg"])

	try:
		duration, reason = utils_mute.get_duration_and_reason(message.get_args().split())
	except Exception as error:
		return await message.reply(f"{error}")

	if not duration and not reason:
		await message.reply("Немає аргументів\nПриклад: /mute 1ч30м спам")

	Users.update(mute=Users.get(Users.id==sender_id).mute + duration).where(Users.id==sender_id).execute()

	await message.reply("Успішно")
	keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text=f"{Admins.get(id=message.chat.id).name}: {message.chat.full_name}", url=get_mention(message.chat)))

	try:
		USER = await bot.get_chat(sender_id)
		await bot.send_message(-100nnnnnnnnnn,
			f"#MUTE\n<b>Адмін:</b> <a href='{get_mention(message.chat)}'>{message.chat.full_name}</a>\n<b>Причина:</b> {'null' if not reason else reason}\n<b>Юзер:</b> <a href='{get_mention(USER)}'>{USER.full_name}</a>\n<b>Час:</b> {duration}"
		)
	except: pass

	ims = await bot.send_message(sender_id, f"Ти був зам'ючений на <code>{duration}</code>" + (f" з причини: <code>{reason}</code>" if reason else ""), reply_markup=keyboard, reply_to_message_id=get_reply_id(replies, sender_id))
	await bot.pin_chat_message(ims.chat.id, ims.message_id)
	await bot.unpin_chat_message(ims.chat.id, ims.message_id)


@dp.message_handler(text="UNLOADALL")
async def unload(msg):
	for user in Users.select(Users.id):
		Users.update(mute=datetime.now()).where(Users.id==user.id).execute()
	await msg.reply("ok")


@dp.message_handler(commands=["unmute"])
async def unmute(message: Message):
	if not Admins.get_or_none(id=message.chat.id):
		return
	if not "mute" in Admins.get(id=message.chat.id).rights:
		return await message.reply(strings["no_rights"])
	if not message.reply_to_message:
		return await message.reply(strings["no_reply"])

	replies = get_reply_data(message.chat.id, message.reply_to_message.message_id)
	sender_id = get_reply_sender(message.chat.id, message.reply_to_message.message_id)
	if not sender_id:
		return await message.reply(strings["no_msg"])

	Users.update(mute=datetime.now()).where(Users.id==sender_id).execute()

	await message.reply("Успішно")
	keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text=f"{Admins.get(id=message.chat.id).name}: {message.chat.full_name}", url=get_mention(message.chat)))

	ims = await bot.send_message(sender_id, f"Ти був розм'ючений", reply_markup=keyboard, reply_to_message_id=get_reply_id(replies, sender_id))
	await bot.pin_chat_message(ims.chat.id, ims.message_id)
	await bot.unpin_chat_message(ims.chat.id, ims.message_id)
