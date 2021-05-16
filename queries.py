import sqlite3
import pandas as pd



def performances_nationales(annee):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT sum({}) 
        
        FROM sales
        JOIN temps ON sales.id_temps = temps.id_temps
        
        WHERE temps.annee = '{}';
    """
    ca_obj = pd.read_sql(query.format('ca_objectif', annee), conn).values[0][0]
    ca_reel = pd.read_sql(query.format('ca_reel', annee), conn).values[0][0]
    ventes_objectif = pd.read_sql(query.format('ventes_objectif', annee), conn).values[0][0]
    vente_reel = pd.read_sql(query.format('vente_reel', annee), conn).values[0][0]
    marge_objectif = pd.read_sql(query.format('marge_objectif', annee), conn).values[0][0]
    marge_reel = pd.read_sql(query.format('marge_reel', annee), conn).values[0][0]

    conn.close()

    return {
        "ca_obj" : ca_obj,
        "ca_reel" : ca_reel,
        "ventes_objectif" : ventes_objectif,
        "vente_reel" : vente_reel,
        "marge_objectif" : marge_objectif,
        "marge_reel" : marge_reel
    }




def performances_region(annee, list_departement):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT sum({}) 
        
        FROM sales
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN villes ON sales.id_ville = villes.id_ville
        
        WHERE 
            temps.annee = '{}' AND
            villes.lib_departement IN {};
    """
    ca_obj = pd.read_sql(query.format('ca_objectif', annee, list_departement), conn).values[0][0]
    ca_reel = pd.read_sql(query.format('ca_reel', annee, list_departement), conn).values[0][0]
    ventes_objectif = pd.read_sql(query.format('ventes_objectif', annee, list_departement), conn).values[0][0]
    vente_reel = pd.read_sql(query.format('vente_reel', annee, list_departement), conn).values[0][0]
    marge_objectif = pd.read_sql(query.format('marge_objectif', annee, list_departement), conn).values[0][0]
    marge_reel = pd.read_sql(query.format('marge_reel', annee, list_departement), conn).values[0][0]

    conn.close()

    return {
        "ca_obj" : ca_obj,
        "ca_reel" : ca_reel,
        "ventes_objectif" : ventes_objectif,
        "vente_reel" : vente_reel,
        "marge_objectif" : marge_objectif,
        "marge_reel" : marge_reel
    }



