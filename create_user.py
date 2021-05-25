from create_app import *
from models import User
from werkzeug.security import generate_password_hash, check_password_hash



if __name__ == "__main__":


    myfile = open("data/staging_utilisateur_000", "r")
    records = myfile.readlines()
    myfile.close()

    user_list = [
        ( 
            record[:-1].split('|')[0],
            record[:-1].split('|')[1],
            record[:-1].split('|')[2],
            record[:-1].split('|')[3],
            record[:-1].split('|')[4],
            int(record[:-1].split('|')[5]) if len(record[:-1].split('|')[5]) > 0 else None,
            int(record[:-1].split('|')[6]) if len(record[:-1].split('|')[6]) > 0 else None,
            int(record[:-1].split('|')[7]) if len(record[:-1].split('|')[7]) > 0 else None,
            int(record[:-1].split('|')[8]) if len(record[:-1].split('|')[8]) > 0 else None,
        )
        for record in records
    ]

    #print(records_list)

    
    db.create_all(app = create_app())

    app = create_app()
    with app.app_context():

        for user in user_list :   #('babe', 'rene', 'rene_babe', 'babe', 'rene_babe@darties.com', 1, None, None, 2021)

            new_user = User(  
                email='alexei.80@hotmail.fr', 
                name='alex', 
                password=generate_password_hash('alex', method='sha256'), 
                user_type='admin'
            )
            db.session.add(new_user)
        
            db.session.commit()
