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


# Get user by id route
# Must be an admin to access this route
@user_views.route("/api/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_action(user_id):
    if not current_identity.is_admin():
        return jsonify({"message": "Access denied"}), 403
    user = get_user(user_id)
    if user:
        return jsonify(user.to_json()), 200
    return jsonify({"message": "User not found"}), 404


# Delete user route
# Must be an admin to access this route
@user_views.route("/api/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_action(user_id):
    if not current_identity.is_admin():
        return jsonify({"message": "Access denied"}), 403
    user = get_user(user_id)
    if user:
        delete_user(user_id)
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404


# Get user by access level route
# Must be an admin to access this route
@user_views.route("/api/users/access/<int:access_level>", methods=["GET"])
@jwt_required()
def get_user_by_access_action(access_level):
    if not current_identity.is_admin():
        return jsonify({"message": "Access denied"}), 403
    users = get_users_by_access(access_level)
    if users:
        return jsonify([user.to_json() for user in users]), 200
    return jsonify({"message": "No users found"}), 404
