# import tools
from tools import blue, green, red, show_splash, argument, check_update
from main import VERSION, R3dditScrapper

def test_check_update():
    """
    Test check_update function
    """
    assert check_update() is True