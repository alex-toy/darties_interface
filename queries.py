import sqlite3
import pandas as pd



def performances_nationales(annee):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT sum({}) 
        
        FROM sales
        JOIN temps ON sales.id_temps = temps.id_temps
        
        WHERE temps.annee = {};
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
            temps.annee = {} AND
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



def hist_indicator(indicator, annee, lib_mois, lib_famille_produit):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT sum({}) 
        
        FROM sales
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        JOIN temps ON sales.id_temps = temps.id_temps
        
        WHERE 
            temps.annee = {} AND
            temps.lib_mois = '{}' AND
            famille_produit.lib_famille_produit = '{}';
    """
    indic = pd.read_sql(query.format(indicator, annee, lib_mois, lib_famille_produit), conn).values[0][0]
    conn.close()

    return indic



def hist_indicator_cumul(indicator, annee, mois, lib_famille_produit):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT sum({}) 
        
        FROM sales
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        JOIN temps ON sales.id_temps = temps.id_temps
        
        WHERE 
            temps.annee = {} AND
            temps.mois <= '{}' AND
            famille_produit.lib_famille_produit = '{}';
    """
    indic = pd.read_sql(query.format(indicator, annee, mois, lib_famille_produit), conn).values[0][0]
    conn.close()

    return indic



def hist(annee, lib_mois):
    hifi_prev = hist_indicator('ca_objectif', annee, lib_mois, 'hifi')
    hifi_reel = hist_indicator('ca_reel', annee, lib_mois, 'hifi')

    magneto_prev = hist_indicator('ca_objectif', annee, lib_mois, 'magneto')
    magneto_reel = hist_indicator('ca_reel', annee, lib_mois, 'magneto')

    fours_prev = hist_indicator('ca_objectif', annee, lib_mois, 'fours')
    fours_reel = hist_indicator('ca_reel', annee, lib_mois, 'fours')

    return {
        "hifi_prev" : hifi_prev,
        "hifi_reel" : hifi_reel,
        "magneto_prev" : magneto_prev,
        "magneto_reel" : magneto_reel,
        "fours_prev" : fours_prev,
        "fours_reel" : fours_reel
    }




def hist_cumul(annee, mois):
    hifi_prev = hist_indicator_cumul('ca_objectif', annee, mois, 'hifi')
    hifi_reel = hist_indicator_cumul('ca_reel', annee, mois, 'hifi')

    magneto_prev = hist_indicator_cumul('ca_objectif', annee, mois, 'magneto')
    magneto_reel = hist_indicator_cumul('ca_reel', annee, mois, 'magneto')

    fours_prev = hist_indicator_cumul('ca_objectif', annee, mois, 'fours')
    fours_reel = hist_indicator_cumul('ca_reel', annee, mois, 'fours')

    return {
        "hifi_prev_cumul" : hifi_prev,
        "hifi_reel_cumul" : hifi_reel,
        "magneto_prev_cumul" : magneto_prev,
        "magneto_reel_cumul" : magneto_reel,
        "fours_prev_cumul" : fours_prev,
        "fours_reel_cumul" : fours_reel
    }