from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import pandas as pd

from queries import *

app = Flask(__name__)
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
    
    hist_indicators = hist(2020, 'novembre')
    hist_indicators_cumul = hist_cumul(2020, 11)
    
    return render_template(
        'historique.html', 
        hifi_prev=hist_indicators['hifi_prev'],
        hifi_reel=hist_indicators['hifi_reel'],
        magneto_prev=hist_indicators['magneto_prev'],
        magneto_reel=hist_indicators['magneto_reel'],
        fours_prev=hist_indicators['fours_prev'],
        fours_reel=hist_indicators['fours_reel'],

        hifi_prev_cumul=hist_indicators_cumul['hifi_prev_cumul'],
        hifi_reel_cumul=hist_indicators_cumul['hifi_reel_cumul'],
        magneto_prev_cumul=hist_indicators_cumul['magneto_prev_cumul'],
        magneto_reel_cumul=hist_indicators_cumul['magneto_reel_cumul'],
        fours_prev_cumul=hist_indicators_cumul['fours_prev_cumul'],
        fours_reel_cumul=hist_indicators_cumul['fours_reel_cumul']
    )



if __name__ == "__main__":
    app.run(debug=True)


