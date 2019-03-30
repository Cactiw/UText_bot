import time

from bin.player_service import get_player
import work_materials.globals as globals
from work_materials.globals import *

MAX_ALLOWED_COMMANDS_PER_SECOND = 3
IGNORE_PLAYER_SECONDS = 5
MAX_BANS_PER_PLAYER = 3
MUTE_TIME = 20 * 60

messages_from_player = {}
bans_per_player = {}


def commands_count(bot, update):
    curr_id = update.message.from_user.id
    count = messages_from_player.get(curr_id)
    if count is None:
        count = 0
    elif count >= MAX_ALLOWED_COMMANDS_PER_SECOND:
        muted_players.update({curr_id: time.time() + IGNORE_PLAYER_SECONDS})
        bot.send_message(chat_id=curr_id, text="В целях защиты от спама не пишите больше 3 сообщений в секунду")
        curr_ban = bans_per_player.get(curr_id)
        if curr_ban is None:
            curr_ban = 1
        elif curr_ban >= MAX_BANS_PER_PLAYER:
            muted_players.update({curr_id: time.time() + MUTE_TIME})
            bot.send_message(chat_id=curr_id, text="<b>Слишком много спама, бан по причине СПАМ на {0} минут</b>".format(int(MUTE_TIME/60)), parse_mode = 'HTML')
        curr_ban += 1
        bans_per_player.update({curr_id: curr_ban})

    count += 1
    messages_from_player.update({curr_id: count})
    player = get_player(update.message.from_user.id, notify_not_found=False)
    if player is not None:
        player.last_message_time = time.time()
        print('setting time: {}, id: {}'.format(player.last_message_time, player.id))

def ignore(bot, update):
    pass


def zeroing():
    while globals.processing:
        messages_from_player.clear()
        time.sleep(1)
        curr_time = time.time()
        for i in list(muted_players):
            if curr_time >= muted_players.get(i):
                muted_players.pop(i)
