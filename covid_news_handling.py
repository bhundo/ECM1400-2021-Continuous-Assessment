import sched
import time
import logging
import json  # pip install sched, pip install json
from newsapi import NewsApiClient  # pip install newsapi

logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG)
newsscheduler = sched.scheduler(time.time, time.sleep)
removed_articles = []


def news_API_request(covid_terms=json.loads(open("config.json").read())["covid_terms"], 
                api_key=open('apikey.txt').read().strip('\n')):
    """Returns the news articles related with the 'covid_terms' specified within the config file"""
    newsapi = NewsApiClient(api_key=api_key)
    all_articles = []
    all_articles = newsapi.get_everything(q=covid_terms)
    logging.info("news_API_request has been called successfully")
    return all_articles['articles']


news_articles = news_API_request()


def remove_news_article(title):
    """Appends removes articles to a removed article array and removes 
        the news articles from the main news article api call."""
    logging.basicConfig(filename="log.log")
    removed_articles.append(title)
    for article in news_articles:
        for remove in removed_articles:
            if article['title'] == remove:
                news_articles.remove(article)
    logging.info("News article "+title+" has been removed")


def update_news(article):
    """Updates the news articles based on whether the news article has been removed or not."""
    all_articles = news_API_request()
    for article in all_articles:
        for remove in removed_articles:
            if article == remove:
                all_articles.remove(article)
    news_articles = all_articles
    return news_articles

def schedule_news_updates(update_interval, update_name, repeat=False, cancelled=False):
    """Schedules updates for the covid data based upon the inputs in the website template.
    'update_interval' - time in seconds before the update commences
    'update_name' - the name of the update
    'repeat' - True = covid update will repeat"""
    e1 = newsscheduler.enter(update_interval, 1, update_news)
    if repeat is True:
        e2 = newsscheduler.enter(update_interval, 3, lambda: schedule_news_updates(
            update_interval=update_interval*24*60*60, update_name=update_name+' repeat', repeat=repeat))
    e3 = newsscheduler.enter(update_interval, 3, logging.info("Scheduled news update has been completed."))        
    if cancelled is True:
        newsscheduler.cancel(e1)
        newsscheduler.cancel(e2)
        newsscheduler.cancel(e3)
    newsscheduler.run()

#schedule_news_updates(3, 'test')
