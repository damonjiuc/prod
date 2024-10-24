from flask import Blueprint, render_template, request, flash, redirect
# from datetime import datetime
from ..extensions import db
from ..models.users import Users

admin = Blueprint('admin', __name__)

@admin.route('/admin/users', methods=['POST', 'GET'])
def all_users():
    users = Users.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/admin/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        card = request.form.get('card')
        password = request.form.get('password')
        surname = request.form.get('surname')
        name = request.form.get('name')
        secname = request.form.get('secname')
        birthday = request.form.get('birthday')
        email = request.form.get('email')
        phone = request.form.get('phone')
        referer = request.form.get('referer')
        bankcard = request.form.get('bankcard')
        bankname = request.form.get('bankname')
        cardholder = request.form.get('cardholder')
        active = request.form.get('active')
        role = request.form.get('role')
        lvl = request.form.get('lvl')

        user = Users(card=card, password=password, surname=surname, name=name, secname=secname, birthday=birthday, email=email, phone=phone,
                     referer=referer, bankcard=bankcard, bankname=bankname, cardholder=cardholder, active=active, role=role, lvl=lvl)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Форма отправлена!')
            return redirect('/')
        except Exception as exc:
            print(str(exc))
            return str(exc)

    else:
        return render_template('admin/add_user.html')


@admin.route('/admin/edit_user/<int:id>', methods=['POST', 'GET'])
def edit_user(id):
    user = Users.query.get(id)
    if request.method == 'POST':
        user.card = request.form.get('card')
        user.password = request.form.get('password')
        user.surname = request.form.get('surname')
        user.name = request.form.get('name')
        user.secname = request.form.get('secname')
        user.birthday = request.form.get('birthday')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        user.referer = request.form.get('referer')
        user.bankcard = request.form.get('bankcard')
        user.bankname = request.form.get('bankname')
        user.cardholder = request.form.get('cardholder')
        user.active = request.form.get('active')
        user.role = request.form.get('role')
        user.lvl = request.form.get('lvl')
        user.company = request.form.get('company')
        user.city = request.form.get('city')
        user.moneytomln = request.form.get('moneytomln')
        user.totalmoney = request.form.get('totalmoney')
        user.apptoken = request.form.get('apptoken')


        try:
            db.session.commit()
            flash('Форма отправлена!')
            return redirect('/')
        except Exception as exc:
            print(str(exc))
            return str(exc)

    else:
        return render_template('admin/edit_user.html', user=user)
