__author__ = 'Donal_Carpenter'

from flask import Blueprint, jsonify, request, render_template, flash, Response, redirect, url_for
from security.models import UserForm
from security.oauth import OAuthSignIn
from flask.ext.security import login_required, current_user, login_user
from security.models import User
from mongoengine import Q

profile_blueprint =  Blueprint('profile', __name__, url_prefix='/authorize')

@profile_blueprint.route('/')
@login_required
def profile():
    uf = UserForm()
    uf.email = current_user.email
    return render_template('security/user_profile.html', user_profile_form=uf)


@profile_blueprint.route('/init/<provider>')
def authorize(provider):
    if not current_user.is_anonymous():
        return url_for('home')
    provider = OAuthSignIn.get_provider(provider)
    if(provider == None):
        return Response("Provider not recognized", 404)
    return provider.authorize()

@profile_blueprint.route('/callback/<provider_name>')
def callback(provider_name):
    if not current_user.is_anonymous():
        return url_for("lolcat.home")
    provider = OAuthSignIn.get_provider(provider_name)
    if(provider == None):
        return Response("Provider not recognized", 404)
    social_id, email = provider.callback()
    #social_id, email= ("facebook$12234", 'donal.carpenter@yahoo.com')
    user = User.objects(Q(social_provider=provider_name) & Q(social_id=social_id)).first()
    if user == None:
        user = User(email=email, social_provider=provider_name, social_id=social_id)
        user.save()
        flash("Your account has been created. enjoy the lols and the cats")
    login_user(user)
    return redirect(url_for("lolcat.home"))


