from App.database import db

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"), nullable=False, unique=True)
    voter_id = db.Column(db.Integer, db.ForeignKey("review.id"), nullable=False, unique=True)
    date = db.Column(db.Date, nullable=False)
    voteType = db.Column(db.String(1000), nullable=False)

    review = db.relationship(
        "Review", backref="review", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, review_id):
        self.review_id = review_id
        self.upvotes = 0
        self.downvotes = 0

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