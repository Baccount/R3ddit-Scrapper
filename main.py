import os
import re
import requests
import praw
import configparser
import concurrent.futures
import argparse


# create config file
def create_config():
    # check if config file exists
    if not os.path.isfile('config.ini'):
        config = configparser.ConfigParser()
        config.add_section('Reddit')
        config.set('Reddit', 'client_id', input('Enter your client_id: '))
        config.set('Reddit', 'client_secret', input('Enter your client_secret: '))
        config.set('Reddit', 'user_agent',
                'Multithreaded Reddit Image Downloader')
        with open('config.ini', 'w') as configfile:
            config.write(configfile)







class redditImageScraper:
    def __init__(self, sub, limit, order, nsfw=False):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.sub = sub
        self.limit = limit
        self.order = order
        self.nsfw = nsfw
        self.path = f'images/{self.sub}/'
        client_id = config['Reddit']['client_id']
        client_secret = config['Reddit']['client_secret']
        user_agent = config['Reddit']['user_agent']
        
        
        self.reddit = praw.Reddit(client_id=client_id,
                                    client_secret=client_secret,
                                    user_agent=user_agent)

    def download(self, image):
        r = requests.get(image['url'])
        with open(image['fname'], 'wb') as f:
            f.write(r.content)

    def start(self):
        images = []
        try:
            go = 0
            if self.order == 'hot':
                submissions = self.reddit.subreddit(self.sub).hot(limit=None)
            elif self.order == 'top':
                submissions = self.reddit.subreddit(self.sub).top(limit=None)
            elif self.order == 'new':
                submissions = self.reddit.subreddit(self.sub).new(limit=None)

            for submission in submissions:
                if not submission.stickied and submission.over_18 == self.nsfw \
                        and submission.url.endswith(('jpg', 'jpeg', 'png')):
                    fname = self.path + \
                        re.search('(?s:.*)\w/(.*)', submission.url).group(1)
                    if not os.path.isfile(fname):
                        images.append({'url': submission.url, 'fname': fname})
                        go += 1
                        if go >= self.limit:
                            break
            if len(images):
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                with concurrent.futures.ThreadPoolExecutor() as ptolemy:
                    ptolemy.map(self.download, images)
        except Exception as e:
            print(e)


def main():
    create_config()
    sub = input('Enter subreddit: ')
    limit = int(input('Number of photos: '))
    order = input('Order (hot, top, new): ')
    scraper = redditImageScraper(sub, limit, order)
    scraper.start()


if __name__ == '__main__':
    # catch keyboard interrupt
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting...')
        exit()