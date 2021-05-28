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

    magasins = None
    if current_user.id_profil == 1 :
        magasins = all_magasin()
    elif current_user.id_region :
        if current_user.id_region > 0 :
            magasins = all_magasin_in_region(current_user.id_region)


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

    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M:%S")
    
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

        today=today
    )









# if __name__ == "__main__":
    
#     app.run(debug=True)