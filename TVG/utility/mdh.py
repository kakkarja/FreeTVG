# -*- coding: utf-8 -*-
# Copyright (c) 2020, KarjaKAK
# All rights reserved.

import os
import re
from sys import platform

import markdown

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


def convhtml(text: str, filename: str, font: str, bg: str = None, fg: str = None):
    # Converting your TVG to html and printable directly from browser.

    try:
        gettext = text.split("\n")
        tohtml = []
        background = bg if bg else "gold"
        foreground = fg if fg else "black"
        kbfg = "333" if foreground == "black" else "eee"

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

        cssstyle = f"""<!DOCTYPE html>
<html>
<button class="button"  onclick="javascript:window.print();">Print</button>
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
"""
        printed = """@media print {
.button { display: none }
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
                if '<p><input type="checkbox"/>' in i:
                    g = '<p><input type="checkbox"/>'
                    fx = (
                        i[: len(g)]
                        + "<span>"
                        + i[len(g) : -4]
                        + "</span>"
                        + i[-4:]
                        + "\n"
                    )
                    fx = fx.replace(
                        g + "<span>",
                        '<p><input type="checkbox" class="strikethrough" name="ck"/><span for="ck">',
                    )
                    fcs.append(fx)
                    del g, fx
                elif '<p><input type="checkbox" checked/>' in i:
                    g = '<p><input type="checkbox" checked/>'
                    fx = (
                        i[: len(g)]
                        + "<span>"
                        + i[len(g) : -4]
                        + "</span>"
                        + i[-4:]
                        + "\n"
                    )
                    fx = fx.replace(
                        g + "<span>",
                        '<p><input type="checkbox" class="strikethrough" name="ck" checked/><span for="ck">',
                    )
                    fcs.append(fx)
                    del g, fx
                else:
                    fcs.append(f"{i}\n")

        if fcs:
            cssstyle = "".join(fcs)
        del fcs
        with open(f"{filename}.html", "w") as whtm:
            whtm.write(cssstyle)
        if platform.startswith("win"):
            os.startfile(f"{filename}.html")
        else:
            os.system(f'open "{filename}.html"')
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
        )
    except Exception as e:
        raise e
