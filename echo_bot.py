from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters.command import CommandException

# Токен Telegram бота
BOT_TOKEN = 'TOKEN'

# Создаём объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Этот хэндлер будет срабатывать на команду /start
@dp.message(Command(commands=['start']))
async def process_start(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот.\nНапиши мне что-нибудь')

# Этот хэндлер будет срабатывать на команду /help
@dp.message(Command(commands=['help']))
async def process_help(message: Message):
    await message.answer(
        'Напиши мне что-нибудь, и я пришлю тебе сообщение в ответ.'
    )

# Этот хэндлер будет срабатывать на любые текстовые сообщения
@dp.message(lambda message: message.text)
async def send_echo(message: Message):
    await message.answer(message.text)

# Этот хэндлер будет срабатывать только на отправленные фотографии
@dp.message(lambda message: message.photo)
async def send_photo(message: Message):
    # Отправляем обратно фотографию
    await message.answer_photo(photo=message.photo[-1].file_id)

# Этот хэндлер будет срабатывать только на отправленные стикеры
@dp.message(lambda message: message.sticker)
async def send_sticker(message: Message):
    # Отправляем обратно стикер
    await message.answer_sticker(sticker=message.sticker.file_id)

if __name__ == '__main__':
    dp.run_polling(bot)

