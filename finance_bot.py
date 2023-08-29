import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import executor

API_TOKEN = "6245246946:AAEyJ6CKPEzM6ULh5SRTQFpz-wE-VmrMs0s"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

currency = "KZT"
budget = None


@dp.message_handler(commands=["start"])
async def on_start(message: types.Message):
    await message.reply(
        f"Hello, I am your finance tracker bot!\nPlease, send me your budget for a month. \nDefault currency is {currency}."
    )


@dp.message_handler(lambda message: budget is None, content_types=types.ContentTypes.TEXT)
async def budget_received(message: types.Message):
    global budget
    budget = message.text
    await message.reply(
        f"Thank you! Your budget is set to {budget} {currency}.\nType command /track to start tracking your finances."
    )


@dp.message_handler(commands=["track"])
async def start_tracking(message: types.Message):
    await message.reply("Please promptly send me the expenditure amount whenever incurred.")


@dp.message_handler(lambda message: budget is not None, content_types=types.ContentTypes.TEXT)
async def budget_tracking(message: types.Message):
    global budget
    try:
        spending = int(message.text)
        remainder = int(budget) - spending
        current_date = datetime.now()
        date = current_date.strftime("%d-%m-%Y")
        await message.reply(
            f"You spent {spending} {currency}. Now, your budget is {remainder} {currency}. \nDate: {date}"
        )
        budget = remainder
    except ValueError:
        await message.reply("Please enter a valid expenditure amount.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
