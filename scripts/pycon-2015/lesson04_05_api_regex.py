import requests
import re
import json
from multiprocessing import Process, Manager

MATCHING = (
    ('Python', '(p|P)ython'),
    ('Ruby', '(r|R)uby'),
    ('JavaScript', 'js|(J|j)ava(s|S)cript'),
    ('NodeJS', 'node(\.?)(?:\js|JS)'),
    ('Java', '(j|J)ava[^(S|s)cript]'),
    ('Objective-C', 'Obj(ective?)(?:\ |-)(C|c)'),
)


def get_story(story_id, stories):
    url = 'https://hacker-news.firebaseio.com/v0/item/%d.json' % story_id
    resp = requests.get(url)
    stories.append(resp.json())


def get_top_stories():
    manager = Manager()
    stories = manager.list()
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    ids = requests.get(url)
    processes = [Process(target=get_story, args=(sid, stories))
                 for sid in ids.json()[:40]]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    return stories


def get_json_stories():
    return json.load(open('../data/topstories.json', 'rb'))


def count_languages():
    stories = get_top_stories()
    final_tallies = {}
    for s in stories:
        long_string = u'{} {}'.format(s.get('title'), s.get('url'))
        for language, regex in dict(MATCHING).items():
            if re.search(regex, long_string):
                if language not in final_tallies.keys():
                    final_tallies[language] = {
                        'score': s.get('score'),
                        'descendants': s.get('descendants')}
                else:
                    final_tallies[language]['score'] += s.get('score')
                    final_tallies[language][
                        'descendants'] += s.get('descendants')
    return final_tallies
