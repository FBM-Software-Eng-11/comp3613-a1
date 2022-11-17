from App.models import *
from App.database import db

def create_vote(review_id, voter_id, voteType):
    review = Review.query.get(review_id)
    user = User.query.get(voter_id)
    if review and user:
        new_vote = Votes(review_id, voter_id, voteType)
        review.votes.append(new_vote)
        db.session.add(new_vote)
        db.session.commit()
        return new_vote
    return None