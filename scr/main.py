from classes.main_class import R3dditScrapper
from functions import argument, create_config, getInput, showSplash

VERSION = "0.2"


def main(skip=False):
    # skip if called from another function
    if not skip:
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
