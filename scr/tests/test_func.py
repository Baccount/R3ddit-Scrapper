import os
import sys
from configparser import ConfigParser

sys.path.insert(1, os.path.join(sys.path[0], ".."))
# trunk-ignore(flake8/E402)
from classes import R3dditScrapper

# trunk-ignore(flake8/E402)
from functions.tools import check_update


def test_check_update():
    """
    Test check_update function
    """
    assert check_update(testing=True) is True


def test_R3dditScrapper():
    """
    Test R3dditScrapper class
    """
    scrapper = R3dditScrapper(
        sub="pics", limit=1, order="hot", nsfw="True", argument=False, path="images"
    )
    assert scrapper.sub == "pics"
    assert scrapper.limit == 1
    assert scrapper.order == "hot"
    assert scrapper.nsfw is True
    assert scrapper.argument is False
    assert scrapper.path == "images/pics/"
    config = ConfigParser()
    config.read("config.ini")
    try:
        # Prioritize arguments path over config path
        path = config["Path"]["path"]
    except KeyError:
        path = "images"
    scrapper = R3dditScrapper(
        sub="pics", limit=1, order="hot", nsfw="True", argument=False, path=path
    )
    assert scrapper.path == path + "/" + "pics/"


def test_download():
    """
    Test download function
    """
    import os

    scrapper = R3dditScrapper(
        sub="pics", limit=1, order="hot", nsfw="True", argument=False, path=None
    )
    scrapper.download(
        {"url": "https://i.redd.it/kq1strmcq3i91.jpg", "fname": "test.jpg"}
    )
    assert os.path.isfile("test.jpg") is True
    os.remove("test.jpg")


def test_nsfw():
    """
    Test nsfw function
    """
    scrapper = R3dditScrapper(
        sub="pics", limit=1, order="hot", nsfw="True", argument=False, path=None
    )
    assert scrapper.nsfw is True
    scrapper = R3dditScrapper(
        sub="pics", limit=1, order="hot", nsfw="False", argument=False, path=None
    )
    assert scrapper.nsfw is False
