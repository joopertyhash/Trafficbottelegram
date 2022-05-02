#Разработчик: @mcscroooge
#Разработчик: @mcscroooge
#Разработчик: @mcscroooge


from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, InputTextMessageContent, InlineQueryResultArticle, InlineQuery
import asyncio


from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import Throttled


import sqlite3
import logging
import string, secrets, hashlib

from config import bot_token, admin_id

import db, keyboard


storage = MemoryStorage()
bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
connection = sqlite3.connect('data.db')
q = connection.cursor()

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO,)

class Form(StatesGroup):
    memory = State()


@dp.message_handler(Command("start"), state=None)
async def welcome(message):
    text = 'Вам в подарок отправлено'
    user_id = message.from_user.id
    splited = message.text.split()
    coin = db.prj_info(2)
    min =  db.prj_info(1)
    link_mas = db.links()
    convertList = ' '.join(map(str,link_mas))
    kb_links = keyboard.kb_links()
    if len(link_mas) > 1:
        links_text = 'каналы'
    else:
        links_text = f'*[канал](https://t.me/{convertList.split(":")[0]})*'
    
    if len(link_mas) > 1:
        links_text1 = 'Наши каналы'
    else:
        links_text1 = f'*Наш [канал](https://t.me/{convertList.split(":")[0]})*'
        
    me = await bot.get_me()
    ref = f'https://t.me/{me.username}?start='
    
    links1 = ''
    
    for links in link_mas:
        links = links.split(":")[0]
        links1 += f'https://t.me/{links}\n'
        
        
    if not db.user_exists(user_id):
        db.create_user(user_id)
        if len(splited) == 2:
            if user_id != int(splited[1]):
                if db.user_exists(int(splited[1])):
                    db.update_refers(user_id, splited[1])
                    await bot.send_message(splited[1], 'У вас новый реферал', reply_markup=keyboard.delete_last)
                    text = 'Ваш друг отправил вам'
                    
    
    referals = db.user_info(user_id, 2)
    balance = db.user_info(user_id, 3)
    await message.answer_sticker('CAACAgEAAxkBAAEEeG9iWF_JYBhO4NhWg-Am9QIc9Y00PgAC-QEAAq5M8UTUQz6LVFGQySME')
    
    

    if await check_sub(user_id) == False:
        await message.answer(f'*{text} несколько монет {coin}, чтобы получить их подпишитесь на {links_text} и нажмите на кнопку \n"🤖 Проверить".*', parse_mode="Markdown", reply_markup=kb_links, disable_web_page_preview=True)
    else:
        await message.answer(f'*Привет!\n\nВы можете пригласить друзей и получить криптовалюту в качестве вознаграждения.\n\n👥 Ваша реферальная ссылка:\n{ref}{user_id}\n\nКол-во ваших подтверждённых рефералов: *`{referals}`* ✅\n\n💰 Ваш баланс: *`{balance} {coin}`*\nВывод станет доступен при накоплении *`{min} {coin}`* на балансе.\n\nВаш ID: *`{user_id}`*\n\n{links_text1} в Телеграмме:\n{links1}*', parse_mode="Markdown",reply_markup=keyboard.main_menu, disable_web_page_preview=True)



@dp.message_handler(Command("admin"), state=None)
async def admin(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer(f'*Админ меню*', parse_mode="Markdown", reply_markup=keyboard.admin)
    else:
        pass

    
async def check_sub(user_id):
    array_list = []
    link_mas = db.links()
    for link in link_mas:
        if '+' in link[0]:
            link2 = link.split(":")[1]
        else:
            link2 = '@' + link.split(":")[0]
        chat_member = (await bot.get_chat_member(chat_id=f'{link2}', user_id=user_id))
        if chat_member['status'] == 'left' or chat_member['status'] == 'kicked':
            array_list.append(False)
        else:
            array_list.append(True)

    if False in array_list:
        return False
    else:
        return True







@dp.callback_query_handler(text='check')
async def check(message: types.Message):
    text = 'Вам в подарок отправлено'
    coin = db.prj_info(2)
    min =  db.prj_info(1)
    link_mas = db.links()
    convertList = ' '.join(map(str,link_mas))
    kb_links = keyboard.kb_links()
    me = await bot.get_me()
    ref = f'https://t.me/{me.username}?start='
    
    links1 = ''
    
    for links in link_mas:
        links = links.split(":")[0]
        links1 += f'https://t.me/{links}\n'
    
    referals = db.user_info(message.from_user.id, 2)
    balance = db.user_info(message.from_user.id, 3)
    if len(link_mas) > 1:
        links_text = 'каналы'
    else:
        links_text = f'*[канал](https://t.me/{convertList.split(":")[0]})*'
    
    if len(link_mas) > 1:
        links_text1 = 'Наши каналы'
    else:
        links_text1 = f'*Наш [канал](https://t.me/{convertList.split(":")[0]})*'
    
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if await check_sub(message.from_user.id) == False:
        await bot.send_message(message.from_user.id, f'*{text} несколько монет {coin}, чтобы получить их подпишитесь на {links_text} и нажмите на кнопку \n"🤖 Проверить".*', parse_mode="Markdown", reply_markup=kb_links, disable_web_page_preview=True)
    else:
        await bot.send_message(message.from_user.id, f'*Привет!\n\nВы можете пригласить друзей и получить криптовалюту в качестве вознаграждения.\n\n👥 Ваша реферальная ссылка:\n{ref}{message.from_user.id}\n\nКол-во ваших подтверждённых рефералов: *`{referals}`* ✅\n\n💰 Ваш баланс: *`{balance} {coin}`*\nВывод станет доступен при накоплении *`{min} {coin}`* на балансе.\n\nВаш ID: *`{message.from_user.id}`*\n\n{links_text1} в Телеграмме:\n{links1}*', parse_mode="Markdown",reply_markup=keyboard.main_menu, disable_web_page_preview=True)
    
@dp.callback_query_handler(text='Deletelast')    
async def delete_last_mes(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)


@dp.callback_query_handler(text='withdraw')
async def withdraw(message: types.Message):
    coin = db.prj_info(2)
    min =  db.prj_info(1)
    balance = db.user_info(message.from_user.id, 3)
    if await check_sub(message.from_user.id) == False:
        await check(message)
    else:
        if float(balance) >= float(min):
            await bot.delete_message(message.from_user.id, message.message.message_id)
            await bot.send_message(message.from_user.id, f'*Доступно для вывода *`{balance} {coin}`', parse_mode='Markdown', reply_markup=keyboard.withdraw1)
        else:
            await bot.answer_callback_query(callback_query_id=message.id, show_alert=False, text="❌ У вас недостаточно средств")

@dp.callback_query_handler(text='withdraw_request')
async def withdraw_request(message: types.Message):
    balance = db.user_info(message.from_user.id, 3)
    coin = db.prj_info(2)
    if await check_sub(message.from_user.id) == False:
        await check(message)
    else:
        db.update_balance(message.from_user.id)
        await bot.delete_message(message.from_user.id, message.message.message_id)
        await bot.send_message(message.from_user.id, f'*💳 Создана заявка на выплату *`{balance} {coin}`*\n\nОжидайте ответа администратора*', parse_mode='Markdown', reply_markup=keyboard.withdraw2)
        await bot.send_message(admin_id, f'*💳 Пользователь *`{message.from_user.id}`* создал заявку на выплату *`{balance} {coin}`', parse_mode='Markdown', reply_markup=keyboard.delete_last)



@dp.callback_query_handler(text='download_bd')
async def download_bd(message: types.Message):
    doc = open('data.db', 'rb')
    await bot.send_document(message.from_user.id, doc, reply_markup=keyboard.delete_last)
    


@dp.callback_query_handler(text='amount_users')
async def amount_users(message: types.Message):
    amount = db.amount_users()
    await bot.answer_callback_query(callback_query_id=message.id, show_alert=True, text=f"Кол-во пользователей: {amount}")
    

@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    me = await bot.get_me()
    coin = db.prj_info(2)
    kbinline = keyboard.inline(me.username, inline_query.from_user.id)
    text = f'❤️ Привет, я хочу подарить тебе немного криптовалюты {coin}, присоеденяйся и сможешь получить ещё больше!'
    input_content = InputTextMessageContent(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
    id=result_id,
    title=f'{text}',
    reply_markup = kbinline,
    input_message_content=input_content,
        )
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)

def generate(length):
    letters_and_digits = string.ascii_letters + string.digits
    crypt_rand_string = ''.join(secrets.choice(
        letters_and_digits) for i in range(length))
    return crypt_rand_string


if __name__ == '__main__':
    print('Бот запущен. Разработчик: @mcscroooge')
    executor.start_polling(dp, skip_updates=True)