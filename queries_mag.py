import sqlite3
import pandas as pd
from config import *


def all_magasin_in_region(id_region) :
    conn = sqlite3.connect('data.db')

    query = """
        SELECT * 
        
        FROM magasin
        JOIN villes ON villes.lib_ville = magasin.lib_magasin

        WHERE villes.lib_departement in {}
        ;
    """
    magasins = pd.read_sql(query.format(reg_id_to_name[id_region]), conn).values

    conn.close()

    return magasins





def region_containing(id_mag) :
    conn = sqlite3.connect('data.db')

    query = """
        SELECT lib_departement 
        
        FROM magasin
        JOIN villes ON villes.lib_ville = magasin.lib_magasin

        WHERE magasin.id_magasin = {}
        ;
    """
    lib_departement = ''
    result = pd.read_sql(query.format(id_mag), conn).values
    conn.close()
    if len(result) > 0 :
        lib_departement = result[0][0]
    

    if lib_departement in dep_reg_1 : return 1
    if lib_departement in dep_reg_2 : return 2
    if lib_departement in dep_reg_3 : return 3
    if lib_departement in dep_reg_4 : return 4
    if lib_departement in dep_reg_5 : return 5

    return 0






def performances_magasin(annee, mois_int, id_mag):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT 
            sum(ca_objectif), sum(ca_reel), 
            sum(ventes_objectif), sum(vente_reel), 
            sum(marge_objectif), sum(marge_reel)
        
        FROM sales
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN villes ON sales.id_ville = villes.id_ville
        JOIN magasin ON magasin.lib_magasin = villes.lib_ville
        
        WHERE 
            temps.annee = {} AND
            temps.mois = {} AND
            magasin.id_magasin = {};
    """
    result = pd.read_sql(query.format(annee, mois_int, id_mag), conn).values
    conn.close()
    

    if len(result) > 0:
        if result[0][0] :
            return result[0]

    return [0.01, 0, 0.01, 0, 0.01, 0]




def performances_magasin_item(annee, mois_int, id_mag, id_famille_produit) :
    conn = sqlite3.connect('data.db')

    query = """
        SELECT 
            sum(ca_objectif), sum(ca_reel), 
            sum(ventes_objectif), sum(vente_reel), 
            sum(marge_objectif), sum(marge_reel)
        
        FROM sales
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN villes ON sales.id_ville = villes.id_ville
        JOIN magasin ON magasin.lib_magasin = villes.lib_ville
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        
        WHERE 
            temps.annee = {} AND
            temps.mois = {} AND
            magasin.id_magasin = {} AND
            famille_produit.id_famille_produit = {};
    """
    result = pd.read_sql(query.format(annee, mois_int, id_mag, id_famille_produit), conn).values
    conn.close()

    if len(result) > 0:
        if result[0][0] :
            return result[0]

    return [0.01, 0, 0.01, 0, 0.01, 0]




def mag_name(id_mag) :
    conn = sqlite3.connect('data.db')

    query = """
        SELECT lib_magasin
        
        FROM magasin 
        
        WHERE 
            magasin.id_magasin = {};
    """
    result = pd.read_sql(query.format(id_mag), conn).values
    conn.close()

    if len(result) > 0:
        return result[0][0]

    return result



def nat_rank_mag(id_mag, classifier, annee, mois) :
    conn = sqlite3.connect('data.db')

    query = """
        SELECT 
            id_mag, lib_ville, kpi_rank
        
        FROM (
            SELECT 
                villes.lib_ville AS lib_ville,
                magasin.id_magasin AS id_mag,
                sum(sales.{0}) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(sales.{0}) DESC) AS kpi_rank
                

            FROM
                sales
                JOIN temps ON sales.id_temps = temps.id_temps
                JOIN villes ON sales.id_ville = villes.id_ville
                JOIN magasin ON magasin.lib_magasin = villes.lib_ville

            WHERE 
                temps.annee = {1} AND
                temps.mois = {2}
            
            GROUP BY villes.lib_ville
            ) innner

        WHERE
            innner.id_mag = {3}
        ;
    """

    formated_query = query.format(classifier, annee, mois, id_mag)

    result = pd.read_sql(formated_query, conn).values
    conn.close()

    if len(result) > 0:
        return result[0][2]

    return result





def nat_rank_mag_item(id_mag, classifier, annee, mois, id_famille_produit) :
    conn = sqlite3.connect('data.db')

    query = """
    SELECT v, RANK () OVER (  ORDER BY {}) rank_no 
    
    FROM
        sales.rank_demo;
    """

    query = """
        SELECT 
            RANK () OVER (  ORDER BY sum({})) rank_no

            sum(ca_objectif), sum({}), 
            sum(ventes_objectif), sum(vente_reel), 
            sum(marge_objectif), sum(marge_reel)
        
        FROM sales
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN villes ON sales.id_ville = villes.id_ville
        JOIN magasin ON magasin.lib_magasin = villes.lib_ville
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        
        WHERE 
            temps.annee = {} AND
            temps.mois = {} AND
            magasin.id_magasin = {} AND
            famille_produit.id_famille_produit = {};
    """

    query = """
        SELECT 
            id_mag, lib_ville, kpi_rank
        
        FROM (
            SELECT 
                villes.lib_ville AS lib_ville,
                magasin.id_magasin AS id_mag,
                sum(sales.{0}) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(sales.{0}) DESC) AS kpi_rank
                

            FROM
                sales
                JOIN temps ON sales.id_temps = temps.id_temps
                JOIN villes ON sales.id_ville = villes.id_ville
                JOIN magasin ON magasin.lib_magasin = villes.lib_ville
                JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

            WHERE 
                temps.annee = {1} AND
                temps.mois = {2} AND
                famille_produit.id_famille_produit = {4}
            
            GROUP BY villes.lib_ville
            ) innner

        WHERE
            innner.id_mag = {3}
        ;
    """

    result = pd.read_sql(query.format(classifier, annee, mois, id_mag, id_famille_produit), conn).values
    conn.close()

    if len(result) > 0:
        return result[0][2]

    return result
