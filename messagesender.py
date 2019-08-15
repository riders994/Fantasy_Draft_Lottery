import json
from fbchat import Client
from fbchat import models


class FacebookMessenger:
    """
    This is a class that I use to send the lottery outcome of my fantasy basketball
    draft directly to a facebook messenger thread. I do this to guarantee that
    the chain of custody of information is completely sanitary (or as sanitary as
    is within reason).
    """

    # I think this tells the chat client that it's a group-chat
    thread_type = models.ThreadType.GROUP

    def __init__(self, creds):
        """
        :param creds: dict. Holds credentials, and thread information for chats.
                      Does not utilize .get() method specifically to error out.
        """
        self.thread_id = creds['thread']
        self.chat_client = Client(creds['email'], creds['pw'])

    def send_message(self, message):
        """
        This is the method that sends messages.
        :param message: str. Message to be sent.
        """
        self.chat_client.send(models.Message(text=message), thread_id=self.thread_id, thread_type=self.thread_type)


if __name__ == '__main__':
    with open('creds.json', 'rb') as file:
        credentials = json.load(file)

    test = FacebookMessenger(credentials)
    test.send_message('lol butts lol')
