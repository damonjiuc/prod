from flask import Blueprint, render_template
from ..extensions import db
from ..models.user import UserTest

user = Blueprint('user', __name__)

@user.route('/user/<name>')
def create_user(name):
    user = UserTest(name=name)
    db.session.add(user)
    db.session.commit()
    return render_template('main/user.html')