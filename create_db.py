import sqlite3


def create_ville() :
    conn = sqlite3.connect('data.db')
    c = conn.cursor()    

    create_villes_query = """
        CREATE TABLE IF NOT EXISTS technos (
            id_techno integer,
            name text,
            type text
        )
    """

    c.execute(create_villes_query)
    conn.commit()
    conn.close()

    print('end create_tables')


def create_tables() :
    conn = sqlite3.connect('developpers.db')
    c = conn.cursor()

    conn = sqlite3.connect('developpers.db')
    c = conn.cursor()

    create_technos_query = """
        CREATE TABLE IF NOT EXISTS technos (
            id_techno integer,
            name text,
            type text
        )
    """

    c.execute(create_developpers_query)
    c.execute(create_technos_query)

    conn.commit()
    conn.close()

    print('end create_tables')


def delete_all() :
    
    conn = sqlite3.connect('developpers.db')
    c = conn.cursor()

    c.execute("DROP TABLE developpers;")
    c.execute("DROP TABLE technos;")

    conn.commit()
    conn.close()

    print('end delete_all')





def populate_tables() :
    conn = sqlite3.connect('developpers.db')
    c = conn.cursor()
    
    developpers = [
        ('julie', 'garandet', 1, 7),
        ('mathieux', 'bordet', 'react', 10),
        ('julien', 'ducros', 3, 5),
        ('valentine', 'penicaud', 2, 5),
        ('marc', 'sanders', 1, 15)
    ]
    insert_developpers_qry = """
        INSERT INTO developpers VALUES (?, ?, ?, ?)
    """
    c.executemany(insert_developpers_qry, developpers)

    technos = [
        (1, 'node.js', 'web'),
        (2, 'react native', 'mobile'),
        (3, 'java', 'web'),
        (4, 'swift', 'mobile')
    ]
    insert_technos_qry = """
        INSERT INTO technos VALUES (?, ?, ?)
    """    
    c.executemany(insert_technos_qry, technos)

    conn.commit()
    conn.close()

    print('end populate_tables')



def show_tables():
    
    conn = sqlite3.connect('developpers.db')
    c = conn.cursor()

    c.execute("SELECT * FROM developpers WHERE first_name = 'alessio';" )
    results = c.fetchall()
    print(results)


    c.execute("SELECT * FROM technos;" )
    results = c.fetchall()
    print(results)

    conn.commit()
    conn.close()







if __name__ == "__main__":

    create_ville()

