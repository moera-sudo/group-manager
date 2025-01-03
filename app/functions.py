from datetime import time, datetime

#Следующие функции были перенесены сюда во избежание излишней громоздкости кода роута
#--Функционал личного кабинета--
def _process_student_info(student, form_data):
    """Process basic student information"""

    student.surname = form_data.get('surname') or None
    student.name = form_data.get('name') or None
    student.last_name = form_data.get('last_name') or None
    

    if form_data.get('birthday'):
        student.birthday = datetime.strptime(form_data['birthday'], '%Y-%m-%d').date()
    else:
        student.birthday = None
    
    student.iin = form_data.get('iin') or None
    student.phone_number = form_data.get('phonenumber') or None
    
    student.gender = form_data.get('gender') or None
    student.education_type = form_data.get('education_type') or None
    student.course = form_data.get('course') or None
    student.hobby = form_data.get('hobby') or None
    
    student.nationality = form_data.get('nationality') or None
    student.citizenship = form_data.get('citizenship') or None
    
    student.special_needs = form_data.get("special_needs") or None
    
    if student.special_needs == 'Присутствуют':
        student.is_invalid = form_data.get('is_invalid') or None
        student.is_have_psyphis_qualities = form_data.get('is_have_psyphis_qualities') or None
        student.is_ifm = form_data.get('is_ifm') or None
        student.is_underachiever = form_data.get('is_underachiever') or None
        student.is_orphan = form_data.get('is_orphan') or None
    else:
        student.special_needs = 'Отсутствуют'
        student.is_invalid = 'Нет'
        student.is_have_psyphis_qualities = 'Нет'
        student.is_ifm = 'Нет'
        student.is_underachiever = 'Нет'
        student.is_orphan = 'Нет'
    
    if form_data.get('citizenship', '').lower() != 'казахстан':
        student.registration = form_data.get('registration') or None
        if form_data.get('doc_validity_period'):
            student.doc_validity_period = datetime.strptime(form_data['doc_validity_period'], '%Y-%m-%d').date()
        else:
            student.doc_validity_period = None
    else:
        student.registration = None
        student.doc_validity_period = None
    
    student.social_status = form_data.get('social_status') or None
    if student.social_status == 'Неполная семья':
        student.lost_parent = form_data.get('lost_parent') or None
        student.retired_parents = form_data.get('retired_parents') or None
        student.is_large_family = form_data.get('is_large_family') or None
    else:
        student.lost_parent = 'Нету'
        student.retired_parents = 'Нету'
        student.is_large_family = 'Нет'
    
    try:
        student.childs_count = int(form_data.get('childs_count'))
    except (ValueError, TypeError):
        student.childs_count = None
    
    return student
    

def _process_getAdress(adress, form_data, prefix):
    adress.city = form_data.get(f'{prefix}-City')
    adress.district = form_data.get(F'{prefix}-District')
    adress.street = form_data.get(F'{prefix}-Street')
    adress.house = form_data.get(F'{prefix}-House')
    adress.entrance = form_data.get(F'{prefix}-Entrance') or None
    adress.floor = form_data.get(F'{prefix}-Floor') or None
    adress.flat = form_data.get(F'{prefix}-Flat') or None

    return adress


def _process_getParent(family, form_data, who, student_id):
    family.student_id = student_id
    if who == 'mother':
        family.mother_parent_type = form_data.get('mother_parent_type') or None
        family.mother_name = form_data.get('mother_name') or None
        family.mother_surname = form_data.get('mother_surname') or None 
        family.mother_last_name = form_data.get('mother_last_name') or None 
        family.mother_phone_number = form_data.get('mother_phone_number') or None 
        family.mother_birthday = form_data.get('mother_birthday') or None
 
        family.mother_workplace = form_data.get('mother_workplace') or None
        family.mother_education_info = form_data.get('mother_education_info') or None 
        family.mother_social_status = form_data.get('mother_social_status') or None

    elif who == 'father':
        family.father_parent_type = form_data.get('father_parent_type') or None
        family.father_name = form_data.get('father_name') or None
        family.father_surname = form_data.get('father_surname') or None 
        family.father_last_name = form_data.get('father_last_name') or None
        family.father_phone_number = form_data.get('father_phone_number') or None
        family.father_birthday = form_data.get('father_birthday') or None

        family.father_workplace = form_data.get('father_workplace') or None
        family.father_education_info = form_data.get('father_education_info') or None
        family.father_social_status = form_data.get('father_social_status') or None

    elif who == 'guardian':
        family.guardian_parent_type = form_data.get('guardian_parent_type') or None
        family.guardian_name = form_data.get('guardian_name') or None 
        family.guardian_surname = form_data.get('guardian_surname') or None
        family.guardian_last_name = form_data.get('guardian_last_name') or None
        family.guardian_phone_number = form_data.get('guardian_phone_number') or None
        family.guardian_birthday = form_data.get('guardian_birthday') or None

        family.guardian_workplace = form_data.get('guardian_workplace') or None
        family.guardian_education_info = form_data.get('guardian_education_info') or None
        family.guardian_social_status = form_data.get('guardian_social_status') or None




    return family
        
        


