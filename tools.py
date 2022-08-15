import argparse as ap
import sys

from pyfiglet import Figlet


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
    from main import VERSION
    clear_screen()
    title = "R3ddit\n Scrapper"
    f = Figlet(font="standard")
    print(blue(f.renderText(title)))
    # add 10 spaces to the title
    print(" " * 45 + red(VERSION))


def argument():
    """
    Parsing the arguments passed by the user.
    optional arguments:
    -s --sub: The subreddit you want to download from
    -l --limit: number of images to download
    -o --order: hot, top, new
    -n --nsfw: False = NO NSFW images
    -p --path: The path you want to save to
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
    parser.add_argument(
        "-p", "--path", nargs='+', help="The folder you want to save to", required=False
    )
    # if no arguments are passed, return
    if len(sys.argv) == 1:
        return
    ol = ["hot", "top", "new"]
    sub = parser.parse_args().sub if parser.parse_args().sub else "pics"
    limit = int(parser.parse_args().limit) if parser.parse_args().limit else 1
    order = parser.parse_args().order if parser.parse_args().order in ol else "hot"
    nsfw = parser.parse_args().nsfw if parser.parse_args().nsfw else "True"
    path = parser.parse_args().path if parser.parse_args().path else None
    # join path with space fix https://stackoverflow.com/a/26990349
    path = ' '.join(path)
    print(f"Subreddit: {sub}")
    print(f"Limit: {limit}")
    print(f"Order: {order}")
    print(f"NSFW: {nsfw}")
    print(f"Path: {path}")
    from main import R3dditScrapper
    R3dditScrapper(sub, limit, order, nsfw, True, path).start()
