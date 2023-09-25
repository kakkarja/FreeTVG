# -*- coding: utf-8 -*-
# Copyright © kakkarja (K A K)


import ast
import importlib
import json
import os
import re
import string
from datetime import datetime as dt
from functools import partial
from itertools import islice
from pathlib import Path
from sys import platform
from tkinter import (
    BROWSE,
    DISABLED,
    END,
    GROOVE,
    INSERT,
    LEFT,
    MULTIPLE,
    NONE,
    NORMAL,
    RIGHT,
    SEL_FIRST,
    SEL_LAST,
    TOP,
    WORD,
    Button,
    E,
    Entry,
    Frame,
    Label,
    Listbox,
    Message,
    Tk,
    Toplevel,
    X,
    colorchooser,
    font,
    messagebox,
    simpledialog,
    ttk,
    SEL,
)

import darkdetect
import tomlkit
from treeview import TreeView as tv
from treeview.dbase import Datab as db

from addon_tvg import Charts, EvalExp, SumAll
from excptr import DEFAULTDIR, DEFAULTFILE, DIRPATH, excp, excpcls

from .structure import Lay1, Lay2, Lay3, Lay4, Lay5, Lay6, Lay7, Lay8, Scribe
from .utility import ParseData, composemail, convhtml, wrwords

if platform.startswith("win"):
    from ctypes import byref, c_int, sizeof, windll


__all__ = ["main"]


DEFAULTDIR = os.path.join(DIRPATH, "FreeTVG_TRACE")
if not os.path.exists(DEFAULTDIR):
    os.mkdir(DEFAULTDIR)
DEFAULTFILE = os.path.join(DEFAULTDIR, Path(DEFAULTFILE).name)


THEME_MODE = darkdetect.theme().lower()

SELECT_MODE = "extended"

HIDDEN_OPT = False

WRAPPING = "none"

CHECKED_BOX = "off"


@excpcls(m=2, filenm=DEFAULTFILE)
class TreeViewGui:
    """
    This is the Gui for TreeView engine. This gui is to make the Writing and editing is viewable.
    """

    FREEZE = False
    MARK = False
    MODE = False
    GEO = None

    def __init__(self, root, filename):
        self.tmode = THEME_MODE
        self.cpp_select = SELECT_MODE
        self.hidopt = HIDDEN_OPT
        self.wrapping = WRAPPING
        self.checked_box = CHECKED_BOX
        self.filename = filename
        self.root = root
        self.plat = platform
        self.glop = Path(os.getcwd())
        self.root.title(f"{self.glop.joinpath(self.filename)}.txt")
        self.root.protocol("WM_DELETE_WINDOW", self.tvgexit)
        self.wwidth = 850 if self.plat.startswith("win") else 835
        self.wheight = 610
        self.root.minsize(self.wwidth, self.wheight)
        self.pwidth = int(self.root.winfo_screenwidth() / 2 - self.wwidth / 2)
        self.pheight = int(self.root.winfo_screenheight() / 3 - self.wheight / 3)
        self.root.geometry(f"{self.wwidth}x{self.wheight}+{self.pwidth}+{self.pheight}")
        self.GEO = f"{self.wwidth}x{self.wheight}+{self.pwidth}+{self.pheight}"
        gpath = self.glop.joinpath(self.glop.parent, "geo.tvg")
        gem = None
        if os.path.exists(gpath):
            with open(gpath, "rb") as geo:
                gem = ast.literal_eval(geo.read().decode("utf-8"))
                self.root.geometry(gem["geo"])
                self.GEO = gem["geo"]
        del gpath
        del gem

        # Variables for functions and other purposes
        self.bt = {}
        self.lock = False
        self.unlock = True
        self.store = None
        self.editorsel = None
        self.tpl = None
        self.ai = None
        self.ew = None
        self.cycle = None

        # Creating style "clam" style for TVG
        self.stl = ttk.Style(self.root)
        self.stl.theme_use("clam")

        # All root bindings
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
            self.root.bind("<Control-Up>", self.fcsent)
            self.root.bind("<Control-Down>", self.fcsent)
            self.root.bind("<Control-Left>", self.fcsent)
            self.root.bind("<Control-Right>", self.fcsent)
            self.root.bind_all("<Control-n>", self.fcsent)
            self.root.bind_all("<Control-Key-F1>", self.fcsent)
            self.root.bind_all("<Control-Key-F2>", self.fcsent)
            self.root.bind_all("<Control-Key-F3>", self.fcsent)
            self.root.bind_all("<Control-Key-F5>", self.configd)
            self.root.bind_all("<Control-Key-F4>", self.exprsum)
        else:
            self.root.bind_all("<Control-Shift-Up>", self.fcsent)
            self.root.bind_all("<Control-Shift-Down>", self.fcsent)
            self.root.bind_all("<Control-Shift-Left>", self.fcsent)
            self.root.bind_all("<Control-Shift-Right>", self.fcsent)
            self.root.bind_all("<Command-n>", self.fcsent)
            self.root.bind_all("<Key-F1>", self.fcsent)
            self.root.bind_all("<Key-F2>", self.fcsent)
            self.root.bind_all("<Key-F3>", self.fcsent)
            self.root.bind_all("<Key-F5>", self.configd)
            self.root.bind_all("<Key-F4>", self.exprsum)

        self.root.bind_all("<Control-Key-1>", self.fcsent)
        self.root.bind_all("<Control-Key-4>", self.fcsent)
        self.root.bind_all("<Control-Key-5>", self.fcsent)

        self.root.bind_class("TButton", "<Enter>", self.ttip)
        self.root.bind_class("TButton", "<Leave>", self.leave)
        self.root.bind_class("TRadiobutton", "<Enter>", self.ttip)
        self.root.bind_class("TRadiobutton", "<Leave>", self.leave)

        # 2nd frame.
        # Frame for first row Buttons.
        self.bframe = Lay2(self.root)
        self.bt["Insert"] = self.bframe.button5
        self.bt["Insert"].configure(command=self.insertwords)
        self.bt["Write"] = self.bframe.button6
        self.bt["Write"].configure(command=self.writefile)
        self.bt["Delete"] = self.bframe.button9
        self.bt["Delete"].configure(command=self.deleterow)
        self.bt["BackUp"] = self.bframe.button7
        self.bt["BackUp"].configure(command=self.backup)
        self.bt["Load"] = self.bframe.button8
        self.bt["Load"].configure(command=self.loadbkp)
        self.bt["Move Child"] = self.bframe.button3
        self.bt["Move Child"].configure(command=self.move_lr)
        self.bt["Change File"] = self.bframe.button16
        self.bt["Change File"].configure(command=self.chgfile)
        self.bt["Fold Childs"] = self.bframe.button33
        self.bt["Fold Childs"].configure(command=self.fold_childs)
        self.bt["CPP"] = self.bframe.button17
        self.bt["CPP"].configure(command=self.cmrows)

        # 3rd frame.
        # Frame for second row buttons.
        self.frb1 = Lay3(self.root)
        self.bt["Insight"] = self.frb1.button10
        self.bt["Insight"].configure(command=self.insight)
        self.bt["Arrange"] = self.frb1.button13
        self.bt["Arrange"].configure(command=self.spaces)
        self.bt["Paste"] = self.frb1.button11
        self.bt["Paste"].configure(command=self.copas)
        self.bt["Checked"] = self.frb1.button4
        self.bt["Checked"].configure(command=self.checked)
        self.bt["Up"] = self.frb1.button
        self.bt["Up"].configure(command=self.moveup)
        self.bt["Down"] = self.frb1.button2
        self.bt["Down"].configure(command=self.movedown)
        self.bt["Hide Parent"] = self.frb1.button14
        self.bt["Hide Parent"].configure(command=self.hiddenchl)
        self.bt["Fold selected"] = self.frb1.button34
        self.bt["Fold selected"].configure(command=self.fold_selected)
        self.bt["Clear hide"] = self.frb1.button15
        self.bt["Clear hide"].configure(command=self.delhid)

        # 4th Frame
        # For third row  of buttons
        self.frb2 = Lay4(self.root)
        self.bt["Create file"] = self.frb2.button23
        self.bt["Create file"].configure(command=self.createf)
        self.bt["Editor"] = self.frb2.button24
        self.bt["Editor"].configure(command=self.editor)
        self.bt["Un/Wrap"] = self.frb2.button25
        self.bt["Un/Wrap"].configure(command=self.wrapped)
        self.bt["Ex"] = self.frb2.button27
        self.bt["Ex"].configure(command=self.editex)
        self.bt["Template"] = self.frb2.button28
        self.bt["Template"].configure(command=self.temp)
        self.bt["Date-Time"] = self.frb2.button20
        self.bt["Date-Time"].configure(command=self.dattim)
        self.bt["Look Up"] = self.frb2.button19
        self.bt["Look Up"].configure(command=self.lookup)
        self.bt["Unfold"] = self.frb2.button35
        self.bt["Unfold"].configure(command=self.unfolding)
        self.bt["Printing"] = self.frb2.button12
        self.bt["Printing"].configure(command=self.saveaspdf)

        # 5th Frame
        # For MD buttons in editor
        self.frb3 = Lay5(self.root)

        # 6th Frame
        # For addon buttons
        self.addonb = Lay6(self.bframe, self.frb1, self.frb2)
        self.bt["Sum-Up"] = self.addonb.button30
        self.bt["Sum-Up"].configure(command=self.gettotsum)
        self.bt["Pie-Chart"] = self.addonb.button31
        self.bt["Pie-Chart"].configure(command=self.createpg)
        self.bt["Del Total"] = self.addonb.button32
        self.bt["Del Total"].configure(command=self.deltots)

        # 7th frame.
        # Frame for text, listbox and scrollbars.
        self.tframe = Lay7(self.root)
        self.text = self.tframe.text
        self.text.configure(wrap=self.wrapping)
        self.text.bind("<MouseWheel>", self.mscrt)
        if self.plat.startswith("win"):
            self.text.bind("<Control-z>", self.undo)
            self.text.bind("<Control-Shift-Key-Z>", self.redo)
        else:
            self.text.bind("<Command-z>", self.undo)
            self.text.bind("<Command-y>", self.redo)
        self.bt["text"] = self.text

        self.scrollbar1 = self.tframe.scrollbar1
        self.scrollbar1.bind("<ButtonRelease>", self.mscrt)
        self.bt["scrollbar1"] = self.scrollbar1

        self.listb = self.tframe.listb
        self.listb.bind("<<ListboxSelect>>", self.infobar)
        self.listb.bind("<MouseWheel>", self.mscrl)
        self.listb.bind("<Up>", self.mscrl)
        self.listb.bind("<Down>", self.mscrl)
        self.listb.bind("<FocusIn>", self.flb)
        self.bt["listb"] = self.listb

        self.scrollbar2 = self.tframe.scrollbar2
        self.scrollbar2.bind("<ButtonRelease>", self.mscrl)
        self.bt["scrollbar2"] = self.scrollbar2

        # 8th frame.
        # Frame for horizontal scrollbar and info label.
        self.fscr = Lay8(self.root)
        self.scrolh = self.fscr.scrolh
        self.scrolh.config(command=self.text.xview)
        self.text.config(xscrollcommand=self.scrolh.set)

        self.info = self.fscr.info
        self.info.set(f'{dt.strftime(dt.today(),"%a %d %b %Y")}')

        # 1st frame.
        # Frame for labels, Entry, radio-buttons and combobox.
        self.fframe = Lay1(self.root)
        self.bt["entry"] = self.fframe.entry
        self.bt["radio1"] = self.fframe.radio1
        self.bt["radio2"] = self.fframe.radio2
        self.bt["label3"] = self.fframe.label3
        self.bt["entry3"] = self.fframe.entry3

        # Creating tool-tip for all buttons and radio-buttons
        self.scribe = Scribe().scribe()
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

        # cheking existing paths for early configuration on TVG
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
        if not self.glop.parent.joinpath("TVG_config.toml").exists():
            _create_config(self.glop.parent.joinpath("TVG_config.toml"))

        # Last touch configuration for font in buttons,
        # and for creating font-chooser that callable in a function
        self.stl.configure(
            "TButton",
            font="verdana 7 bold" if self.plat.startswith("win") else "verdana 8 bold",
        )
        self.root.tk.call(
            "tk",
            "fontchooser",
            "configure",
            "-font",
            self.text["font"],
            "-command",
            self.root.register(self.clb),
            "-parent",
            self.root,
        )

        # Checking theme mode!
        self.ldmode()
        self.cycle_theme()

    def cycle_theme(self):
        """Detecting system theme cycle and apply it to TVG"""

        if darkdetect.theme().lower() != self.tmode:
            self.tmode = darkdetect.theme().lower()
            self.ldmode()
        self.cycle = self.root.after(1000, self.cycle_theme)

    def _windows_only(self):
        # Ref:
        # https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter
        # These attributes are for windows 11
        bar = None
        title = None
        if self.tmode == "dark":
            bar = 0x001A1A1A
            title = 0xEEEEEE
        else:
            bar = 0xEEEEEE
            title = 0x001A1A1A
        HWND = windll.user32.GetParent(self.root.winfo_id())
        DWMWA_CAPTION_COLOR = 35
        DWMWA_TITLE_COLOR = 36
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, DWMWA_CAPTION_COLOR, byref(c_int(bar)), sizeof(c_int)
        )
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, DWMWA_TITLE_COLOR, byref(c_int(title)), sizeof(c_int)
        )
        del bar, title, HWND, DWMWA_CAPTION_COLOR, DWMWA_TITLE_COLOR

    def ldmode(self):
        """Dark mode for easing the eye"""

        oribg = "#dcdad5"
        chbg = "grey30"
        orifg = "black"
        chfg = "white"
        if self.tmode == "dark" or self.tmode is False:
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
            if self.text.cget("background") == "SystemWindow":
                with open(
                    self.glop.joinpath(self.glop.parent, "theme.tvg"), "w"
                ) as thm:
                    thm.write("#4d4d4d")
                self.txtcol(
                    path=self.glop.joinpath(self.glop.parent, "theme.tvg"), wr=False
                )
            if self.plat.startswith("win"):
                self._windows_only()
        elif self.tmode == "light":
            self.stl.configure(
                ".",
                background=oribg,
                foreground=orifg,
                fieldbackground=oribg,
                insertcolor=orifg,
                troughcolor="#bab5ab",
                arrowcolor=orifg,
                bordercolor="#9e9a91",
            )
            self.stl.map(
                ".",
                background=[("background", oribg)],
            )
            self.stl.map(
                "TCombobox",
                fieldbackground=[("readonly", oribg)],
                background=[("active", "#eeebe7")],
                arrowcolor=[("active", "black")],
            )
            self.stl.map(
                "Horizontal.TScrollbar",
                background=[("active", "#eeebe7")],
                arrowcolor=[("active", "black")],
            )
            self.stl.map(
                "Vertical.TScrollbar",
                background=[("active", "#eeebe7")],
                arrowcolor=[("active", "black")],
            )
            self.stl.configure("TEntry", fieldbackground=chfg)
            if self.plat.startswith("win"):
                self._windows_only()
        del oribg, chbg, orifg, chfg
        self.root.update()

    def ttip(self, event=None):
        """Tooltip for TVG buttons"""

        if tx := self.scribe.get(event.widget["text"], None):

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
        self.fframe.pack_forget()
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
        self.fframe.pack(fill="x")
        self.fframe.update()
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

        if self.text.cget("wrap") == "none":
            self.text.config(wrap=WORD)
        else:
            self.text.config(wrap=NONE)

    def infobar(self, event=None):
        """Info Bar telling the selected rows in listbox.
        If nothing, it will display today's date.
        """

        if os.path.exists(f"{self.filename}_hid.json"):
            self.info.set("Hidden Mode")
        elif self.FREEZE and str(self.bt["CPP"]["state"]) == "normal":
            self.info.set("CPP Mode")
        elif self.FREEZE and str(self.bt["Editor"]["state"]) == "normal":
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

    def nonetype(self):
        """For checking file is empty or not"""

        if self.checkfile():
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
        try:
            fcom = str(self.root.focus_get())
        except:
            fcom = ""
        if self.FREEZE is False:
            if event.keysym == "f":
                self.bt["entry"].focus()
            elif event.keysym == "r":
                self.bt["entry3"].focus()
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
                if self.fframe.rb.get() == "parent":
                    self.fframe.rb.set("child")
                    self.fframe.radiobut()
                    self.fframe.focus()
                else:
                    self.fframe.rb.set("parent")
                    self.fframe.radiobut()
                    self.fframe.focus()
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
            elif event.keysym == "1":
                self.gettotsum()
            elif event.keysym == "4":
                self.createpg()
            elif event.keysym == "5":
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
            if self.lock is False:
                if str(self.bt["CPP"].cget("state")) == "normal":
                    if event.keysym == "n":
                        self.cmrows()
                    elif event.keysym == "s":
                        self.insight()
                elif str(self.bt["Hide Parent"].cget("state")) == "normal":
                    if event.keysym == "h":
                        self.hiddenchl()
                    elif event.keysym == "s":
                        self.insight()
                elif (
                    str(self.bt["Editor"].cget("state")) == "normal"
                    and event.keysym == "7"
                ):
                    self.editor()
                elif str(self.bt["Fold selected"].cget("state")) == "normal":
                    if event.keysym == "S":
                        self.fold_selected()
                    elif event.keysym == "s":
                        self.insight()

        del fcom

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

    def _spot_on(self, row: int):
        """View the latest spot of a row"""

        self.text.see(f"{row + 1}.0")
        self.listb.see(row)

    def _move_to(self, top: bool = True):
        if top:
            self.text.yview_moveto(0.0)
            self.listb.yview_moveto(0.0)
        else:
            self.text.yview_moveto(1.0)
            self.listb.yview_moveto(1.0)

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

        if self.nonetype():
            self.text.config(state="normal")
            self.text.delete("1.0", END)
            self.listb.delete(0, END)
            with tv(self.filename) as tvg:
                self._prettyv(tvg.getdata())
                for k, v in tvg.insighttree():
                    self.listb.insert(END, f"{k}: {v[0]}")
            self.tframe.text_view()
            self.text.edit_reset()
            self.text.config(state="disable")
            self._move_to(False)
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

        if self.nonetype():
            if sta:
                if hasattr(self, "sumtot"):
                    with open(self.glop.absolute().joinpath("sumtot.tvg"), "wb") as st:
                        st.write("True".encode())
            else:
                if not self.glop.absolute().joinpath("sumtot.tvg").exists():
                    self._sumchk()
                else:
                    self._sumchk()
                    os.remove(self.glop.absolute().joinpath("sumtot.tvg"))

    def chgfile(self):
        """Changing file on active app environment"""

        def chosen(file):
            fi = file
            self.FREEZE = False
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
                self._move_to(False)
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
            self.FREEZE = True
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
            self.root.update()
            self.lock = False
            if d.result:
                if d.result in files:
                    chosen(d.result)
                else:
                    messagebox.showerror(
                        "TreeViewGui",
                        f"Unable to process for {d.result}!",
                        parent=self.root,
                    )
                    self.FREEZE = False
            else:
                self.FREEZE = False
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
                if self.bt["entry"].get():
                    if not self.bt["entry3"].get():
                        if self.bt["entry"].get() not in cek:
                            with tv(self.filename) as tvg:
                                tvg.writetree(self.bt["entry"].get())
                            del tvg
                            self.bt["entry"].delete(0, END)
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
                rw = self.listb.curselection()[0] if self.listb.curselection() else None
                total = True
                current_size = None
                child = self.bt["entry3"].get()
                if (
                    self.bt["entry"].get()
                    and self.bt["entry"].get() not in cek
                    and (total := self._check_Totals())
                ):
                    current_size = self.listb.size()
                    if self.MARK:
                        if self._chk_total_spc(rw):
                            appr = messagebox.askyesno(
                                "Edit", f"Edit cell {rw}?", parent=self.root
                            )
                            if appr:
                                with tv(self.filename) as tvg:
                                    tvg.edittree(
                                        self.bt["entry"].get(),
                                        rw,
                                        child=child if child else None,
                                    )
                                del tvg
                                self.bt["entry"].delete(0, END)
                    else:
                        total = False
                        with tv(self.filename) as tvg:
                            if child:
                                tvg.quickchild(self.bt["entry"].get(), child)
                            else:
                                tvg.addparent(self.bt["entry"].get())
                        self.bt["entry"].delete(0, END)
                        del tvg
                    self.spaces()
                    if total:
                        if size := self.listb.size() - current_size:
                            self._fold_restruct(size, rw)
                            self.view()
                        else:
                            self._fold_restruct(0, 0, row=rw)
                        del size
                if rw:
                    self._spot_on(rw)
                del rw, total, current_size
        del cek

    def flb(self, event=None):
        """Set Mark for cheking row for edit"""

        self.MARK = True

    def _chk_total_spc(self, row: int):
        """Checking total and space"""

        try:
            with tv(self.filename) as tvg:
                for n, d in tvg.getdata():
                    if n == row:
                        if d.strip().startswith("-TOTAL") or d.startswith("\n"):
                            return False
                return True
        finally:
            del tvg

    def deleterow(self):
        """Deletion on recorded row and updated"""

        self.hidcheck()
        if self.unlock:
            if self.nonetype():
                if self.listb.curselection() and self._chk_total_spc(
                    int(self.listb.curselection()[0])
                ):
                    self.MODE = True
                    current_size = self.listb.size()
                    rw = int(self.listb.curselection()[0])
                    with tv(self.filename) as tvg:
                        if rw != 0:
                            tvg.delrow(rw)
                    del tvg
                    self.spaces()
                    self._fold_restruct(self.listb.size() - current_size, rw)
                    self.view()
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
                            self._spot_on(rw)
                        else:
                            self.listb.select_set(rw - 1)
                            self._spot_on(rw - 1)
                    else:
                        if ck[0] == 1:
                            self.listb.select_set(0)
                        else:
                            self.listb.select_set(len(ck) - 1)
                            self._spot_on(len(ck) - 1)
                    del rw, ck, current_size
                    self.infobar()

    def move_lr(self, event=None):
        """Moving a child row to left or right, as to define spaces needed"""

        self.hidcheck()
        if self.unlock:
            if self.listb.curselection():
                if self.bt["entry3"].get():
                    self.MODE = True
                    try:
                        rw = int(self.listb.curselection()[0])
                        self.text.config(state="normal")
                        with tv(self.filename) as tvg:
                            tvg.movechild(rw, self.bt["entry3"].get())
                        del tvg
                        self._fold_restruct(0, 0, row=rw)
                        self.spaces()
                        self.text.config(state="disable")
                        self.listb.select_set(rw)
                        self._spot_on(rw)
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
            if self.nonetype():
                self.text.config(state="normal")
                self.text.delete("1.0", END)
                with tv(self.filename) as tvg:
                    for k, v in tvg.insighttree():
                        self.text.insert(END, f"row {k}: {v[0]}, {v[1]}")
                del tvg
                self.text.edit_reset()
                self.text.config(state="disable")
                self._move_to()

    def moveup(self, event=None):
        """Step up a row to upper row"""

        self.hidcheck()
        if self.unlock:
            if self.nonetype() and self._check_Totals():
                if self.listb.curselection():
                    rw = int(self.listb.curselection()[0])
                    insight = self.listb.get(rw).split(":")[1].strip()
                    if insight != "space" and "child" in insight:
                        if rw != 0 and rw - 1 != 0:
                            self.MODE = True
                            with tv(self.filename) as tvg:
                                tvg.movetree(rw, rw - 1)
                            del tvg
                            self.spaces()
                            self._fold_restruct(0, 0, row=rw - 1, move=True)
                            self.view()
                            ck = self.listb.get(rw - 1).split(":")[1].strip()
                            if ck != "space":
                                self.listb.select_set(rw - 1)
                                self._spot_on(rw - 1)
                            else:
                                self.listb.select_set(rw - 2)
                                self._spot_on(rw - 2)
                            self.infobar()
                            del ck
                    del rw, insight

    def movedown(self, event=None):
        """Step down a row to below row"""

        self.hidcheck()
        if self.unlock:
            if self.nonetype():
                if self.listb.curselection() and self._check_Totals():
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
                            self.MODE = True
                            mv = None
                            with tv(self.filename) as tvg:
                                if sp:
                                    tvg.movetree(rw, mv := rw + 2)
                                else:
                                    tvg.movetree(rw, mv := rw + 1)
                            del tvg, sp
                            self.spaces()
                            self._fold_restruct(0, 0, row=mv, move=True, down=True)
                            self.view()
                            del mv
                            ck = self.listb.get(rw + 1).split(":")[1].strip()
                            if ck != "parent":
                                self.listb.select_set(rw + 1)
                                self._spot_on(rw + 1)
                            else:
                                self.listb.select_set(rw + 2)
                                self._spot_on(rw + 2)
                            self.infobar()
                    del rw, ck

    def insertwords(self, event=None):
        """Insert a record to any row appear above the assign row"""

        self.hidcheck()
        if self.unlock:
            if self.nonetype():
                cek = ["parent", "child"]
                if self.bt["entry"].get() and (
                    self.bt["entry"].get() not in cek and self._check_Totals()
                ):
                    if self.MARK:
                        appr = messagebox.askyesno(
                            "Edit",
                            f"Edit cell {self.listb.curselection()[0]}?",
                            parent=self.root,
                        )
                        if appr:
                            if self.listb.curselection():
                                current_size = self.listb.size()
                                rw = int(self.listb.curselection()[0])
                                with tv(self.filename) as tvg:
                                    if self.bt["entry3"].get():
                                        tvg.insertrow(
                                            self.bt["entry"].get(),
                                            rw,
                                            self.bt["entry3"].get(),
                                        )
                                    else:
                                        tvg.insertrow(self.bt["entry"].get(), rw)
                                del tvg
                                self.bt["entry"].delete(0, END)
                                self.spaces()
                                self._fold_restruct(
                                    self.listb.size() - current_size, rw
                                )
                                self.view()
                                self._spot_on(rw)
                                del rw, current_size
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
                self._ckinsight()
                if self.checked_box.lower() == "on":
                    gtt = self.text.get(f"{rw + 1}.0", f"{rw + 1}.0 lineend")
                    if gtt:
                        if gtt[0].isspace() and not gtt.strip().startswith("-[x] "):
                            gtt = gtt.partition("-")
                            rwd = "[x] " + gtt[2]
                            with tv(self.filename) as tvg:
                                tvg.edittree(rwd, rw, f"child{len(gtt[0])//4}")
                            del rwd, tvg
                        elif gtt.strip().startswith("-[x] "):
                            gtt = gtt.partition("-[x] ")
                            rwd = gtt[2]
                            with tv(self.filename) as tvg:
                                tvg.edittree(rwd, rw, f"child{len(gtt[0])//4}")
                            del rwd, tvg
                    del gtt
                else:
                    with tv(self.filename) as tvg:
                        tvg.checked(rw)
                    del tvg
                self._fold_restruct(0, 0, row=rw)
                self.view()
                self.listb.select_set(rw)
                self.listb.activate(rw)
                self._spot_on(rw)
                del rw
                self.infobar()

    def backup(self, event=None):
        """Backup to max of 10 datas on csv file.
        And any new one will remove the oldest one.
        """

        self.hidcheck()
        if self.unlock:
            if self.nonetype():
                with tv(self.filename) as tvg:
                    tvg.backuptv()
                del tvg
                messagebox.showinfo("Backup", "Backup done!", parent=self.root)

    def loadbkp(self, event=None):
        """Load any backup data"""

        self.hidcheck()
        if self.unlock:
            if os.path.exists(f"{self.filename}.json"):
                dbs = db(self.filename)
                row = simpledialog.askinteger(
                    "Load Backup",
                    (
                        f"There are {dbs.totalrecs()} rows, please choose a row:\n"
                        f"(Fold selections data will be erased!)"
                    ),
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
                    self._deldatt(False)
                    self._sumchk()
                    self._chkfoldatt()
                    self.spaces()

                del row, dbs

    def copas(self, event=None):
        """Paste a row value to Entry for fixing value"""

        self.hidcheck()
        if self.unlock:
            if self.listb.curselection():
                self.bt["entry"].delete(0, END)
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
                            self.bt["entry"].insert(END, paste)
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

    def _copytofile(self):
        """Copy parents and childs in hidden modes to another existing file or new file."""

        def chosen(flname):
            self.FREEZE = False
            if flname == "New":
                askname = simpledialog.askstring(
                    "TreeViewGui", "New file name:", parent=self.root
                )
                if askname:
                    if not os.path.exists(self.glop.parent.joinpath(f"{askname}_tvg")):
                        tak = self.fildat(self.text.get("1.0", END)[:-1])
                        os.remove(f"{self.filename}_hid.json")
                        self.createf(askname)
                        with tv(self.filename) as tvg:
                            tvg.fileread(tvg.insighthidden(tak, False))
                        self.addonchk(False)
                        del tak, tvg
                        self.spaces()
                        self.infobar()
                    else:
                        messagebox.showinfo(
                            "TreeViewGui",
                            "Cannot create new file because is already exist!",
                            parent=self.root,
                        )
                else:
                    messagebox.showinfo(
                        "TreeViewGui", "Copying is aborted!", parent=self.root
                    )
                del askname
            else:
                if os.path.exists(
                    self.glop.parent.joinpath(
                        flname, f'{flname.rpartition("_")[0]}.txt'
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
                        self.glop = self.glop.parent.joinpath(flname)
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
                    self.glop = self.glop.parent.joinpath(flname)
                    os.chdir(self.glop)
                    self.root.title(f"{self.glop.joinpath(self.filename)}.txt")
                    with tv(self.filename) as tvg:
                        tvg.fileread(tvg.insighthidden(tak, False))
                    del tak, tvg
                    self.addonchk(False)
                    self.spaces()
                    self.infobar()
            del flname

        self.FREEZE = True
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
                self.e1.bind("<KeyRelease>", partial(TreeViewGui.tynam, files=files))
                self.e1.current(0)
                self.e1.grid(row=0, column=1)
                return self.e1

            def apply(self):
                self.result = self.e1.get()

        d = MyDialog(self.root)
        self.root.update()
        self.lock = False
        if d.result:
            if d.result in files:
                chosen(d.result)
            else:
                messagebox.showerror(
                    "TreeViewGui",
                    f"Unable to process for {d.result}!",
                    parent=self.root,
                )
                self.FREEZE = False
        else:
            self.FREEZE = False
        del files, d.result

    def cmrows(self):
        """Copy or move any rows to any point of a row within existing rows."""

        askmove = (
            messagebox.askyesno(
                "TreeViewGui", "Want to move to other file?", parent=self.root
            )
            if self.info.get() == "Hidden Mode"
            else None
        )
        if askmove:
            self._copytofile()
        else:
            self.hidcheck()
            if self.unlock:
                if self.nonetype():
                    if self.listb.cget("selectmode") == "browse":
                        self.listb.config(selectmode=self.cpp_select)
                        self.disab("listb", "CPP", "Insight", "text")
                    else:
                        if gcs := self.listb.curselection():
                            gcs = [int(i) for i in gcs]
                            ask = simpledialog.askinteger(
                                "TreeViewGui",
                                (
                                    f"Move to which row? choose between 0 to {self.listb.size()-1} rows\n"
                                    "WARNING: Fold selection not working in 'MOVE'!"
                                ),
                                parent=self.root,
                            )
                            if ask is not None and ask < self.listb.size():
                                foldsel = (
                                    True if self._ckfoldtvg() is not None else False
                                )
                                while True:
                                    deci = messagebox.askyesnocancel(
                                        "TreeViewGui",
                                        '"Yes" to MOVE to, "No" to COPY to\n',
                                        parent=self.root,
                                    )
                                    if deci:
                                        if foldsel:
                                            messagebox.showwarning(
                                                "TreeViewGui",
                                                "Cannot move in folded data, please choose 'COPY' instead!",
                                                parent=self.root,
                                            )
                                            continue
                                        else:
                                            break
                                    else:
                                        break
                                del foldsel
                                if deci is not None:
                                    if deci:
                                        with tv(self.filename) as tvg:
                                            data = []
                                            for i in range(len(gcs)):
                                                for _, d in islice(
                                                    tvg.getdata(), gcs[i], gcs[i] + 1
                                                ):
                                                    data.append(d)
                                            writer = tvg.satofi()
                                            if ask < tvg.getdatanum() - 1:
                                                for n, d in tvg.getdata():
                                                    if n == ask == 0:
                                                        if not data[0][0].isspace():
                                                            for i in data:
                                                                writer.send(i)
                                                            writer.send(d)
                                                        else:
                                                            writer.send(d)
                                                            for i in data:
                                                                writer.send(i)
                                                    elif n == ask:
                                                        for i in data:
                                                            writer.send(i)
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
                                                    writer.send(i)
                                            writer.close()
                                        del tvg, data, writer
                                        self.spaces()
                                    else:
                                        current_size = self.listb.size()
                                        with tv(self.filename) as tvg:
                                            data = []
                                            for i in range(len(gcs)):
                                                for _, d in islice(
                                                    tvg.getdata(), gcs[i], gcs[i] + 1
                                                ):
                                                    data.append(d)
                                            writer = tvg.satofi()
                                            if ask < tvg.getdatanum() - 1:
                                                for n, d in tvg.getdata():
                                                    if n == ask == 0:
                                                        if not data[0][0].isspace():
                                                            for i in data:
                                                                writer.send(i)
                                                            writer.send(d)
                                                        else:
                                                            writer.send(d)
                                                            for i in data:
                                                                writer.send(i)
                                                    elif n == ask:
                                                        for i in data:
                                                            writer.send(i)
                                                        writer.send(d)
                                                    else:
                                                        writer.send(d)
                                            else:
                                                for n, d in tvg.getdata():
                                                    writer.send(d)
                                                for i in data:
                                                    writer.send(i)
                                            writer.close()
                                        del tvg, data, writer
                                        self.spaces()
                                        self._fold_restruct(
                                            self.listb.size() - current_size, ask
                                        )
                                        del current_size
                                        self.view()
                                self.disab(dis=False)
                                self.listb.config(selectmode=BROWSE)
                                self._spot_on(ask)
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

    def _ckinsight(self):
        if "row 0:" in self.text.get("1.0", "1.0 lineend"):
            self.view()

    def _utilspdf(self):
        try:
            self._ckinsight()
            gttx = []
            line = None
            cg = None
            eldat = self._ckfoldtvg()
            with tv(self.filename) as tvg:
                if hasattr(self, "fold") and eldat:
                    for n, d in tvg.getdata():
                        if n not in eldat:
                            gttx.append(d)
                    return "".join(gttx)
                else:
                    return "".join([d for _, d in tvg.getdata()])
        finally:
            del gttx, line, cg, eldat, tvg

    def saveaspdf(self):
        """Show to browser and directly print as pdf or direct printing"""

        if self.nonetype():
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

            ans = messagebox.askyesno(
                "Preview",
                "Do you want to preview? ('no' will go to web for printing)",
                parent=self.root,
            )
            style = None
            if ans:
                style = convhtml(
                    self._utilspdf(),
                    self.filename,
                    fon,
                    self.text.cget("background")[1:],
                    self.text.cget("foreground"),
                )
            else:
                style = convhtml(
                    self._utilspdf(),
                    self.filename,
                    fon,
                    self.text.cget("background")[1:],
                    self.text.cget("foreground"),
                    preview=False,
                    pdfpath=self.glop.joinpath(f"{self.filename}.pdf")
                    if not self.plat.startswith("win")
                    else None,
                )
            del px, ck, sty, add, fon, style

    def spaces(self):
        """Mostly used by other functions to clear an obselete spaces.
        To appropriate the display better.
        """

        self.hidcheck()
        if self.unlock:
            if self.nonetype():
                if self.MARK and self.MODE is False:
                    self.MARK = False
                else:
                    self.MODE = False
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
                if self.listb.size():
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

        if os.path.exists(f"{self.filename}_hid.json"):
            with open(f"{self.filename}_hid.json") as jfile:
                rd = dict(json.load(jfile))
            rolrd = tuple(tuple(i) for i in tuple(rd.values()) if isinstance(i, list))
            self.view()
            showt = self.text.get("1.0", END).split("\n")[:-2]
            if self.hidopt == "unreverse":
                for wow, wrow in rolrd:
                    for i in range(wow, wrow + 1):
                        showt[i] = 0
                self.text.config(state="normal")
                self.text.delete("1.0", END)
                showt = tuple(f"{i}\n" for i in showt if i != 0)
                self._prettyv(enumerate(showt))
                self.text.config(state="disable")
                self.listb.delete(0, END)
                if showt:
                    with tv(self.filename) as tvg:
                        vals = enumerate(
                            [d[0] for d in tvg.insighthidden(enumerate(showt), False)]
                        )
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
            self._move_to()

    def hiddenchl(self, event=None):
        """Create Hidden position of parent and its childs in json file"""

        if hasattr(self, "fold"):
            messagebox.showinfo("TreeViewGui", "Please unfolding first!")
        else:
            if self.nonetype():
                if not os.path.exists(f"{self.filename}_hid.json"):
                    if self.listb.cget("selectmode") == "browse":
                        self.info.set("Hidden Mode")
                        self.disab("listb", "Hide Parent", "Insight", "text")
                        self.listb.config(selectmode=MULTIPLE)
                    else:
                        if self.listb.curselection():
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
                                with open(f"{self.filename}_hid.json", "w") as jfile:
                                    json.dump(hd, jfile)
                                self.hidform()
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

        if os.path.exists(f"{self.filename}_hid.json"):
            os.remove(f"{self.filename}_hid.json")
            self.spaces()
            messagebox.showinfo(
                "TreeViewGui",
                f"{self.filename}_hid.json has been deleted!",
                parent=self.root,
            )

    def _data_appear(self, dat: str, src: int, max: int = 100):
        match len(dat):
            case num if num < max:
                return dat
            case _:
                hl = len(dat[:src])
                hr = len(dat[src:])
                if hr < hl:
                    return dat[src - (hl - hr) : max]
                else:
                    if hr < max:
                        match max - hr:
                            case cmp if cmp >= src:
                                return dat[src:]
                            case _:
                                return dat[src - cmp :]
                    return dat[src:max]

    def lookup(self, event=None):
        """To lookup word on row and also on editor mode"""

        self.hidcheck()
        if self.unlock:
            if (
                str(self.text.cget("state")) == "normal"
                and str(self.bt["Editor"].cget("state")) == "normal"
            ):
                if self.text.count("1.0", END, "chars")[0] > 1:

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
                        self.FREEZE = True
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
                        self.root.update()
                        self.lock = False
                        if d.result:
                            searchw(d.result)
                        self.FREEZE = False
                        del d.result
            else:
                if self.nonetype():
                    if self.bt["entry"].get():
                        num = self.listb.size()
                        sn = 1
                        sw = self.bt["entry"].get()
                        dat = None
                        if sw.isdigit():
                            sw = int(sw)
                            if sw <= num - 1:
                                self._spot_on(sw)
                                self.listb.focus()
                                self.listb.selection_clear(0, END)
                                self.listb.activate(sw)
                                self.listb.selection_set(sw)
                        else:
                            while sn <= num:
                                dat = self.text.get(
                                    f"{sn}.0", f"{sn}.0 lineend"
                                ).strip()
                                if sw in dat:
                                    src = dat.find(sw)
                                    dat = self._data_appear(dat, src, 81)
                                    self._spot_on(sn - 1)
                                    self.listb.selection_clear(0, END)
                                    self.listb.selection_set(sn - 1)
                                    self.listb.focus()
                                    self.listb.activate(sn - 1)
                                    ask = messagebox.askyesno(
                                        "TreeViewGui",
                                        f"Find in row {sn-1}\nText: '...{dat}...'\nContinue lookup?",
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

        if str(self.bt["entry"].cget("state")) == "normal":
            dtt = f'[{dt.isoformat(dt.today().replace(microsecond = 0)).replace("T"," ")}]'
            ck = ["parent", "child"]
            if self.bt["entry"].get() in ck:
                self.bt["entry"].delete(0, END)
            if self.bt["entry"].get():
                hold = self.bt["entry"].get()
                gt = re.match(r"\[.*?\]", hold)
                if not gt:
                    self.bt["entry"].delete(0, END)
                    self.bt["entry"].insert(0, f"{dtt} {hold}")
                else:
                    try:
                        if isinstance(dt.fromisoformat(gt.group()[1:20]), dt):
                            self.bt["entry"].delete(0, END)
                            self.bt["entry"].insert(0, f"{dtt} {hold[22:]}")
                    except:
                        self.bt["entry"].delete(0, END)
                        self.bt["entry"].insert(0, f"{dtt} {hold}")
                del hold, gt
            else:
                self.bt["entry"].insert(0, f"{dtt} ")
            del dtt, ck
        elif (
            str(self.text.cget("state")) == "normal"
            and str(self.bt["Date-Time"].cget("state")) == "normal"
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
            mkd = self.glop.parent.joinpath(f"{titlemode(fl)}_tvg")
            if not os.path.exists(mkd):
                self.addonchk()
                mkd.mkdir()
                os.chdir(mkd)
                self.glop = mkd
                self._chkfoldatt()
                self.filename = self.glop.name.rpartition("_")[0]
                self.root.title(f"{self.glop.absolute().joinpath(self.filename)}.txt")
                self.text.config(state=NORMAL)
                self.text.delete("1.0", END)
                self.text.config(state=DISABLED)
                self.bt["entry"].delete(0, END)
                self.fframe.rb.set("")
                self.bt["entry"].config(state=DISABLED)
                self.listb.delete(0, END)
                self.addonchk(False)
            else:
                messagebox.showinfo(
                    "TreeViewGui",
                    f"The file {mkd}/{titlemode(fl)}.txt is already exist!",
                    parent=self.root,
                )
            del mkd
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
            if self.nonetype():
                total = None
                stor = self.listb.curselection()
                if stor:
                    if "parent" in self.listb.get(stor := stor[0]) and (
                        total := self._check_Totals()
                    ):
                        self.editor()
                        with tv(self.filename) as tvg:
                            num = stor
                            for p, d in islice(
                                tvg.compdatch(True), stor, tvg.getdatanum()
                            ):
                                if p == "parent":
                                    self.text.insert(END, f"p:{d[:-2]}\n")
                                elif p.partition("child")[1]:
                                    self.text.insert(END, f"c{p[5:]}:{d[1:]}")
                                else:
                                    if p == "space":
                                        break
                                num += 1
                        self.editorsel = (stor, num)
                        del tvg, num
                        self.text.see(self.text.index(INSERT))
                    else:
                        if "child" in self.listb.get(stor):
                            messagebox.showinfo(
                                "TreeViewGui",
                                "Please select a parent row first!",
                                parent=self.root,
                            )
                del total, stor

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
    def tynam(event, files: list | tuple, ca: bool = True):
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
                        event.widget.icursor(index=idx)
                        break
                else:
                    if ca:
                        for em in files:
                            if gt[: idx - 1] in em:
                                event.widget.current(files.index(em))
                                break
                        else:
                            event.widget.delete(0, END)
                            event.widget.insert(0, gt[: idx - 1])
                        event.widget.icursor(index=idx - 1)
            del idx, gt

    def temp(self, event=None):
        """This is to compliment the editor mode.
        If you have to type several outline that has same format,
        You can save them as template and re-use again in the editor mode.
        """

        if (
            str(self.text.cget("state")) == "normal"
            and str(self.bt["Editor"].cget("state")) == "normal"
        ):
            if not os.path.exists(os.path.join(self.glop.parent, "Templates")):
                os.mkdir(os.path.join(self.glop.parent, "Templates"))
                self.tempsave()
            else:
                if self.lock is False:
                    self.FREEZE = True
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
                        self.root.update()
                        self.lock = False
                        if d.result:
                            if d.result in files:
                                path = os.path.join(
                                    self.glop.parent, "Templates", d.result
                                )
                                with open(path) as rdf:
                                    gf = ast.literal_eval(rdf.read())
                                for pr in gf:
                                    self.text.insert(f"{INSERT} linestart", f"{pr}\n")
                                del path, gf, pr
                            else:
                                messagebox.showerror(
                                    "TreeViewGui",
                                    f"Unable to process for {d.result}!",
                                    parent=self.root,
                                )
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
                    self.FREEZE = False
                    del files
            self.text.focus()

    def disab(self, *args, dis=True):
        """Conditioning buttons for functions mode purpose"""

        if dis and args:
            for i in self.bt:
                if "label" not in i and "scrollbar" not in i:
                    if i not in args:
                        self.bt[i].config(state="disable")
            self.FREEZE = True
        else:
            for i in self.bt:
                if "label" not in i and "scrollbar" not in i:
                    if i == "entry3":
                        self.bt[i].config(state="readonly")
                    elif i == "entry":
                        if not self.fframe.rb.get():
                            self.bt[i].config(state="disable")
                        else:
                            self.bt[i].config(state="normal")
                    else:
                        if i != "text":
                            self.bt[i].config(state="normal")
            self.FREEZE = False

    def _mdbuttons(self):
        if not hasattr(self, "mdframe"):
            self.__setattr__("mdb", None)
            self.mdb = {
                "B": ("<Control-Shift-!>", "**"),
                "I": ("<Control-Shift-@>", "*"),
                "U": ("<Control-Shift-#>", "^^"),
                "S": ("<Control-Shift-$>", "~~"),
                "M": ("<Control-Shift-%>", "=="),
                "SA": ("<Control-Shift-^>", "++"),
                "L": ("<Control-Shift-&>", "[]()"),
                "SP": ("<Control-Shift-*>", "^"),
                "SB": ("<Control-Shift-(>", "~"),
                "C": ("<Control-Shift-)>", "[x]"),
                "AR": ("<Control-Shift-Q>", "-->"),
                "AL": ("<Control-Shift-W>", "<--"),
                "AT": ("<Control-Shift-E>", "<-->"),
                "PM": ("<Control-Shift-R>", "+/-"),
                "TM": ("<Control-Shift-T>", "(tm)"),
                "CR": ("<Control-Shift-Y>", "(c)"),
                "R": ("<Control-Shift-I>", "(r)"),
            }

            stb = None

            @excp(2, DEFAULTFILE)
            def storbut(event):
                nonlocal stb
                stb = event.widget.cget("text")

            @excp(2, DEFAULTFILE)
            def check_mdatt():
                sentence = self.text.get(SEL_FIRST, SEL_LAST)

                if all(i not in sentence for i in ["*", "~", "^", "\\"]):
                    return True
                messagebox.showwarning(
                    "TreeViewGui",
                    f"The sentence '{sentence}' has char like | * | ~ | ^ | \ |"
                    " which is represent a Markdown's char or escape char!\n"
                    "Please delete it first!",
                    parent=self.root,
                )

            @excp(2, DEFAULTFILE)
            def insmd():
                if stb and stb in self.mdb:
                    mk = None
                    markd = ("B", "I", "U", "S", "M", "SA", "L", "SP", "SB")
                    match self.text.tag_ranges("sel"):
                        case tsel if tsel and check_mdatt():
                            if stb in markd:
                                match len(mk := self.mdb[stb][1]):
                                    case 1:
                                        self.text.insert(SEL_FIRST, mk[0])
                                        self.text.insert(SEL_LAST, mk[0])
                                    case 2:
                                        self.text.insert(SEL_FIRST, mk[0:])
                                        self.text.insert(SEL_LAST, mk[0:])
                                    case 4:
                                        if "[" in mk:
                                            self.text.insert(SEL_FIRST, mk[:1])
                                            self.text.insert(SEL_LAST, mk[1:])
                                if idx := self.text.search(" ", SEL_LAST, END):
                                    self.text.mark_set("insert", idx)
                                else:
                                    self.text.mark_set("insert", f"{SEL_LAST} lineend")
                                self.text.tag_remove("sel", SEL_FIRST, SEL_LAST)
                                del idx
                        case _:
                            if stb not in markd:
                                if self.text.get(f"{INSERT} - 1c", INSERT).isspace():
                                    self.text.insert(INSERT, self.mdb[stb][1])
                                else:
                                    self.text.insert(INSERT, f" {self.mdb[stb][1]}")

                    self.text.focus()
                    del mk, markd

            @excp(2, DEFAULTFILE)
            def shortcut(event):
                nonlocal stb

                ksm = tuple("QWERTYI")
                ksm = (
                    "exclam",
                    "at",
                    "numbersign",
                    "dollar",
                    "percent",
                    "asciicircum",
                    "ampersand",
                    "asterisk",
                    "parenleft",
                    "parenright",
                ) + ksm
                for k, v in zip(ksm, self.mdb.keys()):
                    if event.keysym == k:
                        stb = v
                        insmd()
                        break
                del ksm

            lmdb = list(self.mdb)
            self.tframe.pack_forget()
            self.fscr.pack_forget()
            self.fframe.pack_forget()

            self.__setattr__("mdframe", None)
            self.frb3.pack(fill=X)
            self.mdframe = ttk.Frame(self.frb3)
            self.mdframe.pack(fill=X, expand=1)

            mdbut = ttk.Button(self.mdframe, text=lmdb[0], width=1, command=insmd)
            mdbut.pack(side=LEFT, padx=2, pady=(0, 2), fill=X, expand=1)
            mdbut.bind("<Enter>", storbut)
            mdbut.bind_all(self.mdb[lmdb[0]][0], shortcut)
            for i in range(1, 17):
                mdbut = ttk.Button(self.mdframe, text=lmdb[i], width=1, command=insmd)
                mdbut.pack(side=LEFT, padx=(0, 2), pady=(0, 2), fill=X, expand=1)
                mdbut.bind("<Enter>", storbut)
                mdbut.bind_all(self.mdb[lmdb[i]][0], shortcut)

            self.tframe.pack(anchor="w", side=TOP, fill="both", expand=1)
            self.tframe.update()
            self.fscr.pack(fill="x")
            self.fscr.update()
            self.fframe.pack(fill="x")
            self.fframe.update()
            del lmdb
        else:
            for i in self.mdframe.winfo_children():
                i.unbind_all(self.mdb[i.cget("text")][0])
                i.unbind("<Enter>")
                i.destroy()
                del i
            self.mdframe.destroy()
            self.__delattr__("mdb")
            self.__delattr__("mdframe")
            self.frb3.pack_forget()

    def _compile_editor(self, rows: int):
        self.store = tuple(i for i in self.text.get("0.0", END)[:-1].split("\n") if i)
        ckc = {f"c{i}": f"child{i}" for i in range(1, 51)}
        compiled = {}
        et = rows
        for i in self.store:
            et += 1
            if "s:" == i.lower()[:2]:
                compiled[et] = ("space", "\n")
            elif "p:" == i.lower()[:2]:
                if i.partition(":")[2].isspace() or not bool(i.partition(":")[2]):
                    raise Exception("Parent cannot be empty!")
                else:
                    compiled[et] = (
                        "parent",
                        i[2:].removeprefix(" "),
                    )
            elif i.lower().partition(":")[0] in list(ckc):
                if i.partition(":")[2].isspace():
                    compiled[et] = (
                        ckc[i.partition(":")[0].lower()],
                        i.partition(":")[2],
                    )
                elif bool(i.partition(":")[2]):
                    compiled[et] = (
                        ckc[i.partition(":")[0].lower()],
                        i.partition(":")[2].removeprefix(" "),
                    )
        if len(self.store) != len(compiled):
            raise Exception("Not Editable!")
        self.store = None
        del ckc
        return compiled, et

    def _check_Totals(self):
        try:
            sumtot = None
            if hasattr(self, "sumtot"):
                sumtot = SumAll(self.filename, sig="+")
                if sumtot.chktot():
                    messagebox.showwarning(
                        "TreeViewGui",
                        "Please delete all 'TOTAL's first",
                        parent=self.root,
                    )
                    return False
                else:
                    return True
            return True
        finally:
            if sumtot:
                del sumtot

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
                if self._check_Totals():
                    self.text.config(state="normal")
                    self.text.delete("1.0", END)
                    ckb = [
                        "Editor",
                        "Template",
                        "Date-Time",
                        "Look Up",
                        "text",
                    ]
                    self.disab(*ckb)
                    self.text.edit_reset()
                    self.text.focus()
                    self._mdbuttons()
                    if not self.plat.startswith("win"):
                        self.root.clipboard_clear()
                    del ckb
            else:
                try:
                    fts = None
                    current_size = self.listb.size()
                    if self.text.count("1.0", END, "chars")[0] > 1:
                        stor = None
                        if self.editorsel or (stor := self.listb.curselection()):
                            stor = (
                                self.editorsel if self.editorsel else (stor[0], stor[0])
                            )
                            p2 = self._compile_editor(stor[0])
                            p1 = None
                            p3 = None
                            with tv(self.filename) as tvg:
                                p1 = islice(tvg.insighttree(), 0, stor[0])
                                if stor[1] <= tvg.getdatanum() - 1:
                                    p3 = islice(
                                        tvg.insighttree(),
                                        stor[1],
                                        tvg.getdatanum(),
                                    )
                                if p3:
                                    p3 = tuple(v for v in dict(p3).values())
                                    p3 = {p2[1] + j + 1: p3[j] for j in range(len(p3))}
                                    combi = iter((dict(p1) | p2[0] | p3).values())
                                else:
                                    combi = iter((dict(p1) | p2[0]).values())
                                tvg.fileread(combi)
                            fts = stor[0]
                            del tvg, p1, p2, combi, p3
                        else:
                            p2 = self._compile_editor(self.listb.size())
                            with tv(self.filename) as tvg:
                                if not self.nonetype():
                                    tvg.fileread(iter(p2[0].values()))
                                else:
                                    combi = iter(
                                        (dict(tvg.insighttree()) | p2[0]).values()
                                    )
                                    tvg.fileread(combi)
                                    del combi
                            del tvg, p2
                        self.text.config(state=DISABLED)
                        self.disab(dis=False)
                        self.spaces()
                        if fts:
                            self._fold_restruct(self.listb.size() - current_size, fts)
                            self.view()
                        del stor, current_size, fts
                        if self.editorsel:
                            self._spot_on(self.editorsel[0])
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
                    self._mdbuttons()
            self.text.edit_reset()
            self.infobar()

    def _fold_restruct(
        self,
        size: int,
        pos: int,
        *,
        row: int = None,
        move: bool = False,
        down: bool = False,
    ):
        pd = ParseData(self.filename, pos, size, data=None)
        if row is None:
            update = pd.update_data()
        else:
            if not move:
                update = pd.update_single_data(row)
            else:
                if down:
                    update = pd.update_move(row, down=down)
                else:
                    update = pd.update_move(row)

        if update:
            with open(self.glop.absolute().joinpath("fold.tvg"), "wb") as cur:
                cur.write(str(update).encode())

        del pd, update

    def tvgexit(self, event=None):
        """Exit mode for TVG and setting everything back to default"""

        if self.FREEZE is False:
            if self.checkfile():
                with open(os.path.join(self.glop.parent, "lastopen.tvg"), "wb") as lop:
                    lop.write(str({"lop": self.filename}).encode())
                if str(self.root.winfo_geometry()) == self.GEO:
                    with open(os.path.join(self.glop.parent, "geo.tvg"), "wb") as geo:
                        geo.write(str({"geo": self.GEO}).encode())
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
                            geo.write(str({"geo": self.GEO}).encode())
                    del ask
                self.addonchk()
            if self.cycle:
                self.root.after_cancel(self.cycle)
            self.__delattr__("bt")
            self.__delattr__("scribe")
            self.__delattr__("addonb")
            self.root.quit()
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

        tlframe = self.tframe.tlframe
        self.listb.destroy()
        self.listb = Listbox(
            tlframe,
            background=self.text["background"],
            foreground=self.text["foreground"],
            font=fon,
            exportselection=False,
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
        del fon, tlframe

    def ft(self, event=None, path=None):
        """Initial starting fonts chooser"""

        if path:
            with open(path) as rd:
                self.clb(rd.read(), wr=False)
        else:
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

        if self.nonetype():
            body = "".join(
                [wrwords(i, 80, 1) + "\n" for i in self._utilspdf().splitlines()]
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
                                for i in self._utilspdf().splitlines()
                            ]
                        )
                    )
                    messagebox.showinfo("TreeViewGui", "Text copied!", parent=self.root)
            else:
                messagebox.showinfo(
                    "TreeViewGui", "Cannot send empty text!", parent=self.root
                )

    def _sumtot_restruct(self, plus: bool = True):
        st = ParseData(self.filename, data=None)
        if update := st.update_data_sum(plus):
            with open(self.glop.absolute().joinpath("fold.tvg"), "wb") as cur:
                cur.write(str(update).encode())
        del st, update

    def gettotsum(self):
        """Get all sums on all parents that have "+" sign in front"""

        if self.nonetype():
            sa = SumAll(self.filename, sig="+")
            match len(sa) > 0:
                case False if hasattr(self, "sumtot"):
                    match os.path.exists(f"{self.filename}_hid.json"):
                        case False:
                            if not hasattr(self, "fold"):
                                self.listb.config(selectmode=MULTIPLE)
                                idx = sa.getidx(False)
                                tot = sa.lumpsum()
                                for i in idx:
                                    self.listb.select_set(i)
                                self.hiddenchl()
                                self.text.config(state=NORMAL)
                                if (
                                    self.text.get(f"{END} - 2 lines", END)
                                    .strip()
                                    .startswith("-TOTAL")
                                ):
                                    self.text.insert(END, f"\nTOTAL SUMS = {tot}")
                                else:
                                    self.text.insert(END, f"TOTAL SUMS = {tot}")
                                self.listb.config(selectmode=BROWSE)
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
                    if not hasattr(self, "sumtot"):
                        self.__setattr__("sumtot", True)
                        sa.sumway()
                        self._sumtot_restruct()
                        self.spaces()
                case False:
                    messagebox.showinfo(
                        "TreeViewGui", "No data to sums!", parent=self.root
                    )
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

        if self.nonetype():
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

        self.hidcheck()
        if self.unlock:
            if self.nonetype():
                with SumAll(self.filename, sig="+") as sal:
                    if hasattr(self, "sumtot") and self.sumtot:
                        self.__delattr__("sumtot")
                        sal.del_total()
                        self._sumtot_restruct(False)
                        self.spaces()
                    else:
                        messagebox.showinfo(
                            "TreeViewGui", "Nothing to delete!", parent=self.root
                        )

    def exprsum(self, event=None):
        """Expression Calculation for Editor mode"""

        if self.lock is False and self.text.cget("state") == NORMAL:
            self.lock = True
            self.FREEZE = True

            err = None
            stor_tuple = tuple()

            @excp(2, DEFAULTFILE)
            def calc(event=None):
                nonlocal err, stor_tuple
                try:
                    if gw := wid.get():
                        if not stor_tuple or gw != stor_tuple[0]:
                            lab["text"] = _ckwrds(gw)
                            if err:
                                err = None
                            stor_tuple = gw, lab["text"]
                        else:
                            lab["text"] = stor_tuple[1]
                        del gw
                    else:
                        raise ValueError("Expression is empty!")
                except Exception as e:
                    if err is None:
                        err = 1
                    messagebox.showerror("Error Message", e)
                    lab.focus()
                    wid.focus()

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
            def insert():
                if isinstance(lab["text"], int | float):
                    calc()
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

            self.__setattr__("labcop", None)
            d = MyDialog(self.root)
            self.lock = False
            self.root.update()
            self.unlock = True
            self.FREEZE = True
            self.__delattr__("labcop")
            del wid, lab, d, err, stor_tuple
        else:
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
            if self.nonetype():
                if not hasattr(self, "fold"):
                    self.__setattr__("fold", True)
                    self.view()
                    self.infobar()

    def _load_selection(self):
        if sels := self._ckfoldtvg():
            for sel in sels:
                self.listb.select_set(sel)

    def _deldatfile(self):
        ParseData(self.filename, data=None).del_data()

    def _deldatt(self, v: bool = True):
        if os.path.exists(self.glop.absolute().joinpath("fold.tvg")):
            os.remove(self.glop.absolute().joinpath("fold.tvg"))
            self._deldatfile()
            if v:
                self.view()
                self.infobar()

    def _noparsp(self, selects: tuple | list):
        accept = []
        if selects:
            for n in selects:
                if self.listb.get(n).partition(" ")[2] not in ["parent", "space"]:
                    accept.append(n)
            del selects
        return tuple(accept)

    def fold_selected(self):
        """Folding selected"""

        self.hidcheck()
        if self.unlock:
            if self.nonetype():
                if self.listb.cget("selectmode") == BROWSE:
                    self.listb.config(selectmode=self.cpp_select)
                    self.disab("Fold selected", "Insight", "listb", "text")
                    self._load_selection()
                    if not hasattr(self, "fold"):
                        self.__setattr__("fold", True)
                else:
                    data = self._noparsp(self.listb.curselection())
                    pd = ParseData(self.filename, data=data if data else None)
                    if data:
                        with open(
                            self.glop.absolute().joinpath("fold.tvg"), "wb"
                        ) as cur:
                            cur.write(str(data).encode())
                        pd.create_data()
                        self.view()
                        self.infobar()
                    else:
                        if self.glop.absolute().joinpath("fold.tvg").exists():
                            if ask := messagebox.askyesno(
                                "TreeViewGui",
                                "Sure to delete selections?",
                                parent=self.root,
                            ):
                                self.__delattr__("fold")
                                self._deldatt()
                    del data, pd
                    self.disab(dis=False)
                    self.listb.selection_clear(0, END)
                    self.listb.config(selectmode=BROWSE)

    def unfolding(self):
        """Unfolding selected and childs"""

        self.hidcheck()
        if self.unlock:
            if self.nonetype():
                if hasattr(self, "fold"):
                    self.__delattr__("fold")
                    self.view()
                    self.infobar()

    def configd(self, event=None):
        """Deleting configuration file to default"""

        if self.lock is False:
            TreeViewGui.FREEZE = True
            self.lock = True

            if self.glop.parent.joinpath("TVG_config.toml").exists():
                with open(self.glop.parent.joinpath("TVG_config.toml")) as rf:
                    cfg = tomlkit.load(rf)

                @excpcls(2, DEFAULTFILE)
                class MyDialog(simpledialog.Dialog):
                    def body(self, master):
                        self.title("Configure TVG")

                        self.fr2 = Frame(master)
                        self.fr2.pack(fill=X, expand=1, pady=(0, 1))
                        Label(self.fr2, text="Select Mode: ").pack(side=LEFT)
                        self.e2 = ttk.Combobox(self.fr2)
                        self.e2["values"] = "extended", "multiple"
                        self.e2.pack(side=RIGHT)
                        self.e2.current(
                            self.e2["values"].index(cfg["Configure"]["SELECT_MODE"])
                        )
                        self.e2.config(state="readonly")

                        self.fr3 = Frame(master)
                        self.fr3.pack(fill=X, expand=1, pady=(0, 1))
                        Label(self.fr3, text="Hidden Opt: ").pack(side=LEFT)
                        self.e3 = ttk.Combobox(self.fr3)
                        self.e3["values"] = "False", "unreverse"
                        self.e3.pack(side=RIGHT)
                        self.e3.current(
                            self.e3["values"].index(str(cfg["Configure"]["HIDDEN_OPT"]))
                        )
                        self.e3.config(state="readonly")

                        self.fr4 = Frame(master)
                        self.fr4.pack(fill=X, expand=1, pady=(0, 1))
                        Label(self.fr4, text="Wrapping: ").pack(side=LEFT)
                        self.e4 = ttk.Combobox(self.fr4)
                        self.e4["values"] = "none", "word"
                        self.e4.pack(side=RIGHT)
                        self.e4.current(
                            self.e4["values"].index(cfg["Configure"]["WRAPPING"])
                        )
                        self.e4.config(state="readonly")

                        self.fr5 = Frame(master)
                        self.fr5.pack(fill=X, expand=1, pady=(0, 1))
                        Label(self.fr5, text="Checked Box: ").pack(side=LEFT)
                        self.e5 = ttk.Combobox(self.fr5)
                        self.e5["values"] = "off", "on"
                        self.e5.pack(side=RIGHT)
                        self.e5.current(
                            self.e5["values"].index(cfg["Configure"]["CHECKED_BOX"])
                        )
                        self.e5.config(state="readonly")
                        return self.e2

                    def apply(self):
                        hid = (
                            ast.literal_eval(self.e3.get())
                            if self.e3.get() == "False"
                            else self.e3.get()
                        )
                        self.result = (
                            self.e2.get(),
                            hid,
                            self.e4.get(),
                            self.e5.get(),
                        )

                d = MyDialog(self.root)
                self.root.update()
                self.lock = False

                if d.result:
                    if tuple(cfg["Configure"].values()) != d.result:
                        global SELECT_MODE, HIDDEN_OPT, WRAPPING, CHECKED_BOX
                        self.cpp_select = SELECT_MODE = d.result[0]
                        self.hidopt = HIDDEN_OPT = d.result[1]
                        if WRAPPING != d.result[2]:
                            self.wrapping = WRAPPING = d.result[2]
                            self.wrapped()
                        self.checked_box = CHECKED_BOX = d.result[3]
                        _create_config(self.glop.parent.joinpath("TVG_config.toml"))
                    else:
                        messagebox.showinfo(
                            "TreeViewGui", "Configuring aborted!", parent=self.root
                        )

            TreeViewGui.FREEZE = False


def _ckwrds(wrd: str):
    try:
        nums = len(wrd)
        values = tuple("0123456789*/-+()%.")
        ck = None

        if nums >= 101:
            raise ValueError(f"{nums} charcters, is exceeding than 100 chars!")

        for i in wrd:
            if i not in values:
                raise ValueError(f"{i!r} is not acceptable expression!")

        ck = EvalExp(wrd, None)
        ck = ck.evlex()
        return ck
    except ValueError:
        raise
    except:
        raise ValueError(f"These expression {wrd!r} are not allowed!")
    finally:
        del wrd, ck, nums, values


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
            self.e1.bind(
                "<KeyRelease>", partial(TreeViewGui.tynam, files=files, ca=False)
            )
            return self.e1

        def apply(self):
            self.result = self.e1.get()

    d = MyDialog(root)
    root.update()
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
def _create_config(pth: str = None):
    """Configuration set according to the user's preference"""

    with open(pth := "TVG_config.toml" if pth is None else pth, "w") as fp:
        tomlkit.dump(
            {
                "Configure": {
                    "SELECT_MODE": SELECT_MODE,
                    "HIDDEN_OPT": HIDDEN_OPT,
                    "WRAPPING": WRAPPING,
                    "CHECKED_BOX": CHECKED_BOX,
                }
            },
            fp,
        )


@excp(m=2, filenm=DEFAULTFILE)
def _load_config():
    """Load configuration"""

    if os.path.exists("TVG_config.toml"):
        global THEME_MODE, SELECT_MODE, HIDDEN_OPT, WRAPPING, CHECKED_BOX
        with open("TVG_config.toml") as rf:
            cfg = tomlkit.load(rf)
        SELECT_MODE = cfg["Configure"]["SELECT_MODE"]
        HIDDEN_OPT = cfg["Configure"]["HIDDEN_OPT"]
        WRAPPING = cfg["Configure"]["WRAPPING"]
        CHECKED_BOX = cfg["Configure"]["CHECKED_BOX"]
        del cfg


@excp(m=2, filenm=DEFAULTFILE)
def titlemode(sent: str):
    try:
        cks = string.printable.partition("!")[0] + "_ "
        j = []
        for st in set(sent):
            if st not in cks:
                return f"Temporer{int(dt.timestamp(dt.today()))}"

        for st in sent.replace("_", " ").split(" "):
            if st.isupper():
                j.append(st)
            else:
                j.append(st.title())
        return " ".join(j)
    finally:
        del cks, j


@excp(m=2, filenm=DEFAULTFILE)
def main():
    """Starting point of running TVG and making directory for non-existing file"""

    findpath()
    _load_config()

    root = Tk()
    root.withdraw()
    # case fontchooser dialog still reacted toward the application sudden exit and cause it to show
    # when application started.
    if root.tk.call("tk", "fontchooser", "configure", "-visible"):
        root.tk.call("tk", "fontchooser", "hide")
        root.update()
    if os.path.exists("lastopen.tvg"):
        ask = messagebox.askyesno("TreeViewGui", "Want to open previous file?")
        root.update()
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
        if not os.path.exists(f"{filename}_tvg"):
            filename = titlemode(filename)
            os.mkdir(f"{filename}_tvg")
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
