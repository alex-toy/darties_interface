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
def index():
    
    perf_nat = performances_nationales(2020)

    list_depart_reg_1 = "('var', 'bouches-du-rhone')"
    perf_reg1 = performances_region(2020, list_depart_reg_1)

    list_depart_reg_2 = "('cher', 'yonne')"
    perf_reg2 = performances_region(2020, list_depart_reg_2)
    
    return render_template(
        'index.html', 
        perf_nat=perf_nat,
        perf_reg1=perf_reg1,
        perf_reg2=perf_reg2
    )




if __name__ == "__main__":
    app.run(debug=True)


