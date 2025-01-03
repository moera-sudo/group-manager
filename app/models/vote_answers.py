from ..extensions import db
from sqlalchemy.sql import func


class VoteAnswers(db.Model):
    __tablename__ = "vote_answers"

    answer_id = db.Column(db.Integer, primary_key=True)
    vote_id = db.Column(db.Integer, db.ForeignKey('votes.vote_id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), nullable=False)
    answer = db.Column(db.String)

    vote = db.relationship('Votes', backref='vote_answers', lazy='select')

    account = db.relationship('Accounts', backref='vote_answers', lazy='select')

    def __init__(self, vote_id, account_id, answer):
        self.vote_id = vote_id
        self.account_id = account_id
        self.answer = answer

    