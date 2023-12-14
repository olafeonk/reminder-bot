import datetime

import telebot
import logging
from ..api.api import create_task, list_tasks
from ..config import BOT_TOKEN

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = telebot.TeleBot(BOT_TOKEN)

user_states = {}


class BotState:
    def __init__(self):
        self.message = ''
        self._state = 'start'

    def start(self):
        self.message = ''
        self._state = 'start'

    def select_time(self, message):
        self.message = message
        self._state = 'select_time'

    @property
    def state(self) -> str:
        return self._state


def get_user_state(chat_id) -> BotState:
    return user_states.get(chat_id, BotState())


def set_user_state(chat_id, state: BotState):
    user_states[chat_id] = state


def handle_error(error):
    logging.error(f"Ошибка: {str(error)}")


def parse_time(text):
    text = datetime.datetime.strptime(text, '%H:%M %d.%m.%Y')
    return text


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    state = get_user_state(chat_id)
    state.start()
    set_user_state(chat_id, state)
    bot.send_message(chat_id, "Привет! Напишите заметку, мы ее запомним)")


@bot.message_handler(commands=["my_ticket"])
def handle_list_tasks(message):
    chat_id = message.chat.id
    user_state = get_user_state(chat_id)
    user_state.start()
    messages = list_tasks(chat_id)
    bot.send_message(chat_id, "Ваши заметки 📝")
    for message in messages:
        bot.send_message(chat_id, f'```\n{message[0]}\n```', parse_mode='MarkdownV2')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_state = get_user_state(chat_id)

    bot.send_message(chat_id, f'Мы записали вашу заметку 😊\n```\n{message.text}\n```\n', parse_mode='MarkdownV2')
    create_task(chat_id, message.text, datetime.datetime.now())
    user_state.start()
    set_user_state(chat_id, user_state)


def bot_start():
    bot.polling(none_stop=True)
