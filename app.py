from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)




@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)




if __name__ == "__main__":
    app.run(debug=True)