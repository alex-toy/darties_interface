import sqlite3
import pandas as pd


def test():
    query = f"""
        SELECT * FROM sales;
    """
    conn = sqlite3.connect('data.db')
    df = pd.read_sql(query, conn)

    print(df)

    return 10

