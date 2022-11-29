from flask import Blueprint, jsonify, request, redirect, render_template, request, send_from_directory, flash
from flask_login import LoginManager, current_user, login_user, login_required, login_manager, login_required
from flask_jwt import jwt_required, current_identity

from App.controllers import *
from App.models import *

review_views = Blueprint("review_views", __name__, template_folder="../templates")

#list all reviews
@review_views.route('/api/reviews', methods=['GET'])
@login_required
def reviews_page():
    reviews = get_all_reviews()
    return render_template('reviews.html', user = current_user, students = get_all_students(), reviews=get_all_reviews())

@review_views.route('/api/reviews/<int:studentId>', methods=['GET'])
@login_required
def getReviewsByStudent(studentId):
    reviews = get_reviews_by_student(studentId)
    return render_template('singleStudentReviews.html', user = current_user, student = get_student(studentId), reviews=get_reviews_by_student(studentId))

# Create review given user id, student id and text
@review_views.route("/api/reviews", methods=["POST"])
@login_required
def create_review_action():
    data = request.form
    review = create_review(
        user_id=current_user.id, student_id=data["student"], text=data["studentReview"], reviewType= data["reviewType"]
    )

    if review:
        flash('Review Created!')
        return render_template('reviews.html', user= current_user, studens = get_all_students(), reviews=get_all_reviews())
    flash("Error Creating Review!")
    return render_template('reviews.html', user= current_user, studens = get_all_students(), reviews=get_all_reviews())


# Gets review given review id
@review_views.route("/api/reviews/<int:review_id>", methods=["GET"])
@jwt_required()
def get_review_action(review_id):
    review = get_review(review_id)
    if review:
        return jsonify(review.to_json()), 200
    return jsonify({"error": "review not found"}), 404


# Votes on a post given post id and user id
@review_views.route("/api/reviews/<int:review_id>/vote/<string:vote>", methods=["POST"])
@login_required
def vote_review_action(review_id,vote):
    review = get_review(review_id)
    if review :
        vote = create_vote(review_id = review_id, voter_id = current_user.id, voteType = vote)
        if vote.voteType == 'up':
            flash("Review Upvoted!")
        else:
            flash("Review Downvoted!")
        return render_template('reviews.html', user = current_user, students = get_all_students(), reviews=get_all_reviews())
    flash('Error Voting!')
    return render_template('reviews.html', user = current_user, students = get_all_students(), reviews=get_all_reviews())

# Votes on a post given post id and user id
@review_views.route("/api/singleReviews/<int:review_id>/vote/<string:vote>/<int:studentId>", methods=["POST"])
@login_required
def vote_single_student_review_page(review_id,vote, studentId):
    review = get_review(review_id)
    if review :
        vote = create_vote(review_id = review_id, voter_id = current_user.id, voteType = vote)
        if vote.voteType == 'up':
            flash("Review Upvoted!")
        else:
            flash("Review Downvoted!")
        return render_template('singleStudentReviews.html', user = current_user, student = get_student(studentId), reviews=get_reviews_by_student(studentId))
    flash('Error Voting!')
    return render_template('singleStudentReviews.html', user = current_user, student = get_student(studentId), reviews=get_reviews_by_student(studentId))

# Updates post given post id and new text
# Only admins or the original reviewer can edit a review
@review_views.route("/api/reviews/<int:review_id>", methods=["PUT"])
@jwt_required()
def update_review_action(review_id):
    data = request.json
    review = get_review(review_id)
    if review:
        if current_identity.id == review.user_id or current_identity.is_admin():
            update_review(review_id, text=data["text"])
            return jsonify({"message": "post updated successfully"}), 200
        else:
            return jsonify({"error": "Access denied"}), 403
    return jsonify({"error": "review not found"}), 404


# Deletes post given post id
# Only admins or the original reviewer can delete a review
@review_views.route("/api/reviews/delete/<int:review_id>")
@login_required
def delete_review_action(review_id):
    review = get_review(review_id)
    if review:
        if current_user.id == review.user_id or current_user.is_admin():
            delete_review(review.id)
            flash("Review Deleted")
            return render_template('reviews.html', user = current_user, students = get_all_students(), reviews=get_all_reviews())
        else:
            flash("Review Not deleted")
            return render_template('reviews.html', user = current_user, students = get_all_students(), reviews=get_all_reviews())
    flash("Review Not found")
    return render_template('reviews.html', user = current_user, students = get_all_students(), reviews=get_all_reviews())

