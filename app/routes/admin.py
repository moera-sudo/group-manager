import json
from flask import Blueprint, request, redirect, url_for, render_template, jsonify
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

admin = Blueprint("admin", __name__)

@admin.route('/admin/account_main/<int:user_id>')
@login_required
def admin_main_view(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    
    events = Events.query.filter( Events.e_status=='Active', Events.date >= datetime.now().date()).order_by(Events.date.asc()).limit(2).all()
    votes = Votes.query.filter(Votes.v_status == 'Active').order_by(Votes.deadline.asc()).limit(2).all()
    
    return render_template('admin/HomePage.html', events=events, votes=votes)

@admin.route('/admin/account_main/<int:user_id>/group', methods=['POST', 'GET'])
@login_required
def admin_main_group(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))

    #Т.К ниже встречается очень много слова групп - объясню
    group = request.args.get("group", '1')
    group_id = int(group) if group else None
    #group и group_id это айдишнки группы которые получаются из селекта админа при загрузке страницы



    list_of_groups = Groups.query.filter_by().all() #В данном случае, переменная для заполнения селекта админа, в других роутах называется чуть иначе, но тут пришлось так



    group_data = Groups.query.filter_by(group_id=group_id).first() #Пришлось добавить чтобы вытаскивать из Groups имя группы и использовать дляя отправки json(в теории, есть вариант вытаскивать через отношение группа-студент)
    group_name = group_data.group_name
    
    print(group_id, 'Penis')
    print(group_name, group_data, 'zalupa')

    group_info = Groups.query.filter_by(group_id = group_id).first()
    group_list = StudGroupList.query.filter_by(group_name = group_name).order_by(StudGroupList.student_fio).all()

    group_list_json = json.dumps([{"sgl_id": student.sgl_id, "group_name": student.group_name, "student_fio": student.student_fio} for student in group_list],
    ensure_ascii=False)
    students_count = len(group_list)
    #Дальше идет все тоже самое - дамп json и отправка на рендер чтобы прогрузить список через js

    return render_template('admin/GroupPage.html', group_list_json = group_list_json,  group_info=group_info, students_count=students_count, list_of_groups=list_of_groups)

@admin.route('/admin/account_main/<int:user_id>/group/delete', methods=['GET', 'POST'])
@login_required
def admin_main_group_delete(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    
    print(request.method)
    if request.method == 'POST':
        print(request.form)

        data = request.get_json()  # Получаем JSON данные
        student_name = data.get('studentName')
        group_id = data.get('groupId')
        

        try:
            group_data = Groups.query.filter_by(group_id=group_id).first()
            group_name = group_data.group_name


            deleting_student = StudGroupList.query.filter_by(
                student_fio=student_name,
                group_name=group_name ).first()       
                 
            if deleting_student:
                db.session.delete(deleting_student)
            deleting_account = Accounts.query.filter_by(name=student_name).first()

            if deleting_account:
                deleting_account.student.student_status = 'Отчислен'
                db.session.delete(deleting_account)

            db.session.commit()
        
        except Exception as e:
            print('Ошибка', str(e))
            db.session.rollback()
            return jsonify({'unsucces' : False})
        return jsonify({'success': True}), 200


    return jsonify({'error': 'Method not allowed'}), 405

@admin.route('/admin/account_main/<int:user_id>/group/add', methods=['GET', 'POST'])
@login_required
def admin_main_group_add(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    
    if request.method == 'POST':
        print(request.form)
        data = request.get_json()  # Получаем JSON данные
        student_name = data.get('studentName')
        group_id = data.get('groupId')
        
        try:
            group_data = Groups.query.filter_by(group_id=group_id).first()
            group_name = group_data.group_name

            new_student = StudGroupList(group_name=group_name, student_fio=student_name)
            db.session.add(new_student)
            
            db.session.commit()
        
        except Exception as e:
            print('Ошибка', str(e))
            db.session.rollback()
            return jsonify({'unsucces' : False})            

        return jsonify({'success': True}), 200


    return jsonify({'error': 'Method not allowed'}), 405

@admin.route('/admin/account_main/<int:user_id>/votes', methods=['GET', 'POST'])
@login_required
def admin_main_votes(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
        


    active_tab = 'All' #по умолчанию вкладка "Все"
    group = request.args.get("group", '')
    group_id = int(group) if group else None

    if request.method == "POST":
        action = request.form['action']
        v_title = request.form['pollTitle']
        v_date = request.form['pollDate']
        v_vars = request.form.getlist('pollVar')

        if action == 'create':
            group_id = request.form.get('group_id')

            group_id = int(group_id) if group_id else None
            vote = Votes(title=v_title, deadline=v_date, answers=v_vars, group_id=group_id)
            try:
                db.session.add(vote)
                db.session.commit()
                return redirect(url_for("admin.admin_main_votes", user_id=current_user.account_id))

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
                    return redirect(url_for("admin.admin_main_votes", user_id=current_user.account_id))
                except Exception as e:
                    print("Ошибка", e)
                    db.session.rollback()
                    return jsonify({"error": "Ошибка обновления опроса"}), 400
            else:
                return jsonify({"error": "Опрос не найден"}), 404
    
    if request.method == 'GET':
        active_tab = request.args.get("tab", "All")
    if group == "":
        if active_tab == 'Active':
            votes = Votes.query.filter(
                Votes.v_status == 'Active').order_by(Votes.v_status, Votes.deadline.desc()).all()
            
        elif active_tab == 'Closed':
            votes = Votes.query.filter(
                Votes.v_status == 'Closed').order_by(Votes.v_status, Votes.deadline.desc()).all()
        else:
            votes = Votes.query.filter(
                    Votes.v_status.in_(['Active', 'Closed'])).order_by(Votes.v_status, Votes.deadline.desc()).all()
    else:
        if active_tab == 'Active':
            votes = Votes.query.filter(
                Votes.group_id == group_id,
                Votes.v_status == 'Active').order_by(Votes.v_status, Votes.deadline.desc()).all()
            
        elif active_tab == 'Closed':
            votes = Votes.query.filter(
                Votes.group_id == group_id,
                Votes.v_status == 'Closed').order_by(Votes.v_status, Votes.deadline.desc()).all()
        else:
            votes = Votes.query.filter(
                Votes.group_id == group_id,
                Votes.v_status.in_(['Active', 'Closed'])).order_by(Votes.v_status, Votes.deadline.desc()).all()
        
    group_list = Groups.query.filter_by().all()



    return render_template("admin/VotePage.html", votes=votes, active_tab=active_tab, group_list = group_list)

@admin.route('/admin/account_main/<int:user_id>/votes/<int:vote_id>/delete', methods=["GET", "POST"])
@login_required
def admin_main_votes_delete(user_id, vote_id):
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
    
@admin.route('/admin/account_main/<int:user_id>/votes/<int:vote_id>/change', methods=['GET', 'POST'])
@login_required
def admin_main_votes_close(user_id, vote_id):
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

@admin.route('/admin/account_main/<int:user_id>/events', methods=['GET', 'POST'])
@login_required
def admin_main_events(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))

    active_tab = 'all'
    
    group = request.args.get("group", '')
    group_id = int(group) if group else None
    print(group_id)
    print(request.method)
    print(request.form)

    if request.method == "POST":
        action = request.form['action']
        e_title = request.form['eventTitle']
        e_date = request.form['eventDate']
        e_icon = request.form['eventIcon1']
        print(action, 'fasdasd')


        if action == 'create':
            group_id = request.form.get('group_id')

            group_id = int(group_id) if group_id else None
        

            print("Received group_id:", group_id)
            event = Events(
                title=e_title, 
                date=e_date, 
                icon=e_icon,
                group_id=group_id,
                e_status='Active'
            )
            try:
                db.session.add(event)
                db.session.commit()
                return redirect(url_for("admin.admin_main_events", user_id=current_user.account_id))
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
            
    group = request.args.get("group", '')
    group_id = int(group) if group else None

    if request.method == 'GET':
        active_tab = request.args.get("tab", "all")

    current_date = datetime.now().date()
    if group == "":
        if active_tab == 'past':
            events = Events.query.filter(
                Events.e_status == 'Active',
                Events.date < current_date
            ).order_by(Events.date.asc()).all()
        elif active_tab == 'future':
            events = Events.query.filter(
                Events.e_status == 'Active',
                Events.date >= current_date
            ).order_by(Events.date.asc()).all()
        else:
            events = Events.query.filter(
                Events.e_status == 'Active'
            ).order_by(Events.date.asc()).all()
    else:
        if active_tab == 'past':
            events = Events.query.filter(
                Events.group_id == group_id,
                Events.e_status == 'Active',
                Events.date < current_date
            ).order_by(Events.date.asc()).all()
        elif active_tab == 'future':
            events = Events.query.filter(
                Events.group_id == group_id,
                Events.e_status == 'Active',
                Events.date >= current_date
            ).order_by(Events.date.asc()).all()
        else:
            events = Events.query.filter(
                Events.group_id == group_id,
                Events.e_status == 'Active'
            ).order_by(Events.date.asc()).all()
    
    group_name = Groups.query.filter_by()

    group_list = Groups.query.filter_by().all()


    return render_template("admin/EventsPage.html", events=events, active_tab=active_tab, group_name=group_name, group_list=group_list)

@admin.route("/admin/account_main/<int:user_id>/events/<int:event_id>/delete", methods=["GET", "POST"])
@login_required
def admin_main_events_delete(user_id, event_id):
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

@admin.route('/admin/account_main/<int:user_id>/posts', methods=['POST', 'GET'])
@login_required
def admin_main_posts(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    
    group = request.args.get("group", '')
    group_id = int(group) if group else None
    print(group_id)


    if request.method == 'POST':
        action = request.form['action']  
        
        if action == 'create':
            post_title = request.form["announcementTitle"]
            post_content = request.form["announcementContent"]
            post_type = request.form["announcementCategory"]
            group_id = request.form.get('group_id')
            
            group_id = int(group_id) if group_id else None
            
              # Для отладки

            post = Posts(title=post_title, content=post_content, category=post_type, group_id=group_id)
            try:
                db.session.add(post)
                db.session.commit()
                
                return jsonify({
                    "message": "Пост успешно создан",
                    "post": {
                        "id": post.post_id,
                        "title": post.title,
                        "content": post.content,
                        "category": post.category
                    }
                }), 200
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify({"error": f"Ошибка создания поста {e}"}), 500

        elif action == 'edit':
            post_id = request.form.get('post_id')
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


    if group == "":
        posts = Posts.query.filter_by(p_status='Active').order_by(Posts.creation_date.desc()).all()
    else:
        posts = Posts.query.filter_by(p_status='Active', group_id = group).order_by(Posts.creation_date.desc()).all()


    group_list = Groups.query.filter_by().all()


    return render_template("admin/AnnouncementPage.html", posts=posts, group_list=group_list)

@admin.route('/admin/account_main/<int:user_id>/posts/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def admin_main_posts_delete(user_id, post_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    
    try:
        deleting_post = Posts.query.filter_by(post_id=post_id).first()

        if not deleting_post:
            return jsonify({"error": "Объявление не найдено"}), 404
        
        deleting_post.p_status = 'Delete'
        db.session.commit()

        return jsonify({"message": "Объявление успешно удалено"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

