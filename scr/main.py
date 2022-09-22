from arguments.arguments import argument
from classes.main_class import R3dditScrapper
from functions import create_config, getInput, showSplash

VERSION = "0.3"


def main(skip=False):
    create_config()
    argument()
    showSplash()
    sub, limit, order, nsfw = getInput()
    R3dditScrapper(sub, limit, order, nsfw=nsfw).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(1)
