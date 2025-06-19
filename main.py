import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
import os

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Получаем токен бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Убедись, что он указан в Render в разделе Environment.")

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Обработчик команды /start
@dp.message(commands=["start"])
async def cmd_start(message: Message):
    await message.answer("Привет! Бот работает 🎉")

# Точка входа
async def main():
    logging.info("🚀 Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"⚠️ Произошла ошибка при запуске бота: {e}")