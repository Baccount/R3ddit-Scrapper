import argparse as ap
import sys
from time import sleep
import configparser

from pyfiglet import Figlet


def blue(text: str) -> str:
    """
    `blue` takes a string and returns a blue string
    """
    return "\033[34m" + text + "\033[0m"


def green(text: str) -> str:
    """
    `green` takes a string and returns a green string
    """
    return "\033[32m" + text + "\033[0m"


def red(text: str) -> str:
    """
    `red` takes a string and returns a red string
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
        "-p", "--path", nargs="+", help="The folder you want to save to", required=False
    )
    # if no arguments are passed, return
    if len(sys.argv) == 1:
        return
    sort = ["hot", "top", "new"]
    sub = parser.parse_args().sub if parser.parse_args().sub else "pics"
    limit = int(parser.parse_args().limit) if parser.parse_args().limit else 1
    order = parser.parse_args().order if parser.parse_args().order in sort else "hot"
    nsfw = parser.parse_args().nsfw if parser.parse_args().nsfw else "True"
    path = parser.parse_args().path if parser.parse_args().path else None
    # join path with space fix https://stackoverflow.com/a/26990349
    path = " ".join(path) if path else None
    print(f"Subreddit: {sub}")
    print(f"Limit: {limit}")
    print(f"Order: {order}")
    print(f"NSFW: {nsfw}")
    print(f"Path: {path if path else 'Local directory'}")
    from main import R3dditScrapper

    R3dditScrapper(
        sub=sub, limit=limit, order=order, nsfw=nsfw, argument=True, path=path
    ).start()


def check_update() -> bool:
    # download latest version asynchronously
    """
    Check if there is a new version of the program
    """
    # download async the version file
    try:
        import requests

        from main import VERSION

        r = requests.get(
            "https://raw.githubusercontent.com/Baccount/Reddit_Downloader/master/version.txt"
        )
        r = r.text.strip()
        if not r == VERSION:
            print(" " * 45 + red(VERSION))
            print(f"There is a new version of the program: {r}")
            print(blue("https://github.com/Baccount/Reddit_Downloader"))
            sleep(2)
            return True
        else:
            print(green("Currently running the latest version"))
            print(" " * 45 + red(VERSION))
        return True
    # trunk-ignore(flake8/E722)
    except:
        print("Could not check for updates")
        return False

def options():
    from main import setPath, main
    clear_screen()
    # print the options
    print(blue("\nOptions:\n"))
    option = input(
        "P: Set path\nV: View current path \nC: Check for updates\nQ: Quit\n: "
    )
    if option.lower() == "p":
        setPath()
    elif option.lower() == "v":
        config = configparser.ConfigParser()
        config.read("config.ini")
        if config.has_section("Path"):
            print(green(config["Path"]["path"]))
        else:
            print(red("No path set"))
        sleep(2)
    elif option.lower() == "c":
        check_update()
    elif option.lower() == "q":
        main()
    main()
