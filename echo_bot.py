from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


# Токен Telegram бота
BOT_TOKEN = 'TOKEN'

# Создаём объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Этот хэндлер будет срабатывать на команду /start
@dp .message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот.\nНапиши мне что-нибудь')

# Этот хэндлер будет срабатывать на команду /help
@dp .message(Command(commands='help'))    
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь, и я пришлю тебе сообщение в ответ.'
    )


# Этот хэндлер будет срабатывать на любые сообщения
# Кроме комнды /start и /help
@dp .message()

async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается ботом'
        )


if __name__ == '__main__':
    dp.run_polling(bot)

