from robobrowser import RoboBrowser
import requests
import json
from bs4 import BeautifulSoup
import random
from pymongo import MongoClient
import updatestats
import datetime
from tqdm import tqdm
import re

HEADERS_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]


# print(updatestats.initialize())
# input("JJ")


# respektor/timeline/tweets?include_available_features=1&include_entities=1&max_position=1007280762566033408&reset_error_state=false


def get_tweets(handle, max_position=None):
    session = requests.Session()
    browser = RoboBrowser(session=session, user_agent=random.choice(HEADERS_LIST), parser="lxml")

    url = "https://twitter.com/i/profiles/show/" + handle + "/timeline/tweets?include_available_features=false&include_entities=false&reset_error_state=false"
    if max_position != None:
        url = url + "&" + "max_position=" + max_position
    browser.open(url)
    result = json.loads(browser.response.content)
    min_position = result['min_position']
    soup = BeautifulSoup(result['items_html'], 'lxml')
    links = []
    for link in soup.find_all('a'):
        if str("/" + handle + "/status/") in str(link):
            links.append(link.get('href'))
    updatestats.update_tweets(len(links))
    return min_position, links  # , result['items_html'], browser.url


def get_people(link, handle):
    session = requests.Session()
    people_list = []
    browser = RoboBrowser(session=session, user_agent=random.choice(HEADERS_LIST), parser="lxml")
    url = "https://twitter.com" + link
    try:
        browser.open(url)
        updatestats.update_chars(len(str(browser.parsed)))
        results = browser.find_all("a", {
            "class": "account-group js-account-group js-action-profile js-user-profile-link js-nav"})
        for link in results:
            people_list.append(str(link.get('href')).replace("/", ""))
    except:
        pass
    return people_list


#
# def total_tweets(handle):
#     url = "https://twitter.com/" + handle
#     browser.open(url)
#     results = browser.find_all("span", {"class": "ProfileNav-value"})
#     return int(results[0].text.replace(',', ''))


def connections(handle):
    session = requests.Session()
    browser = RoboBrowser(session=session, user_agent=random.choice(HEADERS_LIST), parser="lxml")
    client = MongoClient("mongodb://root:PhMb1okSjv6w@35.185.118.72:27017/")
    db = client['sixdos']
    # ttweets = total_tweets(handle)

    if db.data.find({'_id': handle}).count() == 0:
        print(handle)
        updatestats.update_last(handle)
        min_position, links = get_tweets(handle)

        with tqdm(10000) as pbar:
            while (True):
                min_position1, links1 = get_tweets(handle, min_position)
                links = links + links1
                pbar.update(len(links1))
                if (min_position1 == None):
                    break
                min_position = min_position1

        people_list = []

        for link in tqdm(links):
            if handle in link:
                people_list = people_list + get_people(link, handle)

        print("Handle: ", handle, "Length: ", str(len(people_list)), people_list)
        t = datetime.datetime.now()
        # t = datetime.datetime(year, month, day)
        s = t.strftime('%Y-%m-%d %H:%M:%S.%f')

        result = {"_id": handle, "Length": str(len(people_list)), "Connections": str(people_list), "date": s[:-3]}
        update = db.data.update({'_id': handle}, {"$set": result}, upsert=True)
        people_list = []
        return update

updatestats.initialize()

updatestats.update_last('respektor')
connections('respektor')

client = MongoClient("mongodb://root:PhMb1okSjv6w@35.185.118.72:27017/")
db = client['sixdos']
documents = db.data.find()
for document in documents:
    quoted = re.compile("(?<=')[^']+(?=')")
    for value in quoted.findall(document['Connections']):
        if ',' not in value:
            # print(value)
            connections(value)
            updatestats.updatetotalusers()

