import logging
import os
import random
import sys

import requests
from dotenv import load_dotenv


class KnownError(Exception):
    pass


def check_vk_response(response):
    if 'error' in response:
        error_message = response['error']['error_msg']
        raise KnownError(error_message)


def load_img(filename, url):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def load_comic(comic_number, filename):
    url = f'http://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    img_url = response.json()['img']
    load_img(filename, img_url)
    comic_comment = response.json()['alt']
    return comic_comment


def get_quantity_of_comics():
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
    response = response.json()
    check_vk_response(response)
    return response['response']['upload_url']


def load_comic_to_vk_server(filename, url):
    with open(filename, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response = response.json()
        check_vk_response(response)
        return response['server'], response['photo'], response['hash']


def save_comic_to_community(token_vk, api_version, group_id, vk_server, vk_photo, vk_hash):
    url = 'https://api.vk.com/method/photos.saveWallPhoto/'
    payload = {
        'access_token': token_vk,
        'v': api_version,
        'group_id': group_id,
        'photo': vk_photo,
        'server': vk_server,
        'hash': vk_hash,
    }
    response = requests.post(url, params=payload)
    response = response.json()
    check_vk_response(response)
    return response['response'][0]['id'], response['response'][0]['owner_id']


def post_comic_to_the_wall(token_vk, api_version, group_id, message, vk_answer_media_id, vk_answer_owner_id):
    url = 'https://api.vk.com/method/wall.post/'
    payload = {
        'access_token': token_vk,
        'v': api_version,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'message': message,
        'attachments': f'photo{vk_answer_owner_id}_{vk_answer_media_id}'
    }
    response = requests.post(url, params=payload)
    check_vk_response(response.json())


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')
    api_version = '5.130'
    filename = 'comic.png'
    load_dotenv()
    token_vk = os.getenv("VK_ACCESS_TOKEN")
    group_id = os.getenv("VK_GROUP_ID")
    comic_number = random.randint(1, get_quantity_of_comics())
    comic_comment = load_comic(comic_number, filename)
    try:
        adress_for_comic = get_adress_for_comic(token_vk, api_version, group_id)
        vk_server, vk_photo, vk_hash = \
            load_comic_to_vk_server(filename, adress_for_comic)
        vk_answer_media_id, vk_answer_owner_id = \
            save_comic_to_community(
                token_vk,
                api_version,
                group_id,
                vk_server,
                vk_photo,
                vk_hash,
            )
        post_comic_to_the_wall(
            token_vk,
            api_version,
            group_id,
            comic_comment,
            vk_answer_media_id,
            vk_answer_owner_id,
        )
    except KnownError as e:
        logging.error(e)
        sys.exit(1)
    finally:
        os.remove(filename)


if __name__ == '__main__':
    main()
