# import tools
from main import R3dditScrapper
from tools import check_update
import configparser


def test_check_update():
    """
    Test check_update function
    """
    assert check_update() is True


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


def test_path_create():
    """
    Test multiple download function
    """
    import os
    sub = "memes"
    config = configparser.ConfigParser()
    config.read("config.ini")
    path = config["Path"]["path"]
    if path == "":
        path = "images/"
    savePath = path + '/' + sub
    R3dditScrapper(sub=sub, limit=5, order='hot', nsfw='True', argument=True, path=path, test=True).start()
    # check if the path exists
    assert os.path.isdir(savePath) is True
    # check if the path is not empty
    assert os.listdir(savePath) is not []
    # delete jpegs gifs and pngs from the path
    print(os.listdir(savePath))
    for file in os.listdir(savePath):
        if file.endswith(".jpg") or file.endswith(".gif") or file.endswith(".png") or file.endswith(".jpeg"):
            os.remove(path + sub + '/' +  file)
    # if folder is empty delete it
    if os.listdir(savePath) == []:
        os.rmdir(savePath)