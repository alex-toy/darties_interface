from create_app import *
from models import User
from werkzeug.security import generate_password_hash, check_password_hash




def create_users() :

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

    
    db.create_all(app = create_app())

    app = create_app()
    with app.app_context():

        for user in user_list :   

            new_user = User(  
                nom=user[0], 
                prenom=user[1], 
                login=user[2], 
                pwd=generate_password_hash(user[3], method='sha256'),
                mail=user[4],
                id_profil=user[5],
                id_region=user[6],
                id_magasin=user[7]
            )
            db.session.add(new_user)
        
            db.session.commit()




def show_users() :

    myfile = open("data/staging_utilisateur_000", "r")
    records = myfile.readlines()
    myfile.close()
    print(records)





if __name__ == "__main__":

    #create_users()

    show_users()

# babe|rene|rene_babe|babe|rene_babe@darties.com|1|||2021
# playa|stephanie|stephanie_playa|playa|splaya31@gmail.com|2|1||2021
# rea|alessio|alessio_rea|rea|alessio_rea@darties.com|2|2||2021
# garraouii|oussama|oussama_garraouii|garraouii|oussama.garraouii@gmail.com|3||1|2021
# touati|mahe|mahe_touati|touati|touaaatimahe@gmail.com|3||11|2021
# perrin|aenor|aenor_perrin|perrin|aenor_perrin@darties.com|3||47|2021