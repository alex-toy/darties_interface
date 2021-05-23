from create_app import *
from models import User
from werkzeug.security import generate_password_hash, check_password_hash



if __name__ == "__main__":

    
    db.create_all(app = create_app())

    app = create_app()
    with app.app_context():

        new_user = User(
            email='alexei.80@hotmail.fr', 
            name='alex', 
            password=generate_password_hash('alex', method='sha256'), 
            user_type='admin'
        )
        db.session.add(new_user)
        
        new_user = User(
            email='splaya@agapei.asso.fr', 
            name='splaya', 
            password=generate_password_hash('splaya', method='sha256'), 
            user_type='dir_gen'
        )
        db.session.add(new_user)
        
        new_user = User(
            email='touaaatimahe@gmail.com', 
            name='touaaatimahe', 
            password=generate_password_hash('touaaatimahe', method='sha256'), 
            user_type='dir_reg1'
        )
        db.session.add(new_user)

        new_user = User(
            email='oussama.garraouii@gmail.com', 
            name='oussama', 
            password=generate_password_hash('oussama', method='sha256'), 
            user_type='dir_reg2'
        )
        db.session.add(new_user)
        
        
        db.session.commit()
