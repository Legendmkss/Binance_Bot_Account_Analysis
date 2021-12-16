import logging
import config
from typing import Text
 
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types.message_entity import MessageEntity
from aiogram.utils.markdown import hbold, hlink

from binance.client import Client

from server import get_asset

# Присоединяемся к аккаунту #

client = Client(config.API_KEY, config.API_SECRET_KEY)
print("logged in")
      
# Тестовая версия получения баланса определенной монеты #

def get_balance(assets, symbols):
    balance = client.get_asset_balance(asset=assets)
    tickers = client.get_ticker(symbol = symbols)
    last_price = float(tickers['lastPrice'])
    sum = float(balance["free"])

    all_price_btc = f"{assets} куплено на {round(sum * last_price, 1)} $"
    return all_price_btc

# Активация телеграм бота #

API_TOKEN = config.API_TOKEN

# Configure logging #
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher #
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
   start_buttons = ['Стоимость портфеля', 'wait', 'wait']
   keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
   keybord.add(*start_buttons)

   await message.answer("Выберите категорию", reply_markup=keybord)

@dp.message_handler(Text(equals='Стоимость портфеля'))
async def price_case(message: types.Message):
    price_case_buttons = ['BTC', 'SHIB']
    price_case_buttons.append(get_asset())
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(*price_case_buttons)

    await message.answer("Какая криптовалюта интересует?", reply_markup=keybord)

@dp.message_handler(Text(equals='BTC'))
async def get_price_btc(message: types.Message):
    await message.answer(get_balance('BTC', 'BTCUSDT'))
    

@dp.message_handler(Text(equals='SHIB'))
async def get_price_shib(message: types.Message):
    await message.answer(get_balance('SHIB', 'SHIBUSDT'))


# Включение #

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)