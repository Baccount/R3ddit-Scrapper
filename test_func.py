from main import R3dditScrapper
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
        sub="pics", limit=1, order="hot", nsfw="True", argument=False, path=None
    )
    assert scrapper.sub == "pics"
    assert scrapper.limit == 1
    assert scrapper.order == "hot"
    assert scrapper.nsfw is True
    assert scrapper.argument is False
    assert scrapper.path == "images/pics/"


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
