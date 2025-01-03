from flask import Flask
from .extensions import db, login_manager
from .config import config
from .routes.headman import headman
from .routes.auth import auth
from .routes.admin import admin
from .routes.student import student
from .models.accounts import Accounts
from .models.addresses import Addresses
from .models.groups import Groups
from .models.student_info import StudentInfo
from .models.familyInfo import SFamilyInfo
from .models.posts import Posts
from .models.events import Events
from .models.votes import Votes
from .models.vote_answers import VoteAnswers


def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(auth)
    app.register_blueprint(headman)
    app.register_blueprint(student)
    app.register_blueprint(admin)



    

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'auth.auth_view'
    login_manager.login_message = ''

    @login_manager.user_loader
    def load_user(user_id):
        return Accounts.query.get(int(user_id))
    



    with app.app_context():
        db.create_all()

    return app