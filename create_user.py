import sqlite3


def create_admin() :
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()    

    create_villes_query = """
        CREATE TABLE IF NOT EXISTS admin (
            id integer,
            email text,
            password text,
            name text
        )
    """
    c.execute(create_villes_query)

    records = [
        (1, 'alexei.80@hotmail.fr', 'mypwd', 'alex')
    ]

    insert_records_qry = """
        INSERT INTO admin VALUES (?, ?, ?, ?)
    """
    c.executemany(insert_records_qry, records)
    conn.commit()
    conn.close()
    print('end create_admin')




def delete_all() :
    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute("DROP TABLE admin;")
    

    conn.commit()
    conn.close()

    print('end delete_all')







def show_tables(table_name):
    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(f"SELECT * FROM {table_name};" )
    results = c.fetchall()
    print(results)

    conn.commit()
    conn.close()



def show():
    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(".database" )
    results = c.fetchall()
    print(results)

    c.execute(".tables" )
    results = c.fetchall()
    print(results)

    conn.commit()
    conn.close()







if __name__ == "__main__":

    #delete_all()

    #create_admin()

    #show_tables('admin')

    show()

