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
import os

from queries import *
from queries_mag import *
from config import *

main_export = Blueprint('main_export', __name__)



@main_export.route('/export/<string:page_name>', methods=['GET', 'POST'])
@login_required
def export(page_name):

    if not (current_user.id_profil == 1) :
        return redirect(url_for('auth.login'))

    
    output_file = ''
    result = request.form.to_dict()
    if result :
        output_file = result['output_file']


    input_file = os.path.join(os.path.os.getcwd(), 'templates', f"{page_name}.html")

    parser = ExcelParser(input_file)
    parser.to_excel(output_file)


    return redirect(url_for('main_app.historique'))









# if __name__ == "__main__":
    
#     app.run(debug=True)