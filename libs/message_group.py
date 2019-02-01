message_groups = {}

class MessageInQueue():

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

class MessageGroup:

    def __init__(self):
        self.id = list(message_groups) + 1
        self.messages = []
        message_groups.update({self.id : self})
