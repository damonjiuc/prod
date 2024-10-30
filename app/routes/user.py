from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user
from ..extensions import db, bcrypt
from ..models.users import Users
from ..forms import UserEditForm, UserLogin
from ..functions import save_picture

user = Blueprint('user', __name__)

@user.route('/user/login', methods=['POST', 'GET'])
def user_login():
    form = UserLogin()
    if form.validate_on_submit():
        login = form.login.data
        if login.isdigit():
            login = int(login)
            user = Users.query.filter_by(card=login).first()
            if not user:
                user = Users.query.filter_by(phone=login).first()
        else:
            user = Users.query.filter_by(email=login).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('user.user_edit_profile'))
    else:
        print('ошипко') # flash
    return render_template('user/login.html', form=form)

@user.route('/user/edit', methods=['POST', 'GET'])
def user_edit_profile():
    form = UserEditForm()
    if form.validate_on_submit():
        user = Users.query.get(form.id.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        avatar_filename = save_picture(form.avatar.data)
        user.phone=form.phone.data
        user.email=form.email.data
        user.birthday=form.birthday.data
        user.avatar=avatar_filename
        user.password=hashed_password
        try:
            db.session.commit()
        except Exception as exc:
            print(str(exc))
        return redirect(url_for('user.user_login'))
    else:
        print('При регистрации произошла ошибка') # flash
    return render_template('user/edit.html', form=form)

@user.route('/user/logout', methods =['POST', 'GET'])
def user_logout():
    logout_user()
    return redirect(url_for('main.index'))