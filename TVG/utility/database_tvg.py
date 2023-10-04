# -*- coding: utf-8 -*-
# Copyright (c) 2023, KarjaKAK
# All rights reserved.

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select
from treeview import TreeView


class TreeViewGuiDataBase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: str
    fold: Optional[str] = None


@dataclass(slots=True, frozen=True)
class DatabaseTVG(TreeView):
    """DataBase for TVG using SQLModel"""

    filename: str
    sqlite_url: str = field(init=False)
    engine: Any = field(init=False)

    def __post_init__(self) -> None:
        if not (filename := self.findext()):
            raise FileExistsError(f"This {self.filename!r} is not exist!")
        super(TreeView, self).__setattr__("filename", filename)
        super(DatabaseTVG, self).__setattr__("sqlite_url", f"sqlite:///{filename}.db")
        super(DatabaseTVG, self).__setattr__("engine", create_engine(self.sqlite_url))

    def findext(self) -> str | None:
        """Checker file path existence with TreeView format file."""

        match Path(self.filename):
            case pt if pt.exists() and ".txt" in pt.name:
                return str(pt.absolute())[:-4]
            case pt if os.path.exists(f"{pt.absolute()}.txt"):
                return str(pt.absolute())
            case _:
                return None

    def create_db_tables(self) -> None:
        """Initialize DataBase"""

        SQLModel.metadata.create_all(self.engine)

    def insert_data(self, fold: tuple[int] = None) -> None:
        """Saving data to DataBase including fold if any"""

        data = f"{tuple(self.compdatch(True))}"
        fold = f"{fold}" if fold else fold
        with Session(self.engine) as session:
            session.add(TreeViewGuiDataBase(data=data, fold=fold))
            session.commit()
        del data, fold, session

    def total_records(self) -> int:
        """Getting total records number"""

        with Session(self.engine) as session:
            result = session.exec(select(TreeViewGuiDataBase.id))
            if result:
                return len(result.all())
            else:
                return 0

    def get_data(self, row: int) -> TreeViewGuiDataBase | None:
        """Get data individually"""

        with Session(self.engine) as session:
            result = session.get(TreeViewGuiDataBase, row)
            return result

    def get_firstid(self) -> int | None:
        """Get the first id number"""

        with Session(self.engine) as session:
            result = session.exec(select(TreeViewGuiDataBase.id))
            if result := result.all():
                return result[0]

    def delete_data(self, row: int) -> None:
        """Delete a data and update the IDs"""

        with Session(self.engine) as session:
            result = session.get(TreeViewGuiDataBase, row)
            session.delete(result)
            session.commit()
        del result, session
        self.resetting_id(row)

    def resetting_id(self, row: int) -> None:
        """Resetting IDs"""

        with Session(self.engine) as session:
            results = session.exec(
                select(TreeViewGuiDataBase).where(TreeViewGuiDataBase.id > row)
            )
            for tvg in results:
                tvg.id -= 1
                session.add(tvg)
            session.commit()
        del results, session

    def check_dbfile(self) -> bool:
        """Checking data base file existence"""

        if Path(f"{self.filename}.db").exists():
            return True
        else:
            return False
