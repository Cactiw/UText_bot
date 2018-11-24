import vk
import os
import requests
import json
from vk_bot import *

session = vk.Session(access_token = 'd6773804b8d3fdeb90db51c322c4d36c297869428d73b481799521fc148a3c1a55b38cc1e83dc1b72b0c2')
api = vk.API(session, v = '5.50')
updater = Updater(api)
updater.start()












def test(server, key, ts, bot, update):
    while True:
        # Последующие запросы: меняется только ts
        longPoll = requests.post('%s'%server, data = {'act': 'a_check',
                                             'key': key,
                                             'ts': ts,
                                             'wait': 25}).json()


        if longPoll['updates'] and len(longPoll['updates']) != 0:
            for updates in longPoll['updates']:
                if updates['type'] == 'message_new':
                    # Помечаем сообщение от этого пользователя как прочитанное
                    api.messages.markAsRead(peer_id = updates['object']['user_id'])
                    print(updates)
                    buttons = json.dumps({"one_time": False,
                        "buttons": [
                          [{
                            "action": {
                              "type": "text",
                              "payload": "{\"button\": \"1\"}",
                              "label": "Red"
                            },
                            "color": "negative"
                          }]
                        ]
                    })
                    user = User(id = updates['object']['user_id'])
                    message = Update.Message(chat_id = updates['object']['user_id'], text = updates['object']['body'], from_user=user)
                    update = Update(api, message=message)
                    __info_buttons_list = [
                        KeyboardButton('Рюкзак'),
                        KeyboardButton('Импланты'),
                        KeyboardButton('Назад')
                    ]
                    print(__info_buttons_list[0].load)
                    print(build_menu(__info_buttons_list, n_cols=2))
                    info_buttons = ReplyKeyboardMarkup(build_menu(__info_buttons_list, n_cols=2), resize_keyboard=True)
                    #api.messages.send(peer_id=updates['object']['user_id'], message='Привет, пошёл на%%%', keyboard = buttons)
                    bot.send_message(chat_id = update.message.from_user.id, text = "Привет", reply_markup = info_buttons)

        ts = longPoll['ts']