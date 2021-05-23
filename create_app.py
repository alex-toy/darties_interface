from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
I from flask_login import LoginManager 
#from flask_login_multi.login_manager import LoginManager 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)

    with app.app_context():

        login_manager = LoginManager()
        #login_manager = LoginManager(app)   

        login_manager.blueprint_login_views = {  
            'user':  "user.user_login",  
            'admin': "admin.admin_login",  
        }

        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        from models import User

        # @login_manager.user_loader
        # def load_user(user_id):
        #     return User.query.get(int(user_id))

        @login_manager.user_loader
        def load_user(user_id, endpoint='user'):
            if endpoint == 'admin':
                return Admin.query.get(int(user_id))
            else:
                return User.query.get(int(user_id))

        from auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        return app


if __name__ == "__main__":

    app = create_app()
    
    app.run(debug=True)

