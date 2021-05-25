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

main_reg = Blueprint('main_reg', __name__)



@main_reg.route('/accueil/<int:region_id>', methods=['GET', 'POST'])
@login_required
def accueil_region(region_id):

    if not (current_user.id_profil == 1) and (not current_user.id_region == region_id) :
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

    perf_reg = performances_region(annee, mois_int, reg_id_to_name[region_id])
    perf_reg_fours = performances_region_produit(annee, mois_int, reg_id_to_name[region_id], 1)
    perf_reg_hifi = performances_region_produit(annee, mois_int, reg_id_to_name[region_id], 1)
    perf_reg_magneto = performances_region_produit(annee, mois_int, reg_id_to_name[region_id], 1)

    magasins = all_magasin_in_region(region_id)
    
    return render_template(
        'accueil_region.html',

        nom=current_user.nom,
        prenom=current_user.prenom,

        current_year=annee,
        mois=mois_string,

        region_id=region_id,
        perf_reg=perf_reg,

        magasins=magasins
    )


if __name__ == "__main__":
    
    app.run(debug=True)