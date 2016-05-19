import requests
from multiprocessing import Process, Manager
from fuzzywuzzy import fuzz
from textblob import TextBlob
import re
import json


def get_story(story_id, stories):
    url = 'https://hacker-news.firebaseio.com/v0/item/%d.json' % story_id
    resp = requests.get(url)
    stories.append(resp.json())
    return stories


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


def get_json_comments():
    return json.load(open('../data/comments.json', 'rb'))


def get_all_comments(sid):
    manager = Manager()
    comments = manager.list()
    story = get_story(sid, [])
    if not story[0].get('kids'):
        return []
    processes = [Process(target=get_story, args=(cid, comments))
                 for cid in story[0].get('kids')]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    return [c for c in comments if c and not c.get('deleted')]


def remove_html(text):
    try:
        return re.sub('<[^<]+?>', '', text)
    except:
        print text
    return text


def is_match(first, second):
    ratio = fuzz.token_sort_ratio(first, second)
    if ratio > 50:
        return True
    return False


def find_matching_comments():
    stories = get_top_stories()
    comments = []
    while len(comments) < 1:
        for s in stories:
            comments.extend(get_all_comments(s.get('id')))
    matches = []
    comment_text = ['%s - %s' % (c.get('by'),
                                 remove_html(c.get('text'))) for c in comments]
    for c in comments:
        ctext = remove_html(c.get('text'))
        comment_text.remove('%s - %s' % (c.get('by'), ctext))
        for txt in comment_text:
            if is_match(ctext, txt):
                matches.append((c, txt))
    return matches


def comment_sentiment():
    stories = get_top_stories()
    comments = get_all_comments(stories[0].get('id'))
    for comm in comments:
        comm['sentiment'] = TextBlob(comm.get(
            'text')).sentiment.polarity
    comments.sort(key=lambda x: x.get('sentiment'))
    return comments
