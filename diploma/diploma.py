import requests
from time import sleep

VERSION = '5.69'
TOKEN = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'


def validate_user_name(user_name):
    params = {
        'access_token': TOKEN,
        'v': VERSION,
        'user_ids': user_name,
    }
    sleep(0.35)
    print('-')
    response = requests.get('https://api.vk.com/method/users.get', params)
    response_json = response.json()
    try:
        return response_json['response'][0]['id']
    except KeyError:
        return None


def get_user_friends_list(user_id=None):
    params = {
        'access_token': TOKEN,
        'v': VERSION,
        'user_id': user_id,
    }
    sleep(0.35)
    print('-')
    response = requests.get('https://api.vk.com/method/friends.get', params)
    response_json = response.json()
    try:
        return response_json['response']['items']
    except KeyError:
        return None


def get_user_groups_list(user_id=None):
    params = {
        'access_token': TOKEN,
        'v': VERSION,
        'user_id': user_id
    }
    sleep(0.35)
    print('-')
    response = requests.get('https://api.vk.com/method/groups.get', params)
    response_json = response.json()
    try:
        return response_json['response']['items']
    except KeyError:
        return None


def get_group_info(group_id):
    params = {
        'access_token': TOKEN,
        'v': VERSION,
        'group_id': group_id,
        'fields': 'members_count'
    }
    sleep(0.35)
    response = requests.get('https://api.vk.com/method/groups.getById', params)
    response_json = response.json()
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
    import json
    with open("groups.json", "w", encoding="utf-8") as file:
        json.dump(groups, file)
    print('Файл сохранён')


def get_result_for_user(user_id):
    friends_list = get_user_friends_list(user_id)
    current_user_groups_list = set(get_user_groups_list(user_id))
    users_groups_list = []
    for friend_id in friends_list:
        try:
            users_groups_list.append(set(get_user_groups_list(friend_id)))
        except TypeError:
            continue
    users_groups_list_union = set.union(*users_groups_list)
    result_groups_list = current_user_groups_list.difference(users_groups_list_union)
    return result_groups_list


if __name__ == '__main__':
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
