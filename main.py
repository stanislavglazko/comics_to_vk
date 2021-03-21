import os
import random

import requests
from dotenv import load_dotenv


def load_img(filename, url):
    response = requests.get(url)
    response.raise_for_status()
    filepath = filename
    with open(filepath, 'wb') as file:
        file.write(response.content)


def load_comic(comic_number):
    url = f'http://xkcd.com/{comic_number}/info.0.json'
    if not comic_number:
        url = 'http://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    img_url = response.json()['img']
    load_img('comic.png', img_url)
    comic_comment = response.json()['alt']
    return comic_comment


def quantity_of_comics():
    url = 'http://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['num']


def get_adress_for_comic(token_vk, api_version, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer/'
    payload = {
        'access_token': token_vk,
        'v': api_version,
        'group_id': group_id,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def load_comic_to_vk_server(token_vk, api_version, group_id):
    with open('comic.png', 'rb') as file:
        url = get_adress_for_comic(token_vk, api_version, group_id)
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()


def save_comic_to_community(token_vk, api_version, group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto/'
    vk_answer = load_comic_to_vk_server(token_vk, api_version, group_id)
    vk_server, vk_photo, vk_hash = vk_answer['server'], vk_answer['photo'], vk_answer['hash']
    payload = {
        'access_token': token_vk,
        'v': api_version,
        'group_id': group_id,
        'photo': vk_photo,
        'server': vk_server,
        'hash': vk_hash,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    return response.json()


def post_comic_to_the_wall(token_vk, api_version, group_id, message):
    url = 'https://api.vk.com/method/wall.post/'
    vk_answer = save_comic_to_community(token_vk, api_version, group_id)['response']
    vk_answer_media_id = vk_answer[0]['id']
    vk_answer_owner_id = vk_answer[0]['owner_id']
    payload = {
        'access_token': token_vk,
        'v': api_version,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'message': message,
        'attachments': f'photo{vk_answer_owner_id}_{vk_answer_media_id}'
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()


def main():
    api_version = '5.130'
    group_id = '203432215'
    load_dotenv()
    id_vk = os.getenv("CLIENT_ID")
    token_vk = os.getenv("ACCESS_TOKEN")
    comic_number = random.randint(1, quantity_of_comics())
    comic_comment = load_comic(comic_number)
    post_comic_to_the_wall(token_vk, api_version, group_id, comic_comment)
    os.remove('comic.png')


if __name__ == '__main__':
    main()
