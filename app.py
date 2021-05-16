from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



def test():
    query = f"""
        SELECT * FROM technos
        WHERE type = '{application_type}';
    """
    conn = sqlite3.connect('developpers.db')
    df = pd.read_sql(query, conn)

    for index, row in df.iterrows():
        content = f"{row['name']}"
        dispatcher.utter_message(text=content)



@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)




if __name__ == "__main__":
    app.run(debug=True)