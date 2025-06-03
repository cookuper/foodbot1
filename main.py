import logging
import json
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import asyncio  # добавлено

API_TOKEN = '8066927688:AAFipaqyM4qoUODZ705PDocSZSSEEGWCVik'
PUPPETEER_URL = 'https://puppeteer-server-g0r7.onrender.com/generate?query='
USERS_FILE = 'users_counter.json'
START_FROM = 40

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("🎲 Рандом еда"))
kb.add(KeyboardButton("🍴 Настроить блюда"))
kb.add(KeyboardButton("✍ Ввести вручную"))
kb.add(KeyboardButton("🏬 По ресторану"))

user_last_message = {}
user_state = {}

def get_user_count(user_id):
    try:
        with open(USERS_FILE, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"base_fake": START_FROM, "real_users": 0, "user_ids": []}

    if "user_ids" not in data:
        data["user_ids"] = []

    if user_id not in data["user_ids"]:
        data["real_users"] += 1
        data["user_ids"].append(user_id)
        with open(USERS_FILE, 'w') as f:
            json.dump(data, f)

    return data["base_fake"] + data["real_users"]

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    count = get_user_count(message.from_user.id)
    await message.answer(f"Добро пожаловать! Выберите действие 👇\nАктивных пользователей за месяц: {count}", reply_markup=kb)

@dp.message_handler(lambda message: message.text.startswith("✍"))
async def handle_manual_input(message: types.Message):
    if message.chat.id in user_last_message:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=user_last_message[message.chat.id])
        except:
            pass
    sent = await message.answer("Отправьте заказ в формате:\nпятерочка лапша кола 700")
    user_last_message[message.chat.id] = sent.message_id
    user_state[message.chat.id] = "manual_input"

@dp.message_handler()
async def handle_message(message: types.Message):
    if message.text in ["🎲 Рандом еда", "🍴 Настроить блюда", "🏬 По ресторану"]:
        user_state.pop(message.chat.id, None)

    if user_state.get(message.chat.id) == "manual_input":
        if message.text[0].isalpha():
            try:
                r = requests.get(PUPPETEER_URL + message.text)
                if message.chat.id in user_last_message:
                    try:
                        await bot.delete_message(chat_id=message.chat.id, message_id=user_last_message[message.chat.id])
                    except:
                        pass
                sent = await message.answer("🧠 Думаю...\n" + r.text)
                user_last_message[message.chat.id] = sent.message_id
                user_state.pop(message.chat.id, None)
            except:
                await message.answer("❌ Ошибка при подключении к серверу")
        else:
            await message.answer("Неверный формат. Пример: пятерочка лапша кола 700")
        return

    if message.chat.id in user_last_message:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=user_last_message[message.chat.id])
        except:
            pass
    sent = await message.answer("Выберите кнопку или введите заказ.")
    user_last_message[message.chat.id] = sent.message_id

# 🔧 добавляем асинхронный запуск с удалением webhook
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
