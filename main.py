import concurrent.futures as futures
import configparser
import os
import re

import praw
import requests

from functions.tools import argument, blue, create_config, getInput, green, red, showSplash

VERSION = "0.1"


class R3dditScrapper:
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        path = config["Path"]["path"]
    except KeyError:
        path = None

    def __init__(
        self,
        sub="pics",
        limit=1,
        order="hot",
        nsfw="True",
        argument=False,
        path=path if path else None,
    ):
        """
        It downloads images from a subreddit, and saves them to a folder
        :param sub: The subreddit you want to download from
        :param limit: The number of images to download
        :param order: hot, top, new
        :param nsfw: If you want to download NSFW images, set this to True, defaults to False (optional)
        :param argument: If you want to use the arguments from the command line, set this to True, defaults to False (optional)
        :param folder: The path you want to save to, defaults to the subreddit name (optional)
        """

        self.sub = sub
        self.limit = limit
        self.order = order
        self.argument = argument
        self.path = f"images/{self.sub}/" if not path else f"{path}/{self.sub}/"
        client_id = self.config["Reddit"]["client_id"]
        client_secret = self.config["Reddit"]["client_secret"]
        user_agent = (
            "R3dditScrapper / https://github.com/Baccount/Reddit_Downloader/tree/master"
        )
        self.nsfw = nsfw
        if self.nsfw.lower() == "true" or self.nsfw.lower() == "t":
            self.nsfw = True
        else:
            self.nsfw = False
        self.reddit = praw.Reddit(
            client_id=client_id, client_secret=client_secret, user_agent=user_agent
        )

    def download(self, image):
        try:
            r = requests.get(image["url"])
            with open(image["fname"], "wb") as f:
                f.write(r.content)
        except Exception as e:
            print(e)

    def setOrder(self):
        """Set the order of the images to download"""
        if self.order == "hot":
            return self.reddit.subreddit(self.sub).hot(limit=None)
        elif self.order == "top":
            return self.reddit.subreddit(self.sub).top(limit=None)
        elif self.order == "new":
            return self.reddit.subreddit(self.sub).new(limit=None)

    def getImages(self) -> list:
        """Get the images from the subreddit"""
        images = []
        try:
            go = 0
            submissions = self.setOrder()
            for submission in submissions:
                if (
                    not submission.stickied
                    and submission.over_18 == self.nsfw
                    and submission.url.endswith(("jpg", "jpeg", "png", "gif"))
                ):
                    fname = self.path + re.search(
                        r"(?s:.*)\w/(.*)",
                        submission.url,
                    ).group(1)
                    if not os.path.isfile(fname):
                        # Add image Only if it does not already exist
                        images.append({"url": submission.url, "fname": fname})
                        go += 1
                        print(green(f"{go}/{self.limit}"))
                        if go >= self.limit:
                            break
            self.make_dir(images)
            return images
        # catch bad request errors
        except Exception as e:
            print(red(str(e)))
            print(red("Subreddit not found"))
            if self.argument:
                # exit after using terminal arguments
                exit(0)
            input("Press enter to continue: ")
            main(skip=True)

    def make_dir(self, images):
        if len(images):
            if not os.path.exists(self.path):
                os.makedirs(self.path)

    def start(self):
        print(blue("Downloading images from r/" + self.sub))
        with futures.ThreadPoolExecutor() as executor:
            executor.map(self.download, self.getImages())
        print(green("Saved images to " + self.path))
        if not self.argument:
            # Not in terminal, show press enter to continue
            input("Press enter to continue: ")
        if self.argument:
            # exit after using terminal arguments
            exit(0)
        else:
            # restart the program if not using terminal arguments
            main(skip=True)


def main(skip=False):
    # skip if called from another function
    if not skip:
        create_config()
        argument()
    showSplash()
    sub, limit, order, path = getInput()
    R3dditScrapper(sub, limit, order).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(1)
