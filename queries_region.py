import sqlite3
import pandas as pd
from config import *


def all_magasin_in_region(id_region) :
    conn = sqlite3.connect('data.db')

    query = """
        SELECT * 
        
        FROM magasin
        JOIN villes ON villes.lib_ville = magasin.lib_magasin

        WHERE villes.lib_departement in {};
    """
    magasins = pd.read_sql(query.format(reg_id_to_name[id_region]), conn).values

    conn.close()

    return magasins



