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



def region_classify(annee, mois, id_region) :

    conn = sqlite3.connect('data.db')

    query = f"""
        SELECT kpi_ca_reel, kpi_vente_reel, kpi_marge_reel

        FROM (
            SELECT 
                region, 
                
                sum(ca_reel) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(region_sub.ca_reel) DESC) AS kpi_ca_reel,

                sum(vente_reel) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(region_sub.vente_reel) DESC) AS kpi_vente_reel,

                sum(marge_reel) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(region_sub.marge_reel) DESC) AS kpi_marge_reel

                
            
            FROM (
                SELECT *, 'region_1' AS region
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville

                WHERE 
                    villes.lib_departement IN {list_departement_reg_1} AND
                    temps.annee = {annee} AND temps.mois = {mois}

                UNION

                SELECT *, 'region_2' AS region
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville

                WHERE 
                    villes.lib_departement IN {list_departement_reg_2} AND
                    temps.annee = {annee} AND temps.mois = {mois}

                UNION

                SELECT *, 'region_3' AS region
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville

                WHERE 
                    villes.lib_departement IN {list_departement_reg_3} AND
                    temps.annee = {annee} AND temps.mois = {mois}

                UNION

                SELECT *, 'region_4' AS region
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville

                WHERE 
                    villes.lib_departement IN {list_departement_reg_4} AND
                    temps.annee = {annee} AND temps.mois = {mois}

                UNION

                SELECT *, 'region_5' AS region
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville

                WHERE 
                    villes.lib_departement IN {list_departement_reg_5} AND
                    temps.annee = {annee} AND temps.mois = {mois}
                ) region_sub

            GROUP BY region ) sub

        WHERE sub.region = 'region_{id_region}'
    """

    result = pd.read_sql(query, conn).values

    conn.close()

    return result[0]






def region_classify_fam_prod(annee, mois, id_region, id_famille_produit) :

    conn = sqlite3.connect('data.db')

    query = f"""
        SELECT kpi_ca_reel, kpi_vente_reel, kpi_marge_reel

        FROM (
            SELECT 
                region, 
                fam_prod,
                
                sum(ca_reel) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(region_sub.ca_reel) DESC) AS kpi_ca_reel,

                sum(vente_reel) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(region_sub.vente_reel) DESC) AS kpi_vente_reel,

                sum(marge_reel) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(region_sub.marge_reel) DESC) AS kpi_marge_reel
            
            FROM (
                SELECT *, 'region_1' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_1} AND
                    temps.annee = {annee} AND temps.mois = {mois} AND
                    famille_produit.id_famille_produit = {id_famille_produit}

                UNION

                SELECT *, 'region_2' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_2} AND
                    temps.annee = {annee} AND temps.mois = {mois} AND
                    famille_produit.id_famille_produit = {id_famille_produit}

                UNION

                SELECT *, 'region_3' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_3} AND
                    temps.annee = {annee} AND temps.mois = {mois} AND
                    famille_produit.id_famille_produit = {id_famille_produit}

                UNION

                SELECT *, 'region_4' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_4} AND
                    temps.annee = {annee} AND temps.mois = {mois} AND
                    famille_produit.id_famille_produit = {id_famille_produit}
                UNION

                SELECT *, 'region_5' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_5} AND
                    temps.annee = {annee} AND temps.mois = {mois} AND
                    famille_produit.id_famille_produit = {id_famille_produit}
                ) region_sub

            GROUP BY region ) sub

            WHERE 
            sub.region = 'region_{id_region}'

    """

    result = pd.read_sql(query, conn).values

    conn.close()

    return result[0]





def region_classify_cumul(annee, mois, id_region) :

    conn = sqlite3.connect('data.db')

    query = f"""
        SELECT kpi_ca_reel, kpi_vente_reel, kpi_marge_reel

        FROM (
            SELECT 
                region, 
                
                sum(ca_reel) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(region_sub.ca_reel) DESC) AS kpi_ca_reel,

                sum(vente_reel) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(region_sub.vente_reel) DESC) AS kpi_vente_reel,

                sum(marge_reel) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(region_sub.marge_reel) DESC) AS kpi_marge_reel

                
            
            FROM (
                SELECT *, 'region_1' AS region
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville

                WHERE 
                    villes.lib_departement IN {list_departement_reg_1} AND
                    temps.annee = {annee} AND temps.mois <= {mois}

                UNION

                SELECT *, 'region_2' AS region
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville

                WHERE 
                    villes.lib_departement IN {list_departement_reg_2} AND
                    temps.annee = {annee} AND temps.mois <= {mois}

                UNION

                SELECT *, 'region_3' AS region
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville

                WHERE 
                    villes.lib_departement IN {list_departement_reg_3} AND
                    temps.annee = {annee} AND temps.mois <= {mois}

                UNION

                SELECT *, 'region_4' AS region
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville

                WHERE 
                    villes.lib_departement IN {list_departement_reg_4} AND
                    temps.annee = {annee} AND temps.mois <= {mois}

                UNION

                SELECT *, 'region_5' AS region
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville

                WHERE 
                    villes.lib_departement IN {list_departement_reg_5} AND
                    temps.annee = {annee} AND temps.mois <= {mois}
                ) region_sub

            GROUP BY region ) sub

        WHERE sub.region = 'region_{id_region}'
    """

    result = pd.read_sql(query, conn).values

    conn.close()

    return result[0]




def region_classify_fam_prod_cumul(annee, mois, id_region, id_famille_produit) :

    conn = sqlite3.connect('data.db')

    query = f"""
        SELECT kpi_ca_reel, kpi_vente_reel, kpi_marge_reel

        FROM (
            SELECT 
                region, 
                fam_prod,
                
                sum(ca_reel) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(region_sub.ca_reel) DESC) AS kpi_ca_reel,

                sum(vente_reel) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(region_sub.vente_reel) DESC) AS kpi_vente_reel,

                sum(marge_reel) AS kpi_sales,
                RANK () OVER ( ORDER BY sum(region_sub.marge_reel) DESC) AS kpi_marge_reel
            
            FROM (
                SELECT *, 'region_1' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_1} AND
                    temps.annee = {annee} AND temps.mois <= {mois} AND
                    famille_produit.id_famille_produit = {id_famille_produit}

                UNION

                SELECT *, 'region_2' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_2} AND
                    temps.annee = {annee} AND temps.mois <= {mois} AND
                    famille_produit.id_famille_produit = {id_famille_produit}

                UNION

                SELECT *, 'region_3' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_3} AND
                    temps.annee = {annee} AND temps.mois <= {mois} AND
                    famille_produit.id_famille_produit = {id_famille_produit}

                UNION

                SELECT *, 'region_4' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_4} AND
                    temps.annee = {annee} AND temps.mois <= {mois} AND
                    famille_produit.id_famille_produit = {id_famille_produit}
                UNION

                SELECT *, 'region_5' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_5} AND
                    temps.annee = {annee} AND temps.mois <= {mois} AND
                    famille_produit.id_famille_produit = {id_famille_produit}
                ) region_sub

            GROUP BY region ) sub

            WHERE 
            sub.region = 'region_{id_region}'

    """

    result = pd.read_sql(query, conn).values

    conn.close()

    return result[0]




def hist_indicator_reg(indicator, annee, mois, lib_famille_produit, region_id):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT sum({}) 
        
        FROM sales
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN villes ON villes.id_ville = sales.id_ville
        
        WHERE 
            temps.annee = {} AND
            temps.mois = '{}' AND
            famille_produit.lib_famille_produit = '{}' AND
            villes.lib_departement in {};
    """
    indic = pd.read_sql(query.format(indicator, annee, mois, lib_famille_produit, reg_id_to_name[region_id]), conn).values[0][0]
    conn.close()

    return indic




def hist_indicator_cumul_reg(indicator, annee, mois, lib_famille_produit, region_id):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT sum({}) 
        
        FROM sales
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN villes ON villes.id_ville = sales.id_ville
        
        WHERE 
            temps.annee = {} AND
            temps.mois <= '{}' AND
            famille_produit.lib_famille_produit = '{}' AND
            villes.lib_departement in {};
    """
    indic = pd.read_sql(query.format(indicator, annee, mois, lib_famille_produit, reg_id_to_name[region_id]), conn).values[0][0]
    conn.close()

    return indic




def hist_indicator_cumul_reg(indicator, annee, mois, lib_famille_produit, region_id):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT sum({}) 
        
        FROM sales
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN villes ON villes.id_ville = sales.id_ville
        
        WHERE 
            temps.annee = {} AND
            temps.mois <= '{}' AND
            famille_produit.lib_famille_produit = '{}' AND
            villes.lib_departement in {};
    """
    indic = pd.read_sql(query.format(indicator, annee, mois, lib_famille_produit, reg_id_to_name[region_id]), conn).values[0][0]
    conn.close()

    return indic




def hist_cumul_reg(annee, mois, region_id):
    hifi_obj = hist_indicator_cumul_reg('ca_objectif', annee, mois, 'hifi', region_id)
    hifi_reel = hist_indicator_cumul_reg('ca_reel', annee, mois, 'hifi', region_id)

    magneto_obj = hist_indicator_cumul_reg('ca_objectif', annee, mois, 'magneto', region_id)
    magneto_reel = hist_indicator_cumul_reg('ca_reel', annee, mois, 'magneto', region_id)

    fours_obj = hist_indicator_cumul_reg('ca_objectif', annee, mois, 'fours', region_id)
    fours_reel = hist_indicator_cumul_reg('ca_reel', annee, mois, 'fours', region_id)

    return {
        "hifi_obj_cumul" : hifi_obj,
        "hifi_reel_cumul" : hifi_reel,
        "magneto_obj_cumul" : magneto_obj,
        "magneto_reel_cumul" : magneto_reel,
        "fours_obj_cumul" : fours_obj,
        "fours_reel_cumul" : fours_reel
    }




def hist_reg(annee, mois, region_id):
    hifi_obj = hist_indicator_reg('ca_objectif', annee, mois, 'hifi', region_id)
    hifi_reel = hist_indicator_reg('ca_reel', annee, mois, 'hifi', region_id)

    magneto_obj = hist_indicator_reg('ca_objectif', annee, mois, 'magneto', region_id)
    magneto_reel = hist_indicator_reg('ca_reel', annee, mois, 'magneto', region_id)

    fours_obj = hist_indicator_reg('ca_objectif', annee, mois, 'fours', region_id)
    fours_reel = hist_indicator_reg('ca_reel', annee, mois, 'fours', region_id)

    return {
        "hifi_obj" : hifi_obj,
        "hifi_reel" : hifi_reel,
        "magneto_obj" : magneto_obj,
        "magneto_reel" : magneto_reel,
        "fours_obj" : fours_obj,
        "fours_reel" : fours_reel
    }




def details_indicators_reg(annee, mois, region_id):
    conn = sqlite3.connect('data.db')

    kpis = ["ca_objectif", "ca_reel", "ventes_objectif", "vente_reel", "marge_objectif", "marge_reel"]

    query = """
        SELECT sum({}), sum({}) , sum({}), sum({}), sum({}) , sum({})
        
        FROM sales
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        JOIN villes ON villes.id_ville = sales.id_ville
        
        WHERE 
            temps.annee = {} AND
            temps.mois = {} AND
            famille_produit.lib_famille_produit = '{}' AND
            villes.lib_departement in {};
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
        'hifi', 
        reg_id_to_name[region_id]
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
        'fours', 
        reg_id_to_name[region_id]
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
        'magneto', 
        reg_id_to_name[region_id]
    ), conn).values[0]
    magneto_kpi = dict(zip(kpis, magneto_kpi_result))

    conn.close()

    return {
        "hifi_kpi" : hifi_kpi,
        "fours_kpi" : fours_kpi,
        "magneto_kpi" : magneto_kpi
    }




def palmares_indicators_reg(annee, mois, classement, region_id):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT 
            magasin.lib_magasin, 
            sum(ca_objectif) AS ca_objectif, 
            sum(ca_reel) AS ca_reel, 
            sum(ventes_objectif) AS ventes_objectif, 
            sum(vente_reel) AS vente_reel, 
            sum(marge_objectif) AS marge_objectif, 
            sum(marge_reel) AS marge_reel
        
        FROM sales
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN magasin ON sales.id_magasin = magasin.id_magasin
        JOIN villes ON villes.id_ville = sales.id_ville

        WHERE 
            temps.annee = {0} AND
            temps.mois = {1}  AND
            villes.lib_departement in {3}
            
        GROUP BY magasin.lib_magasin
        
        ORDER BY {2} DESC;
    """

    indicators = pd.read_sql(query.format(annee, mois, classement, reg_id_to_name[region_id]), conn).values

    conn.close()

    return {
        "indicators" : indicators
    }




def palmares_indicators_region_reg(annee, mois, classement, list_departement_reg, region_id):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT 
            magasin.lib_magasin, 
            sum(ca_objectif) AS ca_objectif, 
            sum(ca_reel) AS ca_reel, 
            sum(ventes_objectif) AS ventes_objectif, 
            sum(vente_reel) AS vente_reel, 
            sum(marge_objectif) AS marge_objectif, 
            sum(marge_reel) AS marge_reel
        
        FROM sales
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN magasin ON sales.id_magasin = magasin.id_magasin
        JOIN villes ON sales.id_ville = villes.id_ville

        WHERE 
            temps.annee = {0} AND
            temps.mois = {1} AND
            villes.lib_departement IN {3}
            
        GROUP BY magasin.lib_magasin
        
        ORDER BY {2} DESC;
    """

    indicators = pd.read_sql(query.format(annee, mois, classement, list_departement_reg), conn).values

    conn.close()

    return indicators
