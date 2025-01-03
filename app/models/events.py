from ..extensions import db
from sqlalchemy.sql import func

class Events(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    creation_date = db.Column(db.Date, default=func.current_date())
    date = db.Column(db.Date)
    icon = db.Column(db.String, db.CheckConstraint("icon IN ('card_giftcard', 'celebration', 'group')"), default='group')
    e_status = db.Column(db.String(10), db.CheckConstraint("e_status IN ('Active', 'Delete')"), default='Active')
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=True)

    group = db.relationship('Groups', backref='events', lazy='select')

    def __init__(self, title, icon , date , e_status='Active', group_id=None):
        self.title = title
        self.icon = icon
        self.date = date
        self.e_status = e_status
        self.group_id = group_id
