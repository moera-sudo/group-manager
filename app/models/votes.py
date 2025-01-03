from ..extensions import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY


class Votes(db.Model):
    __tablename__ = 'votes'

    vote_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    creation_date = db.Column(db.Date, default=func.current_date())
    deadline = db.Column(db.Date)
    answers = db.Column(ARRAY(db.String))
    v_status = db.Column(db.String, db.CheckConstraint("v_status IN ('Active', 'Closed' , 'Delete')"), default='Active')
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=True)

    group = db.relationship('Groups', backref='votes', lazy='select')

    def __init__(self, title, deadline, answers, v_status='Active', group_id=None):
        self.title = title
        self.deadline = deadline
        self.answers = answers
        self.v_status = v_status
        self.group_id = group_id
