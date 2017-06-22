import requests
import random
import pprint
from collections import OrderedDict
import json

pp = pprint.PrettyPrinter(indent=4)
url = 'https://opentdb.com/api.php?amount=50'

QUESTION_ID = 0
REQUEST_AMOUNT = 5
LOOP_COUNT = 0

#  starting with the easiest
#  https://opentdb.com/api_config.php
def get_open_trivia_database(url):

    def get_choices(r):
        choice_id = 0
        answers = [r.get('correct_answer')] + r.get('incorrect_answers')
        random.shuffle(answers)
        choices = []
        right_id = None
        for choice in answers:
            choices.append(
                {
                    'id': choice_id,
                    'label': choice
                }
            )
            if choice == r.get('correct_answer'):
                right_id = choice_id
            choice_id += 1

        return choices, right_id

    session_token = requests.get('https://opentdb.com/api_token.php?command=request').json()
    if not session_token.get('response_code') == 0:
        print("Couldn't get token")
        exit()
    token = session_token.get('token')

    result = []
    global LOOP_COUNT
    while True:
        print(LOOP_COUNT)
        LOOP_COUNT+=1
        rr = requests.get(url+'&token='+token)
        response = rr.json()
        if response.get('response_code') == 4:
            print('Session Token has returned all possible questions for the '
                  'specified query. Resetting the Token is necessary.')
            requests.get('https://opentdb.com/api_token.php?'
                         'command=reset&token='+token)
            return result

        global QUESTION_ID
        for r in response.get('results'):
            choices, answer_id = get_choices(r)
            question = OrderedDict({
                'id': QUESTION_ID,
                'lang': 'EN_US',
                'tags': [r.get('category').split(':')],
                'type': 'MULTIPLE_CHOICE',
                'question': OrderedDict({
                    'title': r.get('question'),
                    'choices': choices
                }),
                'answers': [answer_id]
            })

            QUESTION_ID += 1
            result.append(question)

    return result


r = get_open_trivia_database(url)
with open('quiz1.json', 'w') as file:
    json.dump(r, file, indent=4)