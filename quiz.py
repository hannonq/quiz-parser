import requests

url = 'https://opentdb.com/api.php?amount=10'

GLOBAL_ID = 0


#  starting with the easiest
#  https://opentdb.com/api_config.php
def get_open_trivia_database(url):
    response = requests.get(url).json()
    if not response.get('response_code') == 0:
        print('Error. Check URL')
        return 1

    result = []
    for r in response.get('results'):

        type = r.get('type')

        question = {
            'id': GLOBAL_ID,
            'lang': 'EN_US',
            'category': r.get('category')
        }

        print(r)

get_open_trivia_database(url)