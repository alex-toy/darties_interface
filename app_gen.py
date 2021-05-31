from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, current_user
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import sqlite3
import pandas as pd
import time
from datetime import date

from queries import *
from config import *

main_app = Blueprint('main_app', __name__)


@main_app.route('/accueil', methods=['GET', 'POST'])
@login_required
def accueil():

    if not current_user.id_profil == 1 :
        flash("Vous n'êtes pas autorisé à acceder à cette partie de l'application.")
        return redirect(url_for('auth.login'))

    result = request.form.to_dict()
    currencies = all_devise()
    
    mois_int = 5
    mois_string = 'mai'
    annee = 2021
    devise = "Euro"
    curr_rate = [1, "Euro"]
    if result :
        if 'mois' in result.keys():
            mois_int = int(result['mois'].split('|')[0])
            mois_string = result['mois'].split('|')[1]
        annee = int(result['annee'])
        id_devise = result['devise']
        if int(id_devise) > 0 :
            curr_rate_list = currency_rate(id_devise, annee, mois_int)
            if len(curr_rate_list) > 0 :
                curr_rate = curr_rate_list[0]


    perf_nat = performances_nationales(annee, mois_int)
    perf_reg1 = performances_region(annee, mois_int, list_departement_reg_1)
    perf_reg2 = performances_region(annee, mois_int, list_departement_reg_2)
    perf_reg3 = performances_region(annee, mois_int, list_departement_reg_3)
    perf_reg4 = performances_region(annee, mois_int, list_departement_reg_4)
    perf_reg5 = performances_region(annee, mois_int, list_departement_reg_5)

    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M:%S")
    year = int(now.year)
    month = int(now.month)
    years = [y for y in range(year-2, year+1)]
    months = {m:int_to_name[m] for m in range(month+1, 13)}


    return render_template(
        'accueil.html',

        nom=current_user.nom,
        prenom=current_user.prenom,

        mois_string=mois_string,
        annee=annee,

        currencies=currencies,
        curr_rate=curr_rate,

        perf_nat={k:v*curr_rate[0] for (k,v) in perf_nat.items()},
        perf_reg1={k:v*curr_rate[0] for (k,v) in perf_reg1.items()},
        perf_reg2={k:v*curr_rate[0] for (k,v) in perf_reg2.items()},
        perf_reg3={k:v*curr_rate[0] for (k,v) in perf_reg3.items()},
        perf_reg4={k:v*curr_rate[0] for (k,v) in perf_reg4.items()},
        perf_reg5={k:v*curr_rate[0] for (k,v) in perf_reg5.items()},

        magasins=all_magasin(),

        today=today,
        years=years,
        months=months
    )




@main_app.route('/historique', methods=['GET', 'POST'])
@login_required
def historique():

    if not current_user.id_profil == 1 :
        flash("Vous n'êtes pas autorisé à acceder à cette partie de l'application.")
        return redirect(url_for('auth.login'))

    current_year = date.today().year

    result = request.form.to_dict()
    
    mois_int = 2
    mois_string = 'fevrier'
    if result :
        mois_int = int(result['mois'].split('|')[0])
        mois_string = result['mois'].split('|')[1]

    hist_indicators_prev = hist(current_year-1, mois_int)
    hist_indicators_cumul_prev = hist_cumul(current_year-1, mois_int)
    
    hist_indicators_cur = hist(current_year, mois_int)
    hist_indicators_cumul_cur = hist_cumul(current_year, mois_int)

    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M:%S")
    
    return render_template(
        'historique.html',

        nom=current_user.nom,
        prenom=current_user.prenom,

        annee=current_year,
        mois_string=mois_string,

        hifi_obj_prev=hist_indicators_prev['hifi_obj'],
        hifi_reel_prev=hist_indicators_prev['hifi_reel'],
        magneto_obj_prev=hist_indicators_prev['magneto_obj'],
        magneto_reel_prev=hist_indicators_prev['magneto_reel'],
        fours_obj_prev=hist_indicators_prev['fours_obj'],
        fours_reel_prev=hist_indicators_prev['fours_reel'],

        hifi_obj_cumul_prev=hist_indicators_cumul_prev['hifi_obj_cumul'],
        hifi_reel_cumul_prev=hist_indicators_cumul_prev['hifi_reel_cumul'],
        magneto_obj_cumul_prev=hist_indicators_cumul_prev['magneto_obj_cumul'],
        magneto_reel_cumul_prev=hist_indicators_cumul_prev['magneto_reel_cumul'],
        fours_obj_cumul_prev=hist_indicators_cumul_prev['fours_obj_cumul'],
        fours_reel_cumul_prev=hist_indicators_cumul_prev['fours_reel_cumul'],


        hifi_obj_cur=hist_indicators_cur['hifi_obj'],
        hifi_reel_cur=hist_indicators_cur['hifi_reel'],
        magneto_obj_cur=hist_indicators_cur['magneto_obj'],
        magneto_reel_cur=hist_indicators_cur['magneto_reel'],
        fours_obj_cur=hist_indicators_cur['fours_obj'],
        fours_reel_cur=hist_indicators_cur['fours_reel'],

        hifi_obj_cumul_cur=hist_indicators_cumul_cur['hifi_obj_cumul'],
        hifi_reel_cumul_cur=hist_indicators_cumul_cur['hifi_reel_cumul'],
        magneto_obj_cumul_cur=hist_indicators_cumul_cur['magneto_obj_cumul'],
        magneto_reel_cumul_cur=hist_indicators_cumul_cur['magneto_reel_cumul'],
        fours_obj_cumul_cur=hist_indicators_cumul_cur['fours_obj_cumul'],
        fours_reel_cumul_cur=hist_indicators_cumul_cur['fours_reel_cumul'],

        magasins=all_magasin(),

        today=today
    )




@main_app.route('/details', methods=['GET', 'POST'])
@login_required
def details():

    if not current_user.id_profil == 1 :
        flash("Vous n'êtes pas autorisé à acceder à cette partie de l'application.")
        return redirect(url_for('auth.login'))
    
    result = request.form.to_dict()
    
    mois_int = 1
    mois_string = 'janvier'
    annee = 2020
    if result :
        mois_int = int(result['mois'].split('|')[0])
        mois_string = result['mois'].split('|')[1]
        annee = int(result['annee'])

    di = details_indicators(annee, mois_int)

    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M:%S")
    year = int(now.year)
    month = int(now.month)
    years = [y for y in range(year-2, year+1)]
    months = {m:int_to_name[m] for m in range(month+1, 13)}

    return render_template(
        'details.html',

        nom=current_user.nom,
        prenom=current_user.prenom,

        current_year=annee,
        mois=mois_string,

        hifi_kpi=di["hifi_kpi"],
        fours_kpi=di["fours_kpi"],
        magneto_kpi=di["magneto_kpi"],

        magasins=all_magasin(),

        today=today,
        years=years
    )





@main_app.route('/palmares', methods=['GET', 'POST'])
@login_required
def palmares():

    if not current_user.id_profil == 1 :
        flash("Vous n'êtes pas autorisé à acceder à cette partie de l'application.")
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
        classement = result['classement']


    classement_dict = { 
        'ca_objectif' : 'CA objectif', 
        'ca_reel' : 'CA réel',
        'ventes_objectif' : 'Ventes objectif',
        'vente_reel' : 'Ventes réelles',
        'marge_objectif' : 'Marge objectif',
        'marge_reel' : 'Marge réelle',
    }


    pi = palmares_indicators(annee, mois_int, classement)["indicators"]
    pi_prev = palmares_indicators(annee-1, mois_int, classement)["indicators"]

    pi_reg1 = palmares_indicators_region(annee, mois_int, classement, list_departement_reg_1)[:,0]
    pi_reg1_prev = palmares_indicators_region(annee-1, mois_int, classement, list_departement_reg_1)[:,0]

    pi_reg2 = palmares_indicators_region(annee, mois_int, classement, list_departement_reg_2)[:,0]
    pi_reg2_prev = palmares_indicators_region(annee-1, mois_int, classement, list_departement_reg_2)[:,0]

    pi_reg3 = palmares_indicators_region(annee, mois_int, classement, list_departement_reg_3)[:,0]
    pi_reg3_prev = palmares_indicators_region(annee-1, mois_int, classement, list_departement_reg_3)[:,0]

    pi_reg4 = palmares_indicators_region(annee, mois_int, classement, list_departement_reg_4)[:,0]
    pi_reg4_prev = palmares_indicators_region(annee-1, mois_int, classement, list_departement_reg_4)[:,0]

    pi_reg5 = palmares_indicators_region(annee, mois_int, classement, list_departement_reg_5)[:,0]
    pi_reg5_prev = palmares_indicators_region(annee-1, mois_int, classement, list_departement_reg_5)[:,0]

    ranks = { city_record[0] : index+1 for index, city_record in  enumerate(pi_prev)}

    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M:%S")
    year = int(now.year)
    month = int(now.month)
    years = [y for y in range(year-2, year+1)]
    months = {m:int_to_name[m] for m in range(month+1, 13)}

    return render_template(
        'palmares.html',

        nom=current_user.nom,
        prenom=current_user.prenom,
        
        current_year=annee,
        mois=mois_string,
        classement_indicator=classement_dict[classement],

        pi=pi,
        pi_prev=pi_prev,
        ranks=ranks,

        pi_reg1=pi_reg1,
        pi_reg1_prev=pi_reg1_prev,

        pi_reg2=pi_reg2,
        pi_reg2_prev=pi_reg2_prev,

        pi_reg3=pi_reg3,
        pi_reg3_prev=pi_reg3_prev,

        pi_reg4=pi_reg4,
        pi_reg4_prev=pi_reg4_prev,

        pi_reg5=pi_reg5,
        pi_reg5_prev=pi_reg5_prev,

        magasins=all_magasin(),

        today=today,
        years=years
    )








if __name__ == "__main__":
    
    app.run(debug=True)