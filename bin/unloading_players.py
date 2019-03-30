import time
import logging
import traceback
from work_materials.globals import players
import work_materials.globals as globals

LOAD_OUT_CHECK_EVERY_MINUTES = 5
LOAD_OUT_MINUTES_LIMIT = 30


def player_monitor():
    while globals.processing:
        try:
            players_list = list(players.values())
            for player in players_list:
                print(player.last_message_time, time.time() - player.last_message_time)
                print(player)
                if player.last_message_time is not None and \
                        time.time() - player.last_message_time > LOAD_OUT_MINUTES_LIMIT * 60:
                    try:
                        players.pop(player.id)
                    except Exception:
                        logging.error(traceback.format_exc())
            for i in range(int(LOAD_OUT_CHECK_EVERY_MINUTES * 60)):
                if not globals.processing:
                    return 0
                time.sleep(1)
        except Exception:
            logging.error(traceback.format_exc())
