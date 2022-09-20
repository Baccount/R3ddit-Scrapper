import argparse as ap
import sys

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