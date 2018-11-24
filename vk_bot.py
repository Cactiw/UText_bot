#coding:utf-8
import vk
import json
from signal import signal, SIGINT, SIGTERM, SIGABRT
import logging
import time
import requests
from filters import BaseFilter, Filters
import sys
import traceback


class Bot:

    def __init__(self, api):
        self.api = api

    def send_message(self, chat_id, text, reply_markup = None, parse_mode = None, ):
        self.api.messages.send(peer_id=chat_id, message=text, keyboard=reply_markup)


class CommandHandler:

    def __init__(self, command, function, filters = None, pass_args = False, pass_user_data = False):
        self.command = command
        self.function = function
        self.filters = filters
        #print(command, self.filters)
        self.pass_args = pass_args
        self.pass_user_data = pass_user_data

    def filter(self, message):
        #print(self.filters)
        if self.filters is None:
            return Filters.command(message) and "/{0}".format(self.command) in message.text
        return Filters.command(message) and self.filters(message) and "/{0}".format(self.command) in message.text


class MessageHandler:

    def __init__(self, filters, function, pass_user_data = False):
        self.function = function
        self.filters = filters
        self.pass_user_data = pass_user_data
        self.pass_args = False

    def filter(self, message):
        return Filters.text(message) and self.filters(message)


class Update():

    class Message:
        def __init__(self, chat_id, text, from_user):
            self.chat_id = chat_id
            self.text = text
            self.from_user = from_user


    def __init__(self, api, message):
        self.api = api
        self.message = message

class Updater:

    class Dispatcher:
        def __init__(self, api, bot):
            self.api = api
            self.bot = bot
            self.user_data = {}


        handlers = []
        def add_handler(self, handler):
            self.handlers.append(handler)
            print("adding handler")

        def start(self):
            # Первый запрос к LongPoll: получаем server и key
            longPoll = self.api.groups.getLongPollServer(group_id='174384568')
            server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']
            while True:
                # Последующие запросы: меняется только ts
                longPoll = requests.post('%s' % server, data={'act': 'a_check',
                                                              'key': key,
                                                              'ts': ts,
                                                              'wait': 25}).json()

                if longPoll['updates'] and len(longPoll['updates']) != 0:
                    for updates in longPoll['updates']:
                        if updates['type'] == 'message_new':
                            print(updates)
                            user = User(id=updates['object']['user_id'])
                            message = Update.Message(chat_id=updates['object']['user_id'], text=updates['object']['body'], from_user=user)
                            update = Update(self.api, message=message)
                            for handler in self.handlers:
                                #print(handler)
                                #print(handler.filter)
                                if handler.filter(message):
                                    current_user_data = self.user_data.get(update.message.from_user.id)
                                    if current_user_data is None:
                                        self.user_data.update({message.from_user.id : {}})
                                        current_user_data = self.user_data.get(message.from_user.id)
                                    try:
                                        if handler.pass_user_data is True:
                                            if handler.pass_args is True:
                                                handler.function(self.bot, update, current_user_data, message.text.split(' ')[1:])
                                            else:
                                                handler.function(self.bot, update, current_user_data)
                                        else:
                                            if handler.pass_args is True:
                                                handler.function(self.bot, update, message.text.split(' ')[1:])
                                            else:
                                                handler.function(self.bot, update)
                                        break
                                    except Exception as e:
                                        logging.error(sys.exc_info)
                                        logging.error(e)
                                        traceback.print_exc()

                ts = longPoll['ts']

    def __init__(self, api, bot = None):
        self.running = 0
        self.logger = logging.getLogger(__name__)
        if bot is None:
            self.bot = Bot(api)
        else:
            self.bot = bot
        self.dispatcher = self.Dispatcher(api, self.bot)


    def start(self):
        self.running = 1
        self.dispatcher.start()

    def stop(self):
        self.running = 0
        self.dispatcher.stop()
        globals.processing = 0

    def signal_handler(self, signum, frame):
        self.is_idle = False
        if self.running:
            self.logger.info('Received signal {} ({}), stopping...'.format(
                signum, "stop signal"))
            self.stop()
        else:
            self.logger.warning('Exiting immediately!')
            import os
            os._exit(1)

    def idle(self, stop_signals=(SIGINT, SIGTERM, SIGABRT)):
        """Blocks until one of the signals are received and stops the updater.

        Args:
            stop_signals (:obj:`iterable`): Iterable containing signals from the signal module that
                should be subscribed to. Updater.stop() will be called on receiving one of those
                signals. Defaults to (``SIGINT``, ``SIGTERM``, ``SIGABRT``).

        """
        for sig in stop_signals:
            signal(sig, self.signal_handler)

        self.is_idle = True

        while self.is_idle:
            time.sleep(1)


class User:

    def __init__(self, id):
        self.id = id
        self.username = None

class KeyboardButton:

    def __init__(self, text):

        self.load = [{ "action": {
                          "type": "text",
                          "payload": "{}",
                          "label": "{0}".format(text)
                        },
                        "color": "default"
                      }]


def build_menu(buttons, n_cols):
    #print(buttons)
    #menu_buttons = [buttons[i:i + n_cols].load for i in range(0, len(buttons), n_cols)]

    menu_buttons = [buttons[i].load for i in range(0, len(buttons))]
    #print("menu_buttons = ", menu_buttons)


    #print("menu =", menu)
    return menu_buttons

def ReplyKeyboardMarkup(menu, resize_keyboard = False, one_time_keyboard=False):
    menu = json.dumps({"one_time": one_time_keyboard,
                       "buttons": menu}, ensure_ascii=False)
    return menu

def ReplyKeyboardRemove():
    return json.dumps({"buttons":[],"one_time":True})