from loader import bot, dp
import asyncio
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from data.functions.models import *
from aiogram.types.message_id import MessageId
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.markdown import link

class States(StatesGroup):
	setnick = State()

def get_mention(user):
	return f"tg://resolve?domain={user.username}" if user.username else f"tg://openmessage?user_id={user.id}"

@dp.message_handler(state=States.setnick, content_types="text")
async def setnick(message, state):
	if len(message.text) > 16:
		return await message.reply("Нельзя больше чем 16 символов")
	haha = Users.get(Users.id==message.chat.id).name
	Users.update(name=message.text).where(Users.id==message.chat.id).execute()
	await state.finish()
	if haha:
		await message.reply("Ник изменен")
	else:
		await message.reply("Ник установлен")

@dp.callback_query_handler(text="nick")
async def nick(call: CallbackQuery):
	await call.answer("Это кастомный ник!\nВведи: /nick", show_alert=True)

@dp.message_handler(commands=["rules"])
async def rules(message: Message):
	keyboard = InlineKeyboardMarkup(row_width=2)
	pinushes = [("Дeтcкoe пopнo", "ban"), ("Расчленёнка", "mute"), ("Жёсткое 18+", "purge"), ("Зоофилия", "mute"), ("Флуд/Спам", "mute"), ("Реклама", "purge")]
	for wtf, pinush in pinushes:
		keyboard.add(InlineKeyboardButton(wtf, callback_data="n"), InlineKeyboardButton(pinush, callback_data="n"))
	await message.reply("Правила бота:", reply_markup=keyboard)
    
@dp.message_handler(commands=["cmd"])
async def rules(message: Message):
	keyboard = InlineKeyboardMarkup(row_width=2)
	pinushes = [("/start", "Запуск бота"), ("/rules", "Правила"), ("/nick", "Настройки ника"), ("/stats", "Статистика"), ("/admincmd", "Админ команды")]
	for wtf, pinush in pinushes:
		keyboard.add(InlineKeyboardButton(wtf, callback_data="n"), InlineKeyboardButton(pinush, callback_data="n"))
	await message.reply("Список команд:", reply_markup=keyboard)

@dp.message_handler(commands=["admincmd"])
async def rules(message: Message):
	keyboard = InlineKeyboardMarkup(row_width=2)
	pinushes = [("/admin", "Админ панель"), ("/uid", "ID юзера"), ("/promote", "/demote"), ("/mute", "/unmute"), ("/purge", "Очистка"), ("/ban", "/unban")]
	for wtf, pinush in pinushes:
		keyboard.add(InlineKeyboardButton(wtf, callback_data="n"), InlineKeyboardButton(pinush, callback_data="n"))
	await message.reply("Список команд для администраторов:", reply_markup=keyboard)

@dp.message_handler(commands=["stats"])
async def stats(message: Message):
	users = Users.select()
	await message.reply(f"Юзеров бота: <code>{len(users)}</code>")
    
@dp.message_handler(commands=["help"])
async def help(message: Message):
	await message.reply('Я буду отправлять твои сообщения всем юзерам.\n/cmd - список команд\n\n<a href="https://github.com/onilyxe/echogram">Исходный код</a>', parse_mode="HTML")

@dp.callback_query_handler(text="nick:back")
async def back_back(call):
	message = call.message
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("Установить" if not Users.get(Users.id==message.chat.id).name else "Изменить", callback_data="nick:setup"), InlineKeyboardButton("Удалить", callback_data="nick:del"))
	keyboard.add(
		InlineKeyboardButton("Посмотреть",  callback_data="nick:view"),
		InlineKeyboardButton(
			f'Упоминание {"✅" if Users.get(Users.id==message.chat.id).tag else "❌"}',
			callback_data="nick:tag"
		))
	await message.edit_text("Панель управления ником:", reply_markup=keyboard)

@dp.callback_query_handler(text="nick:tag")
async def nick_tag(call: CallbackQuery):
	message = call.message
	if Users.get(Users.id==message.chat.id).tag:
		Users.update(tag=False).where(Users.id==message.chat.id).execute()
	else:
		Users.update(tag=True).where(Users.id==message.chat.id).execute()
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("Установить" if not Users.get(Users.id==message.chat.id).name else "Изменить", callback_data="nick:setup"), InlineKeyboardButton("Удалить", callback_data="nick:del"))
	keyboard.add(
		InlineKeyboardButton("Посмотреть",  callback_data="nick:view"),
		InlineKeyboardButton(
			f'Упоминание {"✅" if Users.get(Users.id==message.chat.id).tag else "❌"}',
			callback_data="nick:tag"
		))
	await message.edit_text("Панель управления ником:", reply_markup=keyboard)
	await call.answer("OK")

@dp.callback_query_handler(text="nick:setup")
async def nicksetup(call):
	await call.message.answer("Введи ник:")
	await States.setnick.set()

@dp.callback_query_handler(text="nick:del")
async def nickdel(call):
	message = call.message
	keyb = InlineKeyboardMarkup().add(InlineKeyboardButton("Назад", callback_data="nick:back"))

	if not Users.get(Users.id==message.chat.id).name:
		return await message.edit_text("У тебя и не было ника", reply_markup=keyb)
	Users.update(name=None).where(Users.id==message.chat.id).execute()
	await message.edit_text("Ник удалён", reply_markup=keyb)

@dp.callback_query_handler(text="nick:view")
async def viewnick(call):
	keyb = InlineKeyboardMarkup().add(InlineKeyboardButton("Назад", callback_data="nick:back"))

	if Users.get(Users.id==call.message.chat.id).name:
		name = Users.get(Users.id==call.message.chat.id).name
		await call.message.edit_text(f"Твой ник: <code>{name}</code>", reply_markup=keyb)
	else:
		await call.message.edit_text("У тебя нет ника", reply_markup=keyb)

@dp.message_handler(commands=["nick"])
async def nick(message: Message):
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("Установить" if not Users.get(Users.id==message.chat.id).name else "Изменить", callback_data="nick:setup"), InlineKeyboardButton("Удалить", callback_data="nick:del"))
	keyboard.add(
		InlineKeyboardButton("Посмотреть",  callback_data="nick:view"),
		InlineKeyboardButton(
			f'Упоминание {"✅" if Users.get(Users.id==message.chat.id).tag else "❌"}',
			callback_data="nick:tag"
		))
	await message.reply("Панель управления ником:", reply_markup=keyboard)

@dp.message_handler(commands=["start"])
async def hello(message: Message):
	if not Users.select().where(Users.id==message.chat.id).exists():
		Users.create(id=message.chat.id)
	await message.reply("Я буду отправлять твои сообщения всем юзерам")

async def send(message, *args, **kwargs):
	return (await message.copy_to(*args, **kwargs)), args[0]

async def Send(message, keyboard, reply_data):
	result = [{"sender_id": message.chat.id}]
	msgs = await asyncio.gather(*[
		send(message, user.id, reply_markup=keyboard, reply_to_message_id=get_reply_id(reply_data, user.id) if message.reply_to_message else None)
		for user in Users.select(Users.id)
		if user.id != message.chat.id
	], return_exceptions=True)

	for msg_obj in msgs:
		if isinstance(msg_obj, tuple):
			msg, user_id = msg_obj
			if isinstance(msg, MessageId):
				result.append({"chat_id": user_id, "msg_id": msg.message_id})
	else:
		result.append({"chat_id": message.chat.id, "msg_id": message.message_id})
	print(result)
	msgs_db = rdb.get("messages", [])
	msgs_db.append(result)
	rdb.set("messages", msgs_db)

@dp.message_handler(content_types="any")
async def any(message: Message):
	if message.content_type == "pinned_message":
		return
	if datetime.now() < Users.get(Users.id==message.chat.id).mute and not Admins.get_or_none(id=message.chat.id):
		delay = Users.get(Users.id==message.chat.id).mute - datetime.now()
		dur = str(delay).split(".")[0]
		return await message.reply(f"Ты уже отправлял сообщение, вернись через <code>{dur}</code>")
	keyboard = InlineKeyboardMarkup()
	if Users.get(Users.id==message.chat.id).name:
		name = Users.get(Users.id==message.chat.id).name
		if Users.get(Users.id==message.chat.id).tag:
			keyboard.add(InlineKeyboardButton(text=name, url=get_mention(message.chat)))
		else:
			keyboard.add(InlineKeyboardButton(text=name, callback_data="nick"))
	Users.update(mute=datetime.now()).where(Users.id==message.chat.id).execute()
	if message.reply_to_message:
		reply_data = get_reply_data(message.chat.id, message.reply_to_message.message_id)
	if message.text or message.caption:
		if Users.get(Users.id==message.chat.id).last_msg == (message.text or message.caption):
			return await message.reply("Нельзя отправлять сообщения с одинаковым текстом")
		Users.update(last_msg=message.text or message.caption).where(Users.id==message.chat.id).execute()
	if is_flood(message.chat.id):
		Users.update(mute=datetime.now() + timedelta(hours=1)).where(Users.id==message.chat.id).execute()
		ims = await message.reply("Ты замьючен на <code>1:00:00</code> за флуд")
		await bot.pin_chat_message(ims.chat.id, ims.message_id)
		await bot.unpin_chat_message(ims.chat.id, ims.message_id)
		try:
			await bot.send_message(-1001635530740,
				f"#FLOOD\n<b>Юзер:</b> <a href='{get_mention(message.chat)}'>{message.chat.full_name}</a>"
			)
		except: pass
		return
	haha = await message.reply("Отправляю...")
	asyncio.create_task(
		Send(message, keyboard, reply_data if message.reply_to_message else None)
	)
	await haha.edit_text("Сообщение отправлено всем")
	await haha.delete()