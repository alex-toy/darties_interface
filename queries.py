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



def hist_indicator(indicator, annee, mois, lib_famille_produit):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT sum({}) 
        
        FROM sales
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        JOIN temps ON sales.id_temps = temps.id_temps
        
        WHERE 
            temps.annee = {} AND
            temps.mois = '{}' AND
            famille_produit.lib_famille_produit = '{}';
    """
    indic = pd.read_sql(query.format(indicator, annee, mois, lib_famille_produit), conn).values[0][0]
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



def hist(annee, mois):
    hifi_obj = hist_indicator('ca_objectif', annee, mois, 'hifi')
    hifi_reel = hist_indicator('ca_reel', annee, mois, 'hifi')

    magneto_obj = hist_indicator('ca_objectif', annee, mois, 'magneto')
    magneto_reel = hist_indicator('ca_reel', annee, mois, 'magneto')

    fours_obj = hist_indicator('ca_objectif', annee, mois, 'fours')
    fours_reel = hist_indicator('ca_reel', annee, mois, 'fours')

    return {
        "hifi_obj" : hifi_obj,
        "hifi_reel" : hifi_reel,
        "magneto_obj" : magneto_obj,
        "magneto_reel" : magneto_reel,
        "fours_obj" : fours_obj,
        "fours_reel" : fours_reel
    }




def hist_cumul(annee, mois):
    hifi_obj = hist_indicator_cumul('ca_objectif', annee, mois, 'hifi')
    hifi_reel = hist_indicator_cumul('ca_reel', annee, mois, 'hifi')

    magneto_obj = hist_indicator_cumul('ca_objectif', annee, mois, 'magneto')
    magneto_reel = hist_indicator_cumul('ca_reel', annee, mois, 'magneto')

    fours_obj = hist_indicator_cumul('ca_objectif', annee, mois, 'fours')
    fours_reel = hist_indicator_cumul('ca_reel', annee, mois, 'fours')

    return {
        "hifi_obj_cumul" : hifi_obj,
        "hifi_reel_cumul" : hifi_reel,
        "magneto_obj_cumul" : magneto_obj,
        "magneto_reel_cumul" : magneto_reel,
        "fours_obj_cumul" : fours_obj,
        "fours_reel_cumul" : fours_reel
    }




def details_indicators(annee, mois):
    conn = sqlite3.connect('data.db')

    kpis = ["ca_objectif", "ca_reel", "ventes_objectif", "vente_reel", "marge_objectif", "marge_reel"]

    query = """
        SELECT sum({}) 
        
        FROM sales
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        
        WHERE 
            temps.annee = {} AND
            temps.mois = {} AND
            famille_produit.lib_famille_produit = '{}';
    """
    hifi_ca_obj = pd.read_sql(query.format('ca_objectif', annee, mois, 'hifi'), conn).values[0][0]
    hifi_ca_reel = pd.read_sql(query.format('ca_reel', annee, mois, 'hifi'), conn).values[0][0]
    hifi_ventes_obj = pd.read_sql(query.format('ventes_objectif', annee, mois, 'hifi'), conn).values[0][0]
    hifi_ventes_reel = pd.read_sql(query.format('vente_reel', annee, mois, 'hifi'), conn).values[0][0]
    hifi_marge_obj = pd.read_sql(query.format('marge_objectif', annee, mois, 'hifi'), conn).values[0][0]
    hifi_marge_reel = pd.read_sql(query.format('marge_reel', annee, mois, 'hifi'), conn).values[0][0]
    
    fours_ca_obj = pd.read_sql(query.format('ca_objectif', annee, mois, 'fours'), conn).values[0][0]
    fours_ca_reel = pd.read_sql(query.format('ca_reel', annee, mois, 'fours'), conn).values[0][0]
    fours_ventes_obj = pd.read_sql(query.format('ventes_objectif', annee, mois, 'fours'), conn).values[0][0]
    fours_ventes_reel = pd.read_sql(query.format('vente_reel', annee, mois, 'fours'), conn).values[0][0]
    fours_marge_obj = pd.read_sql(query.format('marge_objectif', annee, mois, 'fours'), conn).values[0][0]
    fours_marge_reel = pd.read_sql(query.format('marge_reel', annee, mois, 'fours'), conn).values[0][0]

    query = """
        SELECT sum({}), sum({}) , sum({}), sum({}), sum({}) , sum({})
        
        FROM sales
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        
        WHERE 
            temps.annee = {} AND
            temps.mois = {} AND
            famille_produit.lib_famille_produit = '{}';
    """

    hifi_kpi_result = pd.read_sql(query.format(
        'ca_objectif', 
        'ca_reel',
        'ventes_objectif',
        'vente_reel', 
        'marge_objectif',
        'marge_reel',
        annee, 
        mois, 
        'hifi'
    ), conn).values[0]
    hifi_kpi = dict(zip(kpis, hifi_kpi_result))

    fours_kpi_result = pd.read_sql(query.format(
        'ca_objectif', 
        'ca_reel',
        'ventes_objectif',
        'vente_reel', 
        'marge_objectif',
        'marge_reel',
        annee, 
        mois, 
        'fours'
    ), conn).values[0]
    fours_kpi = dict(zip(kpis, fours_kpi_result))
    
    magneto_kpi_result = pd.read_sql(query.format(
        'ca_objectif', 
        'ca_reel',
        'ventes_objectif',
        'vente_reel', 
        'marge_objectif',
        'marge_reel',
        annee, 
        mois, 
        'magneto'
    ), conn).values[0]
    magneto_kpi = dict(zip(kpis, magneto_kpi_result))

    conn.close()

    return {
        "hifi_ca_obj" : hifi_ca_obj,
        "hifi_ca_reel" : hifi_ca_reel,
        "hifi_ventes_obj" : hifi_ventes_obj,
        "hifi_ventes_reel" : hifi_ventes_reel,
        "hifi_marge_obj" : hifi_marge_obj,
        "hifi_marge_reel" : hifi_marge_reel,

        "fours_ca_obj" : fours_ca_obj,
        "fours_ca_reel" : fours_ca_reel,
        "fours_ventes_obj" : fours_ventes_obj,
        "fours_ventes_reel" : fours_ventes_reel,
        "fours_marge_obj" : fours_marge_obj,
        "fours_marge_reel" : fours_marge_reel,

        "hifi_kpi" : hifi_kpi,
        "fours_kpi" : fours_kpi,
        "magneto_kpi" : magneto_kpi
    }

