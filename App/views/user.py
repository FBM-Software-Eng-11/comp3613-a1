from flask import Blueprint, render_template, jsonify, request, send_from_directory,flash,redirect
from flask_jwt import jwt_required, current_identity
from flask_login import LoginManager, current_user, login_user, login_required, login_manager, login_required
from .forms import SignUp, LogIn


from App.controllers import *


user_views = Blueprint("user_views", __name__, template_folder="../templates")


#loggs in the user
@user_views.route('/auth',methods=['POST'])
def logsIn_user():
    data = request.form
    user = authenticate(data['username'], data['password'])
    if user == None:
        flash('Wrong Username or Password!')
        form = LogIn()
        return render_template("login.html", form=form)
    login_user(user, remember=True)
    return render_template('users.html', users =get_all_users(), current_user= current_user)

#loggs out the user
@user_views.route('/logout')
@login_required
def logout():
    logout_user()
    flash ('You have been logged out')
    return render_template("login.html", form=LogIn())

# List all users
@user_views.route("/api/users", methods=["GET"])
@login_required
def get_users_action():
    return render_template('users.html', users =get_all_users(), current_user= current_user)



# Delete user route
# Must be an admin to access this route
@user_views.route("/api/users/delete/<int:user_id>")
@login_required
def delete_user_action(user_id):
    user = get_user(user_id)
    if user:
        reviews = get_reviews_by_user(user_id)
        for review in reviews:
            delete_review(review.id)
        delete_user(user_id)
        flash("User Deleted!")
        return render_template('users.html', users =get_all_users(), current_user= current_user)
    flash('User not found! ')
    return render_template('users.html', users =get_all_users(), current_user= current_user)
