from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, current_user
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import pandas as pd
import time
from datetime import date
from html2excel import ExcelParser

from queries import *
from queries_mag import *
from config import *

main_export = Blueprint('main_export', __name__)



@main_export.route('/export/<string:page_name>', methods=['GET', 'POST'])
@login_required
def export(page_name):

    print(f"page_name : {page_name}" )


    if not (current_user.id_profil == 1) :
        return redirect(url_for('auth.login'))


    input_file = "/Users/alexei/darties_interface/templates/historique.html"
    output_file = '/Users/alexei/Downloads'


    parser = ExcelParser(input_file)
    parser.to_excel(output_file)


    
    


    return redirect(url_for('main_app.historique'))









# if __name__ == "__main__":
    
#     app.run(debug=True)