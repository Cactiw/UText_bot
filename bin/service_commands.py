from work_materials.globals import *
from vk_bot import ReplyKeyboardRemove
from bin.player_service import get_player, update_status
from bin.show_general_buttons import show_general_buttons
from bin.lvl_up_player import start
from libs.myJob import MyJob


def sql(bot, update, user_data):
    mes = update.message
    request = mes.text.partition(" ")[2]
    try:
        cursor.execute(request)
    except:
        error = sys.exc_info()
        response = ""
        for i in range(0, len(error)):
            response += str(sys.exc_info()[i]) + '\n'
        bot.send_message(chat_id=mes.from_user.id, text=response)
        return
    conn.commit()
    row = cursor.fetchone()
    response = "Результат запроса: "
    while row:
        for i in range(0, len(row)):
            response += str(row[i]) + " "
        row = cursor.fetchone()
        response += "\n\n"
    bot.send_message(chat_id=mes.from_user.id, text=response)


def return_from_info(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    update_status(user_data.get('saved_status'), player, user_data)
    show_general_buttons(bot, update, user_data)


def update_player(bot, update, args):
    id = None
    if not args:
        id = update.message.from_user.id
    else:
        id = int(args[0])
    player = get_player(id)
    if player is None:
        bot.send_message(chat_id = update.message.from_user.id, text = "Игрок не найден, проверьте синтаксис")
        return
    player.update_from_database()
    bot.send_message(chat_id=update.message.from_user.id, text="Игрок обновлён")


def delete_self(bot, update, user_data):
    mes = update.message
    request = "DELETE FROM players WHERE id = '{0}'".format(mes.from_user.id)
    try:
        cursor.execute(request)
    except:
        error = sys.exc_info()
        response = ""
        for i in range(0, len(error)):
            response += str(sys.exc_info()[i]) + '\n'
        bot.send_message(chat_id=mes.from_user.id, text=response)
        return
    conn.commit()
    bot.send_message(chat_id = mes.from_user.id, text = "Игрок удалён из таблицы игроков")
    request = "DELETE FROM inventory WHERE user_id = '{0}'".format(mes.from_user.id)
    j = travel_jobs.get(mes.from_user.id)
    if j is not None:
        j.job.schedule_removal()
    try:
        cursor.execute(request)
    except:
        error = sys.exc_info()
        response = ""
        for i in range(0, len(error)):
            response += str(sys.exc_info()[i]) + '\n'
        bot.send_message(chat_id=mes.from_user.id, text=response)
        return
    bot.send_message(chat_id = mes.from_user.id, text = "Инвентарь удалён")
    user_data.clear()
    try:
        players.pop(mes.from_user.id)
    except KeyError:
        pass
    bot.send_message(chat_id = mes.from_user.id, text = "Удаление игрока завершено", reply_markup=ReplyKeyboardRemove())
    start(bot, update, user_data)
