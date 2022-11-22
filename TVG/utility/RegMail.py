# -*- coding: utf-8 -*-
# Copyright (c) 2020, KarjaKAK
# All rights reserved.

import re
import webbrowser
from sys import platform
from textwrap import fill
from urllib import parse

__all__ = [""]


def composemail(sub: str, body: str):
    subject = f"[TVG]-{sub}"
    if platform.startswith("win"):
        # For default Windows "Mail" app
        webbrowser.open(f"mailto:?subject={subject}&body={parse.quote(body)}", new=1)
    else:
        # For default MacOsX default "Mail" app
        body = re.sub(r"\\", "", body) if "\\" in body else body
        webbrowser.open(f"mailto:?subject={subject}&body={body}", new=1)


def wrwords(text: str, wd: int, num: int):
    regex = re.compile(r"\s+")
    get = regex.match(text)
    if get:
        b = fill(text, wd, subsequent_indent=f'{" " * (get.span()[1]+num)}')
    else:
        b = fill(text, wd)
    return b
