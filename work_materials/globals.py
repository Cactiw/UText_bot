from telegram import KeyboardButton, ReplyKeyboardMarkup
import psycopg2, pytz, tzlocal
from multiprocessing import Queue
from libs.locations.capital import *
from libs.locations.castle import *
from libs.locations.farm_location import *
from libs.locations.headquarters import *
from libs.locations.portal import *
from libs.locations.resource_loc import *
from libs.locations.tower import *
from libs.bot_async_messaging import AsyncBot
from libs.updater_async import AsyncUpdater
from libs.enemies import AIDSEnemy, AIDSEnemy_first_skill, AIDSEnemy_second_skill
from libs.skill import attack_skill, operator_first_skill, operator_second_skill, operator_third_skill, operator_fourth_skill, operator_fifth_skill, \
                        hacker_first_skill, hacker_second_skill, hacker_third_skill, hacker_fourth_skill, hacker_fifth_skill, \
                        gunner_first_skill, gunner_second_skill, gunner_third_skill, gunner_fourth_skill, gunner_fifth_skill, \
                        biomechanic_first_skill, biomechanic_second_skill, biomechanic_third_skill, biomechanic_fourth_skill, biomechanic_fifth_skill, \
                        skip_turn_skill

try:
    from config import request_kwargs
except ImportError:
    request_kwargs = None

bot = AsyncBot(token='757939309:AAE3QMqbT8oeyZ44es-l6eSzxpy1toCf_Bk', workers=8, request_kwargs=request_kwargs)
updater = AsyncUpdater(bot = bot, persistence=None)
job = updater.job_queue

dispatcher = updater.dispatcher
print(dispatcher.user_data)

STATUS_REPORT_CHANNEL_ID = -1001275825401
ALERT_NOTIFICATIONS_CHANNEL_ID = -1001437688300
moscow_tz = pytz.timezone('Europe/Moscow')
try:
    local_tz = tzlocal.get_localzone()
except pytz.UnknownTimeZoneError:
    local_tz = pytz.timezone('Europe/Andorra')

muted_players = {}

players = {}
players_need_update = Queue()
travel_jobs = {}

matchmaking_players = Queue()

pending_battles = {}
battles_need_treating = Queue()
treated_battles = Queue()
battle_with_bots_to_set = Queue()

#Подключаем базу данных, выставляем кодировку
passwd = 'fiP3Gahz'

conn = psycopg2.connect("dbname=UText_bot user=UText_bot password={0}".format(passwd))
conn.set_session(autocommit = True)
cursor = conn.cursor()
print("Connection successful, starting bot")

skills = {
    'Оператор': {
        attack_skill.name: attack_skill,
        operator_first_skill.name: operator_first_skill,
        operator_second_skill.name: operator_second_skill,
        operator_third_skill.name: operator_third_skill,
        operator_fourth_skill.name: operator_fourth_skill,
        operator_fifth_skill.name: operator_fifth_skill,
        skip_turn_skill.name: skip_turn_skill
    },
    'Канонир': {
        attack_skill.name: attack_skill,
        gunner_first_skill.name: gunner_first_skill,
        gunner_second_skill.name: gunner_second_skill,
        gunner_third_skill.name: gunner_third_skill,
        gunner_fourth_skill.name: gunner_fourth_skill,
        gunner_fifth_skill.name: gunner_fifth_skill,
        skip_turn_skill.name: skip_turn_skill
    },
    'Хакер': {
        attack_skill.name: attack_skill,
        hacker_first_skill.name: hacker_first_skill,
        hacker_second_skill.name: hacker_second_skill,
        hacker_third_skill.name: hacker_third_skill,
        hacker_fourth_skill.name: hacker_fourth_skill,
        hacker_fifth_skill.name: hacker_fifth_skill,
        skip_turn_skill.name: skip_turn_skill
    },
    'Биомеханик': {
        attack_skill.name: attack_skill,
        biomechanic_first_skill.name: biomechanic_first_skill,
        biomechanic_second_skill.name: biomechanic_second_skill,
        biomechanic_third_skill.name: biomechanic_third_skill,
        biomechanic_fourth_skill.name: biomechanic_fourth_skill,
        biomechanic_fifth_skill.name: biomechanic_fifth_skill,
        skip_turn_skill.name: skip_turn_skill
    },
    'AI_AIDSEnemy' : {
        attack_skill.name: attack_skill,
        AIDSEnemy_first_skill.name: AIDSEnemy_first_skill,
        AIDSEnemy_second_skill.name: AIDSEnemy_second_skill,
        skip_turn_skill.name: skip_turn_skill
    },
    'AI' : {
        attack_skill.name: attack_skill,
        skip_turn_skill.name: skip_turn_skill
    }
}


def get_skill(game_class, skill_name):
    return skills.get(game_class).get(skill_name)


skill_names = {}

admin_id_list = [231900398, 212657053, 307125511]    #   618831598 - мой твинк (Князь)

processing = 1

locations = {1: portal, 2: feds_castle, 3: trib_castle, 4: stai_castle, 5: feds_south_tower, 6: feds_north_tower, 7: trib_south_tower,
             8: trib_north_tower, 9: stai_south_tower, 10: stai_north_tower, 11: resources_btw_HE, 12: resources_btw_EO, 13: resources_btw_HO,
             14: feds_capital, 15: trib_capital, 16: stai_capital, 17: feds_guild_castle, 18: trib_guild_castle, 19: stai_guild_castle,
             20: feds_forest, 21: feds_mine, 22: trib_forest, 23: trib_mine, 24: stai_forest, 25: stai_mine, 26: feds_farm_loc_010,
             27: feds_farm_loc_1020, 28: feds_farm_loc_2030, 29: feds_farm_loc_3040, 30: feds_farm_loc_4050, 31: trib_farm_loc_010,
             32: trib_farm_loc_1020, 33: trib_farm_loc_2030, 34: trib_farm_loc_3040, 35: trib_farm_loc_4050, 36: stai_farm_loc_010,
             37: stai_farm_loc_1020, 38: stai_farm_loc_2030, 39: stai_farm_loc_3040, 40: stai_farm_loc_4050}


def build_menu(buttons, n_cols, header_buttons = None, footer_buttons = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def format_time(time):
    time_str = ''
    time_str += str(int(time // 60))
    time_str += ':'
    sec = int(time % 60)
    if sec < 10:
        time_str += '0'
    time_str += str(sec)
    return time_str


__info_buttons_list = [
    KeyboardButton('Рюкзак'),
    KeyboardButton('Импланты'),
    KeyboardButton('Назад')
]
info_buttons = ReplyKeyboardMarkup(build_menu(__info_buttons_list, n_cols=2), resize_keyboard=True)


def reconnect_database():
    global conn
    global cursor
    conn = psycopg2.connect("dbname=UText_bot user=UText_bot password={0}".format(passwd))
    conn.set_session(autocommit=True)
    cursor = conn.cursor()
    print("reconnected")
