from random import randrange


def send_message(user_id, vk, message, attach=None):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'attachment': attach if attach else '',
        'random_id': randrange(10 ** 7)})
