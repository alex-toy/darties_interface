import sqlite3
import pandas as pd
from config import *
from distance import levenshtein


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

        WHERE magasin.id_magasin = {};
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

    return None




def similarity(my_string1, my_string2):
    return levenshtein(my_string1, my_string2)




def region_containing_sim(id_mag) :
    conn = sqlite3.connect('data.db')
    conn.create_function("SIMILARITY", 2, similarity)

    magasin_name = mag_name(id_mag)

    query = f"""
        SELECT lib_departement 

        FROM villes

        ORDER BY SIMILARITY(lib_departement,'{magasin_name}') DESC
        
        LIMIT 1
    """
    
    result = pd.read_sql(query, conn).values
    if len(result) > 0 :
        lib_departement = result[0][0]

    if lib_departement in dep_reg_1 : return 1
    if lib_departement in dep_reg_2 : return 2
    if lib_departement in dep_reg_3 : return 3
    if lib_departement in dep_reg_4 : return 4
    if lib_departement in dep_reg_5 : return 5

    return None




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





def reg_rank_mag(id_mag, classifier, annee, mois) :
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
                temps.mois = {2} AND
                villes.lib_departement IN {4}
            
            GROUP BY villes.lib_ville
            ) innner

        WHERE
            innner.id_mag = {3}
        ;
    """

    
    reg_containing = region_containing(id_mag) if region_containing(id_mag) else region_containing_sim(id_mag)

    formated_query = query.format(classifier, annee, mois, id_mag, reg_id_to_name[reg_containing])

    result = pd.read_sql(formated_query, conn).values
    conn.close()

    if len(result) > 0:
        return result[0][2]

    return result




def reg_rank_mag_item(id_mag, classifier, annee, mois, id_famille_produit) :
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
                JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

            WHERE 
                temps.annee = {1} AND
                temps.mois = {2} AND
                villes.lib_departement IN {4} AND
                famille_produit.id_famille_produit = {5}
            
            GROUP BY villes.lib_ville
            ) innner

        WHERE
            innner.id_mag = {3}
        ;
    """

    reg_containing = region_containing(id_mag) if region_containing(id_mag) else region_containing_sim(id_mag)
    formated_query = query.format(classifier, annee, mois, id_mag, reg_id_to_name[reg_containing], id_famille_produit)

    result = pd.read_sql(formated_query, conn).values
    conn.close()

    if len(result) > 0:
        return result[0][2]

    return result





def performances_magasin_cumul_mag(annee, mois_int, id_mag):
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
            temps.mois <= {} AND
            magasin.id_magasin = {};
    """
    result = pd.read_sql(query.format(annee, mois_int, id_mag), conn).values
    conn.close()
    

    if len(result) > 0:
        if result[0][0] :
            return result[0]

    return [0.01, 0, 0.01, 0, 0.01, 0]




def performances_magasin_item_cumul_mag(annee, mois_int, id_mag, id_famille_produit) :
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
            temps.mois <= {} AND
            magasin.id_magasin = {} AND
            famille_produit.id_famille_produit = {};
    """
    result = pd.read_sql(query.format(annee, mois_int, id_mag, id_famille_produit), conn).values
    conn.close()

    if len(result) > 0:
        if result[0][0] :
            return result[0]

    return [0.01, 0, 0.01, 0, 0.01, 0]




def nat_rank_mag_cumul_mag(id_mag, classifier, annee, mois) :
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
                temps.mois <= {2}
            
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





def nat_rank_mag_item_cumul_mag(id_mag, classifier, annee, mois, id_famille_produit) :
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
                JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

            WHERE 
                temps.annee = {1} AND
                temps.mois <= {2} AND
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





def reg_rank_mag_cumul_mag(id_mag, classifier, annee, mois) :
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
                temps.mois <= {2} AND
                villes.lib_departement IN {4}
            
            GROUP BY villes.lib_ville
            ) innner

        WHERE
            innner.id_mag = {3}
        ;
    """

    
    reg_containing = region_containing(id_mag) if region_containing(id_mag) else region_containing_sim(id_mag)

    formated_query = query.format(classifier, annee, mois, id_mag, reg_id_to_name[reg_containing])

    result = pd.read_sql(formated_query, conn).values
    conn.close()

    if len(result) > 0:
        return result[0][2]

    return result




def reg_rank_mag_item_cumul_mag(id_mag, classifier, annee, mois, id_famille_produit) :
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
                JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

            WHERE 
                temps.annee = {1} AND
                temps.mois <= {2} AND
                villes.lib_departement IN {4} AND
                famille_produit.id_famille_produit = {5}
            
            GROUP BY villes.lib_ville
            ) innner

        WHERE
            innner.id_mag = {3}
        ;
    """

    reg_containing = region_containing(id_mag) if region_containing(id_mag) else region_containing_sim(id_mag)
    formated_query = query.format(classifier, annee, mois, id_mag, reg_id_to_name[reg_containing], id_famille_produit)

    result = pd.read_sql(formated_query, conn).values
    conn.close()

    if len(result) > 0:
        return result[0][2]

    return result





def hist_mag(annee, mois, id_mag):
    hifi_obj = hist_indicator_mag('ca_objectif', annee, mois, 'hifi', id_mag)
    hifi_reel = hist_indicator_mag('ca_reel', annee, mois, 'hifi', id_mag)

    magneto_obj = hist_indicator_mag('ca_objectif', annee, mois, 'magneto', id_mag)
    magneto_reel = hist_indicator_mag('ca_reel', annee, mois, 'magneto', id_mag)

    fours_obj = hist_indicator_mag('ca_objectif', annee, mois, 'fours', id_mag)
    fours_reel = hist_indicator_mag('ca_reel', annee, mois, 'fours', id_mag)

    return {
        "hifi_obj" : hifi_obj,
        "hifi_reel" : hifi_reel,
        "magneto_obj" : magneto_obj,
        "magneto_reel" : magneto_reel,
        "fours_obj" : fours_obj,
        "fours_reel" : fours_reel
    }



def hist_indicator_mag(indicator, annee, mois, lib_famille_produit, id_mag):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT sum({}) 
        
        FROM sales
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN magasin ON magasin.id_magasin = sales.id_magasin
        
        WHERE 
            temps.annee = {} AND
            temps.mois = '{}' AND
            famille_produit.lib_famille_produit = '{}' AND
            magasin.id_magasin = {};
    """
    indic = pd.read_sql(query.format(indicator, annee, mois, lib_famille_produit, id_mag), conn).values[0][0]
    conn.close()

    return indic




def hist_indicator_cumul_mag(indicator, annee, mois, lib_famille_produit, id_mag):
    conn = sqlite3.connect('data.db')

    query = """
        SELECT sum({}) 
        
        FROM sales
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN magasin ON magasin.id_magasin = sales.id_magasin
        
        WHERE 
            temps.annee = {} AND
            temps.mois <= '{}' AND
            famille_produit.lib_famille_produit = '{}' AND
            magasin.id_magasin = {};
    """
    indic = pd.read_sql(query.format(indicator, annee, mois, lib_famille_produit, id_mag), conn).values[0][0]
    conn.close()

    return indic





def hist_cumul_mag(annee, mois, id_mag):
    hifi_obj = hist_indicator_cumul_mag('ca_objectif', annee, mois, 'hifi', id_mag)
    hifi_reel = hist_indicator_cumul_mag('ca_reel', annee, mois, 'hifi', id_mag)

    magneto_obj = hist_indicator_cumul_mag('ca_objectif', annee, mois, 'magneto', id_mag)
    magneto_reel = hist_indicator_cumul_mag('ca_reel', annee, mois, 'magneto', id_mag)

    fours_obj = hist_indicator_cumul_mag('ca_objectif', annee, mois, 'fours', id_mag)
    fours_reel = hist_indicator_cumul_mag('ca_reel', annee, mois, 'fours', id_mag)

    return {
        "hifi_obj_cumul" : hifi_obj,
        "hifi_reel_cumul" : hifi_reel,
        "magneto_obj_cumul" : magneto_obj,
        "magneto_reel_cumul" : magneto_reel,
        "fours_obj_cumul" : fours_obj,
        "fours_reel_cumul" : fours_reel
    }





def details_indicators_mag(annee, mois, id_mag):
    conn = sqlite3.connect('data.db')

    kpis = ["ca_objectif", "ca_reel", "ventes_objectif", "vente_reel", "marge_objectif", "marge_reel"]

    query = """
        SELECT sum({}), sum({}) , sum({}), sum({}), sum({}) , sum({})
        
        FROM sales
        JOIN temps ON sales.id_temps = temps.id_temps
        JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit
        JOIN magasin ON magasin.id_magasin = sales.id_magasin
        
        WHERE 
            temps.annee = {} AND
            temps.mois = {} AND
            famille_produit.lib_famille_produit = '{}' AND
            magasin.id_magasin = {};
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
        id_mag
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
        id_mag
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
        id_mag
    ), conn).values[0]
    magneto_kpi = dict(zip(kpis, magneto_kpi_result))

    conn.close()

    return {
        "hifi_kpi" : hifi_kpi,
        "fours_kpi" : fours_kpi,
        "magneto_kpi" : magneto_kpi
    }




def palmares_indicators_mag(annee, mois, classement, id_mag):
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

        WHERE 
            temps.annee = {0} AND
            temps.mois = {1}  AND
            magasin.id_magasin = {3}
        
        ORDER BY {2} DESC;
    """

    indicators = pd.read_sql(query.format(annee, mois, classement, id_mag), conn).values

    conn.close()

    return {
        "indicators" : indicators
    }




def palmares_indicators_region_mag(annee, mois, classement, list_departement_reg, id_mag):
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

        WHERE 
            temps.annee = {0} AND
            temps.mois = {1} AND
            magasin.id_magasin = {3}
        
        ORDER BY {2} DESC;
    """

    indicators = pd.read_sql(query.format(annee, mois, classement, id_mag), conn).values

    conn.close()

    return indicators
