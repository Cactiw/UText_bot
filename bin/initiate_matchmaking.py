from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Unauthorized, BadRequest, TelegramError

from work_materials.globals import build_menu, matchmaking_players
from bin.player_service import update_status, get_player
from libs.player_matchmaking import Player_matchmaking
import logging, traceback

def matchmaking_start(bot, update, user_data):
    if user_data.get("status") != "In Location":
        bot.send_message(chat_id=update.message.chat_id, text="Сейчас вы заняты чем-то ещё")
        return
    group = user_data.get("battle_group")
    if group is not None and group.creator != update.message.chat_id:
        bot.send_message(chat_id=update.message.chat_id, text="Только лидер группы может начинать поиск")
        return
    user_data.update(matchmaking = [0, 0, 0])
    button_list = [
        InlineKeyboardButton("1 x 1", callback_data="mm 1x1"),
        InlineKeyboardButton("3 x 3", callback_data="mm 3x3"),
        InlineKeyboardButton("5 x 5", callback_data="mm 5x5")
    ]
    footer_buttons = [
        InlineKeyboardButton("Начать поиск", callback_data="mm start")
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3, footer_buttons=footer_buttons))
    bot.send_message(chat_id=update.message.chat_id,
                     text = "Выберите настройки битвы:\n\n{0}".format("Информация по группе: /group_info" if user_data.get("battle_group") else ""),
                     reply_markup=reply_markup)

def matchmaking_callback(bot, update, user_data):
    mes = update.callback_query.message
    matchmaking = user_data.get("matchmaking")
    if update.callback_query.data == "mm start" or update.callback_query.data == "mm cancel":
        group = user_data.get("battle_group")
        player = get_player(update.callback_query.from_user.id)

        if update.callback_query.data == "mm cancel":
            if user_data.get("status") != "Matchmaking" and user_data.get(
                    "status") != "Battle":  # TODO Как битвы будут готовы, удалить проверку на статус "Battle", сейчас используется для отладки
                bot.send_message(chat_id=update.callback_query.from_user.id, text="Вы не находитесь в поиске битвы")
                return
            player_matchmaking = Player_matchmaking(player, 0, matchmaking, group = group)
            matchmaking_players.put(player_matchmaking)
            bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                                    text="Подбор игроков успешно отменён", show_alert=False)
            try:
                bot.deleteMessage(chat_id=update.callback_query.from_user.id, message_id=mes.message_id)
            except Unauthorized:
                pass
            except BadRequest:
                pass
            new_status = user_data.get('saved_battle_status')
            update_status(new_status, player, user_data)
            matchmaking_start(bot, update.callback_query, user_data)
            return

        #   Начало подбора игроков
        flag = 0
        for i in matchmaking:
            if i == 1:
                flag = 1
                break
        if flag == 0:
            bot.send_message(chat_id=update.callback_query.from_user.id, text="Необходимо выбрать хотя бы один режим")
            bot.answerCallbackQuery(callback_query_id=update.callback_query.id)
            return
        if group is not None and (matchmaking[0] or (group.num_players() > 3 and matchmaking[1]) or (group.num_players() > 5 and matchmaking[2])):
            bot.answerCallbackQuery(callback_query_id=update.callback_query.id)
            bot.send_message(chat_id = update.callback_query.from_user.id, text = "Игроков в группе больше, чем разрешено в выбранных режимах! (Хотя бы одном)")
            return

        status = user_data.get("status")
        player.saved_battle_status = status
        player_matchmaking = Player_matchmaking(player, 1, matchmaking, group=group)
        # bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text = "Подбор игроков успешно запущен!", show_alert = False)
        button_list = [
            InlineKeyboardButton("Отменить подбор игроков", callback_data="mm cancel")
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
        try:
            bot.deleteMessage(chat_id=update.callback_query.from_user.id, message_id=mes.message_id)
        except TelegramError:
            pass
        bot.send_message(chat_id=update.callback_query.from_user.id, text="Подбор игроков запущен!",
                         reply_markup=reply_markup)
        user_data.update(saved_battle_status=status) if status != 'Matchmaking' else 0
        update_status('Matchmaking', player, user_data)
        matchmaking_players.put(player_matchmaking)
        return

    # Настройки матчмейкинга битв
    callback_data = update.callback_query.data
    if callback_data == "mm 1x1":
        matchmaking[0] = (matchmaking[0] + 1) % 2
    elif callback_data == "mm 3x3":
        matchmaking[1] = (matchmaking[1] + 1) % 2
    elif callback_data == "mm 5x5":
        matchmaking[2] = (matchmaking[2] + 1) % 2
    first_button_text = "{0}1 x 1".format('✅' if matchmaking[0] else "")
    second_button_text = "{0}3 x 3".format('✅' if matchmaking[1] else "")
    third_button_text = "{0}5 x 5".format('✅' if matchmaking[2] else "")
    button_list = [
        InlineKeyboardButton(first_button_text, callback_data="mm 1x1"),
        InlineKeyboardButton(second_button_text, callback_data="mm 3x3"),
        InlineKeyboardButton(third_button_text, callback_data="mm 5x5")
    ]
    footer_buttons = [
        InlineKeyboardButton("Начать поиск", callback_data="mm start")
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3, footer_buttons=footer_buttons))
    try:
        bot.editMessageReplyMarkup(chat_id=mes.chat_id, message_id=mes.message_id, reply_markup=reply_markup)
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id)
    except TelegramError:
        logging.error(traceback.format_exc)
        pass