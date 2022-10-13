from arguments.arguments import argument
from classes.main_class import R3dditScrapper
from functions import create_config, getInput, showSplash

VERSION = "0.2"


def main(skip=False):
    # skip if called from another function
    if not skip:
        create_config()
        argument()
    while True:
        showSplash()
        choice = getInput()
        R3dditScrapper(
            choice["sub"], choice["limit"], choice["order"], choice["nsfw"]
        ).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(1)
