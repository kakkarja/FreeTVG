# -*- coding: utf-8 -*-
# Copyright (c) 2023, KarjaKAK
# All rights reserved.

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Generator

from sqlmodel import Field, Session, SQLModel, create_engine, select


class BibleDataBase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book: str = Field(index=True)
    chapter: int = Field(index=True)
    from_: int = Field(index=True)
    to_: int = Field(index=True)


@dataclass(slots=True, frozen=True)
class DatabaseBibleTVG:
    """DataBase for Bible TVG using SQLModel"""

    filename: str
    sqlite_url: str = field(init=False)
    engine: Any = field(init=False)

    def __post_init__(self) -> None:
        super(DatabaseBibleTVG, self).__setattr__("sqlite_url", f"sqlite:///{self.filename}.db")
        super(DatabaseBibleTVG, self).__setattr__("engine", create_engine(self.sqlite_url))

    def create_db_tables(self) -> None:
        """Initialize DataBase"""

        SQLModel.metadata.create_all(self.engine)

    def insert_data(self, data: BibleDataBase) -> None:
        """Saving data to DataBase including fold if any"""

        with Session(self.engine) as session:
            session.add(data)
            session.commit()
        del data, session

    def total_records(self) -> int:
        """Getting total records number"""

        with Session(self.engine) as session:
            result = session.exec(select(BibleDataBase.id))
            if result:
                return len(result.all())
            else:
                return 0

    def get_data(self, row: int) -> BibleDataBase | None:
        """Get data individually"""

        with Session(self.engine) as session:
            result = session.get(BibleDataBase, row)
            return result

    def get_firstid(self) -> int | None:
        """Get the first id number"""

        with Session(self.engine) as session:
            result = session.exec(select(BibleDataBase.id))
            if result := result.all():
                return result[0]

    def delete_data(self, row: int) -> None:
        """Delete a data and update the IDs"""

        with Session(self.engine) as session:
            result = session.get(BibleDataBase, row)
            session.delete(result)
            session.commit()
        del result, session
        self.resetting_id(row)

    def resetting_id(self, row: int) -> None:
        """Resetting IDs"""

        with Session(self.engine) as session:
            results = session.exec(
                select(BibleDataBase).where(BibleDataBase.id > row)
            )
            for tvg in results:
                tvg.id -= 1
                session.add(tvg)
            session.commit()
        del results, session
    
    def select_datas(self) -> Generator:
        "Getting all datas"

        with Session(self.engine) as session:
            results = session.exec(select(BibleDataBase)).all()
            if results:
                return (r.model_dump(exclude={"id"}) for r in results)
        del session, result
    
    def validity_data(self, data: BibleDataBase) -> bool:
        "To validate data if already exist"

        with Session(self.engine) as session:
            result = session.exec(
                select(BibleDataBase)
                    .where(BibleDataBase.book == data.book)
                    .where(BibleDataBase.chapter == data.chapter)
                    .where(BibleDataBase.from_ == data.from_)
                    .where(BibleDataBase.to_ == data.to_)
            )
            collect = [d for d in result]
            del data, result
            if collect:
                del collect
                return True
            else:
                return False

    def check_dbfile(self) -> bool:
        """Checking data base file existence"""

        if Path(f"{self.filename}.db").exists():
            return True
        else:
            return False


# path that has .json ext
def update_database(path: str):
    if Path(path).exists():
        with open(path) as datas:
            tk = json.load(datas)
            db = DatabaseBibleTVG(str(path).rpartition(".")[0])
            for i in tk["history"]:
                b = BibleDataBase(
                    book=i["book"],
                    chapter=int(i["chapter"]),
                    from_=int(i["from"]),
                    to_=int(i["to"])
                )
                if not db.validity_data(b):
                    db.insert_data(b)
                    print(f"Update: {b}")
            else:
                print("updated! (please delete the file)")

# path that ommited the ext
def checking_update(path: str):
    db = DatabaseBibleTVG(path)
    datas = db.select_datas()
    n = 0
    for i in datas:
        n += 1
        print("No.", n, i)
