import json
import telebot
import random
import requests
from telebot import types

TOKEN = 'Здесь должен быть TOKEN'
QUESTIONS = [
    'Вопрос №1',
    'Вопрос №2',
    'Вопрос №3',
    'Вопрос №4',
    'Вопрос №5',
]

bot = telebot.TeleBot(TOKEN)


def keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.row(key_yes, key_no)
    return keyboard


@bot.message_handler(content_types=['text'])
def get_question(message):
    question = random.choice(QUESTIONS)
    bot.send_message(message.from_user.id, question, reply_markup=keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    bot.edit_message_text(call.message.text, call.message.chat.id, call.message.message_id)

    param = {}
    if call.data == 'yes':
        param = {'answer': 'yes'}
    elif call.data == 'no':
        param = {'answer': 'no'}

    response = requests.get('https://yesno.wtf/api', param)
    gif = json.loads(response.text)["image"]
    bot.send_animation(call.message.chat.id, gif)

    question = random.choice(QUESTIONS)
    bot.send_message(call.message.chat.id, question, reply_markup=keyboard())


bot.polling(none_stop=True, interval=0)
