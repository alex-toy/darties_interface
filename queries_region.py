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





def region_classify_fam_prodold(annee, mois, id_region, id_famille_produit) :

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
                    temps.annee = {annee} AND temps.mois = {mois}

                UNION

                SELECT *, 'region_2' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_2} AND
                    temps.annee = {annee} AND temps.mois = {mois}

                UNION

                SELECT *, 'region_3' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_3} AND
                    temps.annee = {annee} AND temps.mois = {mois}

                UNION

                SELECT *, 'region_4' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_4} AND
                    temps.annee = {annee} AND temps.mois = {mois}

                UNION

                SELECT *, 'region_5' AS region, famille_produit.id_famille_produit AS fam_prod
                
                FROM 
                    sales
                    JOIN temps ON sales.id_temps = temps.id_temps
                    JOIN villes ON sales.id_ville = villes.id_ville
                    JOIN famille_produit ON sales.id_famille_produit = famille_produit.id_famille_produit

                WHERE 
                    villes.lib_departement IN {list_departement_reg_5} AND
                    temps.annee = {annee} AND temps.mois = {mois}
                ) region_sub

            GROUP BY region ) sub

        WHERE 
            sub.region = 'region_{id_region}' AND
            sub.fam_prod = {id_famille_produit}
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