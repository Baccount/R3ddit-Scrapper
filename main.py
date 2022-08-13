import argparse as ap
import concurrent.futures as futures
import configparser
import os
import re
import sys

import praw
import requests
from pyfiglet import Figlet
from time import sleep

class R3dditScrapper:
    def __init__(self, sub="pics", limit=1, order="hot", nsfw="True", argument=False):
        """
        It downloads images from a subreddit, and saves them to a folder
        :param sub: The subreddit you want to download from
        :param limit: The number of images to download
        :param order: hot, top, new
        :param nsfw: If you want to download NSFW images, set this to True, defaults to False (optional)
        :param argument: If you want to use the arguments from the command line, set this to True, defaults to False (optional)
        """

        config = configparser.ConfigParser()
        config.read("config.ini")
        self.sub = sub
        self.limit = limit
        self.order = order
        self.argument = argument
        self.path = f"images/{self.sub}/"
        client_id = config["Reddit"]["client_id"]
        client_secret = config["Reddit"]["client_secret"]
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
        r = requests.get(image["url"])
        with open(image["fname"], "wb") as f:
            f.write(r.content)

    def set_order(self):
        """Set the order of the images to download"""
        if self.order == "hot":
            return self.reddit.subreddit(self.sub).hot(limit=None)
        elif self.order == "top":
            return self.reddit.subreddit(self.sub).top(limit=None)
        elif self.order == "new":
            return self.reddit.subreddit(self.sub).new(limit=None)

    def get_images(self) -> list:
        """Get the images from the subreddit"""
        images = []
        try:
            go = 0
            submissions = self.set_order()
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
                    images.append({"url": submission.url, "fname": fname})
                    go += 1
                    print(green(f"{go}/{self.limit}"))
                    if go >= self.limit:
                        break
            self.make_dir(images)
            return images
        except Exception as e:
            print(e)

    def make_dir(self, images):
        if len(images):
            if not os.path.exists(self.path):
                os.makedirs(self.path)

    def start(self):
        # track the progress of the download with a thread pool
        print(blue("Downloading images from r/" + self.sub))
        with futures.ThreadPoolExecutor() as executor:
            executor.map(self.download, self.get_images())
        print(green("\nDone"))
        if self.argument:
            # exit after using terminal arguments
            exit(0)
        else:
            # restart the program if not using terminal arguments
            sleep(2)
            main()


def argument():
    """Parsing the arguments passed by the user.
    optional arguments:
    -s --sub: The subreddit you want to download from
    -l --limit: The number of images to download
    -o --order: hot, top, new
    -n --nsfw: Set to False of you want to download all NON NSFW images
    """
    parser = ap.ArgumentParser(description="R3ddit Scrapper")
    parser.add_argument(
        "-s", "--sub", help="The subreddit you want to download from", required=False
    )
    parser.add_argument(
        "-l", "--limit", help="The number of images to download", required=False
    )
    parser.add_argument("-o", "--order", help="hot, top, new", required=False)
    parser.add_argument(
        "-n",
        "--nsfw",
        help="Set to False of you want to download all NON NSFW images",
        required=False,
    )
    # if no arguments are passed, return
    if len(sys.argv) == 1:
        return
    ol = ["hot", "top", "new"]
    sub = parser.parse_args().sub if parser.parse_args().sub else "pics"
    limit = int(parser.parse_args().limit) if parser.parse_args().limit else 1
    order = parser.parse_args().order if parser.parse_args().order in ol else "hot"
    nsfw = parser.parse_args().nsfw if parser.parse_args().nsfw else "True"
    print(f"Subreddit: {sub}")
    print(f"Limit: {limit}")
    print(f"Order: {order}")
    print(f"NSFW: {nsfw}")
    Scrapper = R3dditScrapper(
        sub=sub, limit=limit, order=order, nsfw=nsfw, argument=True
    )
    Scrapper.start()


def blue(text: str) -> str:
    """
    `blue` takes a string and returns a string

    :param text: The text to be colored
    :type text: str
    :return: The text is being returned with the color blue.
    """
    return "\033[34m" + text + "\033[0m"

def green(text: str) -> str:
    """
    `green` takes a string and returns a string

    :param text: The text to be colored
    :type text: str
    :return: The text is being returned with the color green.
    """
    return "\033[32m" + text + "\033[0m"

def red(text: str) -> str:
    """
    `red` takes a string and returns a string

    :param text: The text to be colored
    :type text: str
    :return: The text is being returned with the color red.
    """
    return "\033[31m" + text + "\033[0m"

def clear_screen():
    """
    It prints 25 new lines
    """
    print("\n" * 25)


def show_splash():
    """
    Display splash screen
    """
    clear_screen()
    title = "R3ddit\n Scrapper"
    f = Figlet(font="standard")
    print(blue(f.renderText(title)))


def create_config():
    """Create config file if it doesn't exist"""
    if not os.path.isfile("config.ini"):
        config = configparser.ConfigParser()
        config.add_section("Reddit")
        config.set("Reddit", "client_id", input("Enter your client_id: "))
        config.set("Reddit", "client_secret", input("Enter your client_secret: "))
        with open("config.ini", "w") as f:
            config.write(f)


def main():
    create_config()
    argument()
    show_splash()
    sub = input("Enter subreddit: ")
    # catch the exception if sting is entered instead of a number
    try:
        limit = int(input("Number of photos: "))
    except ValueError:
        print(red("This is not a number, defaulting to 1"))
        limit = 1
    order = input("Order (hot, top, new): ")
    if order not in ["hot", "top", "new"]:
        print("Invalid Order")
        sleep(2)
        main()
    R3dditScrapper(sub, limit, order).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()
