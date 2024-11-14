from aiogram import Router
from aiogram.types import Message

router = Router()

# Этот хэндлер будет реагировать на любое сообщение пользователя
# не предусмотренного логикой работы бота
@router.message()
async def send_echo(message: Message):
    await message.answer(f'Это эхо! {message.text}')