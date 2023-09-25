# -*- coding: utf-8 -*-
# Copyright © kakkarja (K A K)


import os
import re
from pathlib import Path
from tkinter import (
    BOTTOM,
    CENTER,
    DISABLED,
    END,
    LEFT,
    NORMAL,
    RIGHT,
    TOP,
    Listbox,
    StringVar,
    Text,
    X,
    font,
    ttk,
)

from excptr import DEFAULTDIR, DEFAULTFILE, DIRPATH, excpcls

DEFAULTDIR = os.path.join(DIRPATH, "FreeTVG_TRACE")
if not os.path.exists(DEFAULTDIR):
    os.mkdir(DEFAULTDIR)
DEFAULTFILE = os.path.join(DEFAULTDIR, Path(DEFAULTFILE).name)

__all__ = [""]


@excpcls(m=2, filenm=DEFAULTFILE)
class Lay1(ttk.Frame):
    def __init__(self, root):
        super().__init__()
        self.pack(fill="x")
        self.entry = ttk.Entry(
            self,
            validate="none",
            validatecommand=self.focus,
            font="verdana 12",
        )
        self.entry.pack(
            side=LEFT, ipady=5, pady=(2, 2), padx=(2, 2), fill="both", expand=1
        )
        self.entry.config(state="disable")

        self.rb = StringVar()
        self.frbt = ttk.Frame(self)
        self.frbt.pack(padx=(12, 12), pady=2)
        self.frrb = ttk.Frame(self.frbt)
        self.frrb.pack(side=BOTTOM)
        self.radio1 = ttk.Radiobutton(
            self.frbt, text="parent", value="parent", var=self.rb, command=self.radiobut
        )
        self.radio1.pack(side=LEFT, anchor="w")
        self.radio2 = ttk.Radiobutton(
            self.frbt, text="child", value="child", var=self.rb, command=self.radiobut
        )
        self.radio2.pack(side=RIGHT, anchor="w")

        self.frcc = ttk.Frame(self.frrb)
        self.frcc.pack(side=TOP)
        self.label3 = ttk.Label(self.frcc, text="Child")
        self.label3.pack(side=LEFT, fill="x")
        self.entry3 = ttk.Combobox(
            self.frcc,
            width=8,
            exportselection=False,
            state="readonly",
            justify="center",
        )
        self.entry3.pack(side=LEFT, padx=1, pady=(0, 1), fill="x")

    def focus(self, event=None):
        """Validation for Entry"""

        if self.entry.validate:
            case = ["child", "parent"]
            if self.entry.get() in case:
                self.entry.delete(0, END)
                return True
            else:
                return False

    def _make_entry(self, ch: bool = True):
        if str(self.entry["state"]) == "disable":
            self.entry.configure(state="normal")
        if ch:
            self.entry3.config(state="normal")
            self.entry3.config(values=tuple([f"child{c}" for c in range(1, 51)]))
            self.entry3.current(0)
            self.entry3.config(state="readonly")
        else:
            self.entry3.config(state="normal")
            self.entry3.config(values="")
            self.entry3.delete(0, END)
            self.entry3.config(state="readonly")
        self.entry.configure(validate="focusin")

    def radiobut(self, event=None):
        """These are the switches on radio buttons, to apply certain rule on child"""

        match self.rb.get():
            case "parent":
                match w := self.entry.get():
                    case "child" | "":
                        self._make_entry(False)
                        if w:
                            self.entry.delete(0, END)
                        self.entry.insert(0, "parent")
                    case w if w != "parent":
                        self._make_entry(False)
            case "child":
                match w := self.entry.get():
                    case "parent" | "":
                        self._make_entry()
                        if w:
                            self.entry.delete(0, END)
                        self.entry.insert(0, "child")
                    case w if w != "child":
                        self._make_entry()


@excpcls(m=2, filenm=DEFAULTFILE)
class Lay2(ttk.Frame):
    def __init__(self, root):
        super().__init__()
        self.pack(side=TOP, fill="x", pady=(2, 0))

        self.button5 = ttk.Button(self, text="Insert", width=1)
        self.button5.pack(side=LEFT, pady=(2, 3), padx=(1, 1), fill="x", expand=1)

        self.button6 = ttk.Button(self, text="Write", width=1)
        self.button6.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)

        self.button9 = ttk.Button(self, text="Delete", width=1)
        self.button9.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)

        self.button7 = ttk.Button(self, text="BackUp", width=1)
        self.button7.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)

        self.button8 = ttk.Button(self, text="Load", width=1)
        self.button8.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)

        self.button3 = ttk.Button(self, text="Move Child", width=1)
        self.button3.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)

        self.button16 = ttk.Button(self, text="Change File", width=1)
        self.button16.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)

        self.button33 = ttk.Button(self, text="Fold Childs", width=1)
        self.button33.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)

        self.button17 = ttk.Button(self, text="CPP", width=1)
        self.button17.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)


@excpcls(m=2, filenm=DEFAULTFILE)
class Lay3(ttk.Frame):
    def __init__(self, root):
        super().__init__()
        self.pack(fill=X)
        self.button10 = ttk.Button(self, text="Insight", width=1)
        self.button10.pack(side=LEFT, pady=(0, 3), padx=(1, 1), fill="x", expand=1)

        self.button13 = ttk.Button(self, text="Arrange", width=1)
        self.button13.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)

        self.button11 = ttk.Button(self, text="Paste", width=1)
        self.button11.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)

        self.button4 = ttk.Button(self, text="Checked", width=1)
        self.button4.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)

        self.button = ttk.Button(self, text="Up", width=1)
        self.button.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)

        self.button2 = ttk.Button(self, text="Down", width=1)
        self.button2.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)

        self.button14 = ttk.Button(self, text="Hide Parent", width=1)
        self.button14.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)

        self.button34 = ttk.Button(self, text="Fold selected", width=1)
        self.button34.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)

        self.button15 = ttk.Button(self, text="Clear hide", width=1)
        self.button15.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)


@excpcls(m=2, filenm=DEFAULTFILE)
class Lay4(ttk.Frame):
    def __init__(self, root):
        super().__init__()
        self.pack(fill=X)
        self.button23 = ttk.Button(self, text="Create file", width=1)
        self.button23.pack(side=LEFT, pady=(0, 2), padx=(1, 1), fill="x", expand=1)

        self.button24 = ttk.Button(self, text="Editor", width=1)
        self.button24.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)

        self.button25 = ttk.Button(self, text="Un/Wrap", width=1)
        self.button25.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)

        self.button27 = ttk.Button(self, text="Ex", width=1)
        self.button27.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)

        self.button28 = ttk.Button(self, text="Template", width=1)
        self.button28.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)

        self.button20 = ttk.Button(self, text="Date-Time", width=1)
        self.button20.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)

        self.button19 = ttk.Button(self, text="Look Up", width=1)
        self.button19.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)

        self.button35 = ttk.Button(self, text="Unfold", width=1)
        self.button35.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)

        self.button12 = ttk.Button(self, text="Printing", width=1)
        self.button12.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)


@excpcls(m=2, filenm=DEFAULTFILE)
class Lay5(ttk.Frame):
    def __init__(self, root):
        super().__init__()
        self.pack(fill=X)
        self.pack_forget()


@excpcls(m=2, filenm=DEFAULTFILE)
class Lay6:
    def __init__(self, frm1, frm2, frm3) -> None:
        self.button30 = ttk.Button(frm1, text="Sum-Up", width=1)
        self.button30.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)

        self.button31 = ttk.Button(frm2, text="Pie-Chart", width=1)
        self.button31.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)

        self.button32 = ttk.Button(frm3, text="Del Total", width=1)
        self.button32.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)


@excpcls(m=2, filenm=DEFAULTFILE)
class Lay7(ttk.Frame):
    def __init__(self, root):
        super().__init__()
        frw = int(round(root.winfo_screenwidth() * 0.9224011713030746))
        lbw = int(round(frw * 0.09285714285714286))
        scw = int(round(frw * 0.011904761904761904))
        ftt = "verdana 11"
        self.pack(anchor="w", side=TOP, fill="both", expand=1)
        self.txframe = ttk.Frame(self)
        self.txframe.pack(anchor="w", side=LEFT, fill="both", expand=1)
        self.txframe.pack_propagate(0)
        self.text = Text(
            self.txframe,
            font=ftt,
            padx=5,
            pady=3,
            undo=True,
            autoseparators=True,
            maxundo=-1,
        )
        self.text.config(state="disable")
        self.text.pack(side=LEFT, fill="both", padx=(2, 1), pady=(1, 0), expand=1)
        self.text.pack_propagate(0)

        self.sc1frame = ttk.Frame(self, width=scw - 1)
        self.sc1frame.pack(anchor="w", side=LEFT, fill="y", pady=1)
        self.sc1frame.pack_propagate(0)
        self.scrollbar1 = ttk.Scrollbar(self.sc1frame, orient="vertical")
        self.scrollbar1.config(command=self.text.yview)
        self.scrollbar1.pack(side="left", fill="y")
        self.text.config(yscrollcommand=self.scrollbar1.set)

        self.tlframe = ttk.Frame(self, width=lbw)
        self.tlframe.pack(anchor="w", side=LEFT, fill="y")
        self.tlframe.pack_propagate(0)
        self.listb = Listbox(self.tlframe, font=ftt, exportselection=False)
        self.listb.pack(side=LEFT, fill="both", expand=1)
        self.listb.pack_propagate(0)

        self.sc2frame = ttk.Frame(self, width=scw)
        self.sc2frame.pack(anchor="w", side=LEFT, fill="y", pady=1)
        self.sc2frame.pack_propagate(0)
        self.scrollbar2 = ttk.Scrollbar(self.sc2frame, orient="vertical")
        self.scrollbar2.config(command=self.listb.yview)
        self.scrollbar2.pack(side="left", fill="y")
        self.listb.config(yscrollcommand=self.scrollbar2.set)
        del frw, lbw, scw

        self.mdw = ("~~", "^^", "==", "*", "^", "~")

    def find_sentence(self, sent: str, pos: tuple[int, int]) -> tuple[int, int] | None:
        regex = re.compile(r"[^\*{2}\*{1}\^{2}\^{1}\~{2}\~{1}\={2}\+{2}]+[\S\s]+?")
        if wordies := regex.search(sent):
            wordies = wordies.span()
            return pos[0] + wordies[0], pos[1] - wordies[0]
        del regex, wordies

    def finditer_sentences(
        self, sents: str, _iter: bool = False
    ) -> list[tuple[int, int]] | list:
        new = []
        regex = re.compile(r"[\*\^\~]+[\S\s]+?[\*\^\~]+|==+?[\S\s]+?==+?")
        for i in regex.finditer(sents):
            if i and "\\" not in i.group():
                match _iter:
                    case False:
                        new.append(self.find_sentence(i.group(), i.span()))
                        if new[-1] is None:
                            new.pop()
                    case True:
                        new.append(i.span())
        return new

    def combine_pos(self, sents: str) -> zip | None:
        p1 = self.finditer_sentences(sents, True)
        p2 = self.finditer_sentences(sents)

        if p1 and len(p1) == len(p2):
            p1 = tuple(p1)
            p2 = tuple(p2)
            return zip(p1, p2)
        del p1, p2

    def stat_changer(self):
        if self.text.cget("state") == DISABLED:
            self.text.configure(state=NORMAL)
        else:
            self.text.configure(state=DISABLED)

    def check(self):
        for i in self.text.tag_names():
            print(f"{i}: {self.text.tag_ranges(i)}")

    def text_view(self):
        container = enumerate(
            tuple(w for w in self.text.get("1.0", END)[:-1].splitlines(keepends=True))
        )
        posses = None
        toch = None
        touch = 0
        length = 0
        part = None
        mdset = []
        mdlen = None
        p1 = p2 = None
        count = 0
        got = False
        ft = str(self.text.cget("font"))
        edit_md = []
        g = None
        gr = None
        em = None
        bullet_width = None
        text_font = None
        try:
            text_font = font.Font(self, font=ft, name=ft, exists=True)
        except:
            text_font = font.Font(self, font=ft, name=ft, exists=False)
        for n, contain in container:
            if contain != "\n" and contain != "":
                if posses := self.finditer_sentences(contain, True):
                    g = re.compile(r"\s+")
                    em = text_font.measure(" ")
                    gr = g.match(contain)
                    if gr and gr.span()[1] > 1:
                        gr = gr.span()[1]
                        bullet_width = text_font.measure(f'{gr*" "}-')
                        self.text.tag_configure(
                            f"{gr}", lmargin1=em, lmargin2=em + bullet_width
                        )
                        got = True
                    for pos1 in posses:
                        toch = len(self.mdw)
                        part = contain[pos1[0] : pos1[1]]
                        ft = str(self.text.cget("font"))
                        while touch < toch:
                            match self.mdw[touch]:
                                case md if md in part and md == "*":
                                    count = part.count(md)
                                    if count > 1 and count % 2 == 0:
                                        if count == 6:
                                            if "bold" in ft and "italic" not in ft:
                                                self.text.tag_configure(
                                                    f"{md}{n+1}{pos1[0]}",
                                                    font=ft + " italic",
                                                )
                                            elif "italic" in ft and "bold" not in ft:
                                                self.text.tag_configure(
                                                    f"{md}{n+1}{pos1[0]}",
                                                    font=ft + " bold",
                                                )
                                            else:
                                                self.text.tag_configure(
                                                    f"{md}{n+1}{pos1[0]}",
                                                    font=ft + " bold italic",
                                                )
                                        elif count == 4:
                                            if "bold" not in ft:
                                                self.text.tag_configure(
                                                    f"{md}{n+1}{pos1[0]}",
                                                    font=ft + " bold",
                                                )
                                        elif count == 2:
                                            if "italic" not in ft:
                                                self.text.tag_configure(
                                                    f"{md}{n+1}{pos1[0]}",
                                                    font=ft + " italic",
                                                )
                                        part = part.replace(md, "")
                                        mdset.append(f"{md}{n+1}{pos1[0]}")
                                case md if md in part and md == "^^":
                                    count = part.count(md)
                                    if count > 1 and count % 2 == 0:
                                        self.text.tag_configure(
                                            f"{md}{n+1}{pos1[0]}", underline=True
                                        )
                                        part = part.replace(md, "")
                                        mdset.append(f"{md}{n+1}{pos1[0]}")
                                case md if md in part and md == "~~":
                                    count = part.count(md)
                                    if count > 1 and count % 2 == 0:
                                        self.text.tag_configure(
                                            f"{md}{n+1}{pos1[0]}", overstrike=True
                                        )
                                        part = part.replace(md, "")
                                        mdset.append(f"{md}{n+1}{pos1[0]}")
                                case md if md in part and md == "==":
                                    count = part.count(md)
                                    if count > 1 and count % 2 == 0:
                                        color = (
                                            "yellow"
                                            if str(self.text.cget("foreground"))
                                            != "white"
                                            else "grey"
                                        )
                                        self.text.tag_configure(
                                            f"{md}{n+1}{pos1[0]}", background=color
                                        )
                                        part = part.replace(md, "")
                                        mdset.append(f"{md}{n+1}{pos1[0]}")
                                        del color
                                case md if md in part and md == "^":
                                    count = part.count(md)
                                    if count > 1 and count % 2 == 0:
                                        fts = list(
                                            self.text.cget("font").rpartition("} ")
                                        )
                                        if fts[1]:
                                            fts[2] = "9" + fts[2][fts[2].find(" ") :]
                                        else:
                                            fts = fts[2].split(" ")
                                            fts[1] = "9"
                                        fts = " ".join(fts)
                                        self.text.tag_configure(
                                            f"{md}{n+1}{pos1[0]}", offset=6, font=fts
                                        )
                                        part = part.replace(md, "")
                                        mdset.append(f"{md}{n+1}{pos1[0]}")
                                        del fts
                                case md if md in part and md == "~":
                                    count = part.count(md)
                                    if count > 1 and count % 2 == 0:
                                        fts = list(
                                            self.text.cget("font").rpartition("} ")
                                        )
                                        if fts[1]:
                                            fts[2] = "9" + fts[2][fts[2].find(" ") :]
                                        else:
                                            fts = fts[2].split(" ")
                                            fts[1] = "9"
                                        fts = " ".join(fts)
                                        self.text.tag_configure(
                                            f"{md}{n+1}{pos1[0]}", offset=-4, font=fts
                                        )
                                        part = part.replace(md, "")
                                        mdset.append(f"{md}{n+1}{pos1[0]}")
                                        del fts
                            touch += 1
                        touch = 0

                        mdlen = contain[pos1[0] : pos1[1]]
                        p1 = self.text.search(mdlen, f"{n+1}.0", f"{n+2}.0")
                        p2 = f"{n+1}.{int(p1.partition('.')[2]) + len(mdlen)}"
                        self.text.delete(p1, p2)
                        self.text.insert(p1, part)
                        edit_md.append(
                            (
                                (
                                    p1,
                                    f"{n+1}.{int(p1.partition('.')[2]) + len(part)}",
                                    mdset.copy(),
                                )
                            )
                        )
                        mdset.clear()
                    contain = self.text.get(f"{n+1}.0", f"{n+1}.0 lineend + 1c")
                    self.text.delete(f"{n+1}.0", f"{n+1}.0 lineend + 1c")
                    if got:
                        got = False
                        self.text.insert(f"{n+1}.0", contain, gr)
                    else:
                        self.text.insert(f"{n+1}.0", contain)
                    for e in edit_md:
                        for m in e[2]:
                            self.text.tag_add(m, e[0], e[1])
                    edit_md.clear()
        del (
            container,
            posses,
            toch,
            touch,
            length,
            part,
            mdset,
            mdlen,
            p1,
            p2,
            ft,
            count,
            edit_md,
            g,
            gr,
            em,
            bullet_width,
            text_font,
        )


@excpcls(m=2, filenm=DEFAULTFILE)
class Lay8(ttk.Frame):
    def __init__(self, root):
        super().__init__()
        frw = int(round(root.winfo_screenwidth() * 0.9224011713030746))
        lbw = int(round(frw * 0.09285714285714286))
        scw = int(round(frw * 0.011904761904761904))
        self.pack(fill="x")
        self.frsc = ttk.Frame(self, height=scw + 1)
        self.frsc.pack(side=LEFT, fill="x", padx=(2, 1), expand=1)
        self.frsc.propagate(0)
        self.scrolh = ttk.Scrollbar(self.frsc, orient="horizontal")
        self.scrolh.pack(side=LEFT, fill="x", expand=1)
        self.scrolh.propagate(0)

        self.info = StringVar()
        self.frlab = ttk.Frame(self.frsc, width=lbw + (scw * 2), height=scw)
        self.frlab.pack(side=LEFT, fill="x")
        self.frlab.propagate(0)
        self.labcor = ttk.Label(
            self.frlab,
            anchor=CENTER,
            textvariable=self.info,
            font="consolas 10 bold",
            justify=CENTER,
        )
        self.labcor.pack(side=LEFT, fill="x", expand=1)
        self.labcor.propagate(0)
        del frw, lbw, scw


@excpcls(m=2, filenm=DEFAULTFILE)
class Scribe:
    def scribe(self):
        return {
            "Insert": "Insert word in outline on selected row",
            "Write": "Write word to outline base on chosen as parent or child",
            "Delete": "Delete an outline row",
            "BackUp": "Backup outline note [max 10 and recycle]",
            "Load": "Load a backuped note",
            "Move Child": "Move a child base note to left or right",
            "Change File": "Change to another existing file",
            "CPP": "Copy or move selected outline rows",
            "Look Up": "Look up word in outline list and in Editor mode",
            "Insight": "Details about outline position rows",
            "Arrange": "Clear selected row and arrange outline internally",
            "Paste": "Paste selected row to word for editing",
            "Checked": 'Insert "Check mark" or "Done" in selected row ',
            "Up": "Move selected row up",
            "Down": "Move selected row down",
            "Printing": "Create html page for printing",
            "Hide Parent": "Hiding parent and its childs or reverse",
            "Clear hide": "Clearing hidden back to appearing again",
            "Date-Time": "Insert time-stamp in Word and Editor mode",
            "Create file": "Create new empty note",
            "Editor": "To create outline note without restriction with proper format",
            "Un/Wrap": "Wrap or unwrap outline note",
            "Ex": "Edit whole notes or selected parent in Editor mode",
            "Template": "Create template for use frequently in Editor mode",
            "parent": "Create parent",
            "child": 'Create child ["Child" for positioning]',
            "B": "Bold for Markdown",
            "I": "Italic for Markdown",
            "U": "Underline for Markdown",
            "S": "Strikethrough for Markdown",
            "M": "Marking highlight for markdown",
            "SA": "Special attribute for markdown",
            "L": "Link url for Markdown",
            "SP": "Super-script for Markdown",
            "SB": "Sub-script for Markdown",
            "C": "Checked for Markdown",
            "AR": "Arrow-right for Markdown",
            "AL": "Arrow-left for Markdown",
            "AT": "Arrow-right-left for Markdown",
            "PM": "Plus-Minus for Markdown",
            "TM": "Trade Mark for Markdown",
            "CR": "Copy-Right for Markdown",
            "R": "Right for Markdown",
            "Fold Childs": "Folding all childs",
            "Fold selected": "Folding selected rows",
            "Unfold": "Unfolding selected or all childs",
        }
