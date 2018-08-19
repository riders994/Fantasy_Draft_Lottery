import json
from fbchat import Client
from fbchat import models


class FacebookMessenger:
    thread_type = models.ThreadType.GROUP

    def __init__(self, creds):
        self.thread_id = creds['thread']
        self.chat_client = Client(creds['email'], creds['pw'])

    def send_message(self, message):
        self.chat_client.send(models.Message(text=message), thread_id=self.thread_id, thread_type=self.thread_type)


if __name__ == '__main__':
    with open('creds.json', 'rb') as file:
        credentials = json.load(file)

    # test = FacebookMessenger(credentials)
    # test.send_message('lol butts lol')
