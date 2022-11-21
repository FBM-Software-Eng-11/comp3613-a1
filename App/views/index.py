from flask import Blueprint, redirect, render_template, request, send_from_directory
from .forms import SignUp, LogIn
index_views = Blueprint("index_views", __name__, template_folder="../templates")


@index_views.route("/", methods=["GET"])
def index_page():
    form = LogIn()
    return render_template("login.html", form=form)

@index_views.route('/signup', methods=['GET'])
def signup():
  form = SignUp() 
  return render_template('signup.html', form=form) 
