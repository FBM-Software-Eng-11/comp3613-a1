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
        
    def to_json(self):
        return {"id": self.id, 
        "review_id": self.review_id, 
        "voter_id": self.voter_id,
        "vote_type": self.voteType,
        "date":self.date
        }