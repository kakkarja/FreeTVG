# -*- coding: utf-8 -*-
# Copyright © kakkarja (K A K)


import os
from pathlib import Path
from tkinter import (
    BOTTOM,
    END,
    LEFT,
    RIGHT,
    TOP,
    StringVar,
    X,
    ttk,
    Text,
    Listbox,
    CENTER,
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
        self.pack(side=TOP, fill="x")
        self.label = ttk.Label(self, text="Words")
        self.label.pack(side=LEFT, pady=3, fill="x")
        self.entry = ttk.Entry(
            self,
            validate="none",
            validatecommand=self.focus,
            font="consolas 12",
        )
        self.entry.pack(side=LEFT, ipady=5, pady=(3, 1), fill="both", expand=1)
        self.entry.config(state="disable")

        self.rb = StringVar()
        self.frbt = ttk.Frame(self)
        self.frbt.pack()
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
        self.label3.pack(side=LEFT, padx=1, pady=(0, 1), fill="x")
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
        self.pack(side=TOP, fill="x")

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
