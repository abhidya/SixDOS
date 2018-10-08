from robobrowser import RoboBrowser
import requests
import json
from bs4 import BeautifulSoup
import random
from pymongo import MongoClient
import updatestats

from tqdm import tqdm

HEADERS_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]

session = requests.Session()
browser = RoboBrowser(session=session, user_agent=random.choice(HEADERS_LIST), parser="lxml")

print(updatestats.initialize())


people = {}


# respektor/timeline/tweets?include_available_features=1&include_entities=1&max_position=1007280762566033408&reset_error_state=false


def get_tweets(handle, max_position=None):
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
    return min_position, links, result['items_html'], browser.url


def get_people(link, handle):
    url = "https://twitter.com" + link
    browser.open(url)
    updatestats.update_chars(len(str(browser.parsed)))
    results = browser.find_all("a", {
        "class": "account-group js-account-group js-action-profile js-user-profile-link js-nav"})
    for link in results:
        people[handle].add(str(link.get('href')).replace("/", ""))


def total_tweets(handle):
    url = "https://twitter.com/" + handle
    browser.open(url)
    results = browser.find_all("span", {"class": "ProfileNav-value"})
    return int(results[0].text.replace(',', ''))


def connections(handle):
    # ttweets = total_tweets(handle)

    min_position, links, parsed_browser, url = get_tweets(handle)

    with tqdm(total=345) as pbar:
        while (True):
            min_position1, links1, parsed_browser, url = get_tweets(handle, min_position)
            links = links + links1
            pbar.update(len(links1))
            if (min_position1 == None):
                break
            min_position = min_position1

    people[handle] = set()

    for link in tqdm(links):
        if handle in link:
            get_people(link, handle)

    print("Handle: ", handle, "Length: ", str(len(people[handle])), people[handle])

    result = {"_id": handle, "Length": str(len(people[handle])), "Connections": people[handle]}
    client = MongoClient('mongodb://localhost:27017/')
    db = client['sixdos']
    update = db.data.insert_one(result)
    return update

#
# connections('respektor')
#
# for person in people:
#     for names in people[person]:
#         connections(names)
#         with open('people.pickle', 'wb') as handle:
#             pickle.dump(people, handle, protocol=pickle.HIGHEST_PROTOCOL)
