from ..extensions import db
from flask_login import UserMixin
from .student_info import StudentInfo

class Accounts(db.Model, UserMixin):
    __tablename__ = 'accounts'

    account_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, db.CheckConstraint("email ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}$'"), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    chat_id = db.Column(db.String, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_info.student_id', ondelete='CASCADE'), nullable=True)
    acc_type = db.Column(db.String, db.CheckConstraint("acc_type IN ('student', 'headman', 'admin', 'curator')"), nullable=False,)
    isAuthorize = db.Column(db.Boolean, default=False, nullable=False)

    # Исправлено название модели на 'StudentInfo' с заглавной буквы
    student = db.relationship('StudentInfo', back_populates='accounts', uselist=False)
    

    def __init__(self, name, email, password, chat_id=None, student_id=None, acc_type='student', isAuthorize=False):
        self.name = name
        self.email = email
        self.password = password
        self.chat_id = chat_id
        self.student_id = student_id
        self.acc_type = acc_type
        self.isAuthorize = isAuthorize

    def get_id(self):
        return str(self.account_id)