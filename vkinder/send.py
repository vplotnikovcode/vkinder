from random import randrange

import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime


def send_couple(user_id, attach, vk,n):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': f"Нашли вам пару\nhttps://vk.com/id{attach[1]}\n Хотите еще - попросите снова",
        'attachment': attach[n],
        'random_id': randrange(10 ** 7)})