from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import get
import send
import db
from config import *

vk_group = vk_api.VkApi(token=TOKEN_GROUP)
vk_user = vk_api.VkApi(token=TOKEN_USER)
longpoll = VkLongPoll(vk_group)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text

            if request.lower() == "найди мне пару":
                client_user_id = event.user_id
                couple_num = db.get_data(client_user_id)
                user_info = get.fetch_user(client_user_id, vk_group)
                if user_info['city'] or user_info['sex']:
                    couple = get.find_couple(user_info, vk_user, couple_num)
                    if couple:
                        attach = get.get_photos_info(couple, vk_user)
                        send.send_message(client_user_id, vk_group,
                                          f"Нашли вам пару\nhttps://vk.com/id{attach[1]}\nХотите еще - попросите снова",
                                          attach[0])
                        couple_num += 1
                        db.set_data(client_user_id, couple_num)
                    else:
                        send.send_message(client_user_id, vk_group, 'Произошла ошибка, попробуйте позже')
                else:
                    send.send_message(client_user_id, vk_group, 'Заполните свой профиль (город, пол), после'
                                                                'чего возвращайтесь')
            else:
                send.send_message(event.user_id, vk_group, 'Не понял Ваш вопрос\nЕсли хотите найти пару введите:'
                                                 '\nНайди мне пару')
