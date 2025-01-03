from ..extensions import db

class StudGroupList(db.Model):
    __tablename__ = 'stud_group_list'

    sgl_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(6))
    student_fio = db.Column(db.String(100))

    def __init__(self, student_fio, group_name):
        self.student_fio = student_fio
        self.group_name = group_name

