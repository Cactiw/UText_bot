from telegram import Bot
from telegram.utils.request import Request


class AsyncBot(Bot):

    def __init__(self, token, workers = 4, request_kwargs = None):
        if request_kwargs is None:
            request_kwargs = {}
        con_pool_size = workers + 4
        if 'con_pool_size' not in request_kwargs:
            request_kwargs['con_pool_size'] = con_pool_size
        self._request = Request(**request_kwargs)
        super(AsyncBot, self).__init__(token=token, request=self._request)