from flask import Blueprint, redirect, render_template, request, send_from_directory, flash
from flask_login import LoginManager, current_user, login_user, login_required, login_manager, login_required
from flask import Flask, redirect
from .forms import SignUp, LogIn
index_views = Blueprint("index_views", __name__, template_folder="../templates")

from App.controllers import *


@index_views.route("/", methods=["GET"])
def login_page():
  if request.method == 'GET':
    form = LogIn()
    return render_template("login.html", form=form)

@index_views.route("/admin")
def create_admin():
  newuser = create_user(username='admin', password='admin', access=2)
  flash('Account Created!')
  form = LogIn()
  return render_template("login.html", form=form)



