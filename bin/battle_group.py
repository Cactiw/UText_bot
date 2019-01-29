import logging, traceback

from work_materials.globals import dispatcher, build_menu, cursor
from bin.player_service import get_player
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from libs.battle_group import BattleGroup


def group_invite(bot, update, user_data):
    mes = update.message
    group = user_data.get("battle_group")
    if group is None:
        group = BattleGroup(mes.from_user.id)
        user_data.update({"battle_group" : group})
    elif group.creator != mes.from_user.id:
        bot.send_message(chat_id=mes.from_user.id, text="Вы не являетесь создателем группы и не можете приглашать в неё новых игроков")
        return
    id = mes.text.partition(" ")[2]
    if not id.isdigit():
        request = "select id from players where nickname = %s"
        cursor.execute(request, (id,))
        row = cursor.fetchone()
        if row is None:
            bot.send_message(chat_id=mes.from_user.id,
                             text="Игрок не найден. Проверьте правильность ввода.")
            return
        id = row[0]
    creator = get_player(mes.from_user.id)
    invited_player = get_player(id, notify_not_found=False)
    if invited_player is None:
        bot.send_message(chat_id=mes.from_user.id,
                         text="Игрок не найден. Проверьте правильность ввода.")
        return
    if dispatcher.user_data.get(id).get("battle_group") is not None:
        bot.send_message(chat_id=mes.from_user.id, text="Данный игрок уже находится в группе.")
        return
    group.invitations.append(id)
    buttons = [
        InlineKeyboardButton("Да", callback_data="bgiy {0}".format(mes.from_user.id)),
        InlineKeyboardButton("Нет", callback_data="bgin {0}".format(mes.from_user.id))
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, 2))
    bot.send_message(chat_id = id, text = "<b>{0}</b> пригласил вас в свою группу. Вы примете приглашение?".format(creator.nickname),
                     parse_mode = 'HTML', reply_markup=reply_markup)
    bot.send_message(chat_id = mes.from_user.id, text = "Приглашение игроку <b>{0}</b> отправлено!".format(invited_player.nickname),
                     parse_mode = 'HTML')


def battle_group_callback(bot, update, user_data):
    chat_id = update.callback_query.from_user.id
    mes = update.callback_query.message
    data = update.callback_query.data
    player_id = update.callback_query.from_user.id
    player = get_player(player_id)
    if user_data.get("status") != "In Location":
        bot.send_message(chat_id=chat_id, text="Сейчас вы заняты чем-то ещё")
        return
    group_id = int(data.partition(" ")[2])
    group = dispatcher.user_data.get(group_id).get("battle_group")
    if group is None:
        bot.deleteMessage(chat_id=player_id, message_id=mes.message_id)
        bot.send_message(chat_id=player_id, text="Данная группа не найдена")
        return
    if update.callback_query.from_user.id not in group.invitations:
        bot.deleteMessage(chat_id=player_id, message_id=mes.message_id)
        bot.send_message(chat_id=player_id, text="Приглашение не найдено")
        return
    if data.find("bgiy") == 0:
        group.invitations.remove(player_id)
        group.players.append(player_id)
        user_data.update({"battle_group" : group})
        bot.deleteMessage(chat_id=player_id, message_id=mes.message_id)
        bot.send_message(chat_id=player_id, text="Приглашение принято!")
        bot.send_message(chat_id = group.creator, text = "<b>{0}</b> принял ваше приглашение в группу.".format(player.nickname),
                         parse_mode = 'HTML')
    else:
        group.invitations.remove(player_id)
        bot.deleteMessage(chat_id=player_id, message_id=mes.message_id)
        bot.send_message(chat_id=player_id, text="Приглашение отклонено.")
        bot.send_message(chat_id=group.creator,
                         text="<b>{0}</b> отклонил ваше приглашение в группу.".format(player.nickname),
                         parse_mode='HTML')

def group_info(bot, update, user_data):
    mes = update.message
    group = user_data.get("battle_group")
    if group is None:
        bot.send_message(chat_id=mes.chat_id, text="На данный момент вы не состоите в группе. Пригласите кого-нибудь! /group_invite")
        return
    response = "Список игроков в группе:\n"
    response += "⭐️"
    for i in range(len(group.players)):
        player = get_player(group.players[i])
        response += "<b>{0}</b>, <b>{1}</b>, Уровень: <b>{2}</b>\n".format(player.nickname, player.game_class, player.lvl)
        if group.creator == mes.from_user.id and group.creator != player.id:
            response += "Выгнать из группы: /group_kick_{0}\n".format(i)
        response += "\n"
    response += "\nПокинуть группу: /group_leave"
    bot.send_message(chat_id = mes.chat_id, text = response, parse_mode = 'HTML')

def group_kick(bot, update, user_data):
    mes = update.message
    group = user_data.get("battle_group")
    if group is None:
        bot.send_message(chat_id=mes.chat_id,
                         text="На данный момент вы не состоите в группе. Пригласите кого-нибудь! /group_invite")
        return
    if group.creator != mes.from_user.id:
        bot.send_message(chat_id=mes.chat_id, text="Вы не являетесь создателем группы и не можете выгонять игроков.")
        return
    num_player = int(mes.text.split("_")[2])
    if num_player == 0:
        bot.send_message(chat_id=mes.chat_id, text="Вы не можете выгнать себя.")
        return
    kick_id = group.players[num_player]
    kick_user_data = dispatcher.user_data.get(kick_id)
    kick_user_data.pop("battle_group")
    group.players.pop(num_player)
    bot.send_message(chat_id = kick_id, text = "Вас исключили из группы.")
    bot.send_message(chat_id = mes.chat_id, text = "Успешно исключён из группы")

def group_leave(bot, update, user_data):
    mes = update.message
    group = user_data.get("battle_group")
    if group is None:
        bot.send_message(chat_id=mes.chat_id, text="На данный момент вы не состоите в группе.")
        return
    if group.creator == mes.from_user.id:
        for id in group.players:
            try:
                dispatcher.user_data.get(id).pop("battle_group")
            except KeyError:
                logging.error(traceback.format_exc())
            bot.send_message(chat_id = id, text = "Ваша группа была распущена")
        return
    user_data.pop("battle_group")
    try:
        group.players.remove(mes.from_user.id)
    except ValueError:
        logging.error(traceback.format_exc())
    player = get_player(mes.from_user.id)
    bot.send_message(chat_id = group.creator, text = "<b>{0}</b> покинул вашу группу".format(player.nickname), parse_mode = 'HTML')
    bot.send_message(chat_id = mes.chat_id, text = "Вы успешно покинули группу")