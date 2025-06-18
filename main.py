import os
import logging
from aiogram import Bot, Dispatcher, types, executor
import openai

logging.basicConfig(level=logging.INFO)

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_API_TOKEN or not OPENAI_API_KEY:
    raise Exception("Отсутствуют обязательные переменные окружения TELEGRAM_API_TOKEN или OPENAI_API_KEY")

bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY


async def ask_openai(prompt):
    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я бот-помощник для подготовки к ОГЭ по математике 9 класса.\n"
        "Задавай вопросы, проси тесты, объяснения тем.\n"
        "Команды:\n"
        "/тема — выбрать тему для изучения\n"
        "/тест — получить тест из нескольких задач\n"
        "/статистика — посмотреть свой прогресс\n"
        "/повторить — повторить сложные темы"
    )


@dp.message_handler(commands=["тест"])
async def send_test(message: types.Message):
    prompt = (
        "Сгенерируй 3 простые задачи для 9 класса по математике для подготовки к ОГЭ, "
        "с краткими ответами. Нумеруй задачи."
    )
    answer = await ask_openai(prompt)
    await message.answer(answer)


@dp.message_handler(commands=["тема"])
async def choose_topic(message: types.Message):
    await message.answer(
        "Пока бот в тестовом режиме. Напиши тему, например:\n"
        "'квадратные уравнения', 'проценты', 'геометрия', 'функции'\n"
        "и я объясню её простыми словами."
    )


@dp.message_handler(commands=["статистика"])
async def show_stats(message: types.Message):
    # Для простоты пока заглушка
    await message.answer("Статистика пока в разработке — скоро добавим!")


@dp.message_handler(commands=["повторить"])
async def repeat_hard_topics(message: types.Message):
    await message.answer("Функция повторения сложных тем пока в разработке — подождите чуть-чуть.")


@dp.message_handler()
async def handle_message(message: types.Message):
    text = message.text
    prompt = (
        f"Объясни простыми словами тему по математике для 9 класса ОГЭ:\n\n{text}\n\n"
        "Объяснение должно быть понятным, с примерами."
    )
    answer = await ask_openai(prompt)
    await message.answer(answer)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
