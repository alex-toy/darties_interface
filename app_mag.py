from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, current_user
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import pandas as pd
import time
from datetime import date

from queries import *
from queries_mag import *
from config import *

main_mag = Blueprint('main_mag', __name__)



@main_mag.route('/magasin/<int:id_mag>', methods=['GET', 'POST'])
@login_required
def accueil_magasin(id_mag):

    print(current_user.id_magasin)

    id_reg = region_containing(id_mag)

    if not (current_user.id_profil == 1) and (not current_user.id_magasin == id_mag) and (not current_user.id_region == id_reg) :
        return redirect(url_for('auth.login'))

    result = request.form.to_dict()
    
    mois_int = 1
    mois_string = 'janvier'
    annee = 2020
    classement = 'ca_reel'
    if result :
        mois_int = int(result['mois'].split('|')[0])
        mois_string = result['mois'].split('|')[1]
        annee = int(result['annee'])

    perf_mag = performances_magasin(annee, mois_int, id_mag)
    perf_mag_hifi = performances_magasin_item(annee, mois_int, id_mag, 1)
    perf_mag_magneto = performances_magasin_item(annee, mois_int, id_mag, 2)
    perf_mag_fours = performances_magasin_item(annee, mois_int, id_mag, 3)
    
    return render_template(
        'accueil_magasin.html',

        nom=current_user.nom,
        prenom=current_user.prenom,

        current_year=annee,
        mois=mois_string,

        id_mag=id_mag,

        perf_mag=perf_mag,
        perf_mag_hifi=perf_mag_hifi,
        perf_mag_magneto=perf_mag_magneto,
        perf_mag_fours=perf_mag_fours,
    )





# @main.route('/accueil', methods=['GET', 'POST'])
# @login_required
# def accueil():

#     if not current_user.id_profil == 1 :
#         return redirect(url_for('auth.login'))

#     result = request.form.to_dict()
#     currencies = all_devise()
    
#     mois_int = 5
#     mois_string = 'mai'
#     annee = 2021
#     devise = "Euro"
#     curr_rate = [1, "Euro"]
#     if result :
#         mois_int = int(result['mois'].split('|')[0])
#         mois_string = result['mois'].split('|')[1]
#         annee = int(result['annee'])
#         id_devise = result['devise']
#         if int(id_devise) > 0 :
#             curr_rate_list = currency_rate(id_devise, annee, mois_int)
#             if len(curr_rate_list) > 0 :
#                 curr_rate = curr_rate_list[0]


#     perf_nat = performances_nationales(annee, mois_int)
#     perf_reg1 = performances_region(annee, mois_int, list_departement_reg_1)
#     perf_reg2 = performances_region(annee, mois_int, list_departement_reg_2)
#     perf_reg3 = performances_region(annee, mois_int, list_departement_reg_3)
#     perf_reg4 = performances_region(annee, mois_int, list_departement_reg_4)
#     perf_reg5 = performances_region(annee, mois_int, list_departement_reg_5)


#     return render_template(
#         'accueil.html',

#         name=current_user.nom,

#         mois_string=mois_string,
#         annee=annee,

#         currencies=currencies,
#         curr_rate=curr_rate,

#         perf_nat={k:v*curr_rate[0] for (k,v) in perf_nat.items()},
#         perf_reg1={k:v*curr_rate[0] for (k,v) in perf_reg1.items()},
#         perf_reg2={k:v*curr_rate[0] for (k,v) in perf_reg2.items()},
#         perf_reg3={k:v*curr_rate[0] for (k,v) in perf_reg3.items()},
#         perf_reg4={k:v*curr_rate[0] for (k,v) in perf_reg4.items()},
#         perf_reg5={k:v*curr_rate[0] for (k,v) in perf_reg5.items()}
#     )




# @main.route('/historique', methods=['GET', 'POST'])
# @login_required
# def historique():

#     if not current_user.id_profil == 1 :
#         return redirect(url_for('auth.login'))

#     current_year = date.today().year

#     result = request.form.to_dict()
    
#     mois_int = 2
#     mois_string = 'fevrier'
#     if result :
#         mois_int = int(result['mois'].split('|')[0])
#         mois_string = result['mois'].split('|')[1]

#     hist_indicators_prev = hist(current_year-1, mois_int)
#     hist_indicators_cumul_prev = hist_cumul(current_year-1, mois_int)
    
#     hist_indicators_cur = hist(current_year, mois_int)
#     hist_indicators_cumul_cur = hist_cumul(current_year, mois_int)
    
#     return render_template(
#         'historique.html',

#         name=current_user.name,

#         annee=current_year,
#         mois_string=mois_string,

#         hifi_obj_prev=hist_indicators_prev['hifi_obj'],
#         hifi_reel_prev=hist_indicators_prev['hifi_reel'],
#         magneto_obj_prev=hist_indicators_prev['magneto_obj'],
#         magneto_reel_prev=hist_indicators_prev['magneto_reel'],
#         fours_obj_prev=hist_indicators_prev['fours_obj'],
#         fours_reel_prev=hist_indicators_prev['fours_reel'],

#         hifi_obj_cumul_prev=hist_indicators_cumul_prev['hifi_obj_cumul'],
#         hifi_reel_cumul_prev=hist_indicators_cumul_prev['hifi_reel_cumul'],
#         magneto_obj_cumul_prev=hist_indicators_cumul_prev['magneto_obj_cumul'],
#         magneto_reel_cumul_prev=hist_indicators_cumul_prev['magneto_reel_cumul'],
#         fours_obj_cumul_prev=hist_indicators_cumul_prev['fours_obj_cumul'],
#         fours_reel_cumul_prev=hist_indicators_cumul_prev['fours_reel_cumul'],


#         hifi_obj_cur=hist_indicators_cur['hifi_obj'],
#         hifi_reel_cur=hist_indicators_cur['hifi_reel'],
#         magneto_obj_cur=hist_indicators_cur['magneto_obj'],
#         magneto_reel_cur=hist_indicators_cur['magneto_reel'],
#         fours_obj_cur=hist_indicators_cur['fours_obj'],
#         fours_reel_cur=hist_indicators_cur['fours_reel'],

#         hifi_obj_cumul_cur=hist_indicators_cumul_cur['hifi_obj_cumul'],
#         hifi_reel_cumul_cur=hist_indicators_cumul_cur['hifi_reel_cumul'],
#         magneto_obj_cumul_cur=hist_indicators_cumul_cur['magneto_obj_cumul'],
#         magneto_reel_cumul_cur=hist_indicators_cumul_cur['magneto_reel_cumul'],
#         fours_obj_cumul_cur=hist_indicators_cumul_cur['fours_obj_cumul'],
#         fours_reel_cumul_cur=hist_indicators_cumul_cur['fours_reel_cumul']
#     )




# @main.route('/details', methods=['GET', 'POST'])
# @login_required
# def details():

#     if not current_user.id_profil == 1 :
#         return redirect(url_for('auth.login'))
    
#     result = request.form.to_dict()
    
#     mois_int = 1
#     mois_string = 'janvier'
#     annee = 2020
#     if result :
#         mois_int = int(result['mois'].split('|')[0])
#         mois_string = result['mois'].split('|')[1]
#         annee = int(result['annee'])

#     di = details_indicators(annee, mois_int)

#     return render_template(
#         'details.html',

#         name=current_user.name,

#         current_year=annee,
#         mois=mois_string,

#         hifi_kpi=di["hifi_kpi"],
#         fours_kpi=di["fours_kpi"],
#         magneto_kpi=di["magneto_kpi"],
#     )





# @main.route('/palmares', methods=['GET', 'POST'])
# def palmares():

#     if not current_user.id_profil == 1 :
#         return redirect(url_for('auth.login'))
    
#     result = request.form.to_dict()
    
#     mois_int = 1
#     mois_string = 'janvier'
#     annee = 2020
#     classement = 'ca_reel'
#     if result :
#         mois_int = int(result['mois'].split('|')[0])
#         mois_string = result['mois'].split('|')[1]
#         annee = int(result['annee'])
#         classement = result['classement']


#     classement_dict = { 
#         'ca_objectif' : 'CA objectif', 
#         'ca_reel' : 'CA réel',
#         'ventes_objectif' : 'Ventes objectif',
#         'vente_reel' : 'Ventes réelles',
#         'marge_objectif' : 'Marge objectif',
#         'marge_reel' : 'Marge réelle',
#     }


#     pi = palmares_indicators(annee, mois_int, classement)["indicators"]
#     pi_prev = palmares_indicators(annee-1, mois_int, classement)["indicators"]

#     ranks = { city_record[0] : index+1 for index, city_record in  enumerate(pi_prev)}

#     return render_template(
#         'palmares.html',

#         name=current_user.name,
        
#         current_year=annee,
#         mois=mois_string,
#         classement_indicator=classement_dict[classement],

#         pi=pi,
#         pi_prev=pi_prev,
#         ranks=ranks
#     )




# @main.route('/accueil/<int:region_id>', methods=['GET', 'POST'])
# def accueil_region(region_id):

#     if not (current_user.id_profil == 1) and (not current_user.id_region == region_id) :
#         return redirect(url_for('auth.login'))

#     result = request.form.to_dict()
    
#     mois_int = 1
#     mois_string = 'janvier'
#     annee = 2020
#     classement = 'ca_reel'
#     if result :
#         mois_int = int(result['mois'].split('|')[0])
#         mois_string = result['mois'].split('|')[1]
#         annee = int(result['annee'])

#     perf_reg = performances_region(annee, mois_int, reg_id_to_name[region_id])
#     perf_reg_fours = performances_region_produit(annee, mois_int, reg_id_to_name[region_id], 1)
#     perf_reg_hifi = performances_region_produit(annee, mois_int, reg_id_to_name[region_id], 1)
#     perf_reg_magneto = performances_region_produit(annee, mois_int, reg_id_to_name[region_id], 1)
    
#     return render_template(
#         'accueil_region.html',

#         nom=current_user.nom,
#         prenom=current_user.prenom,

#         current_year=annee,
#         mois=mois_string,

#         region_id=region_id,
#         perf_reg=perf_reg
#     )







# if __name__ == "__main__":
    
#     app.run(debug=True)