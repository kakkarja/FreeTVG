import markdown
import os
import re

def convhtml(text: str, filename: str, font: str):
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
                    if txt:
                        txt = f'* #### {i[txt.span()[1]:]}'
                    else:
                        txt = '*  '
                    tohtml.append(f'{" " * sp}{txt}\n\n')
                else:
                    if '\n' in i:
                        tohtml.append(f'### {i}\n')
                    else:
                        tohtml.append(f'### {i}\n\n')
        chg = f"""{''.join(tohtml)}"""
        
        a = markdown.markdown(chg)
        setfont = 'body { ' + f"""background-color: gold;
  font-family: '{font}', san-serif;""" + ' }'
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
<body>

"""
        nxt = f"""{a}

</body>
</html>
"""
        cssstyle = cssstyle + printed + nxt
        with open(f'{filename}.html', 'w') as whtm:
            whtm.write(cssstyle)
        os.startfile(f'{filename}.html')
    except Exception as e:
        raise e