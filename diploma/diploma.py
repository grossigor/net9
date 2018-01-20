import json
import requests
from time import sleep

VERSION = '5.69'
TOKEN = 'secret'


def get_token():
    with open("token.json") as file:
        data = json.load(file)
        return data["TOKEN"]


def do_request(method, **kwargs):
    params = {
        'access_token': TOKEN,
        'v': VERSION
    }
    params.update(kwargs)
    while True:
        try:
            print('-')
            response = requests.get(method, params)
            response.raise_for_status()
            response_json = response.json()
            if 'error' in response_json.keys():
                code = response_json['error']
                if code == 6:
                    sleep(0.35)
                    continue
            else:
                return response_json
        except requests.exceptions.HTTPError:
            print('HTTP Error')
            continue


def validate_user_name(user_name):
    response_json = do_request('https://api.vk.com/method/users.get', user_ids=user_name)
    try:
        return response_json['response'][0]['id']
    except KeyError:
        return None


def get_user_friends_list(user_id=None):
    response_json = do_request('https://api.vk.com/method/friends.get', user_id=user_id)
    try:
        return response_json['response']['items']
    except KeyError:
        return None


def get_user_groups_list(user_id=None):
    response_json = do_request('https://api.vk.com/method/groups.get', user_id=user_id)
    try:
        return response_json['response']['items']
    except KeyError:
        return None


def get_group_info(group_id):
    response_json = do_request('https://api.vk.com/method/groups.getById',
                               group_id=group_id, fields='members_count')
    try:
        group_info = {
            'id': response_json['response'][0]['id'],
            'name': response_json['response'][0]['name'],
            'members_count': response_json['response'][0]['members_count']
        }
        return group_info
    except KeyError:
        return None


def save_groups_to_json(groups):
    with open("groups.json", "w") as file:
        json.dump(groups, file)
    print('Файл сохранён')


def get_result_for_user(user_id):
    friends_list = get_user_friends_list(user_id)
    current_user_groups_list = set(get_user_groups_list(user_id))
    users_groups_list = []
    for friend_id in friends_list:
        if get_user_groups_list(friend_id) is None:
            continue
        else:
            users_groups_list.append(set(get_user_groups_list(friend_id)))
    users_groups_list_union = set.union(*users_groups_list)
    result_groups_list = current_user_groups_list.difference(users_groups_list_union)
    return result_groups_list


if __name__ == '__main__':
    TOKEN = get_token()
    print('Введите идентификатор или имя пользователя')
    user_name = input()
    validated_user_name = validate_user_name(user_name)
    if validated_user_name is not None:
        result_groups_list = get_result_for_user(validated_user_name)
        groups = []
        for group_id in result_groups_list:
            groups.append(get_group_info(group_id))
        save_groups_to_json(groups)
    else:
        print('Неправильное имя пользователя')
