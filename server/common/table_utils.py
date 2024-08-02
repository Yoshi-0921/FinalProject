import sqlite3
from datetime import datetime
from typing import List

from config import SQLITE_PATH, TODAY


def get_table_columns(table_name: str) -> List[str]:
    with sqlite3.connect(SQLITE_PATH) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cur.description]

        return columns

def convert_ts(timestamp: int) -> int:
    dt = get_date(timestamp)
    dt = dt.replace(hour=9, minute=0, second=0)
    ts = get_timestamp(dt)
    return ts

def get_date(timestamp: int) -> datetime:
    dt = datetime.fromtimestamp(timestamp)
    return dt

def get_timestamp(datetime: datetime) -> int:
    ts = int(round(datetime.timestamp()))
    return ts


if __name__ == "__main__":
    # ts = convert_ts(1690945011)
    dt = get_date(1690945011)
    print(dt)
    ts = get_timestamp(datetime(2023,8,2,9,0,0))
    print(ts)
    ts = get_timestamp(TODAY)
    print(ts)