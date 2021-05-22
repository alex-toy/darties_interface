import sqlite3


def create_ville() :
    conn = sqlite3.connect('data.db')
    c = conn.cursor()    

    create_villes_query = """
        CREATE TABLE IF NOT EXISTS villes (
            id_ville integer,
            lib_ville text,
            lib_continent text,
            lib_pays text,
            lib_departement text,
            lib_reg_anc text,
            lib_reg_nouv text
        )
    """
    c.execute(create_villes_query)


    myfile = open("data/ville_000.csv", "r")
    records = myfile.readlines()
    myfile.close()

    villes = [
        ( 
            int(record[:-1].split('|')[0]),
            record[:-1].split('|')[1],
            record[:-1].split('|')[2],
            record[:-1].split('|')[3],
            record[:-1].split('|')[4],
            record[:-1].split('|')[5],
            record[:-1].split('|')[6],
        )
        for record in records
    ]

    insert_villes_qry = """
        INSERT INTO villes VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    c.executemany(insert_villes_qry, villes)
    conn.commit()
    conn.close()
    print('end create_ville')




def create_sales() :
    conn = sqlite3.connect('data.db')
    c = conn.cursor()    

    create_query = """
        CREATE TABLE IF NOT EXISTS sales (
            id_ville integer,
            id_temps integer,
            id_famille_produit integer,
            id_magasin integer,
            ventes_objectif float,
            vente_reel float,
            ca_objectif float,
            ca_reel float,
            marge_objectif float,
            marge_reel float
        )
    """
    c.execute(create_query)


    myfile = open("data/sales_000.csv", "r")
    records = myfile.readlines()
    myfile.close()


    records_list = [
        ( 
            int(record[:-1].split('|')[0]),
            int(record[:-1].split('|')[1]),
            int(record[:-1].split('|')[2]),
            int(record[:-1].split('|')[3]),
            float(record[:-1].split('|')[4]),
            float(record[:-1].split('|')[5]) if len(record[:-1].split('|')[5]) > 0 else 0,
            float(record[:-1].split('|')[6]),
            float(record[:-1].split('|')[7]) if len(record[:-1].split('|')[5]) > 0 else 0,
            float(record[:-1].split('|')[8]),
            float(record[:-1].split('|')[9]) if len(record[:-1].split('|')[5]) > 0 else 0,
        )
        for record in records
    ]

    insert_qry = """
        INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    c.executemany(insert_qry, records_list)
    conn.commit()
    conn.close()
    print('end create_sales')



def create_temps() :
    conn = sqlite3.connect('data.db')
    c = conn.cursor()    

    create_query = """
        CREATE TABLE IF NOT EXISTS temps (
            id_temps integer,
            annee integer,
            semestre integer,
            trimestre integer,
            mois integer,
            lib_mois text
        )
    """
    c.execute(create_query)


    myfile = open("data/temps_000.csv", "r")
    records = myfile.readlines()
    myfile.close()


    records_list = [
        ( 
            int(record[:-1].split('|')[0]),
            int(record[:-1].split('|')[1]),
            int(record[:-1].split('|')[2]),
            int(record[:-1].split('|')[3]),
            int(record[:-1].split('|')[4]),
            record[:-1].split('|')[5]
        )
        for record in records
    ]

    insert_qry = """
        INSERT INTO temps VALUES (?, ?, ?, ?, ?, ?)
    """
    c.executemany(insert_qry, records_list)
    conn.commit()
    conn.close()
    print('end create_temps')





def create_magasin() :
    conn = sqlite3.connect('data.db')
    c = conn.cursor()    

    create_query = """
        CREATE TABLE IF NOT EXISTS magasin (
            id_magasin integer,
            lib_magasin text,
            id_enseigne integer
        )
    """
    c.execute(create_query)

    myfile = open("data/magasin_000.csv", "r")
    records = myfile.readlines()
    myfile.close()

    records_list = [
        ( 
            int(record[:-1].split('|')[0]),
            record[:-1].split('|')[1],
            int(record[:-1].split('|')[2])
        )
        for record in records
    ]

    insert_qry = """
        INSERT INTO magasin VALUES (?, ?, ?)
    """
    c.executemany(insert_qry, records_list)
    conn.commit()
    conn.close()
    print('end create_magasin')





def create_famille_produit() :
    conn = sqlite3.connect('data.db')
    c = conn.cursor()    

    create_query = """
        CREATE TABLE IF NOT EXISTS famille_produit (
            id_famille_produit integer,
            lib_famille_produit text
        )
    """
    c.execute(create_query)

    myfile = open("data/famille_produit_000.csv", "r")
    records = myfile.readlines()
    myfile.close()

    records_list = [
        ( 
            int(record[:-1].split('|')[0]),
            record[:-1].split('|')[1]
        )
        for record in records
    ]

    insert_qry = """
        INSERT INTO famille_produit VALUES (?, ?)
    """
    c.executemany(insert_qry, records_list)
    conn.commit()
    conn.close()
    print('end create_famille_produit')



def create_devise() :
    conn = sqlite3.connect('data.db')
    c = conn.cursor()    

    create_query = """
        CREATE TABLE IF NOT EXISTS devise (
            id_devise integer,
            lib_devise text
        )
    """
    c.execute(create_query)

    myfile = open("data/devise_000.csv", "r")
    records = myfile.readlines()
    myfile.close()

    records_list = [
        ( 
            int(record[:-1].split('|')[0]),
            record[:-1].split('|')[1]
        )
        for record in records
    ]

    insert_qry = """
        INSERT INTO devise VALUES (?, ?)
    """
    c.executemany(insert_qry, records_list)
    conn.commit()
    conn.close()
    print('end create_devise')



def create_cours() :
    conn = sqlite3.connect('data.db')
    c = conn.cursor()    

    create_query = """
        CREATE TABLE IF NOT EXISTS cours (
            id_cours integer,
            mois integer,
            annee integer,
            cours_rate
        )
    """
    c.execute(create_query)

    myfile = open("data/cours_000.csv", "r")
    records = myfile.readlines()
    myfile.close()

    records_list = [
        ( 
            int(record[:-1].split('|')[0]),
            int(record[:-1].split('|')[1]),
            int(record[:-1].split('|')[2]),
            float(record[:-1].split('|')[3])
        )
        for record in records
    ]

    insert_qry = """
        INSERT INTO cours VALUES (?, ?, ?, ?)
    """
    c.executemany(insert_qry, records_list)
    conn.commit()
    conn.close()
    print('end create_cours')




def delete_all() :
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute("DROP TABLE villes;")
    c.execute("DROP TABLE sales;")
    c.execute("DROP TABLE temps;")
    c.execute("DROP TABLE magasin;")
    c.execute("DROP TABLE famille_produit;")
    c.execute("DROP TABLE cours;")
    c.execute("DROP TABLE devise;")
    

    conn.commit()
    conn.close()

    print('end delete_all')







def show_tables(table_name):
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute(f"SELECT * FROM {table_name};" )
    results = c.fetchall()
    print(results)

    conn.commit()
    conn.close()







if __name__ == "__main__":

    delete_all()

    create_ville()

    create_sales()

    create_temps()

    create_magasin()

    create_famille_produit()

    create_devise()

    create_cours()

    show_tables('cours')

