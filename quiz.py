import requests
import random
import pprint
from collections import OrderedDict
import json



pp = pprint.PrettyPrinter(indent=4)
url = 'https://opentdb.com/api.php?amount=50'

QUESTION_ID = 0


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

    rr = requests.get(url)
    print(rr)
    response = rr.json()
    if not response.get('response_code') == 0:
        print('Error. Check URL')
        return 1

    result = []
    global QUESTION_ID
    for r in response.get('results'):
        choices, answer_id = get_choices(r)
        question = OrderedDict({
            'id': QUESTION_ID,
            'lang': 'EN_US',
            'category': r.get('category'),
            'type': 'MULTIPLE_CHOICE',
            'question': OrderedDict({
                'title': r.get('question'),
                'choices': choices
            }),
            'answer': answer_id
        })

        QUESTION_ID += 1
        result.append(question)

    return result


r = get_open_trivia_database(url)
with open('quiz1.json', 'w') as file:
    json.dump(r, file, indent=4)
pp.pprint(r)