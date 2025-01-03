from ..extensions import db
from .groups import Groups
from .familyInfo import SFamilyInfo
from .addresses import Addresses


class StudentInfo(db.Model):
    __tablename__ = 'student_info'

    student_id = db.Column(db.Integer, primary_key=True)

    #--Основная информация
    name = db.Column(db.String(20), nullable=True)  # Имя
    surname = db.Column(db.String(50), nullable=True)  # Фамилия
    last_name = db.Column(db.String(50), nullable=True)  # отчество
    birthday = db.Column(db.Date, nullable=True)
    iin = db.Column(db.String(12), unique=True, nullable=True)
    phone_number = db.Column(db.String(15), db.CheckConstraint("phone_number IS NULL OR phone_number ~ '^\+?\d{10,15}$'"), nullable=True)
    gender = db.Column(db.String(15), db.CheckConstraint("gender IS NULL OR gender IN ('Женский', 'Мужской')"), nullable=True)
    education_type = db.Column(db.String(10), db.CheckConstraint("education_type IS NULL OR education_type IN ('Грант', 'Бюджет')"), nullable=True)
    course = db.Column(db.Integer, db.CheckConstraint("course IS NULL OR course IN ('1', '2', '3')"), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id', ondelete='CASCADE'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=True)
    student_status = db.Column(db.String(20), db.CheckConstraint("student_status is Null or student_status in('Учащийся', 'Отчислен')"), nullable=True, default='Учащийся')

    #--Дополнительная информация
    hobby = db.Column(db.String(100), nullable=True)
    special_needs = db.Column(db.String(15), db.CheckConstraint("special_needs IS NULL OR special_needs IN ('Присутствуют', 'Отсутствуют')"), nullable=True)
    is_invalid = db.Column(db.String(10), db.CheckConstraint("is_invalid IS NULL OR is_invalid IN ('Да', 'Нет')"), nullable=True)
    is_have_psyphis_qualities = db.Column(db.String(10), db.CheckConstraint("is_have_psyphis_qualities IS NULL OR is_have_psyphis_qualities IN ('Да', 'Нет')"), nullable=True)
    is_underachiever = db.Column(db.String(10), db.CheckConstraint("is_underachiever IS NULL OR is_underachiever IN ('Да', 'Нет')"), nullable=True)
    is_ifm = db.Column(db.String(10), db.CheckConstraint("is_ifm IS NULL OR is_ifm IN ('Да', 'Нет')"), nullable=True)
    is_orphan = db.Column(db.String(10), db.CheckConstraint("is_orphan IS NULL OR is_orphan IN ('Да', 'Нет')"), nullable=True) 

    #--Гражданский статус
    nationality = db.Column(db.String(50), nullable=True)
    citizenship = db.Column(db.String(50), nullable=True)
    registration = db.Column(db.String(10), db.CheckConstraint("registration IS NULL OR registration IN ('РВП', 'ВНЖ')"), nullable=True)
    doc_validity_period = db.Column(db.Date, nullable=True)

    #--Семья
    social_status = db.Column(db.String(20), db.CheckConstraint("social_status IS NULL OR social_status IN ('Полная семья', 'Неполная семья')"), nullable=True)
    lost_parent = db.Column(db.String(20), db.CheckConstraint("lost_parent IS NULL OR lost_parent IN ('Нету', 'Мать', 'Отец', 'Оба')"), nullable=True)
    retired_parents = db.Column(db.String(20), db.CheckConstraint("retired_parents IS NULL OR retired_parents IN ('Нету', 'Мать', 'Отец', 'Оба')"), nullable=True)
    is_large_family = db.Column(db.String(20), db.CheckConstraint("is_large_family IS NULL OR is_large_family IN ('Да', 'Нет')"), nullable=True)
    childs_count = db.Column(db.Integer, nullable=True)

    #--Информация о проживании
    live_with_whom = db.Column(db.String(30), nullable=True)
    ownership_form = db.Column(db.String(20), db.CheckConstraint("ownership_form IS NULL OR ownership_form IN ('Общежитие', 'Съемная', 'Собственная')"), nullable=True)

    #--Информация об 'откуда прибыл'
    ex_school = db.Column(db.String(50), nullable=True)
    from_where_country = db.Column(db.String(50), nullable=True)
    ex_address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id', ondelete='CASCADE'), nullable=True)

    #--Информация о 'Прописка'
    where_country = db.Column(db.String(50), nullable=True)
    reg_address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id', ondelete='CASCADE'), nullable=True)



    accounts = db.relationship('Accounts', back_populates='student', uselist=True)
    
    group = db.relationship('Groups', backref=db.backref('students', lazy='dynamic'))
    
    # Используем back_populates вместо backref
    family_info = db.relationship('SFamilyInfo', 
                                  back_populates='student', 
                                  uselist=False,  # Один к одному
                                  cascade='all, delete-orphan')  # Каскадное удаление
    
    live_address = db.relationship('Addresses', 
                                    foreign_keys=[address_id], 
                                    backref='primary_students',
                                    lazy='select')
    ex_address = db.relationship('Addresses', 
                                foreign_keys=[ex_address_id], 
                                backref='ex_students',
                                lazy='select')
    reg_address = db.relationship('Addresses', 
                                foreign_keys=[reg_address_id], 
                                backref='registered_students',
                                lazy='select')
    def __init__(self, 
             name=None, 
             surname=None, 
             last_name=None, 
             birthday=None, 
             iin=None, 
             phone_number=None, 
             gender=None, 
             education_type=None, 
             course=None, 
             address_id=None, 
             hobby=None, 
             special_needs=None, 
             is_invalid=None, 
             is_have_psyphis_qualities=None, 
             is_underachiever=None, 
             is_ifm=None, 
             is_orphan=None, 
             nationality=None, 
             citizenship=None, 
             registration=None, 
             doc_validity_period=None, 
             social_status=None,
             is_large_family=None,
             retired_parents=None,
             lost_parent=None,
             childs_count=None, 
             live_with_whom=None, 
             ownership_form=None, 
             ex_school=None, 
             from_where_country=None, 
             where_country=None,
             ex_address_id=None,
             reg_address_id=None,
             group_id=None,
             student_status=None):
    
        self.name = name
        self.surname = surname
        self.last_name = last_name
        self.birthday = birthday
        self.iin = iin
        self.phone_number = phone_number
        self.gender = gender
        self.education_type = education_type
        self.course = course
        self.address_id = address_id
        self.hobby = hobby
        self.special_needs = special_needs
        self.is_invalid = is_invalid
        self.is_have_psyphis_qualities = is_have_psyphis_qualities
        self.is_underachiever = is_underachiever
        self.is_ifm = is_ifm
        self.is_orphan = is_orphan
        self.nationality = nationality
        self.citizenship = citizenship
        self.registration = registration
        self.doc_validity_period = doc_validity_period
        self.social_status = social_status
        self.is_large_family = is_large_family
        self.retired_parents = retired_parents
        self.lost_parent = lost_parent
        self.childs_count = childs_count
        self.live_with_whom = live_with_whom
        self.ownership_form = ownership_form
        self.ex_school = ex_school
        self.from_where_country = from_where_country
        self.where_country = where_country
        self.group_id = group_id
        self.ex_address_id = ex_address_id
        self.reg_address_id = reg_address_id
        self.student_status = student_status