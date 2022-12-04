from flask import Blueprint, jsonify, request, redirect, render_template, request, send_from_directory, flash
from flask_jwt import jwt_required, current_identity
from flask_login import LoginManager, current_user, login_user, login_required, login_manager, login_required
from App.models import *
from App.controllers import *


student_views = Blueprint("student_views", __name__, template_folder="../templates")


# Lists all students
@student_views.route("/api/students", methods=["GET"])
@login_required
def get_all_students_action():
    students = get_all_students()
    return render_template('students.html', user = current_user, students = get_all_students())


# Create student given name, programme and faculty
# Must be an admin to access this route
@student_views.route("/api/students", methods=["POST"])
@login_required
def create_student_action():
    if current_user.is_admin():
        data = request.form
        student = create_student(
            name=data["studentFirstName"] +" " +data["studentLastName"], programme=data["studentProgramme"], faculty=data["studentFaculty"]
        )
        if student:
            flash('Student Created!')
            return render_template('students.html', user = current_user, students = get_all_students())
        flash('Error Creating Student!')
        return render_template('students.html', user = current_user, students = get_all_students())


# Deletes a student given student id
# Must be an admin to access this route
@student_views.route("/api/students/delete/<int:student_id>")
@login_required
def delete_student_action(student_id):
    if current_user.is_admin():
        outcome = delete_student(student_id)
        reviews = get_reviews_by_student(student_id)
        for review in reviews:
            delete_review(review.id)
        if outcome:
            flash('Student Deleted!')
            return render_template('students.html', user = current_user, students = get_all_students())
        flash('Student Not Deleted!')
        return render_template('students.html', user = current_user, students = get_all_students())
    

