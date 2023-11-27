# -*- coding: utf-8 -*-
# Copyright (c) 2023, KarjaKAK
# All rights reserved.

from tkinter import ttk, simpledialog, Frame, Label, Text
from .bible_creator import BibleProduceData, DEFAULT_PATH


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
        bpath=DEFAULT_PATH,
    ) -> None:
        self.book = book
        self.chapter = chapter
        self._from = _from
        self._to = _to
        self.br = BibleProduceData(bpath)
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
            font="verdana 12 bold",
            wrap="word",
            yscrollcommand=self.scroll.set,
        )
        self.scroll["command"] = self.text.yview
        self.scroll.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.text.configure(state="disabled")

        self._read_only()
        if self._checker():
            self.start_record()
        else:
            self.book_selected()

    def _checker(self):
        r = self.book, self.chapter, self._from, self._to
        if all(r):
            return True
        return False

    def start_record(self):
        """Saved record  will be display at start"""
        self.combobox1.current(self.combobox1["value"].index(self.book))
        chp = self.br.chapters(self.combobox1.get())
        self.combobox2["value"] = [i + 1 for i in range(chp)]
        self.combobox2.current(self.combobox2["value"].index(self.chapter))
        _, verses = self.br.verses(self.combobox1.get(), int(self.combobox2.get()))
        self.combobox3["value"] = [i + 1 for i in range(verses)]
        self.combobox3.current(self.combobox3["value"].index(self._from))
        self.combobox4["value"] = [
            i + 1 for i in range(int(self.combobox3.get()) - 1, verses)
        ]
        self.combobox4.current(self.combobox4["value"].index(self._to))
        del chp, verses
        self.display_verses()

    def book_selected(self, event=None):
        """Event for bible Book selected"""

        if self.combobox1.get():
            chp = self.br.chapters(self.combobox1.get())
            self.combobox2["value"] = [i + 1 for i in range(chp)]
            self.combobox2.current(0)
            _, verses = self.br.verses(self.combobox1.get(), int(self.combobox2.get()))
            self.combobox3["value"] = [i + 1 for i in range(verses)]
            self.combobox3.current(0)
            self.combobox4["value"] = [
                i + 1 for i in range(int(self.combobox3.get()) - 1, verses)
            ]
            self.combobox4.current(len(self.combobox4["value"]) - 1)
            del chp, verses
            self.display_verses()

    def chapter_selected(self, event=None):
        """Event for Chapter selected"""

        if self.combobox2.get():
            _, verses = self.br.verses(self.combobox1.get(), int(self.combobox2.get()))
            self.combobox3["value"] = [i + 1 for i in range(verses)]
            self.combobox3.current(0)
            self.combobox4["value"] = [
                i + 1 for i in range(int(self.combobox3.get()) - 1, verses)
            ]
            self.combobox4.current(len(self.combobox4["value"]) - 1)
            del verses
            self.display_verses()

    def fromverse_selected(self, event=None):
        """Event for selected verse"""

        if self.combobox3.get():
            _, verses = self.br.verses(self.combobox1.get(), int(self.combobox2.get()))
            self.combobox4["value"] = [
                i + 1 for i in range(int(self.combobox3.get()) - 1, verses)
            ]
            self.combobox4.current(len(self.combobox4["value"]) - 1)
            del verses
            self.display_verses()

    def _read_only(self):
        if self.combobox1["state"] != "readonly":
            self.combobox1.configure(state="readonly")
        if self.combobox2["state"] != "readonly":
            self.combobox2.configure(state="readonly")
        if self.combobox3["state"] != "readonly":
            self.combobox3.configure(state="readonly")
        if self.combobox4["state"] != "readonly":
            self.combobox4.configure(state="readonly")

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

    def _record(self) -> dict[str, str]:
        """Record state of display"""

        return {
            "book": self.combobox1.get(),
            "chapter": self.combobox2.get(),
            "from": self.combobox3.get(),
            "to": self.combobox4.get(),
        }

    def apply(self) -> None:
        header = (
            f"{self.combobox1.get()} "
            f"{self.combobox2.get()}:{self.combobox3.get()}-{self.combobox4.get()}\n"
        )
        n = 0
        self.result = (
            header
            + "".join(
                [tx[tx.find(" ") :] for tx in self.text.get("1.0", "end").split("\n\n")]
            )[1:-1]
        ), self._record()
        del header

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
