from ..extensions import db
from sqlalchemy.sql import func

class Posts(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.Date, default=func.current_date())
    category = db.Column(db.String(15), db.CheckConstraint("category IN ('Учеба', 'Практика', 'Конференция', 'Другое', 'Сбор данных')"), default='Другое')
    p_status = db.Column(db.String(10), db.CheckConstraint("p_status IN ('Active', 'Delete')"), default='Active')
    # for_all_groups = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=True)

    group = db.relationship('Groups', backref='posts', lazy='select')


    def __init__(self, title, content, category, p_status='Active', group_id=None):
        self.title = title
        self.content = content
        self.category = category
        self.p_status = p_status
        self.group_id = group_id