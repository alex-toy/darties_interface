from flask import Flask, render_template, url_for, request, redirect, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import pandas as pd

from queries import *

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



@app.route('/accueil')
def accueil():
    
    perf_nat = performances_nationales(2020)

    list_depart_reg_1 = "('var', 'bouches-du-rhone')"
    perf_reg1 = performances_region(2020, list_depart_reg_1)

    list_depart_reg_2 = "('cher', 'yonne')"
    perf_reg2 = performances_region(2020, list_depart_reg_2)
    
    return render_template(
        'accueil.html', 
        perf_nat=perf_nat,
        perf_reg1=perf_reg1,
        perf_reg2=perf_reg2
    )




@app.route('/historique')
def historique():

    current_year = 2021

    hist_indicators_prev = hist(current_year-1, 11)
    hist_indicators_cumul_prev = hist_cumul(current_year-1, 11)
    
    hist_indicators_cur = hist(current_year, 11)
    hist_indicators_cumul_cur = hist_cumul(current_year, 11)
    
    return render_template(
        'historique.html',

        current_year=current_year,


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
        fours_reel_cumul_cur=hist_indicators_cumul_cur['fours_reel_cumul']
    )




@app.route('/details', methods=['GET', 'POST'])
def details():
    
    result = request.form.to_dict()
    
    mois_int = 1
    mois_string = 'janvier'
    annee = 2020
    if result :
        mois_int = int(result['mois'].split('|')[0])
        mois_string = result['mois'].split('|')[1]
        annee = int(result['annee'])

    di = details_indicators(annee, mois_int)

    return render_template(
        'details.html',
        current_year=annee,
        mois=mois_string,

        hifi_kpi=di["hifi_kpi"],
        fours_kpi=di["fours_kpi"],
        magneto_kpi=di["magneto_kpi"],
    )





@app.route('/palmares', methods=['GET', 'POST'])
def palmares():
    
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

    ranks = { city_record[0] : index+1 for index, city_record in  enumerate(pi_prev)}

    return render_template(
        'palmares.html',
        current_year=annee,
        mois=mois_string,
        classement_indicator=classement_dict[classement],

        pi=pi,
        pi_prev=pi_prev,
        ranks=ranks
    )





if __name__ == "__main__":
    
    app.run(debug=True)


