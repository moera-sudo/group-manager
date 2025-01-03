from ..extensions import db

class SFamilyInfo(db.Model):
    __tablename__ = 's_family_info'

    family_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_info.student_id', ondelete='CASCADE'))

    #главная информация о матере/мачехе
    mother_parent_type = db.Column(db.String(10), db.CheckConstraint("mother_parent_type IS NULL OR mother_parent_type in('Мать', 'Мачеха', 'Нету')"), nullable=True)
    mother_name = db.Column(db.String(20), nullable=True)#Имя
    mother_surname = db.Column(db.String(50), nullable=True)#Фамилия
    mother_last_name = db.Column(db.String(50), nullable=True)#отчество
    mother_phone_number = db.Column(db.String(15), db.CheckConstraint("mother_phone_number IS NULL OR mother_phone_number ~ '^\+?\d{10,15}$'"), nullable=True)
    mother_birthday = db.Column(db.Date, nullable=True)

    #дополнительная информация о матере/мачехе
    mother_workplace = db.Column(db.String(50), nullable=True)
    mother_education_info = db.Column(db.String(15), db.CheckConstraint("mother_education_info IS NULL OR mother_education_info in('Нет образования', 'Начальное', 'Среднее', 'Среднее профессиональное', 'Высшее', 'Послевузовское')"), nullable=True)
    mother_social_status = db.Column(db.String(15), db.CheckConstraint("mother_social_status IS NULL OR mother_social_status in('Безработный', 'Инвалид', 'Пенсионер', 'Работающий', 'Самозанятый')"), nullable=True)

    #главная информация об отце/отчиме
    father_parent_type = db.Column(db.String(10), db.CheckConstraint("father_parent_type IS NULL OR father_parent_type in('Отец', 'Отчим', 'Нету')"), nullable=True)
    father_name = db.Column(db.String(20), nullable=True)#Имя
    father_surname = db.Column(db.String(50), nullable=True)#Фамилия
    father_last_name = db.Column(db.String(50), nullable=True)#отчество
    father_phone_number = db.Column(db.String(15), db.CheckConstraint("father_phone_number IS NULL OR father_phone_number ~ '^\+?\d{10,15}$'"), nullable=True)
    father_birthday = db.Column(db.Date, nullable=True)

    #дополнительная информация о отце/отчиме
    father_workplace = db.Column(db.String(50), nullable=True)
    father_education_info = db.Column(db.String(15), db.CheckConstraint("father_education_info IS NULL OR father_education_info in('Нет образования', 'Начальное', 'Среднее', 'Среднее профессиональное', 'Высшее', 'Послевузовское')"), nullable=True)
    father_social_status = db.Column(db.String(15), db.CheckConstraint("father_social_status IS NULL OR father_social_status in('Безработный', 'Инвалид', 'Пенсионер', 'Работающий', 'Самозанятый')"), nullable=True)

    #главная информация об опекуне
    guardian_parent_type = db.Column(db.String(10), db.CheckConstraint("guardian_parent_type IS NULL OR guardian_parent_type in('Есть', 'Нету')"), nullable=True)
    guardian_name = db.Column(db.String(20), nullable=True)#Имя
    guardian_surname = db.Column(db.String(50), nullable=True)#Фамилия
    guardian_last_name = db.Column(db.String(50), nullable=True)#отчество
    guardian_phone_number = db.Column(db.String(15), db.CheckConstraint("guardian_phone_number IS NULL OR guardian_phone_number ~ '^\+?\d{10,15}$'"), nullable=True)
    guardian_birthday = db.Column(db.Date, nullable=True)

    #дополнительная информация о опекуне
    guardian_workplace = db.Column(db.String(50), nullable=True)
    guardian_education_info = db.Column(db.String(15), db.CheckConstraint("guardian_education_info IS NULL OR guardian_education_info in('Нет образования', 'Начальное', 'Среднее', 'Среднее профессиональное', 'Высшее', 'Послевузовское')"), nullable=True)
    guardian_social_status = db.Column(db.String(15), db.CheckConstraint("guardian_social_status IS NULL OR guardian_social_status in('Безработный', 'Инвалид', 'Пенсионер', 'Работающий', 'Самозанятый')"), nullable=True)

    # Удаляем backref здесь
    student = db.relationship('StudentInfo', 
                               back_populates='family_info', 
                               foreign_keys=[student_id],
                               uselist=False)
    
    def __init__(self, 
             student_id=None, 
             mother_parent_type=None, 
             mother_name=None, 
             mother_surname=None, 
             mother_last_name=None, 
             mother_address_id=None, 
             mother_phone_number=None, 
             mother_birthday=None, 
             mother_workplace=None, 
             mother_education_info=None, 
             mother_social_status=None, 
             father_parent_type=None, 
             father_name=None, 
             father_surname=None, 
             father_last_name=None, 
             father_address_id=None, 
             father_phone_number=None, 
             father_birthday=None, 
             father_workplace=None, 
             father_education_info=None, 
             father_social_status=None, 
             guardian_parent_type=None, 
             guardian_name=None, 
             guardian_surname=None, 
             guardian_last_name=None, 
             guardian_address_id=None, 
             guardian_phone_number=None, 
             guardian_birthday=None, 
             guardian_workplace=None, 
             guardian_education_info=None, 
             guardian_social_status=None):
    
        self.student_id = student_id
        
        # Мать/Мачеха
        self.mother_parent_type = mother_parent_type
        self.mother_name = mother_name
        self.mother_surname = mother_surname
        self.mother_last_name = mother_last_name
        self.mother_address_id = mother_address_id
        self.mother_phone_number = mother_phone_number
        self.mother_birthday = mother_birthday
        self.mother_workplace = mother_workplace
        self.mother_education_info = mother_education_info
        self.mother_social_status = mother_social_status
        
        # Отец/Отчим
        self.father_parent_type = father_parent_type
        self.father_name = father_name
        self.father_surname = father_surname
        self.father_last_name = father_last_name
        self.father_address_id = father_address_id
        self.father_phone_number = father_phone_number
        self.father_birthday = father_birthday
        self.father_workplace = father_workplace
        self.father_education_info = father_education_info
        self.father_social_status = father_social_status
        
        # Опекун
        self.guardian_parent_type = guardian_parent_type
        self.guardian_name = guardian_name
        self.guardian_surname = guardian_surname
        self.guardian_last_name = guardian_last_name
        self.guardian_address_id = guardian_address_id
        self.guardian_phone_number = guardian_phone_number
        self.guardian_birthday = guardian_birthday
        self.guardian_workplace = guardian_workplace
        self.guardian_education_info = guardian_education_info
        self.guardian_social_status = guardian_social_status