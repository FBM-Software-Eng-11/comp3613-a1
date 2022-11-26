from flask import Blueprint, redirect, render_template, request, send_from_directory, flash
from flask_login import LoginManager, current_user, login_user, login_required, login_manager, login_required
from flask import Flask, redirect
from .forms import SignUp, LogIn
index_views = Blueprint("index_views", __name__, template_folder="../templates")

from App.controllers import *

const_url = "https://8080-fbmsoftwaree-comp3613a1-moaazqix6k3.ws-us77.gitpod.io"

@index_views.route("/login", methods=["GET"])
def login_page():
  if request.method == 'GET':
    form = LogIn()
    return render_template("login.html", form=form)
  
  '''if request.method == "POST":
    form = LogIn()
    if form.validate_on_submit():
        data = request.form
        user = User.query.filter_by(username = data['username']).first()
        if user and user.check_password(data['password']):
          flash('Logged in successfully.')
          login_user(user,True)
          return redirect(const_url+"/identify")
    flash('Invalid credentials')
    return redirect(const_url+"/login")'''

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
        return  redirect(const_url+"/signup")
      newuser = create_user(username=data['username'], password=data['password'])
      flash('Account Created!')
      #form = LogIn()
      return redirect(const_url+"/login")
  flash('Error invalid input!')
  return  redirect(const_url+"/signup")


@index_views.route('/reviews', methods=['GET', 'POST'])
@login_required
def reviews_page():
  if request.method == 'GET':
    user = current_user
    return render_template('reviews_page.html', user = user)

@index_views.route('/students', methods=['GET', 'POST'])
@login_required
def student_page():
  if request.method == 'GET':
    return render_template('students.html')
