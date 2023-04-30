from random import randrange

import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime
import get as g
import send as s
import db

#token = "vk1.a.T-KXfnH1TkViemgd55dadbNrXDS1Sm6GaWU3y8F9D-ti0enHGthbrJp_tUnC5AzfbOhaMube22zJJEzJMBqDWnlg3vuw2QXx1jyzTqB_0yqQmMbfBH3HEky6xVmSl63VFWpccXjNmk5sN_GK-81Cc8KlmtPwDpvF-IMW294s7mJ89idEEHzhL6YOTLyU-r-u3tb4eyrHpSzFGadD9qKtBA"
#token2="vk1.a.XSiborj1TwSgwzix2CHliwRUQXth8xV385U55aTGesEtmzVNNUgnotqBzKHyusvnMUf6LByeysf5yilT07fVdEBqGtNCkYj_yWr_nanVQY4qMP8u2mgjVeNolgbRijet3XVtJ-jyhm3pMwrVHe_o6yKxgO8kbG6N7LEAB6EqCLyr0GAyv3WTxQQSLnc6yG5veAldsBd0tdcgAE1ay_szOg"
token=input("введите токен группы")
token2=input("введите токен пользователя")
vk = vk_api.VkApi(token=token)
vk2 = vk_api.VkApi(token=token2)
longpoll = VkLongPoll(vk)

couple_num=0


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text

            if request.lower() == "найди мне пару":
                client_user_id=event.user_id

                lst=(g.couples(g.get_user(client_user_id, vk),vk2))

                attach=g.photos(lst, vk2,couple_num)
                s.send_couple(client_user_id, attach, vk2, 0)
                db.set_data(client_user_id, attach[1])
                couple_num+=1
            else:
                write_msg(event.user_id, "Не понял ваш вопрос")



