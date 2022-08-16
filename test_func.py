# import tools
from tools import blue, green, red, show_splash, argument, check_update
from main import VERSION, R3dditScrapper

def test_check_update():
    """
    Test check_update function
    """
    assert check_update() is True




def test_R3dditScrapper():
    """
    Test R3dditScrapper class
    """
    scrapper = R3dditScrapper(sub="pics", limit=1, order="hot", nsfw="True", argument=False, path=None)
    assert scrapper.sub == "pics"
    assert scrapper.limit == 1
    assert scrapper.order == "hot"
    assert scrapper.nsfw is True
    assert scrapper.argument is False
    assert scrapper.path == "images/pics/"
    scrapper = R3dditScrapper(sub="pics", limit=1, order="hot", nsfw="True", argument=False, path=None)

def test_download():
    """
    Test download function
    """
    import os
    scrapper = R3dditScrapper(sub="pics", limit=1, order="hot", nsfw="True", argument=False, path=None)
    scrapper.download({"url": "https://i.redd.it/kq1strmcq3i91.jpg", "fname": "test.jpg"})
    assert os.path.isfile("test.jpg") is True
    os.remove("test.jpg")