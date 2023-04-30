import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime


def fetch_user(user_id, vk):
    user = {}
    response = vk.method('users.get', {'user_id': user_id, 'v': 5.131, 'fields': 'first_name, last_name, bdate, sex, city, country'})
    
    for key, value in response[0].items():
        if key == 'city':
            user[key] = value['id']
        elif key == 'bdate' and len(value.split('.')) == 3:
            user['age'] = datetime.datetime.now().year - int(value[-4:])
        else:
            user[key] = value
            
    return user


def search_users(user_info, vk):
    response = vk.method('users.search', {
        'sort': 0,
        'count': 100,
        'city': user_info['city'],
        'sex': 3 - user_info['sex'],
        'status': 6,
        'has_photo': 1
    })
    users_id_list = [item['id'] for item in response['items'] if not item['is_closed']]
    return users_id_list


def find_popular_photos(response):
    popular_photos = []
    likes_counts = [photo['likes']['count'] + photo['comments']['count'] for photo in response['items']]
    top_likes = sorted(likes_counts, reverse=True)

    for photo in response['items']:
        if len(popular_photos) >= 3:
            break
        if sum([photo['likes']['count'] + photo['comments']['count'] == like_count for like_count in top_likes[:3]]):
            popular_photos.append(photo)

    return popular_photos


def fetch_photos_info(users_id_list, vk, index):
    photos_info = {}
    response = vk.method('photos.get', {
        'owner_id': users_id_list[index],
        'album_id': 'profile',
        'extended': 1
    })

    popular_photos = find_popular_photos(response)
    photos_info[popular_photos[0]['owner_id']] = [photo['id'] for photo in popular_photos]

    user_id = users_id_list[index]
    photo_attachments = [f'photo{user_id}_{photo_id}' for photo_id in photos_info[user_id]]

    attachments_list = [','.join(photo_attachments), user_id]
    return attachments_list


def send_message(user_id, message, vk, key=None):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
    })


def send_photo(user_id, attachments_list, vk, index):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': f"https://vk.com/id{attachments_list[1]}",
        'attachment': attachments_list[index],
        'random_id': randrange(10 ** 7)
    })
