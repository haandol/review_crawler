# coding: utf-8

import time
import json
import urllib
import urllib2
import logging
from bs4 import BeautifulSoup as Soup


logging.basicConfig(level=logging.DEBUG)

url = 'https://play.google.com/store/getreviews?authuser=0'
headers = {
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'user-agent': 'Mozilla/5.0'
}

payload = {
    'id': 'com.google.android.apps.maps',
    'reviewType': 0,
    'pageNum': 0,
    'reviewSortOrder': 4,
    'xhr': 1,
    'hl': 'ko'
}


def parse():
    values = urllib.urlencode(payload)
    req = urllib2.Request(url, values, headers)
    response = urllib2.urlopen(req)

    data = json.loads(response.read()[5:])

    soup = Soup(data[0][2])
    for review in soup.select('.single-review'):
        body = review.select('.review-body')[0].text
        rating = int(review.select('.current-rating')[0]['style'].split(':')[1].strip()[:-2])/20
        if 1 == rating:
            logging.warning(body)


while True:
    logging.info('start parsing')
    parse()
    logging.info('parsing ends')
    logging.info('sleep in 60s')
    time.sleep(60)
