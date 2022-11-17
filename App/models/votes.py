from App.database import db
from datetime import datetime

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"), nullable=False, unique=False)
    voter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=False)
    date = db.Column(db.Date, nullable=False)
    voteType = db.Column(db.String(1000), nullable=False)

    def __init__(self, review_id, voter_id, voteType):
        self.review_id = review_id
        self.voter_id = voter_id
        self.voteType = voteType
        self.date = datetime.now()

    # def addUpVote(self, rev_id):
    #     vote = Votes.query.filter_by(review_id=rev_id).first()
    #     vote.upvotes = vote.upvotes + 1
    
    # def removeUpVote(self, rev_id):
    #     vote = Votes.query.filter_by(review_id=rev_id).first()
    #     vote.upvotes = votes.upvotes - 1
    
    # def addDownVote(self, rev_id):
    #     vote = Votes.query.filter_by(review_id=rev_id).first()
    #     vote.downvotes = vote.downvotes + 1
    
    # def removeDownVote(self, rev_id):
    #     vote = Votes.query.filter_by(review_id=rev_id).first()
    #     vote.upvotes = vote.downvotes - 1

    # def to_json(self):
    #     return {"id": self.id, 
    #     "review_id": self.review_id, 
    #     "upvotes": self.upvotes,
    #     "downvotes": self.downvotes
    #     }