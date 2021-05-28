from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main_init as main_init_blueprint
    app.register_blueprint(main_init_blueprint)

    from app_mag import main_mag as main_mag_blueprint
    app.register_blueprint(main_mag_blueprint)

    from app_reg import main_reg as main_reg_blueprint
    app.register_blueprint(main_reg_blueprint)

    from app_gen import main_app as main_app_blueprint
    app.register_blueprint(main_app_blueprint)

    from app_export import main_export as main_export_blueprint
    app.register_blueprint(main_export_blueprint)


    return app




# if __name__ == "__main__":

#     my_app = create_app()
    
#     app.run(debug=True)



my_app = create_app()