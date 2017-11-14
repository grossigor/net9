import requests
from time import sleep

VERSION = '5.69'
TOKEN = '0fb186691a6036fc462d03ee480447c8decf248813fa38a93cf2542319867bc6b4e2edc729bbf90dac47b'


def get_user_friends_list(user_id=None):
    params = {
        'access_token': TOKEN,
        'v': VERSION,
        'user_id': user_id,
    }
    sleep(0.35)
    response = requests.get('https://api.vk.com/method/friends.get', params)
    response_json = response.json()
    try:
        return response_json['response']['items']
    except KeyError:
        return None


if __name__ == '__main__':
    my_friends_list = get_user_friends_list()
    user_friends_list = [set(get_user_friends_list(user_id)) for user_id in my_friends_list]
    user_friends_list_intersection = set.intersection(*user_friends_list)
