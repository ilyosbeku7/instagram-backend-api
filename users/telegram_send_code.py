import requests
import threading


class SmsThread(threading.Thread):

    def __init__(self, sms):
        self.sms = sms
        super (SmsThread, self). __init__()

def run(self):
    send_message(self.sms)

def send_message(message_text):

    url = f'https://api.telegram.org/bot6822713325:AAFnZhE3rMa9QbRuqRIZi1E46YkB37Loh6E/sendMessage'
    params = {
        'chat_id': "6822713325",
        "text": message_text,
    }

    response=requests.post(url, data=params)
    return response.json()

def send_sms(sms_text):
    sms_thread=SmsThread(sms_text)
    sms_thread.start()
    sms_thread.join()