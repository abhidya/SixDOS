# SixDOS
A live time experiment exploring the "Six Degrees of Seperation" As my spider bot crawls through Twitter


Six degrees of separation.
"Six degrees of separation is the idea that all living things and everything else in the world are six or fewer steps away from each other so that a chain of "a friend of a friend" statements can be made to connect any two people in a maximum of six steps. It was originally set out by Frigyes Karinthy in 1929 and popularized in an eponymous 1990 play written by John Guare. "  From Wikipedia, the free encyclopedia


https://bookshelf-221213.appspot.com/spyder.html

## Local run notes

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

MongoDB is configured through environment variables:

```sh
export SIXDOS_MONGO_URI="mongodb://localhost:27017/"
export SIXDOS_MONGO_DB="sixdos"
export SIXDOS_USE_MONGO=1
python server.py
```

The original Twitter crawling pieces use older Twitter web behavior and may need
API/dependency updates before they can be run reliably.

## Offline demo path

The Flask dashboard now imports without PyMongo and returns fixture data for
`/visualization` and `/spyder/visualization` when MongoDB is unavailable:

```sh
python smoke_test.py
```

`/health` reports the current backend mode. The crawler/stat helper scripts now
read MongoDB settings from `SIXDOS_MONGO_URI` and `SIXDOS_MONGO_DB` instead of
hardcoded remote credentials.
