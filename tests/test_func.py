import os
import sys
from configparser import ConfigParser

sys.path.insert(1, os.path.join(sys.path[0], ".."))
# trunk-ignore(flake8/E402)
from functions.tools import check_update
# trunk-ignore(flake8/E402)
from main import R3dditScrapper


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
    path = config["Path"]["path"]
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
