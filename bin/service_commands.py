import work_materials.globals as globals
from work_materials.globals import *

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

def delete_self(bot, update, user_data):
    mes = update.message
    request = "DELETE FROM PLAYERS WHERE id = '{0}'".format(mes.from_user.id)
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
    request = "DROP TABLE inv_{0}".format(mes.from_user.id)
    try:
        cursor.execute(request)
    except:
        error = sys.exc_info()
        response = ""
        for i in range(0, len(error)):
            response += str(sys.exc_info()[i]) + '\n'
        bot.send_message(chat_id=mes.from_user.id, text=response)
        return
    bot.send_message(chat_id = mes.from_user.id, text = "Таблица инвентаря удалена")
    user_data.clear()
    players.pop(mes.from_user.id)
    bot.send_message(chat_id = mes.from_user.id, text = "Удаление игрока завершено")
