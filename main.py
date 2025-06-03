import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import json
import os

API_TOKEN = '8066927688:AAFipaqyM4qoUODZ705PDocSZSSEEGWCVik'
PUPPETEER_URL = 'https://puppeteer-server-g0r7.onrender.com/generate?query='

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("🎲 Рандом еда"))
kb.add(KeyboardButton("🍴 Настроить блюда"))
kb.add(KeyboardButton("✍ Ввести вручную"))
kb.add(KeyboardButton("🏬 По ресторану"))

user_last_message = {}
USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    users = load_users()
    user_id = message.from_user.id
    if user_id not in users:
        users.append(user_id)
        save_users(users)

    fake_start = 40
    count = fake_start + len(users)
    await message.answer(f"Добро пожаловать! Выберите действие 👇\n👥 Пользователей за месяц: {count}", reply_markup=kb)

@dp.message_handler(lambda message: message.text.startswith("\u270d"))
async def handle_manual_input(message: types.Message):
    if message.chat.id in user_last_message:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=user_last_message[message.chat.id])
        except:
            pass
    sent = await message.answer("Отправьте заказ в формате:\nпятерочка лапша кола 700")
    user_last_message[message.chat.id] = sent.message_id

@dp.message_handler()
async def handle_message(message: types.Message):
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
        except:
            await message.answer("❌ Ошибка при подключении к серверу")
    else:
        if message.chat.id in user_last_message:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=user_last_message[message.chat.id])
            except:
                pass
        sent = await message.answer("Выберите кнопку или введите заказ.")
        user_last_message[message.chat.id] = sent.message_id

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)