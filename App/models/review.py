from App.database import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    reviewType = db.Column(db.String(1000), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    votes = db.Column(MutableDict.as_mutable(JSON), nullable=False)

    def __init__(self, user_id, student_id, text):
        self.user_id = user_id
        self.student_id = student_id
        self.text = text
        self.votes = {"num_upvotes": 0, "num_downvotes": 0}

    def vote(self, user_id, vote):
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
        )

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

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "student_id": self.student_id,
            "text": self.text,
            "karma": self.get_karma(),
            "num_upvotes": self.get_num_upvotes(),
            "num_downvotes": self.get_num_downvotes(),
        }
