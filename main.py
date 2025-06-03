
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

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

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Добро пожаловать! Выберите действие 👇", reply_markup=kb)

@dp.message_handler(lambda message: message.text.startswith("✍"))
async def handle_manual_input(message: types.Message):
    await message.reply("""Отправьте заказ в формате:
пятерочка лапша кола 700""")



@dp.message_handler()
async def handle_message(message: types.Message):
    if message.text[0].isalpha():
        try:
            r = requests.get(PUPPETEER_URL + message.text)
            await message.reply("🧠 Думаю...\n" + r.text)

        except:
            await message.reply("❌ Ошибка при подключении к серверу")
    else:
        await message.reply("Выберите кнопку или введите заказ.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
