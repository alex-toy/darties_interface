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
from queries_region import *
from queries_mag import *
from config import *

main_mag = Blueprint('main_mag', __name__)



@main_mag.route('/magasin/<int:id_mag>', methods=['GET', 'POST'])
@login_required
def accueil_magasin(id_mag):

    id_reg = region_containing(id_mag)

    if not (current_user.id_profil == 1) and (not current_user.id_magasin == id_mag) and (not current_user.id_region == id_reg) :
        flash("Vous n'êtes pas autorisé à acceder à cette partie de l'application.")
        return redirect(url_for('auth.login'))

    result = request.form.to_dict()

    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M:%S")
    month = int(now.month)
    year = int(now.year)
    years = [y for y in range(year-2, year+1)]
    months = {m:int_to_name[m] for m in range(month+1, 13)}
    
    mois_int = 1
    mois_int_cumul = 0
    mois_string = 'janvier'
    mois_string_cumul = 'janvier'
    annee = int(now.year)
    if result :
        if 'mois' in result.keys() :
            mois_int = int(result['mois'].split('|')[0])
            mois_string = result['mois'].split('|')[1]
        elif 'mois_cumul' in result.keys():
            mois_int_cumul = int(result['mois_cumul'].split('|')[0])
            print(mois_int_cumul)
            mois_string_cumul = result['mois_cumul'].split('|')[1]
        if 'annee' in result.keys() :
            annee = int(result['annee'])

    cumul = False
    if mois_int_cumul > 0 :
        perf_mag = performances_magasin_cumul_mag(annee, mois_int_cumul, id_mag)
        perf_mag_hifi = performances_magasin_item_cumul_mag(annee, mois_int_cumul, id_mag, 1)
        perf_mag_magneto = performances_magasin_item_cumul_mag(annee, mois_int_cumul, id_mag, 2)
        perf_mag_fours = performances_magasin_item_cumul_mag(annee, mois_int_cumul, id_mag, 3)
        
        nat_rank_ca = nat_rank_mag_cumul_mag(id_mag, 'ca_reel', annee, mois_int_cumul)
        nat_rank_ca_hifi = nat_rank_mag_item_cumul_mag(id_mag, 'ca_reel', annee, mois_int_cumul, 1)
        nat_rank_ca_magneto = nat_rank_mag_item_cumul_mag(id_mag, 'ca_reel', annee, mois_int_cumul, 2)
        nat_rank_ca_fours = nat_rank_mag_item_cumul_mag(id_mag, 'ca_reel', annee, mois_int_cumul, 3)

        nat_rank_vente = nat_rank_mag_cumul_mag(id_mag, 'vente_reel', annee, mois_int_cumul)
        nat_rank_vente_hifi = nat_rank_mag_item_cumul_mag(id_mag, 'vente_reel', annee, mois_int_cumul, 1)
        nat_rank_vente_magneto = nat_rank_mag_item_cumul_mag(id_mag, 'vente_reel', annee, mois_int_cumul, 2)
        nat_rank_vente_fours = nat_rank_mag_item_cumul_mag(id_mag, 'vente_reel', annee, mois_int_cumul, 3)

        nat_rank_marge = nat_rank_mag_cumul_mag(id_mag, 'marge_reel', annee, mois_int_cumul)
        nat_rank_marge_hifi = nat_rank_mag_item_cumul_mag(id_mag, 'marge_reel', annee, mois_int_cumul, 1)
        nat_rank_marge_magneto = nat_rank_mag_item_cumul_mag(id_mag, 'marge_reel', annee, mois_int_cumul, 2)
        nat_rank_marge_fours = nat_rank_mag_item_cumul_mag(id_mag, 'marge_reel', annee, mois_int_cumul, 3)

        reg_rank_ca = reg_rank_mag_cumul_mag(id_mag, 'ca_reel', annee, mois_int_cumul)
        reg_rank_ca_hifi = reg_rank_mag_item_cumul_mag(id_mag, 'ca_reel', annee, mois_int_cumul, 1)
        reg_rank_ca_magneto = reg_rank_mag_item_cumul_mag(id_mag, 'ca_reel', annee, mois_int_cumul, 2)
        reg_rank_ca_fours = reg_rank_mag_item_cumul_mag(id_mag, 'ca_reel', annee, mois_int_cumul, 3)

        reg_rank_vente = reg_rank_mag_cumul_mag(id_mag, 'vente_reel', annee, mois_int_cumul)
        reg_rank_vente_hifi = reg_rank_mag_item_cumul_mag(id_mag, 'vente_reel', annee, mois_int_cumul, 1)
        reg_rank_vente_magneto = reg_rank_mag_item_cumul_mag(id_mag, 'vente_reel', annee, mois_int_cumul, 2)
        reg_rank_vente_fours = reg_rank_mag_item_cumul_mag(id_mag, 'vente_reel', annee, mois_int_cumul, 3)

        reg_rank_marge = reg_rank_mag_cumul_mag(id_mag, 'marge_reel', annee, mois_int_cumul)
        reg_rank_marge_hifi = reg_rank_mag_item_cumul_mag(id_mag, 'marge_reel', annee, mois_int_cumul, 1)
        reg_rank_marge_magneto = reg_rank_mag_item_cumul_mag(id_mag, 'marge_reel', annee, mois_int_cumul, 2)
        reg_rank_marge_fours = reg_rank_mag_item_cumul_mag(id_mag, 'marge_reel', annee, mois_int_cumul, 3)

        cumul = True
    else :
        perf_mag = performances_magasin(annee, mois_int, id_mag)
        perf_mag_hifi = performances_magasin_item(annee, mois_int, id_mag, 1)
        perf_mag_magneto = performances_magasin_item(annee, mois_int, id_mag, 2)
        perf_mag_fours = performances_magasin_item(annee, mois_int, id_mag, 3)
        
        nat_rank_ca = nat_rank_mag(id_mag, 'ca_reel', annee, mois_int)
        nat_rank_ca_hifi = nat_rank_mag_item(id_mag, 'ca_reel', annee, mois_int, 1)
        nat_rank_ca_magneto = nat_rank_mag_item(id_mag, 'ca_reel', annee, mois_int, 2)
        nat_rank_ca_fours = nat_rank_mag_item(id_mag, 'ca_reel', annee, mois_int, 3)

        nat_rank_vente = nat_rank_mag(id_mag, 'vente_reel', annee, mois_int)
        nat_rank_vente_hifi = nat_rank_mag_item(id_mag, 'vente_reel', annee, mois_int, 1)
        nat_rank_vente_magneto = nat_rank_mag_item(id_mag, 'vente_reel', annee, mois_int, 2)
        nat_rank_vente_fours = nat_rank_mag_item(id_mag, 'vente_reel', annee, mois_int, 3)

        nat_rank_marge = nat_rank_mag(id_mag, 'marge_reel', annee, mois_int)
        nat_rank_marge_hifi = nat_rank_mag_item(id_mag, 'marge_reel', annee, mois_int, 1)
        nat_rank_marge_magneto = nat_rank_mag_item(id_mag, 'marge_reel', annee, mois_int, 2)
        nat_rank_marge_fours = nat_rank_mag_item(id_mag, 'marge_reel', annee, mois_int, 3)

        reg_rank_ca = reg_rank_mag(id_mag, 'ca_reel', annee, mois_int)
        reg_rank_ca_hifi = reg_rank_mag_item(id_mag, 'ca_reel', annee, mois_int, 1)
        reg_rank_ca_magneto = reg_rank_mag_item(id_mag, 'ca_reel', annee, mois_int, 2)
        reg_rank_ca_fours = reg_rank_mag_item(id_mag, 'ca_reel', annee, mois_int, 3)

        reg_rank_vente = reg_rank_mag(id_mag, 'vente_reel', annee, mois_int)
        reg_rank_vente_hifi = reg_rank_mag_item(id_mag, 'vente_reel', annee, mois_int, 1)
        reg_rank_vente_magneto = reg_rank_mag_item(id_mag, 'vente_reel', annee, mois_int, 2)
        reg_rank_vente_fours = reg_rank_mag_item(id_mag, 'vente_reel', annee, mois_int, 3)

        reg_rank_marge = reg_rank_mag(id_mag, 'marge_reel', annee, mois_int)
        reg_rank_marge_hifi = reg_rank_mag_item(id_mag, 'marge_reel', annee, mois_int, 1)
        reg_rank_marge_magneto = reg_rank_mag_item(id_mag, 'marge_reel', annee, mois_int, 2)
        reg_rank_marge_fours = reg_rank_mag_item(id_mag, 'marge_reel', annee, mois_int, 3)


    magasins = None
    if current_user.id_profil == 1 :
        magasins = all_magasin()
    elif current_user.id_region :
        if current_user.id_region > 0 :
            magasins = all_magasin_in_region(current_user.id_region)


    
    return render_template(
        'accueil_magasin.html',

        nom=current_user.nom,
        prenom=current_user.prenom,

        annee=annee,
        mois_string=mois_string,
        mois_string_cumul=mois_string_cumul,

        id_mag=id_mag,

        perf_mag=perf_mag,
        perf_mag_hifi=perf_mag_hifi,
        perf_mag_magneto=perf_mag_magneto,
        perf_mag_fours=perf_mag_fours,

        magasins=magasins,

        mag_name=mag_name(id_mag),

        nat_rank_ca=nat_rank_ca,
        nat_rank_ca_hifi=nat_rank_ca_hifi,
        nat_rank_ca_magneto=nat_rank_ca_magneto,
        nat_rank_ca_fours=nat_rank_ca_fours,

        nat_rank_vente=nat_rank_vente,
        nat_rank_vente_hifi=nat_rank_vente_hifi,
        nat_rank_vente_magneto=nat_rank_vente_magneto,
        nat_rank_vente_fours=nat_rank_vente_fours,

        nat_rank_marge=nat_rank_marge,
        nat_rank_marge_hifi=nat_rank_marge_hifi,
        nat_rank_marge_magneto=nat_rank_marge_magneto,
        nat_rank_marge_fours=nat_rank_marge_fours,

        reg_rank_ca=reg_rank_ca,
        reg_rank_ca_hifi=reg_rank_ca_hifi,
        reg_rank_ca_magneto=reg_rank_ca_magneto,
        reg_rank_ca_fours=reg_rank_ca_fours,

        reg_rank_vente=reg_rank_vente,
        reg_rank_vente_hifi=reg_rank_vente_hifi,
        reg_rank_vente_magneto=reg_rank_vente_magneto,
        reg_rank_vente_fours=reg_rank_vente_fours,

        reg_rank_marge=reg_rank_marge,
        reg_rank_marge_hifi=reg_rank_marge_hifi,
        reg_rank_marge_magneto=reg_rank_marge_magneto,
        reg_rank_marge_fours=reg_rank_marge_fours,

        today=today,
        years=years,
        months=months,
        location='magasin',

        cumul=cumul
    )





@main_mag.route('/historique_mag/<int:id_mag>', methods=['GET', 'POST'])
@login_required
def historique(id_mag):

    if not (current_user.id_profil == 1) and (not current_user.id_magasin == id_mag) and (not current_user.id_region == id_reg) :
        flash("Vous n'êtes pas autorisé à acceder à cette partie de l'application.")
        return redirect(url_for('auth.login'))

    current_year = date.today().year

    result = request.form.to_dict()
    
    mois_int = 2
    mois_string = 'fevrier'
    if result :
        if 'mois' in result.keys():
            mois_int = int(result['mois'].split('|')[0])
            mois_string = result['mois'].split('|')[1]

    hist_indicators_prev = hist_mag(current_year-1, mois_int, id_mag)
    hist_indicators_cumul_prev = hist_cumul_mag(current_year-1, mois_int, id_mag)
    
    hist_indicators_cur = hist_mag(current_year, mois_int, id_mag)
    hist_indicators_cumul_cur = hist_cumul_mag(current_year, mois_int, id_mag)

    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M:%S")

    magasins = None
    if current_user.id_profil == 1 :
        magasins = all_magasin()
    elif current_user.id_region :
        if current_user.id_region > 0 :
            magasins = all_magasin_in_region(current_user.id_region)
    
    return render_template(
        'historique_mag.html',

        nom=current_user.nom,
        prenom=current_user.prenom,

        annee=current_year,
        mois_string=mois_string,

        id_mag=id_mag,

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

        magasins=magasins,
        mag_name=mag_name(id_mag),

        today=today,
        location='historique_mag'
    )





@main_mag.route('/details_mag/<int:id_mag>', methods=['GET', 'POST'])
@login_required
def details(id_mag):

    if not (current_user.id_profil == 1) and (not current_user.id_magasin == id_mag) and (not current_user.id_region == id_reg) :
        flash("Vous n'êtes pas autorisé à acceder à cette partie de l'application.")
        return redirect(url_for('auth.login'))
    
    result = request.form.to_dict()
    
    mois_int = 1
    mois_string = 'janvier'
    annee = 2020
    if result :
        if 'mois' in result.keys():
            mois_int = int(result['mois'].split('|')[0])
            mois_string = result['mois'].split('|')[1]
        if 'annee' in result.keys():
            annee = int(result['annee'])

    di = details_indicators_mag(annee, mois_int, id_mag)

    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M:%S")
    year = int(now.year)
    month = int(now.month)
    years = [y for y in range(year-2, year+1)]
    months = {m:int_to_name[m] for m in range(month+1, 13)}

    magasins = None
    if current_user.id_profil == 1 :
        magasins = all_magasin()
    elif current_user.id_region :
        if current_user.id_region > 0 :
            magasins = all_magasin_in_region(current_user.id_region)

    return render_template(
        'details_mag.html',

        nom=current_user.nom,
        prenom=current_user.prenom,

        current_year=annee,
        mois=mois_string,

        id_mag=id_mag,

        hifi_kpi=di["hifi_kpi"],
        fours_kpi=di["fours_kpi"],
        magneto_kpi=di["magneto_kpi"],

        magasins=magasins,
        mag_name=mag_name(id_mag),

        today=today,
        years=years,
        location='details_mag'
    )





@main_mag.route('/palmares_mag/<int:id_mag>', methods=['GET', 'POST'])
@login_required
def palmares(id_mag):

    id_reg = region_containing(id_mag)
    list_departement_reg = reg_id_to_name[id_reg]

    if not (current_user.id_profil == 1) and (not current_user.id_magasin == id_mag) and (not current_user.id_region == id_reg) :
        flash("Vous n'êtes pas autorisé à acceder à cette partie de l'application.")
        return redirect(url_for('auth.login'))
    
    result = request.form.to_dict()
    
    mois_int = 1
    mois_string = 'janvier'
    annee = 2020
    classement = 'ca_reel'
    if result :
        if 'mois' in result.keys():
            mois_int = int(result['mois'].split('|')[0])
            mois_string = result['mois'].split('|')[1]
        if 'annee' in result.keys():
            annee = int(result['annee'])
        if 'classement' in result.keys():
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

    pi_reg = palmares_indicators_region(annee, mois_int, classement, list_departement_reg)
    pi_reg_prev = palmares_indicators_region(annee-1, mois_int, classement, list_departement_reg)

    ranks = { city_record[0] : index+1 for index, city_record in  enumerate(pi)}

    mag_n = mag_name(id_mag)
    rank = { city_record[0] : index+1 for index, city_record in  enumerate(pi)}.get(mag_n, 0)
    rank_prev = { city_record[0] : index+1 for index, city_record in  enumerate(pi_prev)}.get(mag_n, 0)
    rank_reg = { city_record[0] : index+1 for index, city_record in  enumerate(pi_reg)}.get(mag_n, 0)
    rank_reg_prev = { city_record[0] : index+1 for index, city_record in  enumerate(pi_reg_prev)}.get(mag_n, 0)

    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M:%S")
    year = int(now.year)
    month = int(now.month)
    years = [y for y in range(year-2, year+1)]
    months = {m:int_to_name[m] for m in range(month+1, 13)}

    magasins = None
    if current_user.id_profil == 1 :
        magasins = all_magasin()
    elif current_user.id_region :
        if current_user.id_region > 0 :
            magasins = all_magasin_in_region(current_user.id_region)

    return render_template(
        'palmares_mag.html',

        nom=current_user.nom,
        prenom=current_user.prenom,
        
        current_year=annee,
        mois=mois_string,

        id_mag=id_mag,

        classement_indicator=classement_dict[classement],

        pi=pi,
        pi_prev=pi_prev,
        ranks=ranks,
        rank=rank,
        rank_prev=rank_prev,
        rank_reg=rank_reg,
        rank_reg_prev=rank_reg_prev,

        pi_reg=pi_reg,
        pi_reg_prev=pi_reg_prev,

        magasins=magasins,
        mag_name=mag_name(id_mag),

        today=today,
        years=years,
        location='palmares_mag'
    )










# if __name__ == "__main__":
    
#     app.run(debug=True)