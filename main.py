import wikipedia

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.dispatcher import FSMContext  # Адрес на локальное хранилище - Оперативка
from aiogram.dispatcher.filters.state import State, StatesGroup  # Группа вопросов и вопросы
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Хранилице в памяти, куда будем сохранять
from configs import *

wikipedia.set_lang('ru')

# wiki_zapros = input('Введите поисковые данные: ')
#
# python_page = wikipedia.page(wiki_zapros)

storage = MemoryStorage()  # Открываем хранилице
bot = Bot(token=TOKEN, parse_mode='HTML')  # Подключитесь к боту в телеграме, и редактирование в виде HTML
dp = Dispatcher(bot, storage=storage)  # Объект диспейчера, который будет следить за ботом, сохраняем хранилице


class GetQuestions(StatesGroup):
    ques = State()


@dp.message_handler(commands=['start', 'about', 'help'])
async def command_start(message: Message):
    if message.text == '/start':
        await message.answer(
            f'Здравствуйте <b>{message.from_user.full_name}</b>. Я бот с помощью которого вы можете использовать Википедиа')
        await bot.send_message(message.chat.id, f'''Выберите комманду:
/start
/about
/help
''')
        await get_first_question(message)
    elif message.text == '/about':
        await message.answer(f'Данный бот был создан в домашних условиях')
    elif message.text == '/help':
        await message.answer(
            f'При возникших идеях или же проблемах связанные с ботом просим вас обратиться сюда: <tg-spoiler>@boburxon_raxmatov</tg-spoiler>')


async def get_first_question(message: Message):
    await GetQuestions.ques.set()
    await bot.send_message(message.chat.id, 'Введите вопрос на который хотите узнать ответ: ')


@dp.message_handler(state=GetQuestions.ques)
async def show_questions(message: Message, state: FSMContext):
    python_page = wikipedia.page(message.text)
    print(python_page.url)
    try:
        # print(python_page.html)  # HTML код
        # print(python_page.original_title)  # Заголовок
        # print(python_page.summary)  # Статья
        await message.reply(f'''
HTML страницы: {python_page.url}
Заголовок статьи: {python_page.original_title}
{python_page.summary}
''')

        # Создание файла
        with open('text.txt', 'w', encoding='UTF-8') as file:
            file.write(python_page.original_title + '\n')  # Заполняем текстовый файл # Парсится заголовок
            file.write(python_page.summary + '\n')  # Парсится краткое содержание
            file.write('Ссылка на источник: ' + python_page.url + '\n' * 2)

        await state.finish()

    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, 'Введите вопрос точнее!!!')
        await get_first_question(message)


executor.start_polling(dp)
