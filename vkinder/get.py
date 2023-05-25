import datetime

API_VERSION = 5.131
STATUS_SINGLE = 6


def fetch_user(user_id, vk):
    user = {}
    response = vk.method('users.get', {
        'user_id': user_id,
        'v': API_VERSION,
        'fields': 'first_name, last_name, bdate, sex, city, country'})
    for key, value in response[0].items():
        if key == 'city':
            user[key] = value['id']
        elif key == 'bdate' and len(value.split('.')) == 3:
            user['age'] = datetime.datetime.now().year - int(value[-4:])
        else:
            user[key] = value
    return user


def find_couples(user_info, vk, offset):
    response = vk.method('users.search', {
        'sort': 0,
        'count': 50,
        'offset': offset,
        'city': user_info['city'],
        'sex': 3 - user_info['sex'],
        'status': STATUS_SINGLE,
        'has_photo': 1
    })
    try:
        return [item['id'] for item in response['items'] if not item['is_closed']]
    except KeyError():
        return None


def top_photos(response):
    photo_likes_counts = [photo['likes']['count'] + photo['comments']['count'] for photo in response['items']]
    top_likes = sorted(photo_likes_counts, reverse=True)[:3]

    top_photos_list = [photo for photo in response['items'] if (photo['likes']['count'] + photo['comments']['count']) in top_likes]
    return top_photos_list


def get_photos_info(user, vk):
    photos_info = {}
    response = vk.method('photos.get', {
        'owner_id': user,
        'album_id': 'profile',
        'extended': 1
    })
    top_photos_list = top_photos(response)
    photo_ids = [photo['id'] for photo in top_photos_list]
    photos_info[top_photos_list[0]['owner_id']] = photo_ids

    user_id = user
    photo_attachments = [f'photo{user_id}_{photo_id}' for photo_id in photos_info[user_id]]
    attachments_list = [','.join(photo_attachments), user_id]

    return attachments_list
