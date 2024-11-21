import copy
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

# Вставьте токен вашего бота
BOT_TOKEN = ''

# Создём объект бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Инициализируем константу размера игрового поля
FIELD_SIZE = 8

# Создаем словарь соответствий
LEXICON = {
    '/start': 'Вот твоё поле. Можешь делать ход',
    0: ' ',
    1: '🌊',
    2: '💥',
    'miss': 'Мимо!',
    'hit': 'Попал!',
    'used': 'Вы уже стреляли сюда!',
    'next_move': 'Делайте ваш следующий ход'
}

# Расположение кораблей на поле
ships: list[list[int]] = [
     [1, 0, 1, 1, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0]
]

# Инициализируем базу данных пользователей
users: dict[int, dict[str, list]] = {}

# Создаём своц класс фабрики колбэков, указывая префикс
# и структуру callback_data
class FiledCallbackFactory(CallbackData, prefix='user_field'):
    x: int
    y: int

# функция которая пересоздаёт поле для каждого игрока
def reset_field(user_id: int) -> None:
    users[user_id]['ships'] = copy.deepcopy(ships)
    users[user_id]['field'] = [
        [0 for _ in range(FIELD_SIZE)]
        for _ in range(FIELD_SIZE)
    ]

# Функция генерирующая клавиатуру в зависимости от данных
# из матрицы ходов пользователя
def get_field_keyboard(user_id: int) -> InlineKeyboardMarkup:
    array_buttons: list[list[InlineKeyboardButton]] = []

    for i in range(FIELD_SIZE):
        array_buttons.append([])
        for j in range(FIELD_SIZE):
            array_buttons[i].append(InlineKeyboardButton(
                text=LEXICON[users[user_id]['field'][i][j]],
                callback_data=FiledCallbackFactory(x=i, y=j).pack()
            ))
    return InlineKeyboardMarkup(inline_keyboard=array_buttons)

# Этот хэндлер будет срабаьывать на команду /start, записывать
# пользователя в базу данных, обнулять игровое поле и отправлять
# пользователю сообщение с клавиатурой
@dp.message(CommandStart())
async def process_start_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {}
    reset_field(message.from_user.id)
    await message.answer(
        text=LEXICON['/start'],
        reply_markup=get_field_keyboard(message.from_user.id)
    )

# Этот хэндлер будет срабатывать на нажатие любой инлайн-кнопки на поле,
# запускать проверку нажатия и форимирования ответа
@dp.callback_query(FiledCallbackFactory.filter())
async def process_category_process(callback: CallbackQuery,
                                   callback_data: FiledCallbackFactory):
    field = users[callback.from_user.id]['field']
    ships = users[callback.from_user.id]['ships']
    if field[callback_data.x][callback_data.y] == 0 and \
    ships[callback_data.x][callback_data.y] == 0:
        answer = LEXICON['miss']
        field[callback_data.x][callback_data.y] = 1
    elif field[callback_data.x][callback_data.y] == 0 and \
    ships[callback_data.x][callback_data.y] == 1:
        answer = LEXICON['hit']
        field[callback_data.x][callback_data.y] = 2
    else:
        answer = LEXICON['used']

    try:
        await callback.message.edit_text(
            text=LEXICON['next_move'],
            reply_markup=get_field_keyboard(callback.from_user.id)
        )
    except TelegramBadRequest:
        pass
    await callback.answer(answer)

dp.run_polling(bot)
