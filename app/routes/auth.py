from flask import Blueprint, request, redirect, url_for, render_template,jsonify
from flask_login import login_user, logout_user, current_user, login_required
from ..extensions import db, bcrypt, login_manager
from ..models.accounts import Accounts

auth = Blueprint("auth", __name__)

@auth.route("/authorization", methods=['GET', 'POST'])
def auth_view():
    if request.method == 'POST':
        # Проверяем тип контента
        if request.is_json:
            # Обработка данных от Telegram WebApp
            data = request.get_json()
            user_id = data.get("user_id")
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            print(f"Получены данные Telegram WebApp: {user_id}, {username}")
            print(f"Email: {email} {password} {user_id}")


            user = Accounts.query.filter_by(email=email).first()

            if user and bcrypt.check_password_hash(user.password, password):                
                # Определяем маршрут редиректа в зависимости от типа аккаунта
                print(user.acc_type)
                if user.acc_type == 'headman':
                    try:
                        if user_id != user.chat_id:
                            user.chat_id = user_id
                            db.session.commit()

                        if user.isAuthorize == False: 
                            user.isAuthorize = True
                            db.session.commit()

                    except Exception as e:

                        print("Ошибка авторизации", str(e))
                        db.session.rollback()
                        return jsonify({
                            "status": "error",
                            "message": f"Ошибка авторизации{e}"
                        }), 400
                    
                    else:
                        login_user(user)
                        return redirect(url_for("headman.head_main_view", user_id=user.account_id))
                    
                elif user.acc_type == 'student':
                    
                    try:
                        if user_id != user.chat_id:
                            user.chat_id = user_id
                            db.session.commit()

                        if user.isAuthorize == False: 
                            user.isAuthorize = True
                            db.session.commit()

                    except Exception as e:

                        print("Ошибка авторизации", str(e))
                        db.session.rollback()
                        return jsonify({
                            "status": "error",
                            "message": f"Ошибка авторизации{e}"
                        }), 400
                    
                    else:
                        login_user(user)
                        return redirect(url_for("student.student_main_view", user_id=user.account_id))
                                    
                elif user.acc_type == 'admin':
                    try:
                        if user_id != user.chat_id:
                            user.chat_id = user_id
                            db.session.commit()

                        if user.isAuthorize == False: 
                            user.isAuthorize = True
                            db.session.commit()

                    except Exception as e:

                        print("Ошибка авторизации", str(e))
                        db.session.rollback()
                        return jsonify({
                            "status": "error",
                            "message": f"Ошибка авторизации{e}"
                        }), 400
                    
                    else:
                        login_user(user)
                        return redirect(url_for("admin.admin_main_view", user_id=user.account_id))
                else:
                    return jsonify({
                        "status": "error", 
                        "message": "Неизвестный тип аккаунта"
                    }), 400
            else:
                return jsonify({
                    "status": "error", 
                    "message": "Неверный email или пароль"
                }), 401

    return render_template("AutorizePage.html")

@auth.route("/logout/<int:user_id>", methods=['GET', 'POST'])
@login_required
def log_out(user_id):
    if current_user.account_id != user_id:
        print("Запрет доступа")
        return redirect(url_for("auth.auth_view"))
    try:
        current_user.isAuthorize = False
        current_user.chat_id = None
        logout_user()

        db.session.commit()
    except Exception as e:
        print("Ошибка деавторизации", e)
    finally:
        return redirect(url_for('auth.auth_view'))