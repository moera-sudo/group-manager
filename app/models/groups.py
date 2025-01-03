from ..extensions import db


class Groups(db.Model):
    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(6), nullable=False)
    group_code = db.Column(db.String(10), nullable=True)
    courator = db.Column(db.String(100), nullable=True)
    headman = db.Column(db.String(100), nullable=True)

    def __init__(self, group_name, group_code=None, courator=None, headman=None):
        self.group_name = group_name
        self.group_code = group_code
        self.courator = courator
        self.headman = headman

    