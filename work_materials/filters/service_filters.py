from work_materials.globals import *
from telegram.ext import BaseFilter


class Filter_Is_Admin(BaseFilter):
    def filter(self, message):
        return message.from_user.id in admin_id_list


filter_is_admin= Filter_Is_Admin()