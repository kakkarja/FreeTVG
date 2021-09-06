import webbrowser
from urllib import parse
from textwrap import fill
import re
from sys import platform


def composemail(sub: str, body: str):
    subject = f'[TVG]-{sub}'
    if platform.startswith('win'):
        webbrowser.open(f'mailto:?subject={subject}&body={parse.quote(body)}', new = 1)
    else:
        webbrowser.open(f'mailto:?subject={subject}&body={body}', new = 1)
    
def wrwords(text: str, wd: int, num: int):
    regex = re.compile(r'\s+')
    get = regex.match(text)
    if get:
        b = fill(text, wd, subsequent_indent = f'{" " * (get.span()[1]+num)}')
    else:
        b = fill(text, wd)
    return b 