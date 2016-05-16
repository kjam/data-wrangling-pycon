import calculate
import requests
from multiprocessing import Process, Manager
from decimal import Decimal


def get_story(story_id, stories):
    url = 'https://hacker-news.firebaseio.com/v0/item/%d.json' % story_id
    resp = requests.get(url)
    story_data = resp.json()
    user_data = get_user(story_data.get('by'))
    story_data['user_karma'] = user_data.get('karma') or 0
    stories.append(story_data)
    return stories


def get_user(user_id):
    url = 'https://hacker-news.firebaseio.com/v0/user/%s.json' % user_id
    resp = requests.get(url)
    return resp.json()


def get_top_stories_with_user_karma():
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


def calculate_summary_karma():
    stories = get_top_stories_with_user_karma()
    return calculate.summary_stats([
        Decimal(s.get('score')) for s in stories])


def pearsons_karma():
    stories = get_top_stories_with_user_karma()
    user_karma = [Decimal(s.get('user_karma')) for s in stories]
    story_karma = [Decimal(s.get('score')) for s in stories]
    return calculate.pearson(user_karma, story_karma)
