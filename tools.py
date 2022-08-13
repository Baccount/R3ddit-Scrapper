from pyfiglet import Figlet

def blue(text: str) -> str:
    """
    `blue` takes a string and returns a string

    :param text: The text to be colored
    :type text: str
    :return: The text is being returned with the color blue.
    """
    return "\033[34m" + text + "\033[0m"

def green(text: str) -> str:
    """
    `green` takes a string and returns a string

    :param text: The text to be colored
    :type text: str
    :return: The text is being returned with the color green.
    """
    return "\033[32m" + text + "\033[0m"

def red(text: str) -> str:
    """
    `red` takes a string and returns a string

    :param text: The text to be colored
    :type text: str
    :return: The text is being returned with the color red.
    """
    return "\033[31m" + text + "\033[0m"

def show_splash():
    """
    Display splash screen
    """
    clear_screen()
    title = "R3ddit\n Scrapper"
    f = Figlet(font="standard")
    print(blue(f.renderText(title)))