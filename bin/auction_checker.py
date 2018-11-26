from work_materials.globals import *
from bin.item_service import *
from bin.player_service import *
import work_materials.globals as globals
import datetime
import time
import pytz

def auction_checker():
    try:
        reconnect_database()
        conn = globals.conn
        cursor = globals.cursor
        cursor2 = conn.cursor()
        while True:
            request = "select item_type, item_id, player_created_id, player_bid_id, price, lot_id from lots where time_end < '{0}'".format(datetime.datetime.now(tz = pytz.timezone('Europe/Moscow')))
            cursor.execute(request)
            row = cursor.fetchone()
            while row:
                item_type = row[0]
                item_id = row[1]
                player_id = row[2]
                player_bid_id = row[3]
                price = row[4]
                lot_id = row[5]
                if player_bid_id is None:
                    player = get_player(player_id)
                    item_response = get_item_and_list(item_type, item_id, player)
                    list = item_response[0]
                    item = item_response[1]
                    player.add_item(list, item, 1)
                    dispatcher.bot.send_message(chat_id=player_id, text="Аукцион закончен, но никто не сделал ставку. Предмет возвращён")
                    request = "delete from lots where lot_id = '{0}'".format(lot_id)
                    cursor2.execute(request)
                    conn.commit()
                    continue
                player = get_player(player_bid_id)
                item_response = get_item_and_list(item_type, item_id, player)
                list = item_response[0]
                item = item_response[1]
                player.add_item(list, item, 1)
                dispatcher.bot.send_message(chat_id=player_bid_id, text = "Поздравляем, аукцион закончен, вы победили!")
                player = get_player(player_id)
                gold = player.resources.get("gold") + price
                player.resources.update(gold=gold)
                dispatcher.bot.send_message(chat_id=player_bid_id, text = "Поздравляем, аукцион закончен, вы получаете <b>{0}</b> золота!".format(price), parse_mode='HTML')
                request = "delete from lots where lot_id = '{0}'".format(lot_id)
                cursor2.execute(request)
                conn.commit()



                row = cursor.fetchone()
            time.sleep(10)

    except KeyboardInterrupt:
        pass        #TODO сделать невозможным прерывание обработки конкретного лота (LOCK)
