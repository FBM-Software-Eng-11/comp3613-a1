from flask import Blueprint, redirect, render_template, request, send_from_directory, flash
from flask_login import LoginManager, current_user, login_user, login_required, login_manager, login_required
from flask import Flask, redirect
from .forms import SignUp, LogIn
index_views = Blueprint("index_views", __name__, template_folder="../templates")

from App.controllers import *


@index_views.route("/login", methods=["GET"])
def login_page():
  if request.method == 'GET':
    form = LogIn()
    return render_template("login.html", form=form)

@index_views.route('/signup', methods=['GET', 'POST'])
def signup_page():

  if request.method == 'GET':
    form = SignUp() 
    return render_template('signup.html', form=form) 
  
  if request.method == 'POST':
    form = SignUp() 
    if form.validate_on_submit():
      data = request.form
      if get_user_by_username(data["username"]):
        flash('Username already taken!') 
        return render_template("signup.html", form=form)
      newuser = create_user(username=data['username'], password=data['password'])
      flash('Account Created!')
      form = LogIn()
      return render_template("login.html", form=form)
  flash('Error invalid input!')
  return render_template("signup.html", form=form)


