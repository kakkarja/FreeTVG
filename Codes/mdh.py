# -*- coding: utf-8 -*-
#Copyright (c) 2020, KarjaKAK
#All rights reserved.

import markdown
import os
import re

def convhtml(text: str, filename: str, font: str, ckb: bool = False):
    # Converting your TVG to html and printable directly from browser.
    
    try:
        if os.path.isfile(text):
            with open(text) as rdf:
                gettext = rdf.readlines()
        else:
            gettext = text.split('\n')
            
        tohtml = []
        for i in gettext:
            if i != '\n':
                sp = re.match(r'\s+', i)
                if sp:
                    sp = sp.span()[1]-4
                    txt = re.search(r'-', i)
                    if txt and not i[txt.span()[1]:].isspace():
                        txt = f'* {i[txt.span()[1]:]}'
                    else:
                        txt = '*  '
                    tohtml.append(f'{" " * sp}{txt}\n\n')
                else:
                    if '\n' in i:
                        tohtml.append(f'#### {i}\n')
                    else:
                        tohtml.append(f'#### {i}\n\n')
        chg = f"""{''.join(tohtml)}"""
        a  = markdown.markdown(chg)
        setfont = 'body { ' + f"""background-color: gold;
  font-family: '{font}', san-serif;""" + ' }'
        checkbut = """.markdown-body .task-list-item {
  list-style-type: none !important;
}

.markdown-body .task-list-item input[type="checkbox"] {
  margin: 0 4px 0.25em -20px;
  vertical-align: middle;
}
"""
        cssstyle = f"""<!DOCTYPE html>
<html>
<button class="button"  onclick="javascript:window.print();">Print</button>
<header>
<h1>
<strong>
{filename}
</strong>
</h1>
</header>
<style>
{setfont}
"""
        printed = """@media print {
.button { display: none }
}
</style>
<body class="markdown-body">

"""
        nxt = f"""{a}

</body>
</html>
"""
        if ckb:
            cssstyle = cssstyle + checkbut + printed + nxt
            cssstyle = cssstyle.replace('<ul>', '<ul class="task-list">')
            cssstyle = cssstyle.replace('<li>', '<li class="task-list-item">')
            cssstyle = cssstyle.replace('<p>', '<p><input type="checkbox" enabled/>')
        else:
            cssstyle = cssstyle + printed + nxt
        with open(f'{filename}.html', 'w') as whtm:
            whtm.write(cssstyle)
        os.startfile(f'{filename}.html')
    except Exception as e:
        raise e