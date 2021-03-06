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
from queries_dep import *
from config import *

main_reg = Blueprint('main_reg', __name__)



@main_reg.route('/accueil/<int:region_id>', methods=['GET', 'POST'])
@login_required
def accueil_region(region_id):

    if not (current_user.id_profil == 1) and (not current_user.id_region == region_id) :
        flash("Vous n'êtes pas autorisé à acceder à cette partie de l'application.")
        return redirect(url_for('auth.login'))

    result = request.form.to_dict()
    
    mois_int = 1
    mois_string = 'janvier'
    annee = 2020
    classement = 'ca_reel'
    if result :
        if 'mois' in result.keys() :
            mois_int = int(result['mois'].split('|')[0])
            mois_string = result['mois'].split('|')[1]
        if 'annee' in result.keys() :
            annee = int(result['annee'])

    perf_reg = performances_region(annee, mois_int, reg_id_to_name[region_id])
    perf_reg_hifi = performances_region_produit(annee, mois_int, reg_id_to_name[region_id], 1)
    perf_reg_magneto = performances_region_produit(annee, mois_int, reg_id_to_name[region_id], 2)
    perf_reg_fours = performances_region_produit(annee, mois_int, reg_id_to_name[region_id], 3)

    magasins = None
    if current_user.id_profil == 1 :
        magasins = all_magasin()
    elif current_user.id_region :
        if current_user.id_region > 0 :
            magasins = all_magasin_in_region(current_user.id_region)


    region_rank_total = region_classify(annee, mois_int, region_id)
    region_rank_hifi = region_classify_fam_prod(annee, mois_int, region_id, 1)
    region_rank_magneto = region_classify_fam_prod(annee, mois_int, region_id, 2)
    region_rank_fours = region_classify_fam_prod(annee, mois_int, region_id, 3)

    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M:%S")
    year = int(now.year)
    month = int(now.month)
    years = [y for y in range(year-2, year+1)]
    months = {m:int_to_name[m] for m in range(month+1, 13)}

    perf_dep_haute_savoie = performances_dep(annee, mois_int, 'haute-savoie')
    perf_dep_savoie = performances_dep(annee, mois_int, 'savoie')
    perf_dep_ain = performances_dep(annee, mois_int, 'ain')
    perf_dep_isere = performances_dep(annee, mois_int, 'isere')
    
    return render_template(
        'accueil_region.html',

        nom=current_user.nom,
        prenom=current_user.prenom,

        current_year=annee,
        mois=mois_string,

        region_id=region_id,

        perf_reg=perf_reg,
        perf_reg_fours=perf_reg_fours,
        perf_reg_hifi=perf_reg_hifi,
        perf_reg_magneto=perf_reg_magneto,

        magasins=magasins,

        region_rank_total=region_rank_total,
        region_rank_hifi=region_rank_hifi,
        region_rank_magneto=region_rank_magneto,
        region_rank_fours=region_rank_fours,

        perf_dep_haute_savoie=perf_dep_haute_savoie,
        perf_dep_savoie=perf_dep_savoie,
        perf_dep_ain=perf_dep_ain,
        perf_dep_isere=perf_dep_isere,

        today=today,
        years=years,
        months=months,
        location='accueil_region'
    )


if __name__ == "__main__":
    
    app.run(debug=True)