from flask import Blueprint, render_template 
from flask_login import login_required, current_user


main_init = Blueprint('main_init', __name__)


@main_init.route('/')
def index():
    return render_template('index_login.html')



@main_init.route('/profile')
@login_required
def profile():

    id_profil_to_user_type = { 1 : 'directeur général', 2 : 'directeur régional', 3 : 'responsable de magasin'}

    return render_template(
        'profile.html', 
        prenom=current_user.prenom,
        nom=current_user.nom,
        email=current_user.mail,
        user_type=id_profil_to_user_type[current_user.id_profil],
        id_profil=current_user.id_profil,
        id_region=current_user.id_region,
        id_magasin=current_user.id_magasin
    )





if __name__ == "__main__":
    
    app.run(debug=True)

