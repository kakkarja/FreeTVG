# -*- coding: utf-8 -*-
# Copyright (c) 2023, KarjaKAK
# All rights reserved.

from pathlib import Path
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generator, LiteralString

import xmltodict

DEFAULT_PATH = Path(__file__).parent.joinpath(".Bible", "KJV.xml")

@dataclass(frozen=True, slots=True)
class BibleProduceData:
    """Produce Bible from XML file"""

    xml_path: str = field(default=DEFAULT_PATH)

    def __post_init__(self) -> None:
        if not Path(self.xml_path).exists():
            raise FileNotFoundError(f"\"{self.xml_path}\" is not exist!")

    def bible_books(self) -> Generator:
        """Books' Names"""

        try:
            books = []
            with open(self.xml_path) as x:
                for book in xmltodict.parse(x.read(), xml_attribs=True)["XMLBIBLE"]["BIBLEBOOK"]:
                    books.append(book["@bname"])
            return (i for i in books)
        except:
            raise ValueError("Invalid type of data!")
        finally:
            del books
    
    def bible_data(self) -> Generator:
        """Books' Datas"""

        try:
            books_data = {}
            with open(self.xml_path) as x:
                for book in xmltodict.parse(x.read(), xml_attribs=True)["XMLBIBLE"]["BIBLEBOOK"]:
                    if isinstance(book["CHAPTER"], list):
                        books_data[book["@bname"]] = book["CHAPTER"]
                    else:
                        books_data[book["@bname"]] = [book["CHAPTER"]]
            return ((k, v) for k, v in books_data.items())
        except:
            raise ValueError("Invalid type of data!")
        finally:
            del books_data
    
    def _inspect_book(self, book: str) -> str | bool:
        """Inspect the book title"""

        for i in self.bible_books():
            if i == book:
                return book
        else:
            return False
    
    def chapters(self, book: str) -> int | None:
        """Get Book's chapter"""

        inspect = self._inspect_book(book)
        if isinstance(inspect, str):
            for k, v in self.bible_data():
                if k == inspect:
                    return len(v)
        else:
            raise NameError("Invalid type of Book!")
        
    def verses(self, book: str, chapter: int) -> tuple[int,int] | None:
        """Get Book's chapter and total verses"""

        try:
            chp = self.chapters(book)
            for k, v in self.bible_data():
                    if k == book:
                        if chapter <= chp:
                            return chapter, len(v[chapter - 1]["VERS"])
                        else:
                            raise ValueError("Book's chapter is invalid!")
        except Exception as e:
            raise e

    def reader(self, book: str, chapter: int, vnumber: bool = True) -> LiteralString:
        """Bible Verses according to Chapter"""

        try:
            texts = []
            chp = self.chapters(book)
            for k, v in self.bible_data():
                    if k == book:
                        if chapter <= chp:
                            for verse in v[chapter - 1]["VERS"]:
                                if vnumber:
                                    texts.append(f"[{verse["@vnumber"]}] {verse["#text"]}")
                                else:
                                    texts.append(f"{verse["#text"]}")
                        else:
                            raise ValueError("Book's chapter is invalid!")
                    if texts:
                        break
            return " ".join(texts)
        except Exception as e:
            raise e
        finally:
            del texts
    
    def reader_verses(self, book: str, chapter: int, verse: int, toverse: int = 0, /, vnumber: bool = True) -> list:
        """Bible Verses according to verse/s selection"""

        try:
            texts = []
            chp, vrs = self.verses(book=book, chapter=chapter)
            for k, v in self.bible_data():
                    if k == book:
                        if chapter <= chp and verse <= vrs:
                            if toverse and toverse > verse and toverse <= vrs:
                                for vr in v[chapter - 1]["VERS"]:
                                    if verse <= int(vr["@vnumber"]) <= toverse:
                                        if vnumber:
                                            texts.append(f"[{vr["@vnumber"]}] {vr["#text"]}")
                                        else:
                                            texts.append(f"{vr["#text"]}")
                            else:
                                if vnumber:
                                    texts.append(
                                        f"[{v[chapter - 1]["VERS"][verse - 1]["@vnumber"]}] "
                                        f"{v[chapter - 1]["VERS"][verse - 1]["#text"]}"
                                    )
                                else:
                                    texts.append(f"{v[chapter - 1]["VERS"][verse - 1]["#text"]}")
                        else:
                            raise ValueError("Book's chapter/verse is invalid!")
                    if texts:
                        break
            return texts
        except Exception as e:
            raise e
        finally:
            del texts
