import json
from flask import Blueprint, request, redirect, url_for, render_template, jsonify, flash, get_flashed_messages
from flask_login import login_required, current_user
from ..extensions import db, bcrypt, login_manager
from ..functions import _process_student_info, _process_getAdress, _process_getParent
from ..models.accounts import Accounts
from ..models.groups import Groups
from ..models.student_info import StudentInfo
from ..models.familyInfo import SFamilyInfo
from ..models.posts import Posts
from ..models.events import Events
from ..models.votes import Votes
from ..models.addresses import Addresses
from ..models.stud_group_list import StudGroupList
from datetime import datetime

student = Blueprint("student", __name__)


@student.route('/student/registration', methods=['GET', 'POST'])
def student_reg_view():
    print(request.method)
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form['r_password']).decode('utf-8')
        r_email = request.form['r_email']
        print(r_email, hashed_password)

        validate = Accounts.query.filter_by(email=r_email).first()
        # Сначала получаем группу по коду
        group = Groups.query.filter_by(group_code=request.form['r_group']).first()

        print(group.group_name, 'AFASDAD')
        print("Искомое ФИО:", request.form['r_fullname'])
        print("Искомая группа:", group.group_name)
        
        # Проверяем существование группы
        if not group:
            flash('Не найден код группы', 'error')
            print('GroupInputError')
            return redirect(url_for("student.student_reg_view"))

        # Теперь используем имя группы из найденной группы для проверки студента
        student_validate = StudGroupList.query.filter_by(
            group_name=group.group_name,  # Используем group_name из найденной группы
            student_fio=request.form['r_fullname']
        ).first()

        print('Валидация', student_validate)
        
        if not student_validate:
            flash('Вы не состоите в списке введеной группы', 'error')
            print('StudentValidateError')
            return redirect(url_for("student.student_reg_view"))
        
        if validate:
            flash('Данный электронный адрес уже зарегистрирован', 'error')
            print("ValidateError")
            return redirect(url_for("student.student_reg_view"))

        student_name = request.form['r_fullname']

        try:
            student_info = StudentInfo(group_id=group.group_id)
            print('Check', student_info)
            db.session.add(student_info)
            db.session.commit()
            user = Accounts(name=request.form['r_fullname'], email=request.form['r_email'], password=hashed_password, acc_type='student', student_id=student_info.student_id)
            print('check2', user)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("auth.auth_view"))
        
        except Exception as e:
            print(e)
            db.session.rollback()  # Добавил rollback при ошибке

    return render_template('student/RegistrationPage.html')

#TODO: FSDF
#! ALERT
# *
# ?

@student.route('/student/account_main/<int:user_id>')
@login_required
def student_main_view(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    
    group_name = Groups.query.filter_by(group_id=current_user.student.group.group_id).first().group_name
    events = Events.query.filter(Events.group_id == current_user.student.group.group_id,
                                Events.e_status=='Active',
                                Events.date >= datetime.now().date()).order_by(Events.date.asc()).limit(2).all()
    votes = Votes.query.filter(Votes.group_id == current_user.student.group.group_id,
                               Votes.v_status == 'Active').order_by(Votes.deadline.asc()).limit(2).all()

    return render_template('student/HomePage.html', group_name=group_name, events=events, votes=votes)


@student.route('/student/account_main/<int:user_id>/group', methods=['POST', 'GET'])
@login_required
def student_main_group(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    if request.method == 'POST':
        print('Высылка')
    
    group_list = StudGroupList.query.filter_by(group_name = current_user.student.group.group_name).order_by(StudGroupList.student_fio).all()

    group_info = Groups.query.filter_by(group_name = current_user.student.group.group_name).first()

    group_list_json = json.dumps([{"sgl_id": student.sgl_id, "group_name": student.group_name, "student_fio": student.student_fio} for student in group_list],
    ensure_ascii=False)

    students_count = len(group_list)

    return render_template('student/GroupPage.html', group_list_json = group_list_json,  group_info=group_info, students_count=students_count)


@student.route('/student/account_main/<int:user_id>/votes', methods=['GET', 'POST'])
@login_required
def student_main_votes(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))

    active_tab = 'All'

    if request.method == 'GET':
        active_tab = request.args.get("tab", "All")
    
    if active_tab == 'Active':
        votes = Votes.query.filter(
            Votes.group_id == current_user.student.group.group_id,
            Votes.v_status == 'Active').order_by(Votes.v_status, Votes.deadline.desc()).all()
        
    elif active_tab == 'Closed':
        votes = Votes.query.filter(
            Votes.group_id == current_user.student.group.group_id,
            Votes.v_status == 'Closed').order_by(Votes.v_status, Votes.deadline.desc()).all()
    else:
        votes = Votes.query.filter(
            Votes.group_id == current_user.student.group.group_id,
            Votes.v_status.in_(['Active', 'Closed'])).order_by(Votes.v_status, Votes.deadline.desc()).all()

    return render_template("student/VotePage.html", votes=votes, active_tab=active_tab)


@student.route('/student/account_main/<int:user_id>/events', methods=['GET', 'POST'])
@login_required
def student_main_events(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))

    active_tab = 'all'
            
    if request.method == 'GET':
        active_tab = request.args.get("tab", "all")

    current_date = datetime.now().date()
    if active_tab == 'past':
        events = Events.query.filter(
            Events.group_id == current_user.student.group_id,
            Events.e_status == 'Active',
            Events.date < current_date
        ).order_by(Events.date.asc()).all()
    elif active_tab == 'future':
        events = Events.query.filter(
            Events.group_id == current_user.student.group_id,
            Events.e_status == 'Active',
            Events.date >= current_date
        ).order_by(Events.date.asc()).all()
    else:
        events = Events.query.filter(
            Events.group_id == current_user.student.group_id,
            Events.e_status == 'Active'
        ).order_by(Events.date.asc()).all()

    return render_template("student/EventsPage.html", events=events, active_tab=active_tab)


@student.route('/student/account_main/<int:user_id>/posts', methods=['POST', 'GET'])
@login_required
def student_main_posts(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))

    posts = Posts.query.filter(Posts.group_id==current_user.student.group.group_id,
                                Posts.p_status=='Active').order_by(Posts.creation_date.desc()).all()
    return render_template("student/AnnouncementPage.html", posts=posts)

@student.route('/student/account_main/<int:user_id>/personal_acc', methods=['GET', 'POST'])
@login_required
def student_main_pa(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    active_tab = 'student'

    if request.method == 'GET':
        active_tab = request.args.get("tab", "student")

    print(request.method)
    if request.method == 'POST':
        active_tab = request.form.get('current_tab', request.args.get('tab', 'student'))
        print(request.form)

        if active_tab == 'student':
            try:
                student = StudentInfo.query.filter_by(student_id=current_user.student.student_id).first()
                if not student:
                    student = StudentInfo()
                student = _process_student_info(student, request.form)

                db.session.add(student)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                print('Ошибка', str(e))

        elif active_tab == 'family_mom':
            try:
                family = SFamilyInfo.query.filter_by(student_id=current_user.student.student_id).first()
                if not family:
                    family = SFamilyInfo()
                
                family = _process_getParent(family, request.form, 'mother', current_user.student.student_id)

                db.session.add(family)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                print('Ошибка', str(e))

        elif active_tab == 'family_dad':
            try:
                family = SFamilyInfo.query.filter_by(student_id=current_user.student.student_id).first()
                if not family:
                    family = SFamilyInfo()
                
                family = _process_getParent(family, request.form, 'father', current_user.student.student_id)

                db.session.add(family)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                print('Ошибка', str(e))

        elif active_tab == 'family_guardian':
            try:
                family = SFamilyInfo.query.filter_by(student_id=current_user.student.student_id).first()
                if not family:
                    family = SFamilyInfo()
                
                family = _process_getParent(family, request.form, 'guardian', current_user.student.student_id)

                db.session.add(family)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                print('Ошибка', str(e))

        elif active_tab == 'adressLive':
            try:
                liveAdress = Addresses.query.filter_by(address_id=current_user.student.address_id).first()
                if not liveAdress:
                    liveAdress = Addresses()
                option_info = StudentInfo.query.filter_by(student_id=current_user.student.student_id).first()
                if not option_info:
                    option_info = StudentInfo()
                
                adress = _process_getAdress(liveAdress, request.form, prefix='live')
                print(adress)
                db.session.add(adress)
                db.session.flush()

                option_info.address_id = adress.address_id
                option_info.live_with_whom = request.form.get('live_with_whom') or None
                option_info.ownership_form = request.form.get('ownership_form') or None
                print(option_info)
                db.session.add(option_info)
                db.session.commit()
    
            except Exception as e:
                db.session.rollback()
                print("Ошибка", e)

        elif active_tab == 'adressReg':
            try:
                regAdress = Addresses.query.filter_by(address_id=current_user.student.reg_address_id).first()
                if not regAdress:
                    regAdress = Addresses()

                option_info = StudentInfo.query.filter_by(student_id=current_user.student.student_id).first()
                if not option_info:
                    option_info = StudentInfo()
                
                adress = _process_getAdress(regAdress, request.form, prefix='reg')
                print(adress)

                db.session.add(adress)
                db.session.flush()

                option_info.reg_address_id = adress.address_id
                option_info.where_country = request.form.get('reg-country')
                
                db.session.add(option_info)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                print("Ошибка", e)

        elif active_tab == 'adressCameFrom':
            try:
                cf_adress = Addresses.query.filter_by(address_id=current_user.student.ex_address_id).first()
                if not cf_adress:
                    cf_adress = Addresses()
                
                option_info = StudentInfo.query.filter_by(student_id=current_user.student.student_id).first()
                if not option_info:
                    option_info = StudentInfo()
                
                adress = _process_getAdress(cf_adress, request.form, prefix='cameFrom')
                print(adress)

                db.session.add(adress)
                db.session.flush()

                option_info.ex_address_id = adress.address_id
                option_info.from_where_country = request.form.get('cameFrom-country') 
                option_info.ex_school = request.form.get('cameFrom-school')

                db.session.add(option_info)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                print("Ошибка", e) 

    info = student_info = StudentInfo.query.filter_by(student_id=current_user.student.student_id).first()
    family = SFamilyInfo.query.filter_by(student_id=current_user.student.student_id).first()
    acc_info = Accounts.query.filter_by(account_id=current_user.account_id).first()
    print(acc_info.name)

    return render_template("student/PAPage.html", active_tab=active_tab, info=info, family=family, acc_info=acc_info)