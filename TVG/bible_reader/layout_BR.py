# -*- coding: utf-8 -*-
# Copyright (c) 2023, KarjaKAK
# All rights reserved.

import json
from pathlib import Path
from sys import platform
from tkinter import Frame, Label, Text, simpledialog, ttk, messagebox

from .bible_creator import DEFAULT_PATH, BibleProduceData

from pathlib import Path


class BibleReader(simpledialog.Dialog):
    """Bible Reader"""

    def __init__(
        self,
        parent,
        title=None,
        book=None,
        chapter=None,
        _from=None,
        _to=None,
        alt_path=None, 
        bpath=DEFAULT_PATH,
    ) -> None:
        self.book = book
        self.chapter = chapter
        self._from = _from
        self._to = _to
        self.br = BibleProduceData(bpath)
        self.altpath = None
        if alt_path:
            self.altpath = Path(alt_path).parent.joinpath(
                f"history_{Path(bpath).name.partition(".")[0]}.json"
            )
        self.record = None
        super().__init__(parent=parent, title=title)

    def body(self, master):
        self.title("Bible Reader")
        self.frame_main = Frame(master)
        self.frame_main.pack(fill="both", expand=True)

        by4 = 750 // 45
        self.frame_labels = Frame(self.frame_main)
        self.frame_labels.pack(fill="x", expand=True)

        self.frame_lab1 = Frame(self.frame_labels)
        self.frame_lab1.pack(side="left", fill="x", expand=True)
        self.lab1 = Label(self.frame_lab1, text="Book", width=by4, justify="center")
        self.lab1.pack(fill="both")

        self.frame_lab2 = Frame(self.frame_labels)
        self.frame_lab2.pack(side="left", fill="x", expand=True)
        self.lab2 = Label(self.frame_lab2, text="Chapters", width=by4, justify="center")
        self.lab2.pack(fill="both")

        self.frame_lab3 = Frame(self.frame_labels)
        self.frame_lab3.pack(side="left", fill="x", expand=True)
        self.lab3 = Label(
            self.frame_lab3, text="From Verse", width=by4, justify="center"
        )
        self.lab3.pack(fill="both")

        self.frame_lab4 = Frame(self.frame_labels)
        self.frame_lab4.pack(side="left", fill="x", expand=True)
        self.lab4 = Label(self.frame_lab4, text="To Verse", width=by4, justify="center")
        self.lab4.pack(fill="both")

        self.frame_entryb = Frame(self.frame_main)
        self.frame_entryb.pack(fill="both", expand=True)

        self.frame_entry1 = Frame(self.frame_entryb)
        self.frame_entry1.pack(side="left", fill="both", expand=True)
        self.combobox1 = ttk.Combobox(self.frame_entry1, width=by4, justify="center")
        self.combobox1.pack(padx=(2, 0), fill="both")
        self.combobox1["value"] = list(self.br.bible_books())
        self.combobox1.current(0)
        self.combobox1.bind("<<ComboboxSelected>>", self.book_selected)

        self.frame_entry2 = Frame(self.frame_entryb)
        self.frame_entry2.pack(side="left", fill="both", expand=True)
        self.combobox2 = ttk.Combobox(self.frame_entry2, width=by4, justify="center")
        self.combobox2.pack(padx=(2, 0), fill="both")
        self.combobox2.bind("<<ComboboxSelected>>", self.chapter_selected)

        self.frame_entry3 = Frame(self.frame_entryb)
        self.frame_entry3.pack(side="left", fill="both", expand=True)
        self.combobox3 = ttk.Combobox(self.frame_entry3, width=by4, justify="center")
        self.combobox3.pack(padx=(2, 0), fill="both")
        self.combobox3.bind("<<ComboboxSelected>>", self.fromverse_selected)

        self.frame_entry4 = Frame(self.frame_entryb)
        self.frame_entry4.pack(side="left", fill="both", expand=True)
        self.combobox4 = ttk.Combobox(self.frame_entry4, width=by4, justify="center")
        self.combobox4.pack(padx=(2, 2), fill="both")
        self.combobox4.bind("<<ComboboxSelected>>", self.display_verses)

        self.frame_text = Frame(self.frame_main)
        self.frame_text.pack(pady=(3, 0), side="left", fill="both", expand=True)
        self.scroll = ttk.Scrollbar(self.frame_text, orient="vertical")
        self.text = Text(
            self.frame_text,
            font="verdana 10 bold" if platform.startswith("win") else "verdana 12 bold",
            wrap="word",
            yscrollcommand=self.scroll.set,
        )
        self.scroll["command"] = self.text.yview
        self.scroll.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.text.configure(state="disabled")

        self.frame_entry5 = Frame(master)
        self.frame_entry5.pack(side="bottom")
        
        button_add = ttk.Button(
            self.frame_entry5, text="Add", width=10, command=self.create_history, default="active"
        )
        button_add.pack(side="left", padx=(2, 0), pady=(2,0), fill="x")

        self.combobox5 = ttk.Combobox(self.frame_entry5, width=by4, justify="center", state="readonly",)
        self.combobox5.pack(side="left", padx=(2, 2), pady=(2, 0), fill="x")
        self.combobox5.bind("<<ComboboxSelected>>", self.history_choose) 

        button_del = ttk.Button(
            self.frame_entry5, text="Remove", width=10, command=self.history_delete, default="active"
        )
        button_del.pack(side="right", padx=(0, 2), pady=(2,0), fill="x")


        self._read_only()
        if self._checker():
            self.start_record()
        else:
            self.book_selected()
        self._reload_history()

    def _checker(self):
        r = self.book, self.chapter, self._from, self._to
        if all(r):
            return True
        return False

    def start_record(self):
        """Saved record  will be display at start"""

        self.combobox1.current(self.combobox1["value"].index(self.book))
        chp = self.br.chapters(self.combobox1.get())
        self.bible_selection_range(chp=chp)
        _, verses = self.br.verses(self.combobox1.get(), int(self.combobox2.get()))
        self.bible_selection_range(ver=verses)
        del chp, verses
        self.display_verses()

    def _combo4(self, ver: int, skip: bool = False):
        self.combobox4["value"] = [
            i + 1 for i in range(int(self.combobox3.get()) - 1, ver)
        ]
        match skip:
            case False if self._to:
                self.combobox4.current(self.combobox4["value"].index(self._to))
                self._to = None
            case False:
                self.combobox4.current(len(self.combobox4["value"]) - 1)
            case True:
                self.combobox4.current(self.combobox4["value"].index(self.combobox4.get()))



    def bible_selection_range(self, /, chp: int = None, ver: int = None, skip: bool = False):
        if chp:
            self.combobox2["value"] = [i + 1 for i in range(chp)]
            if self.chapter:
                self.combobox2.current(self.combobox2["value"].index(self.chapter))
                self.chapter = None
            else:
                self.combobox2.current(0)
        elif ver:
            if not skip:
                self.combobox3["value"] = [i + 1 for i in range(ver)]
                if self._from:
                    self.combobox3.current(self.combobox3["value"].index(self._from))
                    self._from = None
                else:
                    self.combobox3.current(0)
                self._combo4(ver)
            else:
                if int(self.combobox3.get()) > int(self.combobox4.get()):
                    self._combo4(ver)
                else:
                    self._combo4(ver, skip)                

    def book_selected(self, event=None):
        """Event for bible Book selected"""

        if self.combobox1.get():
            chp = self.br.chapters(self.combobox1.get())
            self.bible_selection_range(chp=chp)
            _, verses = self.br.verses(self.combobox1.get(), int(self.combobox2.get()))
            self.bible_selection_range(ver=verses)
            del chp, verses
            self.display_verses()

    def chapter_selected(self, event=None):
        """Event for Chapter selected"""

        if self.combobox2.get():
            _, verses = self.br.verses(self.combobox1.get(), int(self.combobox2.get()))
            self.bible_selection_range(ver=verses)
            del verses
            self.display_verses()

    def fromverse_selected(self, event=None):
        """Event for selected verse"""

        if self.combobox3.get():
            _, verses = self.br.verses(self.combobox1.get(), int(self.combobox2.get()))
            self.bible_selection_range(ver=verses, skip=True)
            del verses
            self.display_verses()

    def _read_only(self):
        list_combo = [
            self.combobox1, self.combobox2, self.combobox3, self.combobox4
        ]
        for combo in list_combo:
            if combo["state"] != "readonly":
                combo.configure(state="readonly")
        del list_combo

    def _text_state(self, _state: bool = True):
        if _state:
            self.text.configure(state="disabled")
        else:
            self.text.configure(state="normal")

    def display_verses(self, event=None):
        """Event for displaying Verses"""

        self._text_state(False)
        self.text.delete("1.0", "end")
        txt = self.br.reader_verses(
            self.combobox1.get(),
            int(self.combobox2.get()),
            int(self.combobox3.get()),
            int(self.combobox4.get()),
        )
        for tx in txt:
            self.text.insert("end", f"{tx}\n\n")
        self._text_state()
        del txt

    def _record(self, combo=True) -> dict[str, str]:
        """Record state of display"""

        if combo:
            return {
                "book": self.combobox1.get(),
                "chapter": self.combobox2.get(),
                "from": self.combobox3.get(),
                "to": self.combobox4.get(),
            }
        else:
            if self._checking_history():
                select = {}
                book = chapter = _from = _to = ""
                selection = self.combobox5.get().partition(":")
                book, _, chapter = selection[0].rpartition(" ")
                if "-" in selection[2]:
                    _from, _, _to = selection[2].partition("-")
                else:
                    _from = _to = selection[2]
                select["book"] = book
                select["chapter"] = chapter
                select["from"] = _from
                select["to"] = _to
                del book, chapter, _from, _to, selection
                return select
    
    def _bible_verses_format(self, dform: dict[str,str]) -> str:
        if int(dform["from"]) < int(dform["to"]):
            return f"{dform['book']} {dform['chapter']}:{dform['from']}-{dform['to']}"
        else:
            return f"{dform['book']} {dform['chapter']}:{dform['from']}"
    
    def _checking_history(self) -> bool:
       if self.altpath:
            return self.altpath.exists()
    
    def _compile_history_record(self) -> dict[str,list[dict]]:
        return {"history":[self._record()]}
    
    def create_history(self, event=None):
        if not self._checking_history():
            with open(self.altpath, "w") as record:
                json.dump(self._compile_history_record(), record)
        else:
            with open(self.altpath, "r") as record:
                history_rec = json.load(record)
                update = self._record()
            if update not in history_rec["history"]:
                with open(self.altpath, "w") as record:
                    history_rec["history"].append(update)
                    json.dump(history_rec, record)
            del history_rec, update, record
        self._reload_history()

    def _reload_history(self):
        if self._checking_history():
            update = []
            with open(self.altpath, "r") as record:
                history_rec = json.load(record)
                for rec in history_rec["history"]:
                    update.append(self._bible_verses_format(dform=rec))
                del history_rec
            update.reverse()
            self.combobox5["state"] = "normal"
            self.combobox5["value"] = update
            self.combobox5.current(0)
            self.combobox5["state"] = "readonly"
            del update, record
    
    def _combobox_state_value(self):
        cb = (self.combobox1, self.combobox2, self.combobox3, self.combobox4)
        for c in range(len(cb)):
            cb[c]["state"] = "normal"
            if c != 0:
                cb[c]["value"] = []
        del cb

    def history_choose(self, event=None):
        selection = self._record(False)
        setting_book = self.br.book_chap_verse_nums(selection["book"], int(selection["chapter"]))
        self._combobox_state_value()
        self.combobox1.current(
            self.combobox1["value"].index(selection["book"])
        )
        self.combobox2["value"] = [
            str(ch + 1) for ch in range(setting_book[selection["book"]][0])
        ]
        self.combobox2.current(
            self.combobox2["value"].index(selection["chapter"])
        )
        self.combobox3["value"] = [
            str(ch + 1) for ch in range(setting_book[selection["book"]][1])
        ]
        self.combobox3.current(
            self.combobox3["value"].index(selection["from"])
        )
        self.combobox4["value"] = [
            ch for ch in self.combobox3["value"][int(selection["from"]) - 1:] 
        ]
        self.combobox4.current(
            self.combobox4["value"].index(selection["to"])
        )
        self._read_only()
        self.display_verses()
        del selection, setting_book
    
    def history_delete(self, event=None):
        if self._checking_history():
            update = self._record(combo=False)
            msg = "\n" + self._bible_verses_format(dform=update)
            if ask := messagebox.askyesno(
                "Bible Reader", 
                f"Do you want to delete {msg} ?",
                parent=self.master
            ):
                with open(self.altpath, "r") as record:
                    history_rec = json.load(record)
                    history_rec["history"].remove(update)
                with open(self.altpath, "w") as record:
                    json.dump(history_rec, record)
                self._reload_history()
                if update == self._record():
                    self.history_choose()
                del history_rec, record
            del update, msg
            self.focus()

    def apply(self) -> None:
        verse_to_verse = (
            f"{self.combobox3.get()}-{self.combobox4.get()}" 
            if int(self.combobox4.get()) > int(self.combobox3.get()) 
            else f"{self.combobox3.get()}"
        )
        header = (
            f"{self.combobox1.get()} "
            f"{self.combobox2.get()}:{verse_to_verse} ({Path(self.br.xml_path).name.rpartition(".")[0]})\n"
        )
        n = 0
        self.result = (
            header
            + "".join(
                [tx[tx.find(" ") :] for tx in self.text.get("1.0", "end").split("\n\n")]
            )[1:-1]
        ), self._record()
        del header, verse_to_verse

    def buttonbox(self):
        box = Frame(self)

        w = ttk.Button(box, text="Journal", width=10, command=self.ok, default="active")
        w.pack(side="left", padx=5, pady=5)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side="left", padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self, event=None):
        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()

    def cancel(self, event=None):
        self.record = self._record()
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()
