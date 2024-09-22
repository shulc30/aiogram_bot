import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

# Токен Telegram бота
BOT_TOKEN = 'TOKEN'

# Создаём объект бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Количество попыток доступных пользователю в игре
ATTEMPTS = 5

# Словарь в котором будут храниться данные пользователя
user = {}


# Функция возвращающая число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)

# Этот хэндлер будет срабатыватьна команду /start
@dp .message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет! \nДавай сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список '
        'команд - отправб команду /help'
    )
    # Если пользователь только запустил бота и его нет в словаре
    # 'user' - добавляем его  в словарь
    if message.from_user.id not in user:
        user[message.from_user.id] = {
            'in_game': False, 
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }

# Этот хэндлер будет срабатывать на команду /help
@dp .message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а Вам нужно его угадать\nУ Вас есть {ATTEMPTS} '
        f'попыток \n\nЖоступные команды:\n/help - правила игры'
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/start -  посмотреть статистику\n\nДавай сыграем?'
    )

# Этот хэндлер будет срабатывать на команду /start
@dp .message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer(
        f'Всего игр сыграно: '
        f'{user[message.from_user.id]["total_games"]}\n'
        f'Игр выиграно: {user[message.from_user.id]["wins"]}'
    )

# Этот хэндлер будет срабатывать на команду "/cancel"
@dp .message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if user[message.from_user.id]['in_game']:
        user[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если хотите сфграть '
            'сноыва - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с Вами не играем. '
            'Может сыграем разок?'
        )
# Этот хэндлер срабатывает на согласие пользователя сыграть в игру
@dp .message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                 'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not user[message.from_user.id]['in_game']:
        user[message.from_user.id]['in_game'] = True
        user[message.from_user.id]['secret_number'] = get_random_number()
        user[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100,'
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команду /cancek и /start'
        )
# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp .message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not user[message.from_user.id]['in_game']:
        await message.answer(
            'Халь :(\n\nЕсли хотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с Вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )

# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp .message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if user[message.from_user.id]['in_game']:
        if int(message.text) == user[message.from_user.id]['secret_number']:
            user[message.from_user.id]['in_game'] = False
            user[message.from_user.id]['total_games'] += 1
            user[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может сыграем ещё?'
            )
        elif int(message.text) > user[message.from_user.id]['secret_number']:
            user[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < user[message.from_user.id]['secret_number']:
            user[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число больше')

        if user[message.from_user.id]['attempts'] == 0:
            user[message.from_user.id]['in_game'] = False
            user[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению у Вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {user[message.from_user.id]["secret_number"]}\n\nДавайте '
                f'сыграем ещё?'
            )
        else:
            await message.answer('Мы ещё не играем. Хотите сыграть?')

# Этот жзгдлер будет срабатывать на любое сообщение
@dp .message()
async def process_other_answers(message: Message):
    if user[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с Вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )

if __name__ == '__main__':
    dp.run_polling(bot)