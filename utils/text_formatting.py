from sys import platform
if platform in ["cygwin", "win32"]:
    import colorama
    colorama.init()

# ANSI text formatting
END = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
WHITE_BG = "\033[47m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_GREEN_BG = "\033[102m"
BRIGHT_YELLOW_BG = "\033[103m"
BRIGHT_BLUE_BG = "\033[104m"
BRIGHT_MAGENTA_BG = "\033[105m"


def black(text: str) -> str:
    return BLACK + text + END


def red(text: str) -> str:
    return RED + text + END


def green(text: str) -> str:
    return GREEN + text + END


def yellow(text: str) -> str:
    return YELLOW + text + END


def blue(text: str) -> str:
    return BLUE + text + END


def bright_red(text: str) -> str:
    return BRIGHT_RED + text + END


def bright_green(text: str) -> str:
    return BRIGHT_GREEN + text + END


def bright_yellow(text: str) -> str:
    return BRIGHT_YELLOW + text + END


def bright_blue(text: str) -> str:
    return BRIGHT_BLUE + text + END
