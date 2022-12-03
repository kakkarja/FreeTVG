# -*- coding: utf-8 -*-
# Copyright © kakkarja (K A K)


import ast
import importlib
import os
import re
import sys
from datetime import datetime as dt
from functools import partial
from itertools import islice
from pathlib import Path
from sys import platform
from tkinter import *
from tkinter import colorchooser, font, messagebox, simpledialog, ttk

from treeview import TreeView as tv
from treeview.dbase import Datab as db

from excptr import DEFAULTDIR, DEFAULTFILE, DIRPATH, excp, excpcls

from .utility.mdh import convhtml
from .utility.RegMail import composemail, wrwords
from .utility.term import ctlight

__all__ = ["main"]


DEFAULTDIR = os.path.join(DIRPATH, "FreeTVG_TRACE")
if not os.path.exists(DEFAULTDIR):
    os.mkdir(DEFAULTDIR)
DEFAULTFILE = os.path.join(DEFAULTDIR, Path(DEFAULTFILE).name)


match _addon := importlib.util.find_spec("addon_tvg"):
    case _addon if _addon is not None and _addon.name == "addon_tvg":
        if _addon.loader is not None:
            print("Add-On for TVG is ready!")
            from addon_tvg import Charts, EvalExp, SumAll
        else:
            print("Add-On for TVG is missing!")
    case _:
        print("Add-On for TVG is missing!")

THEME_MODE = ctlight()


@excpcls(m=2, filenm=DEFAULTFILE)
class TreeViewGui:
    """
    This is the Gui for TreeView engine. This gui is to make the Writing and editing is viewable.
    """

    DB = None
    FREEZE = False
    MARK = False
    MODE = False
    GEO = None

    def __init__(self, root, filename):
        self._addon = _addon
        self.tmode = THEME_MODE
        self.filename = filename
        self.root = root
        self.plat = platform
        self.glop = Path(os.getcwd())
        self.root.title(f"{self.glop.joinpath(self.filename)}.txt")
        self.root.protocol("WM_DELETE_WINDOW", self.tvgexit)
        self.wwidth = 850 if self._addon and self.plat.startswith("win") else 835
        self.wheight = 610
        self.root.minsize(self.wwidth, self.wheight)
        self.pwidth = int(self.root.winfo_screenwidth() / 2 - self.wwidth / 2)
        self.pheight = int(self.root.winfo_screenheight() / 3 - self.wheight / 3)
        self.root.geometry(f"{self.wwidth}x{self.wheight}+{self.pwidth}+{self.pheight}")
        TreeViewGui.GEO = f"{self.wwidth}x{self.wheight}+{self.pwidth}+{self.pheight}"
        gpath = self.glop.joinpath(self.glop.parent, "geo.tvg")
        gem = None
        if os.path.exists(gpath):
            with open(gpath, "rb") as geo:
                gem = ast.literal_eval(geo.read().decode("utf-8"))
                self.root.geometry(gem["geo"])
                TreeViewGui.GEO = gem["geo"]
        del gpath
        del gem
        self.root.bind_all("<Control-f>", self.fcsent)
        self.root.bind_all("<Control-r>", self.fcsent)
        self.root.bind_all("<Control-t>", self.fcsent)
        self.root.bind_all("<Control-i>", self.fcsent)
        self.root.bind_all("<Control-w>", self.fcsent)
        self.root.bind_all("<Control-b>", self.fcsent)
        self.root.bind_all("<Control-l>", self.fcsent)
        self.root.bind_all("<Control-d>", self.fcsent)
        self.root.bind_all("<Control-m>", self.fcsent)
        self.root.bind_all("<Control-s>", self.fcsent)
        self.root.bind_all("<Control-u>", self.fcsent)
        self.root.bind_all("<Control-o>", self.fcsent)
        self.root.bind_all("<Control-p>", self.fcsent)
        self.root.bind_all("<Control-h>", self.fcsent)
        self.root.bind_all("<Control-a>", self.fcsent)
        self.root.bind_all("<Control-e>", self.fcsent)
        self.root.bind_all("<Shift-Up>", self.scru)
        self.root.bind_all("<Shift-Down>", self.scrd)
        if self.plat.startswith("win"):
            self.root.bind("<Control-Up>", self.fcsent)
            self.root.bind("<Control-Down>", self.fcsent)
            self.root.bind("<Control-Left>", self.fcsent)
            self.root.bind("<Control-Right>", self.fcsent)
        else:
            self.root.bind_all("<Control-Shift-Up>", self.fcsent)
            self.root.bind_all("<Control-Shift-Down>", self.fcsent)
            self.root.bind_all("<Control-Shift-Left>", self.fcsent)
            self.root.bind_all("<Control-Shift-Right>", self.fcsent)
        self.root.bind_all("<Control-n>", self.fcsent)
        self.root.bind_all("<Control-y>", self.fcsent)
        self.root.bind_all("<Control-0>", self.fcsent)
        self.root.bind_all("<Control-minus>", self.fcsent)
        self.root.bind_all("<Control-Key-2>", self.lookup)
        self.root.bind_all("<Control-Key-3>", self.dattim)
        self.root.bind_all("<Control-Key-6>", self.fcsent)
        self.root.bind_all("<Control-Key-7>", self.fcsent)
        self.root.bind_all("<Control-Key-9>", self.fcsent)
        self.root.bind_all("<Control-Key-period>", self.fcsent)
        self.root.bind_all("<Control-Key-comma>", self.fcsent)
        self.root.bind_all("<Control-Key-slash>", self.fcsent)
        self.root.bind_all("<Control-Key-bracketleft>", self.fcsent)
        self.root.bind_all("<Control-Key-bracketright>", self.temp)
        self.root.bind_all("<Control-Key-g>", self.fcsent)
        self.root.bind_all("<Control-Key-question>", self.fcsent)
        self.root.bind_all("<Shift-Return>", self.inenter)
        self.root.bind_all("<Control-Shift-F>", self.fcsent)
        self.root.bind_all("<Control-Shift-S>", self.fcsent)
        self.root.bind_all("<Control-Shift-U>", self.fcsent)

        if self.plat.startswith("win"):
            self.root.bind_all("<Control-Key-F1>", self.fcsent)
            self.root.bind_all("<Control-Key-F2>", self.fcsent)
            self.root.bind_all("<Control-Key-F3>", self.fcsent)
            if self._addon:
                self.root.bind_all("<Control-Key-F4>", self.exprsum)
        else:
            self.root.bind_all("<Key-F1>", self.fcsent)
            self.root.bind_all("<Key-F2>", self.fcsent)
            self.root.bind_all("<Key-F3>", self.fcsent)
            if self._addon:
                self.root.bind_all("<Key-F4>", self.exprsum)

        if self._addon:
            self.root.bind_all("<Control-Key-1>", self.fcsent)
            self.root.bind_all("<Control-Key-4>", self.fcsent)
            self.root.bind_all("<Control-Key-5>", self.fcsent)

        self.root.bind_class("TButton", "<Enter>", self.ttip)
        self.root.bind_class("TButton", "<Leave>", self.leave)
        self.root.bind_class("TRadiobutton", "<Enter>", self.ttip)
        self.root.bind_class("TRadiobutton", "<Leave>", self.leave)

        self.bt = {}
        self.rb = StringVar()
        self.lock = False
        self.store = None
        self.editorsel = None
        self.stl = ttk.Style(self.root)
        self.stl.theme_use("clam")
        if self.plat.startswith("win"):
            self.stl.map("Horizontal.TScrollbar", background=[("active", "#eeebe7")])
            self.stl.map("Vertical.TScrollbar", background=[("active", "#eeebe7")])
        else:
            self.stl.element_create("My.Horizontal.Scrollbar.trough", "from", "default")
            self.stl.layout(
                "My.Horizontal.TScrollbar",
                [
                    (
                        "My.Horizontal.Scrollbar.trough",
                        {
                            "children": [
                                (
                                    "Horizontal.Scrollbar.leftarrow",
                                    {"side": "left", "sticky": ""},
                                ),
                                (
                                    "Horizontal.Scrollbar.rightarrow",
                                    {"side": "right", "sticky": ""},
                                ),
                                (
                                    "Horizontal.Scrollbar.thumb",
                                    {
                                        "unit": "0",
                                        "children": [
                                            (
                                                "Horizontal.Scrollbar.grip",
                                                {"sticky": ""},
                                            )
                                        ],
                                        "sticky": "nswe",
                                    },
                                ),
                            ],
                            "sticky": "we",
                        },
                    )
                ],
            )
            self.stl.element_create("My.Vertical.Scrollbar.trough", "from", "default")
            self.stl.layout(
                "My.Vertical.TScrollbar",
                [
                    (
                        "My.Vertical.Scrollbar.trough",
                        {
                            "children": [
                                (
                                    "Vertical.Scrollbar.uparrow",
                                    {"side": "top", "sticky": ""},
                                ),
                                (
                                    "Vertical.Scrollbar.downarrow",
                                    {"side": "bottom", "sticky": ""},
                                ),
                                (
                                    "Vertical.Scrollbar.thumb",
                                    {
                                        "unit": "0",
                                        "children": [
                                            ("Vertical.Scrollbar.grip", {"sticky": ""})
                                        ],
                                        "sticky": "nswe",
                                    },
                                ),
                            ],
                            "sticky": "ns",
                        },
                    )
                ],
            )
            self.stl.map("My.Horizontal.TScrollbar", background=[("active", "#eeebe7")])
            self.stl.map("My.Vertical.TScrollbar", background=[("active", "#eeebe7")])

        # 1st frame.
        # Frame for label and Entry.
        self.fframe = ttk.Frame(root)
        self.fframe.pack(side=TOP, fill="x")
        self.label = ttk.Label(self.fframe, text="Words")
        self.label.pack(side=LEFT, pady=3, fill="x")
        self.bt["label"] = self.label
        self.entry = ttk.Entry(
            self.fframe,
            validate="focusin",
            validatecommand=self.focus,
            font="consolas 12",
        )
        self.entry.pack(side=LEFT, ipady=5, pady=(3, 1), fill="both", expand=1)
        self.entry.config(state="disable")
        self.bt["entry"] = self.entry

        # 2nd frame in first frame.
        # Frame for radios button.
        self.frbt = ttk.Frame(self.fframe)
        self.frbt.pack()
        self.frrb = ttk.Frame(self.frbt)
        self.frrb.pack(side=BOTTOM)
        self.radio1 = ttk.Radiobutton(
            self.frbt, text="parent", value="parent", var=self.rb, command=self.radiobut
        )
        self.radio1.pack(side=LEFT, anchor="w")
        self.bt["radio1"] = self.radio1
        self.radio2 = ttk.Radiobutton(
            self.frbt, text="child", value="child", var=self.rb, command=self.radiobut
        )
        self.radio2.pack(side=RIGHT, anchor="w")
        self.bt["radio2"] = self.radio2

        # 3rd frame in 2nd frame.
        # Frame for Child ComboBox
        self.frcc = ttk.Frame(self.frrb)
        self.frcc.pack(side=TOP)
        self.label3 = ttk.Label(self.frcc, text="Child")
        self.label3.pack(side=LEFT, padx=1, pady=(0, 1), fill="x")
        self.bt["label3"] = self.label3
        self.entry3 = ttk.Combobox(
            self.frcc,
            width=8,
            exportselection=False,
            state="readonly",
            justify="center",
        )
        self.entry3.pack(side=LEFT, padx=1, pady=(0, 1), fill="x")
        self.bt["entry3"] = self.entry3

        # 3rd frame for top buttons.
        # Frame for first row Buttons.
        self.bframe = ttk.Frame(self.root)
        self.bframe.pack(side=TOP, fill="x")
        self.button5 = ttk.Button(
            self.bframe, text="Insert", width=1, command=self.insertwords
        )
        self.button5.pack(side=LEFT, pady=(2, 3), padx=(1, 1), fill="x", expand=1)
        self.button5.propagate(0)
        self.bt["button5"] = self.button5
        self.button6 = ttk.Button(
            self.bframe, text="Write", width=1, command=self.writefile
        )
        self.button6.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button6"] = self.button6
        self.button9 = ttk.Button(
            self.bframe, text="Delete", width=1, command=self.deleterow
        )
        self.button9.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button9"] = self.button9
        self.button7 = ttk.Button(
            self.bframe, text="BackUp", width=1, command=self.backup
        )
        self.button7.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button7"] = self.button7
        self.button8 = ttk.Button(
            self.bframe, text="Load", width=1, command=self.loadbkp
        )
        self.button8.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button8"] = self.button8
        self.button3 = ttk.Button(
            self.bframe, text="Move Child", width=1, command=self.move_lr
        )
        self.button3.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button3"] = self.button3
        self.button16 = ttk.Button(
            self.bframe, text="Change File", width=1, command=self.chgfile
        )
        self.button16.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button16"] = self.button16
        self.button33 = ttk.Button(
            self.bframe, text="Fold Childs", width=1, command=self.fold_childs
        )
        self.button33.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button33"] = self.button33
        self.button17 = ttk.Button(
            self.bframe, text="CPP", width=1, command=self.cmrows
        )
        self.button17.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button17"] = self.button17

        # 4th frame for below buttons.
        # Frame for second row buttons.
        self.frb1 = ttk.Frame(self.root)
        self.frb1.pack(fill=X)
        self.button10 = ttk.Button(
            self.frb1, text="Insight", width=1, command=self.insight
        )
        self.button10.pack(side=LEFT, pady=(0, 3), padx=(1, 1), fill="x", expand=1)
        self.bt["button10"] = self.button10
        self.button13 = ttk.Button(
            self.frb1, text="Arrange", width=1, command=self.spaces
        )
        self.button13.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button13"] = self.button13
        self.button11 = ttk.Button(self.frb1, text="Paste", width=1, command=self.copas)
        self.button11.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button11"] = self.button11
        self.button4 = ttk.Button(
            self.frb1, text="Checked", width=1, command=self.checked
        )
        self.button4.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button4"] = self.button4
        self.button = ttk.Button(self.frb1, text="Up", width=1, command=self.moveup)
        self.button.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button"] = self.button
        self.button2 = ttk.Button(
            self.frb1, text="Down", width=1, command=self.movedown
        )
        self.button2.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button2"] = self.button2
        self.button14 = ttk.Button(
            self.frb1, text="Hide Parent", width=1, command=self.hiddenchl
        )
        self.button14.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button14"] = self.button14
        self.button34 = ttk.Button(
            self.frb1, text="Fold selected", width=1, command=self.fold_selected
        )
        self.button34.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button34"] = self.button34
        self.button15 = ttk.Button(
            self.frb1, text="Clear hide", width=1, command=self.delhid
        )
        self.button15.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)
        self.bt["button15"] = self.button15

        # 7th Frame
        # For third row  of buttons
        self.frb2 = ttk.Frame(self.root)
        self.frb2.pack(fill=X)
        self.button23 = ttk.Button(
            self.frb2, text="Create file", width=1, command=self.createf
        )
        self.button23.pack(side=LEFT, pady=(0, 2), padx=(1, 1), fill="x", expand=1)
        self.bt["button23"] = self.button23
        self.button24 = ttk.Button(
            self.frb2, text="Editor", width=1, command=self.editor
        )
        self.button24.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)
        self.bt["button24"] = self.button24
        self.button25 = ttk.Button(
            self.frb2, text="Un/Wrap", width=1, command=self.wrapped
        )
        self.button25.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)
        self.bt["button25"] = self.button25
        self.button27 = ttk.Button(self.frb2, text="Ex", width=1, command=self.editex)
        self.button27.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)
        self.bt["button27"] = self.button27
        self.button28 = ttk.Button(
            self.frb2, text="Template", width=1, command=self.temp
        )
        self.button28.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)
        self.bt["button28"] = self.button28
        self.button20 = ttk.Button(
            self.frb2, text="Date-Time", width=1, command=self.dattim
        )
        self.button20.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)
        self.bt["button20"] = self.button20
        self.button19 = ttk.Button(
            self.frb2, text="Look Up", width=1, command=self.lookup
        )
        self.button19.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)
        self.bt["button19"] = self.button19
        self.button35 = ttk.Button(
            self.frb2, text="Unfold", width=1, command=self.unfolding
        )
        self.button35.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)
        self.bt["button35"] = self.button35
        self.button12 = ttk.Button(
            self.frb2, text="Printing", width=1, command=self.saveaspdf
        )
        self.button12.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)
        self.bt["button12"] = self.button12

        self.frb3 = ttk.Frame(self.root)
        self.frb3.pack(fill=X)
        self.frb3.pack_forget()

        if self._addon:
            self.button30 = ttk.Button(
                self.bframe, text="Sum-Up", width=1, command=self.gettotsum
            )
            self.button30.pack(side=LEFT, pady=(2, 3), padx=(0, 1), fill="x", expand=1)
            self.bt["button30"] = self.button30
            self.button31 = ttk.Button(
                self.frb1, text="Pie-Chart", width=1, command=self.createpg
            )
            self.button31.pack(side=LEFT, pady=(0, 3), padx=(0, 1), fill="x", expand=1)
            self.bt["button31"] = self.button31
            self.button32 = ttk.Button(
                self.frb2, text="Del Total", width=1, command=self.deltots
            )
            self.button32.pack(side=LEFT, pady=(0, 2), padx=(0, 1), fill="x", expand=1)
            self.bt["button32"] = self.button32

        self.stl.configure(
            "TButton",
            font="verdana 7 bold" if self.plat.startswith("win") else "verdana 8 bold",
        )

        # 5th frame.
        # Frame for text, listbox and scrollbars.
        frw = int(round(self.root.winfo_screenwidth() * 0.9224011713030746))
        lbw = int(round(frw * 0.09285714285714286))
        scw = int(round(frw * 0.011904761904761904))
        ftt = "verdana 11"
        self.tframe = ttk.Frame(root)
        self.tframe.pack(anchor="w", side=TOP, fill="both", expand=1)
        self.txframe = ttk.Frame(self.tframe)
        self.txframe.pack(anchor="w", side=LEFT, fill="both", expand=1)
        self.txframe.pack_propagate(0)
        self.text = Text(
            self.txframe,
            font=ftt,
            padx=5,
            pady=3,
            wrap=NONE,
            undo=True,
            autoseparators=True,
            maxundo=-1,
        )
        self.text.config(state="disable")
        self.text.pack(side=LEFT, fill="both", padx=(2, 1), pady=(1, 0), expand=1)
        self.text.bind("<MouseWheel>", self.mscrt)
        if self.plat.startswith("win"):
            self.text.bind("<Control-z>", self.undo)
            self.text.bind("<Control-Shift-Key-Z>", self.redo)
        else:
            self.text.bind("<Command-z>", self.undo)
            self.text.bind("<Command-y>", self.redo)
        self.text.pack_propagate(0)
        self.bt["text"] = self.text
        self.sc1frame = ttk.Frame(self.tframe, width=scw - 1)
        self.sc1frame.pack(anchor="w", side=LEFT, fill="y", pady=1)
        self.sc1frame.pack_propagate(0)
        if self.plat.startswith("win"):
            self.scrollbar1 = ttk.Scrollbar(self.sc1frame, orient="vertical")
        else:
            self.scrollbar1 = ttk.Scrollbar(
                self.sc1frame, orient="vertical", style="My.Vertical.TScrollbar"
            )
        self.scrollbar1.config(command=self.text.yview)
        self.scrollbar1.pack(side="left", fill="y")
        self.scrollbar1.bind("<ButtonRelease>", self.mscrt)
        self.text.config(yscrollcommand=self.scrollbar1.set)
        self.bt["scrollbar1"] = self.scrollbar1
        self.tlframe = ttk.Frame(self.tframe, width=lbw)
        self.tlframe.pack(anchor="w", side=LEFT, fill="y")
        self.tlframe.pack_propagate(0)
        self.listb = Listbox(self.tlframe, font=ftt, exportselection=False)
        self.listb.pack(side=LEFT, fill="both", expand=1)
        self.listb.pack_propagate(0)
        self.bt["listb"] = self.listb
        self.sc2frame = ttk.Frame(self.tframe, width=scw)
        self.sc2frame.pack(anchor="w", side=LEFT, fill="y", pady=1)
        self.sc2frame.pack_propagate(0)
        if self.plat.startswith("win"):
            self.scrollbar2 = ttk.Scrollbar(self.sc2frame, orient="vertical")
        else:
            self.scrollbar2 = ttk.Scrollbar(
                self.sc2frame, orient="vertical", style="My.Vertical.TScrollbar"
            )
        self.scrollbar2.config(command=self.listb.yview)
        self.scrollbar2.pack(side="left", fill="y")
        self.scrollbar2.bind("<ButtonRelease>", self.mscrl)
        self.listb.config(yscrollcommand=self.scrollbar2.set)
        self.listb.bind("<<ListboxSelect>>", self.infobar)
        self.listb.bind("<MouseWheel>", self.mscrl)
        self.listb.bind("<Up>", self.mscrl)
        self.listb.bind("<Down>", self.mscrl)
        self.listb.bind("<FocusIn>", self.flb)
        self.bt["scrollbar2"] = self.scrollbar2

        # 6th frame.
        # Frame for horizontal scrollbar and info label.
        self.fscr = ttk.Frame(self.root)
        self.fscr.pack(fill="x")
        self.frsc = ttk.Frame(self.fscr, height=scw + 1)
        self.frsc.pack(side=LEFT, fill="x", padx=(2, 1), expand=1)
        self.frsc.propagate(0)
        if self.plat.startswith("win"):
            self.scrolh = ttk.Scrollbar(self.frsc, orient="horizontal")
        else:
            self.scrolh = ttk.Scrollbar(
                self.frsc, orient="horizontal", style="My.Horizontal.TScrollbar"
            )
        self.scrolh.pack(side=LEFT, fill="x", expand=1)
        self.scrolh.config(command=self.text.xview)
        self.scrolh.propagate(0)
        self.text.config(xscrollcommand=self.scrolh.set)
        self.info = StringVar()
        self.info.set(f'{dt.strftime(dt.today(),"%a %d %b %Y")}')
        self.frlab = ttk.Frame(self.fscr, width=lbw + (scw * 2), height=scw)
        self.frlab.pack(side=LEFT, fill="x")
        self.frlab.propagate(0)
        self.labcor = Label(
            self.frlab, textvariable=self.info, font="consolas 10 bold", justify=CENTER
        )
        self.labcor.pack(side=LEFT, fill="x", expand=1)
        self.labcor.propagate(0)
        self.unlock = True

        if os.path.exists(self.glop.joinpath(self.glop.parent, "ft.tvg")):
            self.ft(path=self.glop.joinpath(self.glop.parent, "ft.tvg"))

        if os.path.exists(self.glop.joinpath(self.glop.parent, "theme.tvg")):
            self.txtcol(
                path=self.glop.joinpath(self.glop.parent, "theme.tvg"), wr=False
            )

        if os.path.isfile(self.glop.joinpath(self.glop.parent, "hbts.tvg")):
            frm = [self.bframe, self.frb1, self.frb2]
            for fr in frm:
                fr.pack_forget()
            del frm

        if os.path.exists(self.glop.absolute().joinpath("fold.tvg")):
            self.fold = True

        self.ldmode()

        self.tpl = None
        self.ai = None
        self.scribe = {
            "Insert": "Insert word in outline on selected row",
            "Write": "Write word to outline base on chosen as parent or child",
            "Delete": "Delete an outline row",
            "BackUp": "Backup outline note [max 10 and recycle]",
            "Load": "Load a backuped note",
            "Move Child": "Move a child base note to left or right",
            "Change File": "Change to another existing file",
            "CPP": "Copy or move selected outline rows",
            "Send Note": "Switch to TeleTVG for sending note or chat",
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
            "Save": "Save note as encrypted text and can be send",
            "Open": "Open the encrypted TVG text file and can be saved",
            "Create file": "Create new empty note",
            "Editor": "To create outline note without restriction with proper format",
            "Un/Wrap": "Wrap or unwrap outline note",
            "Calculator": "Switch to calculator",
            "Ex": "Edit whole notes or selected parent in Editor mode",
            "Template": "Create template for use frequently in Editor mode",
            "Emoji": "Insert emoji to note",
            "HTML View": "Viewing html page that has been created before",
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

        self.ew = None
        if self._addon:
            on = {
                "Sum-Up": "Summing all add-on",
                "Pie-Chart": "Graph base on all sums",
                "Del Total": "Delete all totals",
            }
            self.scribe = self.scribe | on
            self.ew = list(on) + ["child", "R"]
            if os.path.exists(self.glop.absolute().joinpath("sumtot.tvg")):
                self.sumtot = True
                os.remove(self.glop.absolute().joinpath("sumtot.tvg"))
        else:
            self.ew = ["CPP", "Clear hide", "Printing", "child", "R"]
        self.rsv_frame = None

    def ldmode(self):
        """Dark mode for easing the eye"""

        oribg = "#dcdad5"
        chbg = "grey30"
        orifg = "black"
        chfg = "white"
        if self.tmode == "dark" or not self.tmode:
            self.stl.configure(
                ".",
                background=chbg,
                foreground=chfg,
                fieldbackground=chbg,
                insertcolor=chfg,
                troughcolor=chbg,
                arrowcolor=chfg,
                bordercolor=chbg,
            )
            self.stl.map(
                ".",
                background=[("background", chbg)],
            )
            self.stl.map(
                "TCombobox",
                fieldbackground=[("readonly", chbg)],
                background=[("active", "gold")],
                arrowcolor=[("active", "black")],
            )
            self.stl.map(
                "Horizontal.TScrollbar",
                background=[("active", "gold")],
                arrowcolor=[("active", "black")],
            )
            self.stl.map(
                "Vertical.TScrollbar",
                background=[("active", "gold")],
                arrowcolor=[("active", "black")],
            )
            self.stl.configure("TEntry", fieldbackground=chbg)
            self.labcor.config(bg=chbg, fg=chfg)
            if str(self.text.cget("background")) == "SystemWindow":
                with open(
                    self.glop.joinpath(self.glop.parent, "theme.tvg"), "w"
                ) as thm:
                    thm.write("#4d4d4d")
                self.txtcol(
                    path=self.glop.joinpath(self.glop.parent, "theme.tvg"), wr=False
                )
            del oribg, chbg, orifg, chfg
        elif self.tmode == "light":
            self.stl.configure(
                ".",
                background=oribg,
                foreground=orifg,
                fieldbackground=oribg,
                insertcolor=orifg,
                troughcolor=oribg,
                arrowcolor=orifg,
                bordercolor=oribg,
            )
            self.stl.configure("TEntry", fieldbackground="white")
            self.stl.map(
                "TCombobox",
                fieldbackground=[
                    ("focus", "dark blue"),
                    ("readonly", oribg),
                    ("disabled", "white"),
                ],
                background=[("active", "#eeebe7")],
            )
            self.stl.map("Horizontal.TScrollbar", background=[("active", "#eeebe7")])
            self.stl.map("Vertical.TScrollbar", background=[("active", "#eeebe7")])
            self.labcor.config(bg="White", fg=orifg)
            del oribg, chbg, orifg, chfg

    def ttip(self, event=None):
        """Tooltip for TVG buttons"""

        ckframe = (
            ".!frame.!frame",
            ".!frame2",
            ".!frame3",
            ".!frame4",
            self.rsv_frame,
        )
        if event.widget.winfo_parent() in ckframe and (
            tx := self.scribe.get(event.widget["text"], None)
        ):

            def exit():
                self.root.update()
                self.ai = None
                self.tpl = None
                master.destroy()

            master = Toplevel(self.root)
            master.overrideredirect(1)
            ft = font.Font(master, font="verdana", weight=font.BOLD)

            if self.plat.startswith("win"):
                msr = int(ft.measure(tx) / 2)
                spc = int(ft.measure(tx) / 2.6)
                fnt = "verdana 7 bold"
            else:
                msr = int(ft.measure(tx) / 1.4)
                spc = int(ft.measure(tx) / 2)
                fnt = "verdana 8 bold"

            if event.widget["text"] in self.ew:
                master.geometry(
                    f"{msr}x{15}+{event.widget.winfo_rootx()-spc}+{event.widget.winfo_rooty()+25}"
                )
            else:
                master.geometry(
                    f"{msr}x{15}+{event.widget.winfo_rootx()}+{event.widget.winfo_rooty()+25}"
                )

            a = Message(
                master=master,
                text=tx,
                justify="center",
                aspect=int(ft.measure(tx) * 50),
                bg="white",
                font=fnt,
                fg="black",
            )
            a.pack(fill="both", expand=1)
            del ft, tx, msr, spc, fnt
            self.ai = self.root.after(3000, exit)
            self.tpl = master

    def leave(self, event=None):
        """On hovering and leaving a button the tooltip will be destroyed"""

        if self.ai and self.tpl:
            self.root.after_cancel(self.ai)
            self.tpl.destroy()
            self.ai = self.tpl = None

    def hidbs(self, event=None):
        """Hide Buttons"""

        frm = [self.bframe, self.frb1, self.frb2]
        pth = self.glop.joinpath(self.glop.parent, "hbts.tvg")
        self.tframe.pack_forget()
        self.fscr.pack_forget()
        if bool(frm[0].winfo_ismapped()):
            for fr in frm:
                fr.pack_forget()
            with open(pth, "w") as bh:
                bh.write("buttons hide")
        else:
            for fr in frm:
                fr.pack(side=TOP, fill="x")
            self.stl.configure("TButton", font="verdana 8 bold")
            os.remove(pth)
        self.tframe.pack(anchor="w", side=TOP, fill="both", expand=1)
        self.tframe.update()
        self.fscr.pack(fill="x")
        self.fscr.update()
        del frm, pth

    def inenter(self, event):
        """For invoking any focus button or radiobutton"""

        ck = ["button", "radio"]
        fcs = str(event.widget).rpartition("!")[2]
        if ck[0] in fcs or ck[1] in fcs:
            event.widget.invoke()
        del ck, fcs

    def undo(self, event=None):
        """Undo only in Editor"""

        if str(self.text["state"]) == "normal":
            try:
                self.text.edit_undo()
            except:
                messagebox.showerror(
                    "TreeViewGui", "Nothing to undo!", parent=self.root
                )

    def redo(self, event=None):
        """Redo only in Editor"""

        if str(self.text["state"]) == "normal":
            try:
                self.text.edit_redo()
            except:
                messagebox.showerror(
                    "TreeViewGui", "Nothing to redo!", parent=self.root
                )

    def wrapped(self, event=None):
        """Wrap the records so that all filled the text window"""
        # The scrolling horizontal become inactive.

        if str(self.text.cget("wrap")) == "none":
            self.text.config(wrap=WORD)
        else:
            self.text.config(wrap=NONE)

    def infobar(self, event=None):
        """Info Bar telling the selected rows in listbox.
        If nothing, it will display today's date.
        """

        if os.path.exists(f"{self.filename}_hid.json"):
            self.info.set("Hidden Mode")
        elif TreeViewGui.FREEZE and str(self.bt["button17"]["state"]) == "normal":
            self.info.set("CPP Mode")
        elif TreeViewGui.FREEZE and str(self.bt["button24"]["state"]) == "normal":
            self.info.set("Editor Mode")
        elif self.listb.curselection():
            st = int(self.listb.curselection()[0])
            insight = None
            with tv(f"{self.filename}") as tvg:
                insight = tuple(islice(tvg.compdatch(True), st, st + 1))
                ck = insight[0][1][:12]
            self.info.set(f"{st}: {ck[:-1]}...")
            self.text.see(f"{st}.0")
            del ck, tvg, st, insight
        else:
            self.info.set(f'{dt.strftime(dt.today(),"%a %d %b %Y")}')

    def checkfile(self):
        """Checking file if it is exist"""

        if os.path.exists(f"{self.filename}.txt"):
            return True
        else:
            return False

    def mscrt(self, event=None):
        """Mouse scroll on text window, will sync with list box on the right"""

        if self.text.yview()[1] < 1.0:
            self.listb.yview_moveto(self.text.yview()[0])
        else:
            self.listb.yview_moveto(self.text.yview()[1])

    def mscrl(self, event=None):
        """Mouse scroll on list box window, will sync with text window on the right"""

        if self.listb.yview()[1] < 1.0:
            self.text.yview_moveto(self.listb.yview()[0])
        else:
            self.text.yview_moveto(self.listb.yview()[1])

    def fcsent(self, event=None):
        """Key Bindings to keyboards"""

        fcom = str(self.root.focus_get())
        if TreeViewGui.FREEZE is False:
            if event.keysym == "f":
                self.entry.focus()
            elif event.keysym == "r":
                self.entry3.focus()
            elif event.keysym == "t":
                st = self.listb.curselection()
                if st:
                    self.listb.focus()
                    self.listb.activate(int(st[0]))
                    self.listb.see(int(st[0]))
                    self.text.yview_moveto(self.listb.yview()[0])
                else:
                    self.listb.focus()
            elif event.keysym == "i":
                self.insertwords()
            elif event.keysym == "w":
                self.writefile()
            elif event.keysym == "b":
                self.backup()
            elif event.keysym == "l":
                self.loadbkp()
            elif event.keysym == "d":
                self.deleterow()
            elif event.keysym == "m":
                self.move_lr()
            elif event.keysym == "s":
                self.insight()
            elif event.keysym == "u":
                self.moveup()
            elif event.keysym == "o":
                self.movedown()
            elif event.keysym == "p":
                self.saveaspdf()
            elif event.keysym == "h":
                self.hiddenchl()
            elif event.keysym == "a":
                if self.rb.get() == "parent":
                    self.rb.set("child")
                    self.radiobut()
                else:
                    self.rb.set("parent")
                    self.radiobut()
            elif event.keysym == "e":
                self.copas()
            elif event.keysym == "y":
                self.checked()
            elif event.keysym == "0":
                self.spaces()
            elif event.keysym == "minus":
                self.delhid()
            elif event.keysym == "Left" and "entry" not in fcom:
                self.pwidth = self.root.winfo_x() - 1
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == "Right" and "entry" not in fcom:
                self.pwidth = self.root.winfo_x() + 1
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == "Down" and "entry" not in fcom:
                self.pheight = self.root.winfo_y() + 1
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == "Up" and "entry" not in fcom:
                self.pheight = self.root.winfo_y() - 1
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == "n":
                self.cmrows()
            elif event.keysym == "g":
                self.chgfile()
            elif event.keysym == "6":
                self.createf()
            elif event.keysym == "7":
                self.editor()
            elif event.keysym == "9":
                self.wrapped()
            elif self._addon and event.keysym == "1":
                self.gettotsum()
            elif self._addon and event.keysym == "4":
                self.createpg()
            elif self._addon and event.keysym == "5":
                self.deltots()
            elif event.keysym == "bracketleft":
                self.editex()
            elif event.keysym == "period":
                self.txtcol()
            elif event.keysym == "comma":
                self.ft()
            elif event.keysym == "slash":
                self.oriset()
            elif event.keysym == "F2":
                self.hidbs()
            elif event.keysym == "F3":
                self.send_reg()
            elif event.keysym == "F1":
                self.tutorial()
            elif event.keysym == "F":
                self.fold_childs()
            elif event.keysym == "U":
                self.unfolding()
            elif event.keysym == "S":
                self.fold_selected()
        else:
            if (
                str(self.bt["button17"].cget("state")) == "normal"
                and event.keysym == "n"
            ):
                self.cmrows()
            elif (
                str(self.bt["button14"].cget("state")) == "normal"
                and event.keysym == "h"
            ):
                self.hiddenchl()
            elif (
                str(self.bt["button24"].cget("state")) == "normal"
                and event.keysym == "7"
            ):
                self.editor()
            elif (
                str(self.bt["button34"].cget("state")) == "normal"
                and event.keysym == "S"
            ):
                self.fold_selected()
        del fcom

    def radiobut(self, event=None):
        """These are the switches on radio buttons, to apply certain rule on child"""

        case = {"": self.rb.get(), "child": "child", "parent": "parent"}
        self.entry.config(state="normal")
        if self.entry.get() in case:
            if case[self.rb.get()] == "child":
                self.entry3.config(values=tuple([f"child{c}" for c in range(1, 51)]))
                self.entry3.current(0)
            elif case[self.rb.get()] != "child":
                self.entry3.config(values="")
                self.entry3.config(state="normal")
                self.entry3.delete(0, END)
                self.entry3.config(state="readonly")
            self.entry.delete(0, END)
            if len(str(self.entry.focus_get())) > 5:
                if str(self.entry.focus_get())[-5:] != "entry":
                    self.entry.insert(0, case[""])
            else:
                self.entry.insert(0, case[""])
        else:
            if case[self.rb.get()] == "child":
                self.entry3.config(values=tuple([f"child{c}" for c in range(1, 51)]))
                self.entry3.current(0)
            elif case[self.rb.get()] != "child":
                self.entry3.config(values="")
                self.entry3.config(state="normal")
                self.entry3.delete(0, END)
                self.entry3.config(state="readonly")
            self.entry.selection_clear()
        del case

    def focus(self, event=None):
        """Validation for Entry"""

        if self.entry.validate:
            case = ["child", "parent"]
            if self.entry.get() in case:
                self.entry.delete(0, END)
                return True
            else:
                return False
            del case

    def scrd(self, event=None):
        """Scroll to the bottom on keyboard, down arrow button"""

        a = self.text.yview()[0]
        a = eval(f"{a}") + 0.01
        self.text.yview_moveto(str(a))
        self.listb.yview_moveto(str(a + 0.01))
        del a

    def scru(self, event=None):
        """Scroll to the first position on keyboard, up arrow button"""

        a = self.text.yview()[0]
        a = eval(f"{a}") - 0.01
        self.text.yview_moveto(str(a))
        self.listb.yview_moveto(str(a))
        del a

    def _prettyv(self, tx):
        """Wrapping mode view purpose"""

        self._deltags()
        nf = str(self.text.cget("font"))
        try:
            text_font = font.Font(self.root, font=nf, name=nf, exists=True)
        except:
            text_font = font.Font(self.root, font=nf, name=nf, exists=False)
        g = re.compile(r"\s+")
        em = text_font.measure(" ")
        for _, v in tx:
            gr = g.match(v)
            if gr and gr.span()[1] > 1:
                bullet_width = text_font.measure(f'{gr.span()[1]*" "}-')
                self.text.tag_configure(
                    f"{gr.span()[1]}", lmargin1=em, lmargin2=em + bullet_width
                )
                self.text.insert(END, v, f"{gr.span()[1]}")
            else:
                self.text.insert(END, v)
            del gr
        del tx, nf, text_font, g, em

    def view(self, event=None):
        """Viewing engine for most module fuction"""

        if self.checkfile() and self.nonetype():
            self.text.config(state="normal")
            self.text.delete("1.0", END)
            self.listb.delete(0, END)
            with tv(self.filename) as tvg:
                self._prettyv(tvg.getdata())
                for k, v in tvg.insighttree():
                    self.listb.insert(END, f"{k}: {v[0]}")
            self.text.edit_reset()
            self.text.config(state="disable")
            self.text.yview_moveto(1.0)
            self.listb.yview_moveto(1.0)
            del tvg
            self.foldfun()

    def _sumchk(self):
        sumtot = SumAll(self.filename, sig="+")
        if sumtot.chksign() and sumtot.chktot():
            if not hasattr(self, "sumtot"):
                self.__setattr__("sumtot", True)
        else:
            if hasattr(self, "sumtot"):
                self.__delattr__("sumtot")
        del sumtot

    def addonchk(self, sta: bool = True):
        """Checking on addon for sumtot attribute purpose"""

        if self._addon:
            if self.checkfile():
                if sta:
                    if hasattr(self, "sumtot"):
                        with open(
                            self.glop.absolute().joinpath("sumtot.tvg"), "wb"
                        ) as st:
                            st.write("True".encode())
                else:
                    if not self.glop.absolute().joinpath("sumtot.tvg").exists():
                        self._sumchk()
                    else:
                        self._sumchk()
                        os.remove(self.glop.absolute().joinpath("sumtot.tvg"))
            else:
                if hasattr(self, "sumtot"):
                    self.__delattr__("sumtot")

    def chgfile(self):
        """Changing file on active app environment"""

        def chosen(file):
            fi = file
            TreeViewGui.FREEZE = False
            ask = messagebox.askyesno(
                "TreeViewGui",
                '"Yes" to change file, "No" to delete directory',
                parent=self.root,
            )
            if ask:
                self.addonchk()
                os.chdir(self.glop.joinpath(self.glop.parent, fi))
                self.filename = fi.rpartition("_")[0]
                self.glop = Path(self.glop.joinpath(self.glop.parent, fi))
                self._chkfoldatt()
                self.root.title(f"{self.glop.joinpath(self.filename)}.txt")
                if os.path.exists(self.glop.joinpath(f"{self.filename}.txt")):
                    if not os.path.exists(
                        self.glop.joinpath(f"{self.filename}_hid.json")
                    ):
                        self.spaces()
                        self.infobar()
                    else:
                        self.hidform()
                        self.infobar()
                else:
                    self.text.config(state="normal")
                    self.text.delete("1.0", END)
                    self.text.config(state="disable")
                    self.listb.delete(0, END)
                self.addonchk(False)
            else:
                import shutil

                if self.glop.name != fi:
                    lf = os.listdir(self.glop.joinpath(self.glop.parent, fi))
                    lsc = messagebox.askyesno(
                        "TreeViewGui",
                        f"Do you really want to delete {fi} directory with all\n{lf}\nfiles?",
                        parent=self.root,
                    )
                    if lsc:
                        shutil.rmtree(self.glop.joinpath(self.glop.parent, fi))
                    else:
                        messagebox.showinfo(
                            "TreeViewGui",
                            "Deleting directory is aborted!",
                            parent=self.root,
                        )
                else:
                    messagebox.showerror(
                        "TreeViewGui",
                        "You are unable to delete present directory!!!",
                        parent=self.root,
                    )
            del fi, ask, file

        files = [file for file in os.listdir(self.glop.parent) if "_tvg" in file]
        files.sort()
        if self.lock is False and files:
            TreeViewGui.FREEZE = True
            self.lock = True

            @excpcls(2, DEFAULTFILE)
            class MyDialog(simpledialog.Dialog):
                def body(self, master):
                    self.title("Choose File")
                    Label(master, text="File: ").grid(row=0, column=0, sticky=E)
                    self.e1 = ttk.Combobox(master)
                    self.e1["values"] = files
                    self.e1.grid(row=0, column=1)
                    self.e1.bind(
                        "<KeyRelease>", partial(TreeViewGui.tynam, files=files)
                    )
                    return self.e1

                def apply(self):
                    self.result = self.e1.get()

            d = MyDialog(self.root)
            self.lock = False
            if d.result:
                chosen(d.result)
            else:
                TreeViewGui.FREEZE = False
            del d
        del files

    def writefile(self, event=None):
        """Write first entry and on next updated line.
        Write also on chosen row for update.
        """

        self.hidcheck()
        cek = ["child", "parent"]
        if self.unlock:
            if not self.checkfile():
                if self.entry.get():
                    if not self.entry3.get():
                        if self.entry.get() not in cek:
                            with tv(self.filename) as tvg:
                                tvg.writetree(self.entry.get())
                            del tvg
                            self.entry.delete(0, END)
                            self.spaces()
                    else:
                        messagebox.showinfo(
                            "TreeViewGui",
                            f"No {self.filename}.txt file yet created please choose parent first!",
                            parent=self.root,
                        )
                else:
                    messagebox.showinfo(
                        "TreeViewGui",
                        f"No {self.filename}.txt file yet created!",
                        parent=self.root,
                    )
            else:
                rw = None
                if self.entry3.get():
                    if self.entry.get() and self.entry.get() not in cek:
                        if TreeViewGui.MARK:
                            rw = self.listb.curselection()[0]
                            appr = messagebox.askyesno(
                                "Edit", f"Edit cell {rw}?", parent=self.root
                            )
                            if appr:
                                with tv(self.filename) as tvg:
                                    insight = tuple(
                                        islice(
                                            tvg.compdatch(True),
                                            int(rw),
                                            int(rw) + 1,
                                        )
                                    )
                                    if insight[0][0] != "space":
                                        tvg.edittree(
                                            self.entry.get(),
                                            int(rw),
                                            self.entry3.get(),
                                        )
                                del tvg, insight
                                self.entry.delete(0, END)
                        else:
                            with tv(self.filename) as tvg:
                                tvg.quickchild(self.entry.get(), self.entry3.get())
                            self.entry.delete(0, END)
                            del tvg
                        self.spaces()
                else:
                    if self.entry.get() and self.entry.get() not in cek:
                        if TreeViewGui.MARK:
                            rw = self.listb.curselection()[0]
                            appr = messagebox.askyesno(
                                "Edit", f"Edit cell {rw}?", parent=self.root
                            )
                            if appr:
                                with tv(self.filename) as tvg:
                                    insight = tuple(
                                        islice(
                                            tvg.compdatch(True),
                                            int(rw),
                                            int(rw) + 1,
                                        )
                                    )
                                    if insight[0][0] != "space":
                                        tvg.edittree(self.entry.get(), int(rw))
                                del tvg, insight
                                self.entry.delete(0, END)
                        else:
                            with tv(self.filename) as tvg:
                                tvg.addparent(self.entry.get())
                            del tvg
                            self.entry.delete(0, END)
                        self.spaces()
                if rw and rw < len(self.listb.get(0, END)) - 1:
                    self.text.see(f"{int(rw)}.0")
                    self.listb.see(rw)
                del rw
        del cek

    def flb(self, event=None):
        """Set Mark for cheking row for edit"""

        TreeViewGui.MARK = True

    def deleterow(self):
        """Deletion on recorded row and updated"""

        self.hidcheck()
        if self.unlock:
            if self.checkfile() and self.nonetype():
                if self.listb.curselection():
                    TreeViewGui.MODE = True
                    rw = int(self.listb.curselection()[0])
                    with tv(self.filename) as tvg:
                        if rw != 0:
                            tvg.delrow(rw)

                    del tvg
                    self.spaces()
                    if rw > self.listb.size() - 1:
                        if self.listb.get(rw - 1):
                            rw = rw - 1
                        else:
                            rw = rw - 2
                    ck = tuple(
                        [
                            self.listb.size(),
                            self.listb.get(rw).split(":")[1].strip(),
                        ]
                    )

                    if rw < ck[0]:
                        if ck[1] != "space" and rw != 0:
                            self.listb.select_set(rw)
                            self.listb.see(rw)
                            self.text.see(f"{(rw)}.0")
                        else:
                            self.listb.select_set(rw - 1)
                            self.listb.see(rw - 1)
                            self.text.see(f"{(rw-1)}.0")
                    else:
                        if ck[0] == 1:
                            self.listb.select_set(0)
                        else:
                            self.listb.select_set(len(ck) - 1)
                            self.listb.see(len(ck) - 1)
                            self.text.see(f"{(len(ck)-1)}.0")
                    del rw, ck
                    self.infobar()

    def move_lr(self, event=None):
        """Moving a child row to left or right, as to define spaces needed"""

        self.hidcheck()
        if self.unlock:
            if self.listb.curselection():
                if self.entry3.get():
                    TreeViewGui.MODE = True
                    try:
                        rw = int(self.listb.curselection()[0])
                        self.text.config(state="normal")
                        with tv(self.filename) as tvg:
                            tvg.movechild(rw, self.entry3.get())
                        del tvg
                        self.spaces()
                        self.text.config(state="disable")
                        self.listb.select_set(rw)
                        self.listb.see(rw)
                        self.text.see(f"{rw}.0")
                    except:
                        self.text.insert(
                            END, "Parent row is unable to be move to a child"
                        )
                        self.text.config(state="disable")
                    del rw
                    self.infobar()

    def insight(self, event=None):
        """To view the whole rows, each individually with the correspondent recorded values"""

        self.hidcheck()
        if self.unlock:
            if self.checkfile() and self.nonetype():
                self.text.config(state="normal")
                self.text.delete("1.0", END)
                with tv(self.filename) as tvg:
                    for k, v in tvg.insighttree():
                        self.text.insert(END, f"row {k}: {v[0]}, {v[1]}")
                del tvg
                self.text.edit_reset()
                self.text.config(state="disable")

    def moveup(self, event=None):
        """Step up a row to upper row"""

        self.hidcheck()
        if self.unlock:
            if self.checkfile() and self.nonetype():
                if self.listb.curselection():
                    rw = int(self.listb.curselection()[0])
                    insight = self.listb.get(rw).split(":")[1].strip()
                    if insight != "space" and "child" in insight:
                        if rw != 0 and rw - 1 != 0:
                            TreeViewGui.MODE = True
                            with tv(self.filename) as tvg:
                                tvg.movetree(rw, rw - 1)
                            del tvg
                            self.spaces()
                            ck = self.listb.get(rw - 1).split(":")[1].strip()
                            if ck != "space":
                                self.listb.select_set(rw - 1)
                                self.listb.see(rw - 1)
                                self.text.see(f"{rw - 1}.0")
                            else:
                                self.listb.select_set(rw - 2)
                                self.listb.see(rw - 2)
                                self.text.see(f"{rw - 2}.0")
                            self.infobar()
                            del ck
                    del rw, insight

    def movedown(self, event=None):
        """Step down a row to below row"""

        self.hidcheck()
        if self.unlock:
            if self.checkfile() and self.nonetype():
                if self.listb.curselection():
                    rw = int(self.listb.curselection()[0])
                    ck = self.listb.get(rw).split(":")[1].strip()
                    if "child" in ck:
                        if all(self.listb.size() > i for i in [rw, rw + 1]):
                            sp = (
                                True
                                if self.listb.get(rw + 1).split(":")[1].strip()
                                == "space"
                                else False
                            )
                            TreeViewGui.MODE = True
                            with tv(self.filename) as tvg:
                                if sp:
                                    tvg.movetree(rw, rw + 2)
                                else:
                                    tvg.movetree(rw, rw + 1)
                            del tvg, sp
                            self.spaces()
                            ck = self.listb.get(rw + 1).split(":")[1].strip()
                            if ck != "parent":
                                self.listb.select_set(rw + 1)
                                self.listb.see(rw + 1)
                                self.text.see(f"{(rw+1)}.0")
                            else:
                                self.listb.select_set(rw + 2)
                                self.listb.see(rw + 2)
                                self.text.see(f"{(rw+2)}.0")
                            self.infobar()
                    del rw, ck

    def insertwords(self, event=None):
        """Insert a record to any row appear above the assign row"""

        self.hidcheck()
        if self.unlock:
            if self.checkfile() and self.nonetype():
                cek = ["parent", "child"]
                if self.entry.get() and self.entry.get() not in cek:
                    if TreeViewGui.MARK:
                        appr = messagebox.askyesno(
                            "Edit",
                            f"Edit cell {self.listb.curselection()[0]}?",
                            parent=self.root,
                        )
                        if appr:
                            if self.listb.curselection():
                                rw = int(self.listb.curselection()[0])
                                with tv(self.filename) as tvg:
                                    if self.entry3.get():
                                        tvg.insertrow(
                                            self.entry.get(), rw, self.entry3.get()
                                        )
                                    else:
                                        tvg.insertrow(self.entry.get(), rw)
                                del tvg
                                self.entry.delete(0, END)
                                self.spaces()
                                self.listb.see(rw)
                                self.text.see(f"{rw}.0")
                                del rw
                        del appr
                del cek

    def checked(self, event=None):
        """To add checked unicode for finished task.
        WARNING: is active according to your computer encoding system. (Active on encoding: "utf-8")
        """

        self.hidcheck()
        if self.unlock:
            if self.listb.curselection():
                rw = int(self.listb.curselection()[0])
                with tv(self.filename) as tvg:
                    tvg.checked(rw)
                del tvg
                self.view()
                self.listb.select_set(rw)
                self.listb.activate(rw)
                self.listb.see(rw)
                self.text.see(f"{rw}.0")
                del rw
                self.infobar()

    def backup(self, event=None):
        """Backup to max of 10 datas on csv file.
        And any new one will remove the oldest one.
        """

        self.hidcheck()
        if self.unlock:
            if self.checkfile() and self.nonetype():
                with tv(self.filename) as tvg:
                    tvg.backuptv()
                del tvg
                messagebox.showinfo("Backup", "Backup done!", parent=self.root)

    def loadbkp(self, event=None):
        """Load any backup data"""

        self.hidcheck()
        if self.unlock:
            try:
                dbs = db(self.filename)
                row = simpledialog.askinteger(
                    "Load Backup",
                    f"There are {dbs.totalrecs()} rows, please choose a row:",
                    parent=self.root,
                )
                if row and row <= dbs.totalrecs():
                    with tv(self.filename) as tvg:
                        tvg.loadbackup(self.filename, row=row - 1, stat=True)
                    del tvg
                    messagebox.showinfo(
                        "Load Backup",
                        "Load backup is done, chek again!",
                        parent=self.root,
                    )
                    self.spaces()
            except Exception as e:
                messagebox.showwarning("TreeViewGui", e, parent=self.root)
            del row, dbs

    def copas(self, event=None):
        """Paste a row value to Entry for fixing value"""

        self.hidcheck()
        if self.unlock:
            if self.listb.curselection():
                self.entry.delete(0, END)
                rw = int(self.listb.curselection()[0])
                paste = None
                with tv(self.filename) as tvg:
                    for r, l in tvg.getdata():
                        if r == rw:
                            if l == "\n":
                                break
                            elif l[0] == " ":
                                paste = l[re.match(r"\s+", l).span()[1] + 1 : -1]
                            else:
                                paste = l[:-2]
                            self.entry.insert(END, paste)
                            break
                del tvg, rw, paste

    def fildat(self, dat: str, b: bool = True):
        """Returning data pattern to cmrows"""

        if b:
            return enumerate(
                [f"{i}\n" for i in dat.split("\n") if not i.startswith("TOTAL SUMS =")]
            )
        else:
            return enumerate(
                [i for i in dat.split("\n") if i and not i.startswith("TOTAL SUMS =")]
            )

    def cmrows(self):
        """Copy or move any rows to any point of a row within existing rows.
        And copy parents and childs in hidden modes to another existing file or new file.
        """

        askmove = (
            messagebox.askyesno(
                "TreeViewGui", "Want to move to other file?", parent=self.root
            )
            if self.info.get() == "Hidden Mode"
            else None
        )
        if askmove:

            def chosen(flname):
                TreeViewGui.FREEZE = False
                if flname == "New":
                    askname = simpledialog.askstring(
                        "TreeViewGui", "New file name:", parent=self.root
                    )
                    if askname:
                        if not os.path.isdir(
                            self.glop.joinpath(
                                self.glop.parent, f"{askname.title()}_tvg"
                            )
                        ):
                            tak = self.fildat(self.text.get("1.0", END)[:-1])
                            os.remove(f"{self.filename}_hid.json")
                            self.createf(askname)
                            with tv(f"{askname.title()}") as tvg:
                                tvg.fileread(tvg.insighthidden(tak, False))
                            self.addonchk(False)
                            del tak, tvg
                            self.spaces()
                            self.infobar()
                        else:
                            messagebox.showinfo(
                                "TreeViewGui",
                                "Cannot create new file because is already exist!!!",
                                parent=self.root,
                            )
                    else:
                        messagebox.showinfo(
                            "TreeViewGui", "Copying is aborted!", parent=self.root
                        )
                    del askname
                else:
                    if os.path.exists(
                        self.glop.joinpath(
                            self.glop.parent, flname, f'{flname.rpartition("_")[0]}.txt'
                        )
                    ):
                        if not os.path.exists(
                            self.glop.parent.joinpath(
                                flname,
                                f'{flname.rpartition("_")[0]}_hid.json',
                            )
                        ):
                            tak = self.fildat(self.text.get("1.0", END)[:-1], False)
                            os.remove(f"{self.filename}_hid.json")
                            self.addonchk()
                            self.filename = flname.rpartition("_")[0]
                            self.glop = Path(
                                self.glop.joinpath(self.glop.parent, flname)
                            )
                            os.chdir(self.glop)
                            self.root.title(f"{self.glop.joinpath(self.filename)}.txt")
                            with tv(self.filename) as tvg:
                                tak = tvg.insighthidden(tak, False)
                                for p, d in tak:
                                    if p == "parent":
                                        tvg.addparent(d[:-1])
                                    else:
                                        tvg.quickchild(d[1:], p)
                            self.addonchk(False)
                            del tvg, tak
                            self.spaces()
                            self.infobar()
                        else:
                            messagebox.showinfo(
                                "TreeViewGui",
                                "You cannot copied to hidden mode file!",
                                parent=self.root,
                            )
                    else:
                        tak = self.fildat(self.text.get("1.0", END)[:-1])
                        os.remove(f"{self.filename}_hid.json")
                        self.addonchk()
                        self.filename = flname.rpartition("_")[0]
                        self.glop = Path(self.glop.joinpath(self.glop.parent, flname))
                        os.chdir(self.glop)
                        self.root.title(f"{self.glop.joinpath(self.filename)}.txt")
                        with tv(self.filename) as tvg:
                            tvg.fileread(tvg.insighthidden(tak, False))
                        del tak, tvg
                        self.addonchk(False)
                        self.spaces()
                        self.infobar()
                del flname

            TreeViewGui.FREEZE = True
            self.lock = True
            files = [file for file in os.listdir(self.glop.parent) if "_tvg" in file]
            files.insert(0, "New")

            @excpcls(2, DEFAULTFILE)
            class MyDialog(simpledialog.Dialog):
                def body(self, master):
                    self.title("Choose File")
                    Label(master, text="File: ").grid(row=0, column=0, sticky=E)
                    self.e1 = ttk.Combobox(master)
                    self.e1["values"] = files
                    self.e1.bind(
                        "<KeyRelease>", partial(TreeViewGui.tynam, files=files)
                    )
                    self.e1.current(0)
                    self.e1.grid(row=0, column=1)
                    return self.e1

                def apply(self):
                    self.result = self.e1.get()

            d = MyDialog(self.root)
            self.lock = False
            if d.result:
                chosen(d.result)
            else:
                TreeViewGui.FREEZE = False
            del files, d.result
        else:
            self.hidcheck()
            if self.unlock:
                if self.checkfile() and self.nonetype():
                    if self.text.get("1.0", "1.0 lineend")[:-1]:
                        if self.listb.cget("selectmode") == "browse":
                            self.disab("listb", "button17", "text")
                            self.listb.config(selectmode=EXTENDED)
                        else:
                            if self.listb.curselection():
                                gcs = [int(i) for i in self.listb.curselection()]
                                ask = simpledialog.askinteger(
                                    "TreeViewGui",
                                    f"Move to which row? choose between 0 to {self.listb.size()-1} rows",
                                    parent=self.root,
                                )
                                if ask is not None and ask < self.listb.size():
                                    deci = messagebox.askyesno(
                                        "TreeViewGui",
                                        '"Yes" to MOVE to, "No" to COPY to',
                                        parent=self.root,
                                    )
                                    if deci:
                                        with tv(self.filename) as tvg:
                                            data = list(
                                                islice(
                                                    tvg.getdata(), gcs[0], gcs[-1] + 1
                                                )
                                            )
                                            writer = tvg.satofi()
                                            if ask < tvg.getdatanum() - 1:
                                                for n, d in tvg.getdata():
                                                    if n == ask == 0:
                                                        if not data[0][1][0].isspace():
                                                            for i in data:
                                                                writer.send(i[1])
                                                            writer.send(d)
                                                        else:
                                                            writer.send(d)
                                                            for i in data:
                                                                writer.send(i[1])
                                                    elif n == ask:
                                                        for i in data:
                                                            writer.send(i[1])
                                                        writer.send(d)
                                                    elif n in gcs:
                                                        continue
                                                    else:
                                                        writer.send(d)
                                            else:
                                                for n, d in tvg.getdata():
                                                    if n in gcs:
                                                        continue
                                                    else:
                                                        writer.send(d)
                                                for i in data:
                                                    writer.send(i[1])
                                            writer.close()
                                        del tvg, data, writer
                                        self.spaces()
                                    else:
                                        with tv(self.filename) as tvg:
                                            data = list(
                                                islice(
                                                    tvg.getdata(), gcs[0], gcs[-1] + 1
                                                )
                                            )
                                            writer = tvg.satofi()
                                            if ask < tvg.getdatanum() - 1:
                                                for n, d in tvg.getdata():
                                                    if n == ask == 0:
                                                        if not data[0][1][0].isspace():
                                                            for i in data:
                                                                writer.send(i[1])
                                                            writer.send(d)
                                                        else:
                                                            writer.send(d)
                                                            for i in data:
                                                                writer.send(i[1])
                                                    elif n == ask:
                                                        for i in data:
                                                            writer.send(i[1])
                                                        writer.send(d)
                                                    else:
                                                        writer.send(d)
                                            else:
                                                for n, d in tvg.getdata():
                                                    writer.send(d)
                                                for i in data:
                                                    writer.send(i[1])
                                            writer.close()
                                        del tvg, data, writer
                                        self.spaces()
                                    self.disab(dis=False)
                                    self.listb.config(selectmode=BROWSE)
                                    self.text.see(f"{ask}.0")
                                    self.listb.see(ask)
                                else:
                                    self.disab(dis=False)
                                    self.listb.config(selectmode=BROWSE)
                                    if ask:
                                        messagebox.showerror(
                                            "TreeViewGui",
                                            f"row {ask} is exceed existing rows",
                                            parent=self.root,
                                        )
                                del gcs, ask
                            else:
                                self.disab(dis=False)
                                self.listb.config(selectmode=BROWSE)
                        self.listb.selection_clear(0, END)
                        self.infobar()

    def _utilspdf(self):

        try:
            gttx = []
            line = None
            cg = None
            eldat = self._ckfoldtvg()
            if hasattr(self, "fold"):
                for i in range(1, self.listb.size() + 1):
                    line = self.text.get(f"{float(i)}", f"{float(i)} lineend")
                    if line:
                        match eldat:
                            case eldat if eldat:
                                if not line[0].isspace():
                                    gttx.append(line + "\n")
                                elif i - 1 not in eldat:
                                    gttx.append(line + "\n")
                            case _:
                                if not line[0].isspace():
                                    gttx.append(line + "\n")
                return "".join(gttx)
            else:
                return self.text.get("1.0", END)[:-1]
        finally:
            del gttx, line, cg, eldat

    def saveaspdf(self):
        """Show to browser and directly print as pdf or direct printing"""

        if self.checkfile() and self.nonetype():
            if (a := self.text["font"].find("}")) != -1:
                px = int(re.search(r"\d+", self.text["font"][a:]).group()) * 1.3333333
            else:
                px = int(re.search(r"\d+", self.text["font"]).group()) * 1.3333333
            ck = ["bold", "italic"]
            sty = ""
            for i in ck:
                if i in self.text["font"]:
                    sty += "".join(f"{i} ")
            if sty:
                add = f" {sty}{px:.3f}px "
            else:
                add = f" {px:.3f}px "
            if "}" in self.text["font"]:
                fon = self.text["font"].partition("}")[0].replace("{", "")
                fon = f"{add}{fon}"
            else:
                fon = self.text["font"].partition(" ")[0]
                fon = f"{add}{fon}"
            ask = messagebox.askyesno(
                "TreeViewGui", "Add checkboxes?", parent=self.root
            )
            if ask:
                convhtml(
                    self._utilspdf(),
                    self.filename,
                    fon,
                    self.text.cget("background")[1:],
                    self.text.cget("foreground"),
                    ckb=True,
                )
            else:
                convhtml(
                    self._utilspdf(),
                    self.filename,
                    fon,
                    self.text.cget("background")[1:],
                    self.text.cget("foreground"),
                )
            del px, ck, sty, add, ask, fon

    def nonetype(self):
        """For checking file is empty or not"""

        try:
            with tv(self.filename) as tvg:
                if next(tvg.getdata()):
                    return True
        except:
            self.text.config(state="normal")
            self.text.delete("1.0", END)
            self.text.config(state="disabled")
            self.listb.delete(0, END)
            return False
        finally:
            del tvg

    def spaces(self):
        """Mostly used by other functions to clear an obselete spaces.
        To appropriate the display better.
        """

        self.hidcheck()
        if self.unlock:
            if self.checkfile() and self.nonetype():
                if TreeViewGui.MARK and TreeViewGui.MODE is False:
                    TreeViewGui.MARK = False
                else:
                    TreeViewGui.MODE = False
                with tv(self.filename) as tvg:
                    data = (i[:-1] for _, i in tvg.getdata() if i != "\n")
                    writer = tvg.satofi()
                    try:
                        writer.send(f"{next(data)}\n")
                    except StopIteration:
                        writer.close()
                    else:
                        for d in data:
                            if d[0].isspace():
                                writer.send(f"{d}\n")
                            else:
                                writer.send("\n")
                                writer.send(f"{d}\n")
                        writer.close()
                del tvg, writer, data
                self.view()
            else:
                if self.listb.get(0, END):
                    self.listb.delete(0, END)
            if str(self.root.focus_get()) != ".":
                self.root.focus()
            self.infobar()

    def hidcheck(self):
        """Core checking for hidden parent on display, base on existing json file"""

        if os.path.exists(f"{self.filename}_hid.json"):
            ans = messagebox.askyesno(
                "TreeViewGui", f"Delete {self.filename}_hid.json?", parent=self.root
            )
            if ans:
                os.remove(f"{self.filename}_hid.json")
                self.view()
                self.unlock = True
                messagebox.showinfo(
                    "TreeViewGui",
                    f"{self.filename}_hid.json has been deleted!",
                    parent=self.root,
                )
            else:
                self.unlock = False
                messagebox.showinfo(
                    "TreeViewGui",
                    "This function has been terminated!!!",
                    parent=self.root,
                )
            del ans
        else:
            if self.unlock == False:
                self.unlock = True

    def hidform(self):
        """To display records and not hidden one from collection position in json file"""

        import json

        if os.path.exists(f"{self.filename}_hid.json"):
            with open(f"{self.filename}_hid.json") as jfile:
                rd = dict(json.load(jfile))
            rolrd = tuple(tuple(i) for i in tuple(rd.values()) if isinstance(i, list))
            self.view()
            showt = self.text.get("1.0", END).split("\n")[:-2]
            if rd["reverse"] is False:
                for wow, wrow in rolrd:
                    for i in range(wow, wrow + 1):
                        showt[i] = 0
                self.text.config(state="normal")
                self.text.delete("1.0", END)
                showt = tuple(f"{i}\n" for i in showt if i != 0)
                self._prettyv(enumerate(showt))
                self.text.config(state="disable")
                with tv(self.filename) as tvg:
                    vals = enumerate(
                        [d[0] for d in tvg.insighthidden(enumerate(showt), False)]
                    )
                self.listb.delete(0, END)
                for n, p in vals:
                    self.listb.insert(END, f"{n}: {p}")
                del tvg, vals
            else:
                ih = []
                for wow, wrow in rolrd:
                    for i in range(wow, wrow + 1):
                        ih.append(f"{showt[i]}\n")
                ih = tuple(ih)
                self.text.config(state="normal")
                self.text.delete("1.0", END)
                self._prettyv(enumerate(ih))
                self.text.config(state="disable")
                with tv(self.filename) as tvg:
                    vals = enumerate(
                        [d[0] for d in tvg.insighthidden(enumerate(ih), False)]
                    )
                self.listb.delete(0, END)
                for n, p in vals:
                    self.listb.insert(END, f"{n}: {p}")
                del ih, tvg, vals
            del rd, rolrd, showt

    def hiddenchl(self, event=None, chs: bool = None):
        """Create Hidden position of parent and its childs in json file"""

        import json

        if hasattr(self, "fold"):
            messagebox.showinfo("TreeViewGui", "Please unfolding first!")
        else:
            if self.checkfile() and self.nonetype():
                if not os.path.exists(f"{self.filename}_hid.json"):
                    if self.listb.cget("selectmode") == "browse":
                        self.info.set("Hidden Mode")
                        self.disab("listb", "button14", "text")
                        self.listb.config(selectmode=MULTIPLE)
                    else:
                        if self.listb.curselection():
                            ask = (
                                messagebox.askyesno(
                                    "TreeViewGui",
                                    '"Yes" to hide selected, "No" reverse hide instead!',
                                    parent=self.root,
                                )
                                if chs is None
                                else chs
                            )
                            allrows = [int(i) for i in self.listb.curselection()]
                            rows = {
                                n: pc.split(":")[1].strip()
                                for n, pc in enumerate(self.listb.get(0, END))
                            }
                            hd = {}
                            num = 0
                            for row in allrows:
                                num += 1
                                if row in rows:
                                    if row < len(rows) - 1:
                                        if (
                                            rows[row] == "parent"
                                            and "child" in rows[row + 1]
                                        ):
                                            srow = row + 1
                                            while True:
                                                if srow < len(rows):
                                                    if rows[srow] == "space":
                                                        break
                                                    srow += 1
                                                else:
                                                    srow -= 1
                                                    break
                                            hd[num] = (row, srow)
                                        else:
                                            if rows[row] == "parent":
                                                hd[num] = (row, row + 1)
                                    else:
                                        if rows[row] == "parent":
                                            hd[num] = (row, row)
                            if hd:
                                if ask:
                                    rev = {"reverse": False}
                                    with open(
                                        f"{self.filename}_hid.json", "w"
                                    ) as jfile:
                                        json.dump(hd | rev, jfile)
                                    self.hidform()
                                else:
                                    rev = {"reverse": True}
                                    with open(
                                        f"{self.filename}_hid.json", "w"
                                    ) as jfile:
                                        json.dump(hd | rev, jfile)
                                    self.hidform()
                                del ask, rev
                            else:
                                self.listb.selection_clear(0, END)
                                messagebox.showinfo(
                                    "TreeViewGui",
                                    "Please choose Parent only!",
                                    parent=self.root,
                                )
                            del allrows, rows, hd, num
                        self.disab(dis=False)
                        self.listb.config(selectmode=BROWSE)
                        self.infobar()
                else:
                    messagebox.showinfo(
                        "TreeViewGui",
                        "Hidden parent is recorded, please clear all first!",
                        parent=self.root,
                    )

    def delhid(self, event=None):
        """Deleting accordingly each position in json file, or can delete the file"""

        import json

        if f"{self.filename}_hid.json" in os.listdir():
            with open(f"{self.filename}_hid.json") as jfile:
                rd = dict(json.load(jfile))
            if rd["reverse"] is False:
                rd = [i for i in list(rd.values()) if isinstance(i, list)]
                ans = messagebox.askyesno(
                    "TreeViewGui",
                    'Please choose "Yes" to delete ascending order, or "No" to delete all?',
                    parent=self.root,
                )
                if ans:
                    if rd:
                        rd.pop()
                        if rd:
                            rd = {k: v for k, v in list(enumerate(rd))}
                            rev = {"reverse": False}
                            with open(f"{self.filename}_hid.json", "w") as jfile:
                                json.dump(rd | rev, jfile)
                            self.hidform()
                            del rev
                        else:
                            os.remove(f"{self.filename}_hid.json")
                            self.spaces()
                            messagebox.showinfo(
                                "TreeViewGui",
                                f"{self.filename}_hid.json has been deleted!",
                                parent=self.root,
                            )
                else:
                    os.remove(f"{self.filename}_hid.json")
                    self.spaces()
                    messagebox.showinfo(
                        "TreeViewGui",
                        f"{self.filename}_hid.json has been deleted!",
                        parent=self.root,
                    )
                del rd, ans
            else:
                os.remove(f"{self.filename}_hid.json")
                self.spaces()
                messagebox.showinfo(
                    "TreeViewGui",
                    f"{self.filename}_hid.json has been deleted!",
                    parent=self.root,
                )

    def lookup(self, event=None):
        """To lookup word on row and also on editor mode"""

        self.hidcheck()
        if self.unlock:
            if (
                str(self.text.cget("state")) == "normal"
                and str(self.bt["button24"].cget("state")) == "normal"
            ):
                if self.text.get("1.0", END)[:-1]:

                    @excp(2, DEFAULTFILE)
                    def searchw(words: str):
                        self.text.tag_config("hw", underline=1)
                        idx = self.text.search(words, "1.0", END, nocase=1)
                        ghw = None
                        while idx:
                            idx2 = f"{idx}+{len(words)}c"
                            ghw = self.text.get(idx, idx2)
                            self.text.delete(idx, idx2)
                            self.text.insert(idx, ghw, "hw")
                            self.text.see(idx2)
                            c = messagebox.askyesno(
                                "TreeViewGui", "Continue search?", parent=self.root
                            )
                            if c:
                                self.text.delete(idx, idx2)
                                self.text.insert(idx, ghw)
                                idx = self.text.search(words, idx2, END, nocase=1)
                                self.text.mark_set("insert", idx2)
                                self.text.focus()
                                continue
                            else:
                                r = messagebox.askyesno(
                                    "TreeViewGui", "Replace word?", parent=self.root
                                )
                                if r:
                                    rpl = simpledialog.askstring(
                                        "Replace", "Type word:", parent=self.root
                                    )
                                    if rpl:
                                        self.text.delete(idx, idx2)
                                        self.text.insert(idx, rpl)
                                        self.text.mark_set(
                                            "insert", f"{idx}+{len(rpl)}c"
                                        )
                                        self.text.focus()
                                    else:
                                        self.text.delete(idx, idx2)
                                        self.text.insert(idx, ghw)
                                        self.text.mark_set("insert", idx2)
                                        self.text.focus()
                                else:
                                    self.text.delete(idx, idx2)
                                    self.text.insert(idx, ghw)
                                    self.text.mark_set("insert", idx2)
                                    self.text.focus()
                                break
                        self.text.tag_delete(*["hw"])
                        del ghw, idx

                    if self.lock is False:
                        self.lock = True
                        self.root.update()

                        @excpcls(2, DEFAULTFILE)
                        class MyDialog(simpledialog.Dialog):
                            def body(self, master):
                                self.title("Search Words")
                                Label(master, text="Words: ").grid(
                                    row=0, column=0, sticky=E
                                )
                                self.e1 = ttk.Entry(master)
                                self.e1.grid(row=0, column=1)
                                return self.e1

                            def apply(self):
                                self.result = self.e1.get()

                        d = MyDialog(self.root)
                        self.lock = False
                        if d.result:
                            searchw(d.result)
                        del d.result
            else:
                if self.checkfile() and self.nonetype():
                    if self.entry.get():
                        num = self.listb.size()
                        sn = 1
                        sw = self.entry.get()
                        dat = None
                        if sw.isdigit():
                            sw = int(sw)
                            if sw <= num - 1:
                                self.listb.see(sw)
                                self.text.see(f"{sw}.0")
                                self.listb.focus()
                                self.listb.selection_clear(0, END)
                                self.listb.activate(sw)
                                self.listb.selection_set(sw)
                        else:
                            while sn <= num:
                                dat = self.text.get(f"{sn}.0", f"{sn+1}.0")
                                if sw in dat:
                                    dat = self.text.get(
                                        self.text.search(sw, f"{sn}.0", f"{sn+1}.0"),
                                        f"{sn+1}.0",
                                    )
                                    self.text.see(f"{sn}.0")
                                    self.listb.see(sn)
                                    self.listb.selection_clear(0, END)
                                    self.listb.selection_set(sn - 1)
                                    self.listb.focus()
                                    self.listb.activate(sn - 1)
                                    ask = messagebox.askyesno(
                                        "TreeViewGui",
                                        f"Find in row {sn-1}\nText: '{dat.strip()[:100]}...'\nContinue lookup?",
                                        parent=self.root,
                                    )
                                    if ask:
                                        sn += 1
                                        continue
                                    else:
                                        break
                                else:
                                    sn += 1
                            else:
                                self.text.yview_moveto(1.0)
                                self.listb.yview_moveto(1.0)
                        del dat, num, sn, sw
                    self.infobar()

    def dattim(self, event=None):
        """To insert date and time"""

        if str(self.entry.cget("state")) == "normal":
            dtt = f'[{dt.isoformat(dt.today().replace(microsecond = 0)).replace("T"," ")}]'
            ck = ["parent", "child"]
            if self.entry.get() in ck:
                self.entry.delete(0, END)
            if self.entry.get():
                hold = self.entry.get()
                gt = re.match(r"\[.*?\]", hold)
                if not gt:
                    self.entry.delete(0, END)
                    self.entry.insert(0, f"{dtt} {hold}")
                else:
                    try:
                        if isinstance(dt.fromisoformat(gt.group()[1:20]), dt):
                            self.entry.delete(0, END)
                            self.entry.insert(0, f"{dtt} {hold[22:]}")
                    except:
                        self.entry.delete(0, END)
                        self.entry.insert(0, f"{dtt} {hold}")
                del hold, gt
            else:
                self.entry.insert(0, f"{dtt} ")
            del dtt, ck
        elif (
            str(self.text.cget("state")) == "normal"
            and str(self.bt["button20"].cget("state")) == "normal"
        ):
            dtt = f'[{dt.isoformat(dt.today().replace(microsecond = 0)).replace("T"," ")}]'
            self.text.insert(INSERT, f"{dtt} ")
            self.text.focus()
            del dtt

    def createf(self, name: str = None):
        """Creating new file not able to open existing one"""

        fl = (
            simpledialog.askstring("TreeViewGui", "New file name?", parent=self.root)
            if name is None
            else name
        )
        if fl:
            mkd = f"{fl.title()}_tvg"
            files = [file for file in os.listdir(self.glop.parent) if "_tvg" in file]
            if mkd not in files:
                self.addonchk()
                self.glop.parent.joinpath(mkd).mkdir()
                os.chdir(self.glop.parent.joinpath(mkd))
                self.glop = self.glop.parent.joinpath(mkd)
                self._ckfoldtvg()
                self.filename = fl.title()
                self.root.title(f"{self.glop.absolute().joinpath(self.filename)}.txt")
                self.text.config(state=NORMAL)
                self.text.delete("1.0", END)
                self.text.config(state=DISABLED)
                self.entry.delete(0, END)
                self.rb.set("")
                self.entry.config(state=DISABLED)
                self.listb.delete(0, END)
                self.addonchk(False)
            else:
                messagebox.showinfo(
                    "TreeViewGui",
                    f"The file {mkd}/{fl.title()}.txt is already exist!",
                    parent=self.root,
                )
            del mkd, files
        else:
            messagebox.showinfo("TreeViewGui", "Nothing created yet!", parent=self.root)
        del fl, name

    def editex(self, event=None):
        """Edit existing file in the editor mode which can be very convinient and powerful.
        However, before edit in editor mode, it is advice to make backup first!
        Just in case you want to get back to previous file.
        """

        self.hidcheck()
        if self.unlock:
            if self.checkfile() and self.nonetype():
                ask = messagebox.askyesno(
                    "TreeViewGui",
                    '"Yes" Edit whole file, or "No" Edit selected parent only?',
                    parent=self.root,
                )
                if ask:
                    self.editor()
                    with tv(self.filename) as tvg:
                        for p, d in tvg.compdatch(True):
                            if p == "parent":
                                self.text.insert(END, f"p:{d[:-2]}\n")
                            elif p == "space":
                                self.text.insert(END, "s:\n")
                            else:
                                self.text.insert(END, f"c{p[5:]}:{d[1:]}")
                    del tvg, p, d
                    self.text.see(self.text.index(INSERT))
                    os.remove(f"{self.filename}.txt")
                else:
                    if self.listb.curselection():
                        stor = int(self.listb.curselection()[0])
                        self.editor()
                        with tv(self.filename) as tvg:
                            num = stor
                            for p, d in islice(
                                tvg.compdatch(True), stor, tvg.getdatanum()
                            ):
                                if num == stor and p != "parent":
                                    messagebox.showinfo(
                                        "TreeViewGui",
                                        "Please select a parent row only!",
                                        parent=self.root,
                                    )
                                    break
                                if p == "parent":
                                    self.text.insert(END, f"p:{d[:-2]}\n")
                                elif p.partition("child")[1]:
                                    self.text.insert(END, f"c{p[5:]}:{d[1:]}")
                                else:
                                    if p == "space" or p == "parent":
                                        break
                                num += 1
                        self.editorsel = (stor, num)
                        del tvg, p, d, stor, num
                        self.text.see(self.text.index(INSERT))
                    else:
                        messagebox.showinfo(
                            "TreeViewGui",
                            "Please select a parent row first!",
                            parent=self.root,
                        )
                del ask
        self.text.focus()

    def tempsave(self):
        """Saving template"""

        if wordies := self.text.get("1.0", END)[:-1]:
            fname = simpledialog.askstring(
                "Save to template", "Name?", parent=self.root
            )
            if fname:
                dest = os.path.join(self.glop.parent, "Templates", f"{fname}.tvg")
                with open(dest, "w") as wt:
                    wr = []
                    for word in wordies.splitlines():
                        if (ck := word.partition(":")[0].lower()) in [
                            "p",
                            "s",
                        ] or ck.count("c") == 1:
                            wr.append(word)
                        else:
                            wr.clear()
                            break
                    if wr:
                        wt.write(str(wr))
                        messagebox.showinfo(
                            "TreeViewGui",
                            f"Template {fname}.tvg saved!",
                            parent=self.root,
                        )
                    else:
                        messagebox.showinfo(
                            "TreeViewGui",
                            "Unable save template, please use right format!",
                            parent=self.root,
                        )
                del dest, wr, wt
            else:
                messagebox.showinfo(
                    "TreeViewGui", "Save template is aborted!", parent=self.root
                )
            del fname
        else:
            messagebox.showinfo("TreeViewGui", "Nothing to be save!", parent=self.root)

    @excp(2, DEFAULTFILE)
    @staticmethod
    def tynam(event, files: list | tuple):
        if event.widget.get():
            idx = event.widget.index(INSERT)
            gt = event.widget.get()
            event.widget.delete(0, END)
            event.widget.insert(0, gt[:idx])
            if event.widget.get():
                for em in files:
                    if (
                        event.widget.get() in em
                        and event.widget.get()[: idx + 1]
                        == em[: len(event.widget.get())]
                    ):
                        event.widget.current(files.index(em))
                        break
            event.widget.icursor(index=idx)
            del idx, gt

    def temp(self, event=None):
        """This is to compliment the editor mode.
        If you have to type several outline that has same format,
        You can save them as template and re-use again in the editor mode.
        """

        if (
            str(self.text.cget("state")) == "normal"
            and str(self.bt["button24"].cget("state")) == "normal"
        ):
            if not os.path.exists(os.path.join(self.glop.parent, "Templates")):
                os.mkdir(os.path.join(self.glop.parent, "Templates"))
                self.tempsave()
            else:
                if self.lock is False:
                    self.lock = True
                    files = [
                        i
                        for i in os.listdir(os.path.join(self.glop.parent, "Templates"))
                        if ".tvg" in i
                    ]
                    files.sort()
                    if files:

                        def deltemp():
                            if gt := cmbb.get():
                                if ask := messagebox.askyesno(
                                    "TreeViewGui", "Delete template?", parent=self.root
                                ):
                                    pth = os.path.join(
                                        self.glop.parent, "Templates", gt
                                    )
                                    os.remove(pth)
                                    files.remove(gt)
                                    cmbb.delete(0, END)
                                    cmbb["values"] = files
                                del ask, gt

                        cmbb = None

                        @excpcls(2, DEFAULTFILE)
                        class MyDialog(simpledialog.Dialog):
                            def body(self, master):
                                nonlocal cmbb
                                self.title("Choose Template")
                                self.fr1 = Frame(master)
                                self.fr1.pack()
                                self.lab = Label(self.fr1, text="File: ")
                                self.lab.pack(side=LEFT, pady=2, padx=2)
                                self.e1 = ttk.Combobox(self.fr1)
                                self.e1["values"] = files
                                self.e1.bind(
                                    "<KeyRelease>",
                                    partial(TreeViewGui.tynam, files=files),
                                )
                                self.e1.pack(side=RIGHT, padx=(0, 2), pady=2)
                                cmbb = self.e1
                                self.bt = Button(
                                    master,
                                    text="Delete",
                                    command=deltemp,
                                    relief=GROOVE,
                                )
                                self.bt.pack(fill=X, pady=(0, 2), padx=2)
                                return self.e1

                            def apply(self):
                                self.result = self.e1.get()

                        d = MyDialog(self.root)
                        self.lock = False
                        if d.result:
                            path = os.path.join(self.glop.parent, "Templates", d.result)
                            with open(path) as rdf:
                                gf = ast.literal_eval(rdf.read())
                            for pr in gf:
                                self.text.insert(f"{INSERT} linestart", f"{pr}\n")
                            del path, gf, pr
                        else:
                            if ask := messagebox.askyesno(
                                "TreeViewGui",
                                "Do you want to save a template?",
                                parent=self.root,
                            ):
                                self.tempsave()
                        del d.result, cmbb
                    else:
                        self.lock = False
                        messagebox.showinfo(
                            "TreeViewGui", "No templates yet!", parent=self.root
                        )
                        self.tempsave()
                    del files
            self.text.focus()

    def disab(self, *args, dis=True):
        """Conditioning buttons for functions mode purpose"""

        if dis and args:
            for i in self.bt:
                if "label" not in i and "scrollbar" not in i:
                    if i not in args:
                        self.bt[i].config(state="disable")
            TreeViewGui.FREEZE = True
        else:
            for i in self.bt:
                if "label" not in i and "scrollbar" not in i:
                    if i == "entry3":
                        self.bt[i].config(state="readonly")
                    elif i == "entry":
                        if not self.rb.get():
                            self.bt[i].config(state="disable")
                        else:
                            self.bt[i].config(state="normal")
                    else:
                        if i != "text":
                            self.bt[i].config(state="normal")
            TreeViewGui.FREEZE = False

    def _mdbuttons(self):

        if not hasattr(self, "mdframe"):

            mdb = {
                "B": "****",
                "I": "**",
                "U": "^^^^",
                "S": "~~~~",
                "M": "====",
                "SA": "++++",
                "L": "[]()",
                "SP": "^^",
                "SB": "~~",
                "C": "[x]",
                "AR": "-->",
                "AL": "<--",
                "AT": "<-->",
                "PM": "+/-",
                "TM": "(tm)",
                "CR": "(c)",
                "R": "(r)",
            }

            stb = None

            @excp(2, DEFAULTFILE)
            def storbut(event):
                nonlocal stb
                stb = event.widget.cget("text")

            @excp(2, DEFAULTFILE)
            def insmd():
                if stb and stb in mdb:
                    mk = None
                    match self.text.tag_ranges("sel"):
                        case tsel if tsel:
                            if stb in ("B", "I", "U", "S", "M", "SA", "L", "SP", "SB"):
                                match len(mk := mdb[stb]):
                                    case 2:
                                        self.text.insert(SEL_FIRST, mk[:1])
                                        self.text.insert(SEL_LAST, mk[:1])
                                    case 4:
                                        if "[" in mk:
                                            self.text.insert(SEL_FIRST, mk[:1])
                                            self.text.insert(SEL_LAST, mk[1:])
                                        else:
                                            self.text.insert(SEL_FIRST, mk[:2])
                                            self.text.insert(SEL_LAST, mk[:2])
                                if idx := self.text.search(" ", SEL_LAST, END):
                                    self.text.mark_set("insert", idx)
                                else:
                                    self.text.mark_set("insert", f"{SEL_LAST} lineend")
                                self.text.tag_remove("sel", SEL_FIRST, SEL_LAST)
                                del idx
                    if mk is None:
                        if self.text.get(f"{INSERT} - 1c", INSERT).isspace():
                            self.text.insert(INSERT, mdb[stb])
                        else:
                            self.text.insert(INSERT, f" {mdb[stb]}")
                    self.text.focus()
                    del mk

            lmdb = list(mdb)
            self.tframe.pack_forget()
            self.fscr.pack_forget()

            self.__setattr__("mdframe", None)
            self.frb3.pack(fill=X)
            self.mdframe = ttk.Frame(self.frb3)
            self.mdframe.pack(fill=X, expand=1)

            mdbut = ttk.Button(self.mdframe, text=lmdb[0], width=1, command=insmd)
            mdbut.pack(side=LEFT, padx=2, pady=(0, 2), fill=X, expand=1)
            mdbut.bind("<Enter>", storbut)
            self.rsv_frame = mdbut.winfo_parent()
            for i in range(1, 17):
                mdbut = ttk.Button(self.mdframe, text=lmdb[i], width=1, command=insmd)
                mdbut.pack(side=LEFT, padx=(0, 2), pady=(0, 2), fill=X, expand=1)
                mdbut.bind("<Enter>", storbut)

            self.tframe.pack(anchor="w", side=TOP, fill="both", expand=1)
            self.tframe.update()
            self.fscr.pack(fill="x")
            self.fscr.update()
            del lmdb
        else:
            for i in self.mdframe.winfo_children():
                i.destroy()
                del i
            self.mdframe.destroy()
            self.__delattr__("mdframe")
            self.frb3.pack_forget()

    def editor(self):
        """This is direct editor on text window.
        FORMAT:
        "s:" for 'space'
        "p:" for 'parent'
        "c1:" - "c50:" for 'child1' to 'child50'
        """

        self.hidcheck()
        if self.unlock:
            if str(self.text.cget("state")) == "disabled":
                self.text.config(state="normal")
                self.text.delete("1.0", END)
                ckb = [
                    "button24",
                    "button28",
                    "button20",
                    "button19",
                    "text",
                ]
                self.disab(*ckb)
                self.text.edit_reset()
                self.text.focus()
                self._mdbuttons()
                del ckb
            else:
                try:
                    if self.text.get("1.0", END)[:-1]:
                        self.store = self.text.get("1.0", END)
                        if self.checkfile() and self.nonetype():
                            if self.editorsel:
                                stor = self.editorsel
                                ed = tuple(i for i in self.store[:-1].split("\n") if i)
                                ckc = {f"c{i}": f"child{i}" for i in range(1, 51)}
                                et = stor[0]
                                p2 = {}
                                p1 = None
                                p3 = None
                                for i in ed:
                                    et += 1
                                    if "s:" == i.lower()[:2]:
                                        p2[et] = ("space", "\n")
                                    elif "p:" == i.lower()[:2]:
                                        if i.partition(":")[2].isspace() or not bool(
                                            i.partition(":")[2]
                                        ):
                                            raise Exception("Parent cannot be empty!")
                                        else:
                                            p2[et] = (
                                                "parent",
                                                i[2:].removeprefix(" "),
                                            )
                                    elif i.lower().partition(":")[0] in list(ckc):
                                        if i.partition(":")[2].isspace():
                                            p2[et] = (
                                                ckc[i.partition(":")[0].lower()],
                                                i.partition(":")[2],
                                            )
                                        elif bool(i.partition(":")[2]):
                                            p2[et] = (
                                                ckc[i.partition(":")[0].lower()],
                                                i.partition(":")[2].removeprefix(" "),
                                            )
                                if len(ed) != len(p2):
                                    raise Exception("Not Editable!")
                                with tv(self.filename) as tvg:
                                    p1 = islice(tvg.insighttree(), 0, stor[0])
                                    if stor[1] < tvg.getdatanum() - 1:
                                        p3 = islice(
                                            tvg.insighttree(),
                                            stor[1],
                                            tvg.getdatanum(),
                                        )
                                    if p3:
                                        p3 = tuple(v for v in dict(p3).values())
                                        p3 = {et + j + 1: p3[j] for j in range(len(p3))}
                                        combi = iter((dict(p1) | p2 | p3).values())
                                    else:
                                        combi = iter((dict(p1) | p2).values())
                                    tvg.fileread(combi)
                                del stor, tvg, p1, ed, ckc, et, p2, combi, p3
                            else:
                                et = self.listb.size()
                                ed = tuple(i for i in self.store[:-1].split("\n") if i)
                                ckc = {f"c{i}": f"child{i}" for i in range(1, 51)}
                                p2 = {}
                                for i in ed:
                                    et += 1
                                    if "s:" == i.lower()[:2]:
                                        p2[et] = ("space", "\n")
                                    elif "p:" == i.lower()[:2]:
                                        if i.partition(":")[2].isspace() or not bool(
                                            i.partition(":")[2]
                                        ):
                                            raise Exception("Parent cannot be empty!")
                                        else:
                                            p2[et] = (
                                                "parent",
                                                i[2:].removeprefix(" "),
                                            )
                                    elif i.lower().partition(":")[0] in list(ckc):
                                        if i.partition(":")[2].isspace():
                                            p2[et] = (
                                                ckc[i.partition(":")[0].lower()],
                                                i.partition(":")[2],
                                            )
                                        elif bool(i.partition(":")[2]):
                                            p2[et] = (
                                                ckc[i.partition(":")[0].lower()],
                                                i.partition(":")[2].removeprefix(" "),
                                            )
                                if len(ed) != len(p2):
                                    raise Exception("Not Editable!")
                                with tv(self.filename) as tvg:
                                    combi = iter(
                                        (dict(tvg.insighttree()) | p2).values()
                                    )
                                    tvg.fileread(combi)
                                del tvg, et, ed, ckc, p2, combi
                        else:
                            ed = tuple(i for i in self.store[:-1].split("\n") if i)
                            et = -1
                            ckc = {f"c{i}": f"child{i}" for i in range(1, 51)}
                            p2 = {}
                            for i in ed:
                                et += 1
                                if "s:" == i.lower()[:2]:
                                    p2[et] = ("space", "\n")
                                elif "p:" == i.lower()[:2]:
                                    if i.partition(":")[2].isspace() or not bool(
                                        i.partition(":")[2]
                                    ):
                                        raise Exception("Parent cannot be empty!")
                                    else:
                                        p2[et] = ("parent", i[2:].removeprefix(" "))
                                elif i.lower().partition(":")[0] in list(ckc):
                                    if i.partition(":")[2].isspace():
                                        p2[et] = (
                                            ckc[i.partition(":")[0].lower()],
                                            i.partition(":")[2],
                                        )
                                    elif bool(i.partition(":")[2]):
                                        p2[et] = (
                                            ckc[i.partition(":")[0].lower()],
                                            i.partition(":")[2].removeprefix(" "),
                                        )
                            if len(ed) != len(p2):
                                raise Exception("Not Editable!")
                            with tv(self.filename) as tvg:
                                tvg.fileread(iter(p2.values()))
                            del tvg, ed, et, ckc, p2
                        self.text.config(state=DISABLED)
                        self.disab(dis=False)
                        self.spaces()
                        if self.editorsel:
                            self.text.see(f"{self.editorsel[0]}.0")
                            self.editorsel = None
                    else:
                        self.text.config(state=DISABLED)
                        self.disab(dis=False)
                        self.spaces()
                        if self.editorsel:
                            self.editorsel = None
                except Exception as a:
                    messagebox.showerror("TreeViewGui", f"{a}", parent=self.root)
                if self.text.cget("state") == DISABLED:
                    self.chktempo()
                    self._mdbuttons()
            self.store = None
            self.text.edit_reset()
            self.infobar()

    def chktempo(self):
        """Checking Add-On expression attribute"""

        if self._addon and hasattr(self, "toptempo"):
            self.toptempo.destroy()
            self.__delattr__("toptempo")

    def tvgexit(self, event=None):
        """Exit mode for TVG and setting everything back to default"""

        if TreeViewGui.FREEZE is False:
            if self.checkfile():
                with open(os.path.join(self.glop.parent, "lastopen.tvg"), "wb") as lop:
                    lop.write(str({"lop": self.filename}).encode())
                if str(self.root.winfo_geometry()) == TreeViewGui.GEO:
                    with open(os.path.join(self.glop.parent, "geo.tvg"), "wb") as geo:
                        geo.write(str({"geo": TreeViewGui.GEO}).encode())
                else:
                    ask = messagebox.askyesno(
                        "TreeViewGui",
                        "Do you want to set your new window's position?",
                        parent=self.root,
                    )
                    if ask:
                        with open(
                            os.path.join(self.glop.parent, "geo.tvg"), "wb"
                        ) as geo:
                            geo.write(
                                str({"geo": str(self.root.winfo_geometry())}).encode()
                            )
                    else:
                        with open(
                            os.path.join(self.glop.parent, "geo.tvg"), "wb"
                        ) as geo:
                            geo.write(str({"geo": TreeViewGui.GEO}).encode())
                    del ask
                self.addonchk()
            self.root.destroy()
        else:
            messagebox.showerror(
                "TreeViewGui", "Do not exit before a function end!!!", parent=self.root
            )

    def txtcol(self, event=None, path=None, wr=True):
        """Setting colors for text and listbox"""

        color = None
        if path:
            with open(path) as rd:
                color = rd.read()
        else:
            color = colorchooser.askcolor()[1]
        rgb = [
            int(f"{i}{j}", 16) / 255
            for i, j in list(zip(color[1:][0::2], color[1:][1::2]))
        ]
        rgb = True if round(((1 / 2) * (max(rgb) + min(rgb))) * 100) < 47 else False
        if rgb:
            self.text.config(foreground="white")
            self.text.config(insertbackground="white")
            self.listb.config(foreground="white")
        else:
            self.text.config(foreground="black")
            self.text.config(insertbackground="black")
            self.listb.config(foreground="black")
        self.text.config(bg=color)
        self.listb.config(bg=color)
        if wr:
            with open(os.path.join(self.glop.parent, "theme.tvg"), "w") as thm:
                thm.write(color)
        del color, rgb, path, wr

    def _deltags(self):
        for i in self.text.tag_names():
            for x in self.text.tag_ranges(i):
                if self.text.index(x) in (tnt := self.text.tag_nextrange(i, x, END)):
                    self.text.tag_remove(i, *tnt)
        self.text.tag_delete(*self.text.tag_names())

    def clb(self, event, wr=True):
        """Setting font for text and listbox"""

        ckf = [str(i) for i in range(41) if i >= 10]
        if "}" in event:
            n = len(event[: event.find("}")])
            f = re.search(r"\d+", event[event.find("}") :])
            fl = event[: (n + f.span()[0])] + "11" + event[(n + f.span()[1]) :]
            if f.group() in ckf:
                f = event
            else:
                if int(f.group()) < 10:
                    f = event[: (n + f.span()[0])] + "10" + event[(n + f.span()[1]) :]
                else:
                    f = event[: (n + f.span()[0])] + "40" + event[(n + f.span()[1]) :]
            del n
        else:
            f = re.search(r"\d+", event)
            fl = event[: f.span()[0]] + "11" + event[f.span()[1] :]
            if f.group() in ckf:
                f = event
            else:
                if int(f.group()) < 10:
                    f = event[: (f.span()[0])] + "10" + event[(f.span()[1]) :]
                else:
                    f = event[: (f.span()[0])] + "40" + event[(f.span()[1]) :]

        self._deltags()
        self.text["font"] = f
        if wr:
            if fl != self.listb["font"]:
                self.reblist(fl)
            with open(os.path.join(self.glop.parent, "ft.tvg"), "w") as ftvg:
                ftvg.write(event)
        else:
            self.listb["font"] = fl
        if not os.path.exists(f"{self.filename}_hid.json"):
            self.spaces()
        else:
            self.hidform()
        del ckf, fl, f

    def reblist(self, fon: str):
        """Destroy Listbox and rebuild it again,
        for font in listbox to be appear correctly
        """

        self.listb.destroy()
        self.listb = Listbox(
            self.tlframe,
            background=self.text["background"],
            foreground=self.text["foreground"],
            font=fon,
        )
        self.listb.pack(side=LEFT, fill="both", expand=1)
        self.listb.pack_propagate(0)
        self.bt["listb"] = self.listb
        self.listb.config(yscrollcommand=self.scrollbar2.set)
        self.scrollbar2.config(command=self.listb.yview)
        self.listb.bind("<<ListboxSelect>>", self.infobar)
        self.listb.bind("<MouseWheel>", self.mscrl)
        self.listb.bind("<Up>", self.mscrl)
        self.listb.bind("<Down>", self.mscrl)
        self.listb.bind("<FocusIn>", self.flb)
        self.listb.update()
        del fon

    def ft(self, event=None, path=None):
        """Initial starting fonts chooser"""

        if path:
            with open(path) as rd:
                self.clb(rd.read(), wr=False)
        else:
            self.root.tk.call(
                "tk",
                "fontchooser",
                "configure",
                "-font",
                self.text["font"],
                "-command",
                self.root.register(self.clb),
            )
            self.root.tk.call("tk", "fontchooser", "show")
        del path

    def oriset(self, event=None):
        """Set back to original setting of theme and font"""

        lf = [
            i for i in os.listdir(self.glop.parent) if i == "ft.tvg" or i == "theme.tvg"
        ]
        if lf:
            ask = messagebox.askyesno(
                "TreeViewGui", "Set back to original?", parent=self.root
            )
            if ask:
                for i in lf:
                    os.remove(os.path.join(self.glop.parent, i))
                messagebox.showinfo(
                    "TreeViewGui", "All set back to original setting!", parent=self.root
                )
            else:
                messagebox.showinfo("TreeViewGui", "None change yet!", parent=self.root)
            del ask
        del lf

    def tutorial(self, event=None):
        """Call for TVG tutorial pdf"""

        pth = os.path.join(Path(__file__).parent, "Tutorial TVG.pdf")
        if os.path.isfile(pth):
            if self.plat.startswith("win"):
                os.startfile(pth)
            else:
                os.system(f'open "{pth}"')

    def send_reg(self, event=None):
        """Compose email for registration"""

        body = "".join(
            [
                wrwords(i, 80, 1) + "\n"
                for i in self.text.get("1.0", END)[:-1].split("\n")
            ]
        )
        if body != "\n":
            ask = messagebox.askyesno(
                "TreeViewGui",
                '"yes" to compose email or "no" to copy text.',
                parent=self.root,
            )
            if ask:
                composemail(sub=f"{self.filename}", body=body)
            else:
                self.root.clipboard_clear()
                self.root.clipboard_append(
                    "".join(
                        [
                            wrwords(i, 40, 1) + "\n"
                            for i in self.text.get("1.0", END)[:-1].split("\n")
                        ]
                    )
                )
                messagebox.showinfo("TreeViewGui", "Text copied!", parent=self.root)
        else:
            messagebox.showinfo(
                "TreeViewGui", "Cannot send empty text!", parent=self.root
            )

    def gettotsum(self):
        """Get all sums on all parents that have "+" sign in front"""

        if self.checkfile() and self.nonetype():
            sa = SumAll(self.filename, sig="+")
            self.listb.config(selectmode=MULTIPLE)
            match len(sa) > 0:
                case False if hasattr(self, "sumtot"):
                    match os.path.exists(f"{self.filename}_hid.json"):
                        case False:
                            if not hasattr(self, "fold"):
                                idx = sa.getidx(False)
                                tot = sa.lumpsum()
                                for i in idx:
                                    self.listb.select_set(i)
                                self.hiddenchl(chs=False)
                                self.text.config(state=NORMAL)
                                if (
                                    self.text.get(f"{END} - 2 lines", END)
                                    .strip()
                                    .startswith("-TOTAL")
                                ):
                                    self.text.insert(END, f"\nTOTAL SUMS = {tot}")
                                else:
                                    self.text.insert(END, f"TOTAL SUMS = {tot}")
                                self.text.config(state=DISABLED)
                                del idx, tot
                            else:
                                messagebox.showwarning(
                                    "TreeViewGui",
                                    "Please unfolding first!",
                                    parent=self.root,
                                )
                        case True:
                            messagebox.showwarning(
                                "TreeViewGui",
                                "Hidden parent is recorded, please clear all first!",
                                parent=self.root,
                            )
                case True:
                    self.__setattr__("sumtot", True)
                    sa.sumway()
                    self.spaces()
                case False:
                    messagebox.showinfo(
                        "TreeViewGui", "No data to sums!", parent=self.root
                    )
            self.listb.config(selectmode=BROWSE)
            del sa

    def chktp(self):
        """Clearing Toplevel widget"""

        for i in self.root.winfo_children():
            if ".!toplevel" in str(i):
                i.destroy()
                del i

    def grchk(self, *values):
        """Get colors for charts"""

        def ck(val):
            if val < 0:
                return "r"
            else:
                return "b"

        return tuple(map(ck, values))

    def createpg(self):
        """Creating graph for all summable data"""

        if self.checkfile() and self.nonetype():
            with SumAll(self.filename, sig="+") as sal:
                try:
                    pc = tp = gr = None
                    if hasattr(self, "sumtot") and self.sumtot:
                        self.chktp()
                        tp = Toplevel(self.root)
                        gr = sal.for_graph()
                        pc = Charts(gr, f"{self.filename}", self.grchk(*gr.values()))
                        pc.pchart(tp)
                    else:
                        messagebox.showinfo(
                            "TreeViewGui",
                            "No data to create Pie Chart!",
                            parent=self.root,
                        )
                except Exception as e:
                    self.chktp()
                    messagebox.showerror("TreeViewGui", e, parent=self.root)
                finally:
                    del pc, tp, gr, sal

    def deltots(self):
        """Deleting all Totals"""

        if self.checkfile() and self.nonetype():
            with SumAll(self.filename, sig="+") as sal:
                if hasattr(self, "sumtot") and self.sumtot:
                    self.__delattr__("sumtot")
                    sal.del_total()
                else:
                    messagebox.showinfo(
                        "TreeViewGui", "Nothing to delete!", parent=self.root
                    )
            del sal
            self.spaces()

    def _ckwrds(self, wrd: str):

        if self._addon:
            nums = len(wrd)
            if nums >= 101:
                raise Exception(f"{nums} charcters, is exceeding than 100 chars!")

            for i in wrd:
                if i not in tuple("0123456789*/-+()%."):
                    raise ValueError(f"{i!r} is not acceptable expression!")

            ck = re.compile(r"[\W+]{2}")
            if ck := ck.search(wrd):
                raise ValueError(f"These {ck.group()!r} are not allowed!")
            del ck, nums

    def exprsum(self, event=None):
        """Expression Calculation for Editor mode"""

        if self.unlock and self.text.cget("state") == NORMAL:
            self.unlock = False

            err = None

            @excp(2, DEFAULTFILE)
            def calc(event=None):
                nonlocal err
                try:
                    if gw := wid.get():
                        self._ckwrds(gw)
                        ms = EvalExp(gw, None)
                        lab["text"] = ms.evlex()
                        if err:
                            err = None
                        del ms, gw
                    else:
                        raise ValueError("Expression is empty!")
                except Exception as e:
                    if err is None:
                        err = 1
                    messagebox.showerror("Error Message", e)

            @excp(2, DEFAULTFILE)
            def utilins(lab: str):
                gtx = (
                    self.text.get(
                        f"{self.text.index(INSERT)} linestart",
                        f"{self.text.index(INSERT)} lineend",
                    )
                    .strip()
                    .rpartition(" ")[2]
                )
                if gtx.replace(",", "").replace(".", "").replace("-", "").isdigit():
                    idx = self.text.search(
                        gtx,
                        self.text.index(f"{self.text.index(INSERT)} linestart"),
                        self.text.index(f"{self.text.index(INSERT)} lineend"),
                    )
                    self.text.delete(idx, f"{idx} + {len(gtx)}c")
                    self.text.insert(idx, lab)
                else:
                    if self.text.index(INSERT) == self.text.index(
                        f"{self.text.index(INSERT)} lineend"
                    ):
                        if self.text.get(f"{INSERT} - 1c", INSERT) == " ":
                            self.text.insert(INSERT, lab)
                        else:
                            self.text.insert(INSERT, f" {lab}")
                    else:
                        if (
                            self.text.get(
                                f"{self.text.index(f'{self.text.index(INSERT)} lineend')} - 1c",
                                self.text.index(f"{self.text.index(INSERT)} lineend"),
                            )
                            == " "
                        ):
                            self.text.insert(
                                self.text.index(f"{self.text.index(INSERT)} lineend"),
                                lab,
                            )
                        else:
                            self.text.insert(
                                self.text.index(f"{self.text.index(INSERT)} lineend"),
                                f" {lab}",
                            )

            @excp(2, DEFAULTFILE)
            def updatelab():
                try:
                    ms = None
                    if gw := wid.get():
                        self._ckwrds(gw)
                        ms = EvalExp(gw, None)
                    if lab["text"] != (ms := ms.evlex()):
                        lab["text"] = ms
                except:
                    calc()
                finally:
                    del ms, gw

            @excp(2, DEFAULTFILE)
            def insert():
                if isinstance(lab["text"], int | float):
                    updatelab()
                    match self.labcop:
                        case lc if lc is None:
                            self.labcop = f"{lab['text']:,.2f}"
                        case lc if self.text.get(
                            f"{INSERT} - {len(lc)}c", INSERT
                        ) == lc:
                            self.text.delete(f"{INSERT} - {len(lc)}c", INSERT)
                            self.labcop = f"{lab['text']:,.2f}"
                        case _:
                            self.labcop = f"{lab['text']:,.2f}"
                    utilins(self.labcop)
                    lab["text"] = "click for result"

                elif bool(wid.get()):
                    nonlocal err

                    calc()
                    if err is None:
                        insert()
                    else:
                        err = None

            wid = None
            lab = None

            @excpcls(2, DEFAULTFILE)
            class MyDialog(simpledialog.Dialog):
                def body(self, master):
                    nonlocal wid, lab
                    self.title("Expression Calc")
                    self.fr1 = Frame(master)
                    self.fr1.pack(padx=1, pady=1, fill=X)
                    Label(self.fr1, text="Expression: ").pack(side=LEFT)
                    self.e1 = Entry(self.fr1)
                    self.e1.pack(side=RIGHT)
                    wid = self.e1
                    self.e2 = Label(master, text="click for result", relief=GROOVE)
                    self.e2.pack(padx=1, pady=(0, 1), fill=X)
                    self.e2.bind("<ButtonPress>", calc)
                    lab = self.e2
                    self.bp = Button(
                        master, text="Paste", command=insert, relief=GROOVE
                    )
                    self.bp.pack(padx=1, pady=(0, 1), fill=X)
                    self.fcs()
                    return self.e1

                def buttonbox(self) -> None:
                    fb = Frame(self)
                    bt = Button(fb, text="Done", command=self.ok, relief=GROOVE)
                    bt.pack(pady=5)
                    fb.pack()

                def ok(self, event=None):
                    self.destroy()

                def fcs(self):
                    if self.grab_status() is not None:
                        self.grab_release()
                        self.attributes("-topmost", 1)
                    else:
                        self.after(1000, self.fcs)

            mas = Toplevel(self.root)
            mas.withdraw()
            self.__setattr__("toptempo", mas)
            self.__setattr__("labcop", None)
            d = MyDialog(mas)
            self.unlock = True
            if hasattr(self, "toptempo"):
                mas.destroy()
                self.__delattr__("toptempo")
            self.__delattr__("labcop")
            del wid, lab, d, mas, err
        else:
            if not hasattr(self, "toptempo"):
                messagebox.showinfo(
                    "TreeViewGui", "Only work for Editor mode", parent=self.root
                )

    def _indconv(self, n: int):
        return f"{float(n)}", f"{float(n + 1)}"

    def _ckfoldtvg(self):
        pth = self.glop.absolute().joinpath("fold.tvg")
        if os.path.exists(pth):
            with open(pth, "rb") as cur:
                gt = ast.literal_eval(cur.read().decode())
            return gt
        else:
            return None

    def foldfun(self):
        """For folding childs"""

        if hasattr(self, "fold"):
            gt = self._ckfoldtvg()
            seen = None
            for n in range(1, self.listb.size() + 1):
                idx = self._indconv(n)
                if (
                    tx := self.text.get(idx[0], f"{idx[0]} lineend + 1c")
                ) != "\n" and tx[0].isspace():
                    if gt:
                        if n - 1 in gt:
                            self.text.tag_add(idx[0], *idx)
                            self.text.tag_config(idx[0], elide=self.fold)
                            seen = n
                    else:
                        self.text.tag_add(idx[0], *idx)
                        self.text.tag_config(idx[0], elide=self.fold)

                del idx, tx
            if seen:
                self.listb.see(seen - 1)
                self.text.see(f"{seen}.0")
            else:
                self.text.yview_moveto(1.0)
                self.listb.yview_moveto(1.0)
            del gt, seen

    def _chkfoldatt(self):
        if os.path.exists(self.glop.absolute().joinpath("fold.tvg")):
            if not hasattr(self, "fold"):
                self.__setattr__("fold", True)
        else:
            if hasattr(self, "fold"):
                self.__delattr__("fold")

    def fold_childs(self):
        """Folding all childs"""

        self.hidcheck()
        if self.unlock:
            if not hasattr(self, "fold"):
                self.__setattr__("fold", True)
            self.foldfun()

    def fold_selected(self):
        """Folding selected"""

        self.hidcheck()
        if self.unlock:
            if self.listb.cget("selectmode") == BROWSE:
                self.listb.config(selectmode=EXTENDED)
                self.disab("button34", "listb")
                if not hasattr(self, "fold"):
                    self.__setattr__("fold", True)
            else:
                if self.listb.curselection():
                    with open(self.glop.absolute().joinpath("fold.tvg"), "wb") as cur:
                        cur.write(str(self.listb.curselection()).encode())
                    self.foldfun()
                self.disab(dis=False)
                self.listb.selection_clear(0, END)
                self.listb.config(selectmode=BROWSE)

    def unfolding(self):
        """Unfolding selected and childs"""

        self.hidcheck()
        if self.unlock:
            if hasattr(self, "fold"):
                self.__delattr__("fold")

            if os.path.exists(self.glop.absolute().joinpath("fold.tvg")):
                os.remove(self.glop.absolute().joinpath("fold.tvg"))

            self.view()


@excp(m=2, filenm=DEFAULTFILE)
def askfile(root):
    """Asking file for creating or opening initial app start"""

    files = [
        file.rpartition("_")[0] for file in os.listdir(os.getcwd()) if "_tvg" in file
    ]
    files.sort()

    @excpcls(2, DEFAULTFILE)
    class MyDialog(simpledialog.Dialog):
        def body(self, master):
            self.title("Choose File")
            Label(master, text="File: ").grid(row=0, column=0, sticky=E)
            self.e1 = ttk.Combobox(master)
            self.e1["values"] = files
            self.e1.grid(row=0, column=1)
            self.e1.bind("<KeyRelease>", partial(TreeViewGui.tynam, files=files))
            return self.e1

        def apply(self):
            self.result = self.e1.get()

    d = MyDialog(root)
    if d.result:
        return d.result
    else:
        return None


@excp(m=2, filenm=DEFAULTFILE)
def findpath():
    """Select default path for TVG"""

    pth = (
        os.path.join(os.path.expanduser("~"), "Documents", "TVG")
        if os.path.isdir(os.path.join(os.path.expanduser("~"), "Documents"))
        else os.path.join(os.path.expanduser("~"), "TVG")
    )
    if os.path.isdir(pth):
        os.chdir(pth)
    else:
        os.mkdir(pth)
        os.chdir(pth)


@excp(m=2, filenm=DEFAULTFILE)
def _modetheme(mode: str):
    global THEME_MODE

    match mode := mode:
        case mode if mode.lower() == "dark":
            if THEME_MODE is True:
                THEME_MODE = "dark"
        case mode if mode.lower() == "light":
            if THEME_MODE is False:
                THEME_MODE = "light"
        case _:
            pass


@excp(m=2, filenm=DEFAULTFILE)
def main():
    """Starting point of running TVG and making directory for non-existing file"""

    match ment := len(sys.argv):
        case ment if ment == 2:
            _modetheme(sys.argv[1])
        case _:
            pass

    global _addon
    if _addon and _addon.name == "addon_tvg":
        _addon = True
    else:
        _addon = False

    findpath()
    root = Tk()
    root.withdraw()
    if os.path.exists("lastopen.tvg"):
        root.update()
        ask = messagebox.askyesno("TreeViewGui", "Want to open previous file?")
        if ask:
            with open("lastopen.tvg", "rb") as lop:
                rd = eval(lop.read().decode("utf-8"))
            filename = rd["lop"]
        else:
            os.remove("lastopen.tvg")
            filename = askfile(root)
    else:
        filename = askfile(root)
    if filename:
        filename = filename.title()
        if not os.path.exists(f"{filename}_tvg"):
            try:
                os.mkdir(f"{filename}_tvg")
                os.chdir(f"{filename}_tvg")
            except:
                os.chdir(f"{filename}_tvg")
        else:
            os.chdir(f"{filename}_tvg")
        begin = TreeViewGui(root=root, filename=filename)
        begin.root.deiconify()
        if os.path.exists(f"{filename}_hid.json"):
            begin.hidform()
            begin.infobar()
        else:
            begin.view()
        begin.text.edit_reset()
        begin.root.mainloop()
    else:
        messagebox.showwarning("File", "No File Name!")
        root.destroy()
