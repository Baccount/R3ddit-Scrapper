import os

from main import create_config, redditImageScraper


def test_create_config():
    create_config()
    assert os.path.isfile("config.ini")
