from telegram import Bot


class AsyncBot(Bot):

    def __init__(self, token):
        super(AsyncBot, self).__init__(token=token)