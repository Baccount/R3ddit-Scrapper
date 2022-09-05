from functions import *

from classes.main_class import R3dditScrapper

VERSION = "0.1"

def main(skip=False):
    # skip if called from another function
    if not skip:
        create_config()
        argument()
    showSplash()
    sub, limit, order = getInput()
    R3dditScrapper(sub, limit, order).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(1)
