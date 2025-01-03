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

headman = Blueprint("headman", __name__)


@headman.route('/headman/registration', methods=['GET', 'POST'])
def head_reg_view():
    print(request.method)
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form['r_password']).decode('utf-8')
        r_email = request.form['r_email']
        print(r_email, hashed_password)

        validate = Accounts.query.filter_by(email=r_email).first()
        group_validate = Groups.query.filter_by(group_name=request.form['r_group']).first()
        print(group_validate)
        student_validate = StudGroupList.query.filter_by(group_name = request.form['r_group'], student_fio=request.form['r_fullname']).first()
        if not student_validate:
            flash('Вы не состоите в списке введеной группы', 'error')
            return redirect(url_for("headman.head_reg_view"))
        
        if group_validate:
            flash('Такая группа уже существует', 'error')
            return redirect(url_for("headman.head_reg_view"))
        

        if validate:
            flash('Данный электронный адрес уже зарегистрирован', 'error') 
            return redirect(url_for("headman.head_reg_view"))
        
        headman_name = request.form['r_fullname']

        group = Groups(group_name=request.form['r_group'], headman=headman_name)
        try:
            
            db.session.add(group)
            db.session.commit()
            student_info = StudentInfo(group_id=group.group_id)
            print('Check', student_info)
            db.session.add(student_info)
            db.session.commit()
            user = Accounts(name=request.form['r_fullname'], email=request.form['r_email'], password=hashed_password, acc_type='headman', student_id=student_info.student_id)
            print('check2', user)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("auth.auth_view"))
        
        except Exception as e:
            print(e)

    

    return render_template('headman/RegistrationPage.html')



@headman.route('/headman/account_main/<int:user_id>')
@login_required
def head_main_view(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    
    group_name = Groups.query.filter_by(group_id=current_user.student.group.group_id).first().group_name
    
    events = Events.query.filter(Events.group_id == current_user.student.group.group_id,
                                Events.e_status=='Active',
                                Events.date >= datetime.now().date()).order_by(Events.date.asc()).limit(2).all()
    votes = Votes.query.filter(Votes.group_id == current_user.student.group.group_id,
                               Votes.v_status == 'Active').order_by(Votes.deadline.asc()).limit(2).all()
    

    return render_template('headman/HomePage.html', group_name=group_name, events=events, votes=votes)



@headman.route('/headman/account_main/<int:user_id>/group', methods=['POST', 'GET'])
@login_required
def head_main_group(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    
    group_list = StudGroupList.query.filter_by(group_name = current_user.student.group.group_name).order_by(StudGroupList.student_fio).all()

    group_info = Groups.query.filter_by(group_name = current_user.student.group.group_name).first()

    group_list_json = json.dumps([{"sgl_id": student.sgl_id, "group_name": student.group_name, "student_fio": student.student_fio} for student in group_list],
    ensure_ascii=False)

    students_count = len(group_list)

    return render_template('headman/GroupPage.html', group_list_json = group_list_json,  group_info=group_info, students_count=students_count)

@headman.route('/headman/account_main/<int:user_id>/votes', methods=['GET', 'POST'])
@login_required
def head_main_votes(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    print('met', request.method)
    print(request.form)


    active_tab = 'All' #по умолчанию вкладка "Все"
    if request.method == "POST":
        action = request.form['action']
        v_title = request.form['pollTitle']
        v_date = request.form['pollDate']
        v_vars = request.form.getlist('pollVar')
        print(f'Данные опроса: title{v_title}, date{v_date}, vars{v_vars}')

        if action == 'create':
            vote = Votes(title=v_title, deadline=v_date, answers=v_vars, group_id=current_user.student.group.group_id)
            try:
                db.session.add(vote)
                db.session.commit()
                return redirect(url_for("headman.head_main_votes", user_id=current_user.account_id))

            except Exception as e:
                print("Ошибка", e)
                db.session.rollback()
                return jsonify({"error": "Ошибка создания события"})
        if action == 'edit':
            vote_id = request.form.get('voteId')
            editing_vote = Votes.query.filter_by(vote_id=vote_id).first()
            
            if editing_vote:
                try:
                    editing_vote.title = v_title
                    editing_vote.deadline = v_date
                    editing_vote.answers = v_vars
                    
                    db.session.commit()
                    return redirect(url_for("headman.head_main_votes", user_id=current_user.account_id))
                except Exception as e:

                    print("Ошибка", e)
                    db.session.rollback()
                    return jsonify({"error": "Ошибка обновления опроса"}), 400
            else:
                return jsonify({"error": "Опрос не найден"}), 404
    
    
    if request.method == 'GET':
        active_tab = request.args.get("tab", "All")
    
    #Фильтрация
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

    return render_template("headman/VotePage.html", votes=votes, active_tab=active_tab)

@headman.route('/headman/account_main/<int:user_id>/votes/<int:vote_id>/delete', methods=["GET", "POST"])
@login_required
def head_main_votes_delete(user_id, vote_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view")), 403
    try:
        deleting_vote = Votes.query.filter_by(vote_id=vote_id).first()
        if not deleting_vote:
            return jsonify({'error': "Опрос не найден"})
        deleting_vote.v_status = 'Delete'
        db.session.commit()

        return jsonify({"message": "Опрос успешно удален"})
    except Exception as e:
        print("Ошибка удаления опроса", str(e))
        db.session.rollback()
        return jsonify({"error": str(e)})
    
@headman.route('/headman/account_main/<int:user_id>/votes/<int:vote_id>/change', methods=['GET', 'POST'])
@login_required
def head_main_votes_close(user_id, vote_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view")), 403
    try:
        closing_vote = Votes.query.filter_by(vote_id=vote_id).first()
        if not closing_vote:
            return jsonify({'error': 'Опрос не найден'})
        if closing_vote.v_status == 'Active': 
            closing_vote.v_status = 'Closed'
        elif closing_vote.v_status == 'Closed':
            closing_vote.v_status = 'Active'
        db.session.commit()

        return jsonify({"message": "Статус опроса успешно изменен"})
    except Exception as e:
        print("Ошибка при попытке закрыть опрос", str(e))
        db.session.rollback()
        return jsonify({'error': str(e)})


@headman.route('/headman/account_main/<int:user_id>/events', methods=['GET', 'POST'])
@login_required
def head_main_events(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))

    active_tab = 'all'  # По умолчанию "Все"
    if request.method == "POST":
        action = request.form['action']
        e_title = request.form['eventTitle']
        e_date = request.form['eventDate']
        e_icon = request.form['eventIcon1']

        if action == 'create':
            event = Events(
                title=e_title, 
                date=e_date, 
                icon=e_icon,
                group_id=current_user.student.group_id,
                e_status='Active'
            )
            try:
                db.session.add(event)
                db.session.commit()
                return redirect(url_for("headman.head_main_events", user_id=current_user.account_id))
            except Exception as e:
                print("Ошибка", e)
                db.session.rollback()
                return jsonify({"error": "Ошибка создания события"})
        
        elif action == 'edit':
            event_id = request.form.get('eventId')
            editing_event = Events.query.filter_by(event_id=event_id).first()
            
            if editing_event:
                editing_event.title = e_title
                editing_event.date = e_date
                editing_event.icon = e_icon
                
                try:
                    db.session.commit()
                    return jsonify({"message": "Событие успешно обновлено"}), 200
                except Exception as e:
                    print("Ошибка", e)
                    db.session.rollback()
                    return jsonify({"error": "Ошибка обновления события"}), 400
            else:
                return jsonify({"error": "Событие не найдено"}), 404
            
            
    #гет запрос для получения нужной вкладки
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

    return render_template("headman/EventsPage.html", events=events, active_tab=active_tab)

@headman.route("/headman/account_main/<int:user_id>/events/<int:event_id>/delete", methods=["GET", "POST"])
@login_required
def head_main_events_delete(user_id, event_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view")), 403
    try:
        deleting_event = Events.query.filter_by(event_id = event_id).first()
        if not deleting_event:
            return jsonify({"error": "Событие не найдено"})
        
        deleting_event.e_status = 'Delete'
        db.session.commit()

        return jsonify({"message": "Объявление успешно удалено"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})




@headman.route('/headman/account_main/<int:user_id>/posts', methods=['POST', 'GET'])
@login_required
def head_main_posts(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    
    if request.method == 'POST':
        action = request.form['action']  
        
        if action == 'create':
            post_title = request.form["announcementTitle"]
            post_content = request.form["announcementContent"]
            post_type = request.form["announcementCategory"]

            post = Posts(title=post_title, content=post_content, category=post_type, group_id=current_user.student.group.group_id)
            try:
                db.session.add(post)
                db.session.commit()
                
                return redirect(url_for('headman.head_main_posts', user_id=user_id)), 200
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify({"error": "Ошибка создания поста"}), 500

        elif action == 'edit':
            post_id = request.form.get('post_id')  # Получаем post_id из формы
            post_newTitle = request.form['editAnnouncementTitle']
            post_newContent = request.form['editAnnouncementContent']
            post_newCategory = request.form['editAnnouncementCategory']
            
            try:
                editing_post = Posts.query.filter_by(post_id=post_id).first()
                if not editing_post:
                    return jsonify({'error': "Пост не найден"}), 404
                
                editing_post.title = post_newTitle
                editing_post.content = post_newContent
                editing_post.category = post_newCategory
                db.session.commit()

                return jsonify({"message": "Объявление изменено"}), 200
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify({"error": "Ошибка взаимодействия с базой данных"}), 500

    posts = Posts.query.filter(Posts.group_id==current_user.student.group.group_id,
                            Posts.p_status=='Active').order_by(Posts.creation_date.desc()).all()
    return render_template("headman/AnnouncementPage.html", posts=posts)

@headman.route('/headman/account_main/<int:user_id>/posts/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def head_main_posts_delete(user_id, post_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    
    try:
        deleting_post = Posts.query.filter_by(post_id=post_id, group_id = current_user.student.group.group_id).first()

        print(deleting_post)
        if not deleting_post:
            return jsonify({"error": "Объявление не найдено"}), 404
        
        deleting_post.p_status = 'Delete'
        db.session.commit()

        return jsonify({"message": "Объявление успешно удалено"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@headman.route('/headman/account_main/<int:user_id>/personal_acc', methods=['GET', 'POST'])
@login_required
def head_main_pa(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    #Страница student по умолчанию
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
            pass
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


    #Вытаскиваем из бд 3 пакета данных. 
    info = student_info = StudentInfo.query.filter_by(student_id=current_user.student.student_id).first()

    family = SFamilyInfo.query.filter_by(student_id=current_user.student.student_id).first()

    acc_info = Accounts.query.filter_by(account_id=current_user.account_id).first()
    print(acc_info.name)

    return render_template("headman/PAPage.html", active_tab=active_tab, info=info, family=family, acc_info=acc_info)




    

