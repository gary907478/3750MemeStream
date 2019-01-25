import threading
import sys
from datetime import timedelta
import requests
from time import sleep
import json
from db import DB

class scraper (threading.Thread):
    def __init__(self, do_logging=False, db_connection = DB(), refresh_interval = timedelta(minutes=10)):
        self._db = db_connection
        self._do_logging = do_logging
        self._refresh_interval = refresh_interval
        super().__init__()

    def run(self):
        self._log("Starting scraper. Refreshes every %f seconds" % self._refresh_interval.total_seconds(), file=sys.stderr)
        while(True):
            self._log("Scraping", file=sys.stderr)

            links = []

            queryparams = '?'
            for i in range(10):
                r = requests.get('https://9gag.com/v1/group-posts/group/default/type/hot' + queryparams)
                text = r.text
                obj = json.loads(text)
                links += [ self._get_url_from_post(x) for x in obj['data']['posts'] if x['nsfw'] == 0 ]
                queryparams = '?' + obj['data']['nextCursor']

            self._db.execute("TRUNCATE TABLE SCRAPED_MEMES")
            self._db.executemany("INSERT INTO SCRAPED_MEMES (LINK) VALUES (%s)", [(x,) for x in links ])
            self._db.commit()

            for second in range(int(self._refresh_interval.total_seconds()), 0, -1):
                self._log("Waiting %d more seconds" % second, file=sys.stderr)
                sleep(1)

    def _get_url_from_post(self, post):
        if (post['type']) == 'Animated':
            return post['images']['image460sv']['url']
        else:
            return post['images']['image700']['url']

    def _log(self, *args, **kwargs):
        if self._do_logging:
            print(*args, **kwargs)

if __name__ == "__main__":
    memescraper = scraper(do_logging=True, refresh_interval=timedelta(seconds=10))
    memescraper.start()
