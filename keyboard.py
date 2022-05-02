from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import db

def kb_links():
    link_mas = db.links()
    sub = types.InlineKeyboardMarkup(row_width=1)


    x = ''
    
    if len(link_mas) > 1:
        x = 1
    
    for link in link_mas:
        link = link.split(":")[0]
        sub.add(types.InlineKeyboardButton(f'❤️ Перейти на канал {str(x)}', url=f'https://t.me/{link}'))
        if len(link_mas) > 1:
            x = x + 1

    sub.add(
        types.InlineKeyboardButton(f'🤖 Проверить', callback_data = 'check'),
        )
    
    return sub


delete_last = types.InlineKeyboardMarkup(row_width=1)
delete_last.add(
        types.InlineKeyboardButton(f'❌ Закрыть', callback_data = 'Deletelast'),
        )

main_menu = types.InlineKeyboardMarkup(row_width=2)
main_menu.add(
        types.InlineKeyboardButton(f'📃 Обновить данные', callback_data = 'check'),
        types.InlineKeyboardButton(f'💳 Заявка на вывод', callback_data = 'withdraw'),
        )
main_menu.add(
        types.InlineKeyboardButton(f'👨‍👦 Пригласить друга', switch_inline_query=''),
        )

def inline(username, id):
    inline = types.InlineKeyboardMarkup(row_width=1)
    inline.add(
        types.InlineKeyboardButton(f'💵 Получить', url=f'https://t.me/{username}?start={id}'),
        )
    
    return inline


withdraw1 = types.InlineKeyboardMarkup(row_width=2)
withdraw1.add(
        types.InlineKeyboardButton(f'👈 Назад', callback_data = 'check'),
        types.InlineKeyboardButton(f'🙏 Подать заявку', callback_data = 'withdraw_request'),
        )

withdraw2 = types.InlineKeyboardMarkup(row_width=2)
withdraw2.add(
        types.InlineKeyboardButton(f'👈 Назад', callback_data = 'check'),
        )


admin = types.InlineKeyboardMarkup(row_width=2)
admin.add(
        types.InlineKeyboardButton(f'📦 Скачать базу данных', callback_data = 'download_bd'),
        types.InlineKeyboardButton(f'👥 Кол-во пользователей', callback_data = 'amount_users'),
        types.InlineKeyboardButton(f'❌ Закрыть', callback_data = 'Deletelast'),
        )