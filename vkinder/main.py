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
couples_dict = dict()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text

            if request.lower() == "найди мне пару":
                client_user_id = event.user_id
                couple_num = db.get_data(client_user_id, 'offset')
                couple_num = couple_num[0][0] if couple_num else 0
                user_info = get.fetch_user(client_user_id, vk_group)
                if 'city' in user_info and 'sex' in user_info:
                    if event.user_id not in couples_dict or not couples_dict[event.user_id]:
                        couples_dict[client_user_id] = get.find_couples(user_info, vk_user, couple_num)
                    showed_couples = db.get_data(client_user_id, 'couples')
                    if showed_couples and len(showed_couples) == 1:
                        showed_couples = showed_couples[0][0]
                    showed_couples = showed_couples.split(', ') if type(showed_couples) == str else []
                    showed_couples = list(map(int, list(showed_couples))) if showed_couples else []
                    couple = couples_dict[client_user_id].pop(0)
                    if showed_couples:
                        while (couple in showed_couples) and couples_dict[client_user_id]:
                            couple = couples_dict[client_user_id].pop(0)
                    if couple:
                        attach = get.get_photos_info(couple, vk_user)
                        send.send_message(client_user_id, vk_group,
                                          f"Нашли вам пару\nhttps://vk.com/id{attach[1]}\nХотите еще - попросите снова",
                                          attach[0])
                        couple_num += 1
                        showed_couples.append(couple)
                        text = ', '.join(list(map(str, showed_couples))) if len(showed_couples) > 1 else str(couple)
                        db.set_data(client_user_id, couple_num, text)
                    else:
                        send.send_message(client_user_id, vk_group, 'Произошла ошибка, попробуйте позже')
                else:
                    send.send_message(client_user_id, vk_group, 'Заполните свой профиль (город, пол), после '
                                                                'чего возвращайтесь')
            else:
                send.send_message(event.user_id, vk_group, 'Не понял Ваш вопрос\nЕсли хотите найти пару введите:'
                                                 '\nНайди мне пару')
