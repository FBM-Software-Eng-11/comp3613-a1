from App.database import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict
from datetime import datetime


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    reviewType = db.Column(db.String(1000), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    votes = db.relationship(
        "Votes", backref="review", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, user_id, student_id, text, reviewType):
        self.user_id = user_id
        self.student_id = student_id
        self.text = text
        self.reviewType = reviewType
        self.date = datetime.now()

    '''def vote(self, user_id, vote):
        self.votes.update({user_id: vote})
        self.votes.update(
            {"num_upvotes": len([vote for vote in self.votes.values() if vote == "up"])}
        )
        self.votes.update(
            {
                "num_downvotes": len(
                    [vote for vote in self.votes.values() if vote == "down"]
                )
            }
        )'''
    def get_time(self):
        return self.date
     
    def get_review_karma(self):
        karma = 0
        if self.reviewType == "positive":
            karma += 20
            for vote in self.votes:
                if vote.voteType == "up" :
                    karma += 1
                else:
                    karma -=1
        else:
            karma -= 10
            for vote in self.votes:
                if vote.voteType == "up" :
                    karma -= 1
                else:
                    karma +=1
        return karma

    def get_num_upvotes(self):
        upvotes = 0
        for vote in self.votes:
            if vote.voteType == "up":
                upvotes += 1
        return upvotes

    def get_num_downvotes(self):
        downvotes = 0
        for vote in self.votes:
            if vote.voteType == "down":
                downvotes += 1
        return downvotes
    

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "student_id": self.student_id,
            "time": self.date,
            "review type": self.reviewType,
            "text": self.text,
            "karma": self.get_review_karma(),
            "num_upvotes": self.get_num_upvotes(),
            "num_downvotes": self.get_num_downvotes(),
        }
