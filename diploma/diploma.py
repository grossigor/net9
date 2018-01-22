import json
import requests
from time import sleep

VERSION = '5.69'
TOKEN = 'secret'
TOO_MANY_REQUESTS_CODE = 6
PERMISSION_DENIED = 7
USER_DELETED_OR_BANNED = 18


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
    url = 'https://api.vk.com/method/' + method
    while True:
        try:
            print('-')
            response = requests.get(url, params)
            response.raise_for_status()
            response_json = response.json()
            if 'error' in response_json:
                code = response_json['error']['error_code']
                if code == TOO_MANY_REQUESTS_CODE:
                    print('Ошибка: Слишком много запросов в секунду. Запрос повторяется')
                    sleep(0.35)
                    continue
                if code == USER_DELETED_OR_BANNED:
                    print('Ошибка: Пользователь был удалён или заблокирован. Запрос будет пропущен.')
                    print(response_json)
                    return response_json
                if code == PERMISSION_DENIED:
                    print('Ошибка: Отсутствуют права для выполнения действия. Запрос будет пропущен.')
                    print(response_json)
                    return response_json
                else:
                    print('Неопознаная ошибка. Запрос {0} вернул ответ:'.format(method))
                    print(response_json)
                    return response_json
            else:
                return response_json
        except requests.exceptions.HTTPError as err:
            print('Ошибка: HTTP Error. Приостановите работу программы и попробуйте позже')
            print(err)
            continue


def validate_user_name(user_name):
    response_json = do_request('users.get', user_ids=user_name)
    try:
        return response_json['response'][0]['id']
    except KeyError:
        return None


def get_user_friends_list(user_id=None):
    response_json = do_request('friends.get', user_id=user_id)
    try:
        return response_json['response']['items']
    except KeyError:
        return None


def get_user_groups_list(user_id=None):
    response_json = do_request('groups.get', user_id=user_id)
    try:
        return response_json['response']['items']
    except KeyError:
        return None


def get_group_info(group_id):
    response_json = do_request('groups.getById', group_id=group_id, fields='members_count')
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
    validated_user_id = validate_user_name(user_name)
    if validated_user_id is not None:
        result_groups_list = get_result_for_user(validated_user_id)
        groups = []
        for group_id in result_groups_list:
            groups.append(get_group_info(group_id))
        save_groups_to_json(groups)
    else:
        print('Неправильное имя пользователя')
