import datetime
import time
import pytz

from telegram.error import BadRequest
from work_materials.globals import *
from work_materials.buttons.auction_buttons import auction_reply_markup
from bin.service_commands import *
from bin.equipment_service import *
from bin.item_service import *
from libs.lot import *


def auction(bot, update):
    response = "Вы вошли в здание аукциона\n\n"
    response += "Список активных лотов: /lots [name]\n"
    response += "Выставить предмет на продажу: /create_lot_{id предмета}_{начальная цена}_{цена выкупа}_{время в часах}\n"
    response += "\nВаши лоты: /my_lots\n"
    response += "Ваши ставки: /my_bids\n"
    bot.send_message(chat_id=update.message.from_user.id, text=response, reply_markup = auction_reply_markup)

def auction_callback(bot, update, user_data):
    response = "Доступные лоты:\n"
    type = update.callback_query.data.split()[1]

    if type == "nahuy":
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id)
        show_general_buttons(bot, update.callback_query.from_user.id, user_data)
        return

    request = "select lot_id, item_name, time_end, price, buyout_price from lots " \
              "where item_type = '{0}' order by time_end limit 10".format(type)
    cursor.execute(request)
    row = cursor.fetchone()
    while row:
        time_end = row[2] - datetime.datetime.now(tz=pytz.timezone('UTC'))
        new_response = "<b>{0}</b>\nТекущая цена - 💰<b>{1}</b>\nВремя до окончания: <b>{2}</b>\nСделать ставку: /bet_{3}_[Новая цена]\n\n".format(
            row[1], row[3], time_end, row[0])
        response += new_response

        row = cursor.fetchone()
    try:
        bot.editMessageText(chat_id=update.callback_query.from_user.id, message_id=update.callback_query.message.message_id,
                            text=response, parse_mode='HTML', reply_markup=auction_reply_markup)
    except BadRequest:
        pass
    bot.answerCallbackQuery(callback_query_id=update.callback_query.id)

def create_lot(bot, update):
    print(time.time())
    args = update.message.text.split("_")
    if len(args) < 6:
        bot.send_message(chat_id=update.message.from_user.id, text="Неверный синтаксис")
        return
    equipment_id = int(args[2])
    price = int(args[3])
    buyout_price = int(args[4])
    duration = float(args[5])

    if price <= 0 or buyout_price <= 0 or duration <= 0:
        bot.send_message(chat_id=update.message.from_user.id, text="Цена и время должны быть строго положительны!")
        return

    equipment = get_equipment(equipment_id)
    if equipment is None:
        bot.send_message(chat_id=update.message.from_user.id, text="Указанный предмет не найден")
        return
    player = get_player(update.message.from_user.id)
    if player is None:
        return
    if player.remove_item(player.eq_backpack, equipment, 1) != 0:
        bot.send_message(chat_id=update.message.from_user.id, text="Убедитесь, что указанный предмет в инвентаре")
        return
    lot = Lot(equipment, player, price, buyout_price, duration)
    new_id = lot.create()
    bot.send_message(chat_id=update.message.from_user.id, text="Лот № <b>{0}</b> успешно создан\nОтменить лот: /cancel_lot_{0}".format(new_id), parse_mode='HTML')



def cancel_lot(bot, update):
    request = "select item_type, item_id, player_bid_id, price from lots where lot_id = '{0}' and player_created_id = '{1}'".format(update.message.text.split("_")[2], update.message.from_user.id)
    cursor.execute(request)
    row = cursor.fetchone()
    if row is None:
        bot.send_message(chat_id=update.message.from_user.id, text="Указанный лот не найден")
        return
    item_type = row[0]
    item_id = row[1]
    player_bid_id = row[2]
    price = row[3]
    player = get_player(update.message.from_user.id)
    item_response = get_item_and_list(item_type, item_id, player)
    list = item_response[0]
    item = item_response[1]
    player.add_item(list, item, 1)
    request = "delete from lots where lot_id = '{0}'".format(update.message.text.split("_")[2])
    cursor.execute(request)
    conn.commit()
    if player_bid_id is None:
        bot.send_message(chat_id=update.message.from_user.id, text="Лот успешно отменён")
        return
    player = get_player(player_bid_id)
    gold = player.resources.get("gold") + price
    player.resources.update(gold = gold)
    bot.send_message(chat_id=player_bid_id, text="Лот, на который вы сделали ставку, был отменён. Золото возвращено.")
    bot.send_message(chat_id=update.message.from_user.id, text="Лот успешно отменён")


def bet(bot, update):
    args = update.message.text.split("_")
    request = "select price, player_bid_id from lots where lot_id = '{0}'".format(args[1])
    cursor.execute(request)
    row = cursor.fetchone()
    if row is None:
        bot.send_message(chat_id=update.message.from_user.id, text="Указанный лот не найден")
        return
    price = int(row[0])
    new_price = int(args[2])
    if new_price <= price:
        bot.send_message(chat_id=update.message.from_user.id, text="Новая цена должна быть больше текущей")
        return
    player_bid_id = row[1]
    if player_bid_id == update.message.from_user.id:
        bot.send_message(chat_id=update.message.from_user.id, text="Вы не можете перебивать свою же ставку")
        return
    player = get_player(update.message.from_user.id)
    gold = player.resources.get("gold")
    if new_price > gold:
        bot.send_message(chat_id=update.message.from_user.id, text="Не хватает денег")
        return
    gold -= new_price
    player.resources.update(gold=gold)
    request = "update lots set price = '{0}', player_bid_id = '{1}' where lot_id = '{2}'".format(new_price, update.message.from_user.id, args[1])   #TODO сделать увеличение времени, если оно почти кончилось
    cursor.execute(request)
    conn.commit()
    bot.send_message(chat_id=update.message.from_user.id, text="Ставка успешно сделана")
    if player_bid_id is not None:
        player = get_player(player_bid_id)
        gold = player.resources.get("gold") + price
        player.resources.update(gold=gold)
        bot.send_message(chat_id=player_bid_id, text="Ваша ставка была перебита. Золото возвращено.")


def lots(bot, update):
    item_name = "" + update.message.text.partition(" ")[2]
    request = "select lot_id, item_name, time_end, price, buyout_price from lots where item_name ~* '{0}' order by time_end".format(item_name)
    cursor.execute(request)
    row = cursor.fetchone()
    response = "Список лотов:\n\n"
    while row:
        time_end = row[2] - datetime.datetime.now(tz = pytz.timezone('UTC'))
        new_response = "<b>{0}</b>\nТекущая цена - 💰<b>{1}</b>\nВремя до окончания: <b>{2}</b>\nСделать ставку: /bet_{3}_[Новая цена]\n\n".format(row[1], row[3], time_end, row[0])

        if len(response + new_response) >= 4096:
            bot.send_message(chat_id=update.message.from_user.id, text=response, parse_mode='HTML')
            response = ""
        response += new_response

        row = cursor.fetchone()
    bot.send_message(chat_id=update.message.from_user.id, text=response, parse_mode='HTML')


def my_lots(bot, update):
    item_name = "" + update.message.text.partition(" ")[2]
    request = "select lot_id, item_name, time_end, price, buyout_price from lots where item_name ~* '{0}' and player_created_id = '{1}' order by time_end".format(
        item_name, update.message.from_user.id)
    cursor.execute(request)
    row = cursor.fetchone()
    response = "Список ваших лотов:\n\n"
    while row:
        time_end = row[2] - datetime.datetime.now(tz=pytz.timezone('UTC'))
        new_response = "<b>{0}</b>\nТекущая цена - 💰<b>{1}</b>\nВремя до окончания: <b>{2}</b>\n\n\n".format(
            row[1], row[3], time_end)
        if len(response + new_response) >= 4096:
            bot.send_message(chat_id=update.message.from_user.id, text=response, parse_mode='HTML')
            response = ""
        response += new_response
        row = cursor.fetchone()
    bot.send_message(chat_id=update.message.from_user.id, text=response, parse_mode='HTML')


def my_bids(bot, update):
    item_name = "" + update.message.text.partition(" ")[2]
    request = "select lot_id, item_name, time_end, price, buyout_price from lots where item_name ~* '{0}' and player_bid_id = '{1}' order by time_end".format(
        item_name, update.message.from_user.id)
    cursor.execute(request)
    row = cursor.fetchone()
    response = "Список ваших ставок:\n\n"
    while row:
        time_end = row[2] - datetime.datetime.now(tz=pytz.timezone('UTC'))
        new_response = "<b>{0}</b>\nТекущая цена - 💰<b>{1}</b>\nВремя до окончания: <b>{2}</b>\n\n\n".format(
            row[1], row[3], time_end)
        if len(response + new_response) >= 4096:
            bot.send_message(chat_id=update.message.from_user.id, text=response, parse_mode='HTML')
            response = ""
        response += new_response
        row = cursor.fetchone()
    bot.send_message(chat_id=update.message.from_user.id, text=response, parse_mode='HTML')