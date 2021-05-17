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

    current_year = 2020
    mois = 11
    
    di = details_indicators(current_year, mois)

    result = request.form.to_dict()
    print(result)
    n = result['nom'] if result['nom'] else ''
    p = result['prenom'] if result['prenom'] else ''
    
    return render_template(
        'details.html',
        current_year=current_year,
        mois=mois,

        hifi_kpi=di["hifi_kpi"],
        fours_kpi=di["fours_kpi"],
        magneto_kpi=di["magneto_kpi"],

        nom=n, 
        prenom=p
    )





if __name__ == "__main__":
    

    # app.debug = True
    # app.run()

    app.run(debug=True)


