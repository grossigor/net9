import requests
TOKEN = "AQAAAAAL-e2HAASsqTd8hwZRkki6uzONITZLHA8"


class YMBase:

    def __init__(self, token):
        self.token = token


class YMUser(YMBase):
    def __init__(self, token):
        super().__init__(token)

    def get_counters(self):
        headers = {
            'Authorization': 'OAuth {}'.format(self.token),
            'Content-Type': 'application/x-yametrika+json'
        }
        response = requests.get(
            'https://api-metrika.yandex.ru/management/v1/counters',
            headers=headers
        )
        return response.json()


class Counter(YMBase):
    STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/data'

    def __init__(self, counter_id, token):
        self.counter_id = counter_id
        super().__init__(token)

    def get_visits(self):
        headers = {
            'Authorization': 'OAuth {}'.format(self.token),
            'Content-Type': 'application/x-yametrika+json'
        }
        params = {
            'ids': self.counter_id,
            'metrics': 'ym:s:visits'
        }
        response = requests.get(
            self.STAT_URL,
            headers=headers,
            params=params
        )
        return response.json()

    def get_users(self):
        headers = {
            'Authorization': 'OAuth {}'.format(self.token),
            'Content-Type': 'application/x-yametrika+json'
        }
        params = {
            'ids': self.counter_id,
            'metrics': 'ym:s:users'
        }
        response = requests.get(
            self.STAT_URL,
            headers=headers,
            params=params
        )
        return response.json()

    def get_views(self):
        headers = {
            'Authorization': 'OAuth {}'.format(self.token),
            'Content-Type': 'application/x-yametrika+json'
        }
        params = {
            'ids': self.counter_id,
            'metrics': 'ym:s:pageviews'
        }
        response = requests.get(
            self.STAT_URL,
            headers=headers,
            params=params
        )
        return response.json()


user = YMUser(TOKEN)
counter = Counter(user.get_counters()['counters'][0]['id'], TOKEN)
print(counter.get_visits())
print(counter.get_users())
print(counter.get_views())
