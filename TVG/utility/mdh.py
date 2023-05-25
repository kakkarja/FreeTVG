# -*- coding: utf-8 -*-
# Copyright (c) 2020, KarjaKAK
# All rights reserved.

import re
import subprocess
from pathlib import Path
from sys import platform

import markdown
import webview

__all__ = [""]


extensions = [
    "pymdownx.extra",
    "pymdownx.caret",
    "pymdownx.tilde",
    "pymdownx.mark",
    "pymdownx.tasklist",
    "pymdownx.escapeall",
    "pymdownx.smartsymbols",
    "pymdownx.keys",
]

extension_configs = {
    "pymdownx.keys": {"strict": True},
    "pymdownx.tasklist": {
        "clickable_checkbox": True,
    },
}


def _pattern(wrd: str, pat: str):
    try:
        last = g = fx = pt = None
        if "<p>" not in wrd:
            last = -5
        else:
            last = -4
        g = wrd.partition(pat)
        g = g[0] + g[1]
        pt = (
            '<input type="checkbox" class="strikethrough" name="ck"/><span for="ck">'
            if not "checked" in pat
            else '<input type="checkbox" class="strikethrough" name="ck" checked/><span for="ck">'
        )
        fx = (
            wrd[: len(g)]
            + "<span>"
            + wrd[len(g) : last]
            + "</span>"
            + wrd[last:]
            + "\n"
        ).replace(
            f"{pat}<span>",
            pt,
        )
        return fx
    finally:
        del last, g, fx, pt, wrd, pat


def convhtml(
    text: str,
    filename: str,
    font: str,
    bg: str = None,
    fg: str = None,
    preview: bool = True,
    width: int = 0,
    height: int = 0,
):
    # Converting your TVG to html and printable directly from browser.

    try:
        gettext = text.split("\n")
        tohtml = []
        background = bg if bg else "gold"
        foreground = fg if fg else "black"
        kbfg = "333" if foreground == "black" else "eee"
        startupinfo = None
        window = None
        pointer_event = None

        for i in gettext:
            if i != "\n":
                sp = re.match(r"\s+", i)
                if sp:
                    sp = sp.span()[1] - 4
                    txt = re.search(r"-", i)
                    if txt and not i[txt.span()[1] :].isspace():
                        txt = f"* {i[txt.span()[1]:]}"
                    else:
                        txt = "*  "
                    tohtml.append(f'{" " * sp}{txt}\n\n')
                else:
                    if "\n" in i and re.search(r"\w+", i):
                        tohtml.append(f"#### {i}\n")
                    elif re.search(r"\w+", i):
                        tohtml.append(f"#### {i}\n\n")
        chg = f"""{''.join(tohtml)}"""
        a = markdown.markdown(
            chg, extensions=extensions, extension_configs=extension_configs
        )
        setfont = (
            "body { "
            + f"""font: {font};
background-color: #{background};
color: {foreground};
"""
            + "}"
        )

        kbd = (
            """kbd { border-radius: 3px;"""
            + f"""border: 1px solid #b4b4b4;
box-shadow: 0 1px 1px rgba(0, 0, 0, .2), 0 2px 0 0 rgba(255, 255, 255, .7) inset;
color: #{kbfg};
display: inline-block;
font-size: .85em;
font-weight: 700;
line-height: 1;
padding: 2px 4px;
white-space: nowrap;"""
            + "}"
        )

        tasklist = """.task-list-item {
list-style-type: none !important;
}

.task-list-item input[type="checkbox"] {
    margin: 0 4px 0.25em -20px;
    vertical-align: middle;
}

.strikethrough:checked + span {
    text-decoration: line-through;
}
"""
        if preview:
            pointer_event = """body { pointer-events: none; }"""

        cssstyle = f"""<!DOCTYPE html>
<html>
<button class="button" onclick="javascript:window.print();">Print</button>
<header>
<meta charset="UTF-8">
<h1>
<strong>
{filename}
</strong>
</h1>
</header>
<style>
{setfont}
{kbd}
{tasklist}
{pointer_event if preview else ""}

"""
        printed = """@media print {
.button { display: none; }

body { 
    background-color: white !important;
    color: black !important;
    }

kbd { color: black !important; }
}
</style>
<body>
"""
        nxt = f"""{a}
</body>
</html>
"""

        cssstyle = cssstyle + printed + nxt
        fcs = []
        if 'input type="checkbox"' in cssstyle:
            for i in cssstyle.split("\n"):
                if '<input type="checkbox" checked/>' in i:
                    fcs.append(_pattern(i, '<input type="checkbox" checked/>'))
                elif '<input type="checkbox"/>' in i:
                    fcs.append(_pattern(i, '<input type="checkbox"/>'))
                else:
                    fcs.append(f"{i}\n")

        if fcs:
            cssstyle = "".join(fcs)
        del fcs
        with open(f"{filename}.html", "w") as whtm:
            whtm.write(cssstyle)
        pro = None
        if platform.startswith("win"):
            # ToDo: Preview for arm64 architecture
            # In preview no interactive printing even it open on browser
            pro = [
                "powershell.exe",
                "start",
                "msedge",
                f"'\"{Path(f'{filename}.html').absolute()}\"'",
            ]
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(pro, startupinfo=startupinfo)
        else:
            if preview:
                window = webview.create_window(
                    "TVG",
                    html=cssstyle,
                    resizable=False,
                    width=width if width else 800,
                    height=height if height else 600,
                    on_top=True,
                )
                webview.start()
            else:
                pro = ["open", "-a", "Safari", f"{Path(f'{filename}.html').absolute()}"]
                subprocess.run(pro)
    except Exception as e:
        raise e
    finally:
        del (
            text,
            filename,
            font,
            bg,
            fg,
            gettext,
            tohtml,
            background,
            foreground,
            kbfg,
            chg,
            setfont,
            cssstyle,
            printed,
            nxt,
            pro,
            startupinfo,
            pointer_event,
            window,
            preview,
            width,
            height,
        )
