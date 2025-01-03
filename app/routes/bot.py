from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, logout_user
from ..extensions import db, bcrypt, login_manager
from ..models.accounts import Accounts

bot = Blueprint("bot", __name__)