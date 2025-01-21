from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from flask_ckeditor.utils import cleanify

from app.extensions import db, bcrypt
from app.models.users import Users
from app.models.orders import Orders
from app.models.items import Items
from app.models.prizes import Prizes
from app.models.ref import Ref
from app.models.news import News
from app.functions import role_required
from app.email import send_registration_email, bonus_paid

admin = Blueprint('admin', __name__)

@admin.route('/admin/users', methods=['POST', 'GET'])
@login_required
@role_required(1)
def all_users():
    users = db.session.query(Users).order_by(Users.id.desc()).all()
    return render_template('admin/users.html', users=users)


@admin.route('/admin/add_user', methods=['POST', 'GET'])
@login_required
@role_required(1)
def add_user():
    if request.method == 'POST':
        card = request.form.get('card')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        surname = request.form.get('surname')
        name = request.form.get('name')
        birthday = request.form.get('birthday')
        email = request.form.get('email')
        phone = request.form.get('phone')
        bankcard = request.form.get('bankcard')
        bankname = request.form.get('bankname')
        cardholder = request.form.get('cardholder')
        city = request.form.get('city')
        company = request.form.get('company')
        active = request.form.get('active')
        role = request.form.get('role')
        lvl = request.form.get('lvl')
        comment = request.form.get('comment')

        user = Users(card=card, password=hashed_password, surname=surname, name=name, birthday=birthday,
                     email=email, phone=phone, bankcard=bankcard, bankname=bankname, cardholder=cardholder,
                     city=city, company=company, active=active, role=role, lvl=lvl, comment=comment)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Пользователь добавлен!', category='success')
            if name and email and phone and card and password:
                send_registration_email(name, email, phone, card, password)
            return redirect(url_for('admin.users'))
        except Exception as exc:
            flash('Некорректно введены данные!', category='error')
            print(str(exc))
            # return str(exc)

    else:
        return render_template('admin/add_user.html')


@admin.route('/admin/edit_user/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required(1)
def edit_user(id):
    user = db.session.query(Users).get(id)
    orders = db.session.query(Orders).order_by(Orders.order_date.desc()).filter_by(card_num=user.card).all()
    if request.method == 'POST':
        user.card = request.form.get('card')
        user.surname = request.form.get('surname')
        user.name = request.form.get('name')
        user.birthday = request.form.get('birthday')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        user.bankcard = request.form.get('bankcard')
        user.bankname = request.form.get('bankname')
        user.cardholder = request.form.get('cardholder')
        user.active = request.form.get('active')
        user.role = request.form.get('role')
        user.lvl = request.form.get('lvl')
        user.company = request.form.get('company')
        user.city = request.form.get('city')
        user.comment = request.form.get('comment')

        try:
            db.session.commit()
            flash('Данные пользователя изменены!', category='success')
            return redirect(f'/admin/edit_user/{user.id}')
        except Exception as exc:
            print(str(exc))
            return str(exc)

    else:
        return render_template('admin/edit_user.html', user=user, orders=orders)


@admin.route('/admin/edit_user_ref/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required(1)
def edit_user_pwd(id):
    user = db.session.query(Users).query.get(id)
    if request.method == 'POST':
        password = request.form.get('password')
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            db.session.commit()
            flash('Форма отправлена!', category='success')
            return redirect(url_for('admin.edit_user', id=user.id))
        except Exception as exc:
            print(str(exc))
            return str(exc)

    else:
        return render_template('admin/edit_user_pwd.html', user=user)


@admin.route('/admin/delete_user/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required(1)
def delete_user(id):
    user = db.session.query(Users).get(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь удален', category='success')
        return redirect('/admin/users')
    except Exception as exc:
        print(str(exc))
        return str(exc)


@admin.route('/admin/edit_order/<int:order_id>', methods=['POST', 'GET'])
@login_required
@role_required(1)
def edit_order(order_id):
    order = db.session.query(Orders).get(order_id)
    items = db.session.query(Items).filter_by(order_id=order_id).all()
    if request.method == 'POST':
        order.bonus_paid = int(request.form.get('bonus_paid'))
        try:
            db.session.commit()
            if order.bonus_paid == 1:
                user = Users.query.filter(Users.card.contains(order.card_num)).first()
                email = user.email
                bonus_paid(email=email, order_num=order.order_num, bonus=order.bonus)
            return redirect(url_for('admin.edit_order', order_id=order.order_id))
        except Exception as exc:
            print(str(exc))
            return str(exc)
    return render_template('admin/edit_order.html', items=items, order=order)


@admin.route('/admin/add_prize/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required(1)
def add_prize(id):
    user = db.session.query(Users).query.get(id)
    user_card = user.card
    if request.method == 'POST':
        user_card = request.form.get('user_card')
        type = request.form.get('type')
        date = request.form.get('date')

        prize = Prizes(user_card=user_card, type=type, date=date)
        print(prize)

        try:
            db.session.add(prize)
            db.session.commit()
            flash('Приз добавлен!', category='success')
            return redirect(url_for('admin.edit_user', id=id))
        except Exception as exc:
            flash('Некорректно введены данные!', category='error')
            print(str(exc))
            print('беда')

    else:
        return render_template('admin/add_prize.html', id=id, user_card=user_card)


@admin.route('/admin/edit_user_ref/<int:card>', methods=['POST', 'GET'])
@login_required
@role_required(1)
def edit_user_ref(card):
    refs = db.session.query(Ref).order_by(Ref.id.desc()).filter_by(referer_card=card).all()
    if request.method == 'POST':
        referer_card = card
        referral_card = request.form.get('referral_card')
        ref = Ref(referer_card=referer_card,  referral_card=referral_card, paid=0)

        try:
            db.session.add(ref)
            db.session.commit()
            flash('Реферал добавлен!', category='success')
            return redirect(f'/admin/edit_user_ref/{card}')
        except Exception as exc:
            print(str(exc))
            return str(exc)

    else:
        return render_template('admin/edit_user_ref.html', card=card, refs=refs)


@admin.route('/admin/ref_paid/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required(1)
def ref_paid(id):
    ref = db.session.query(Ref).query.get(id)
    ref.paid = 1 if ref.paid == 0 else 0
    print(ref.id, ref.referer_card, ref.referral_card, ref.paid)
    try:
        db.session.commit()
        flash('Статус выплаты бонуса за реферала изменен', category='success')
        return redirect(f'/admin/edit_user_ref/{ref.referer_card}')
    except Exception as exc:
        print(str(exc))
        return str(exc)


@admin.route('/admin/news', methods=['POST', 'GET'])
@login_required
@role_required(1)
def all_news():
    news = db.session.query(News).order_by(News.id.desc()).all()
    return render_template('admin/news.html', news=news)


@admin.route('/admin/add_article', methods=['POST', 'GET'])
@login_required
@role_required(1)
def add_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = cleanify(request.form.get('ckeditor'))
        article_date = request.form.get('article_date')

        article = News(title=title, content=content, date=article_date)

        try:
            db.session.add(article)
            db.session.commit()
            flash('Новость добавлена', category='success')
            return redirect(url_for('admin.all_news'))
        except Exception as exc:
            flash('Некорректно введены данные!', category='error')
            print(str(exc))
            return str(exc)

    else:
        return render_template('admin/add_article.html')


@admin.route('/admin/edit_article/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required(1)
def edit_article(id):
    article = db.session.query(News).get(id)
    if request.method == 'POST':
        article.title = request.form.get('title')
        article.content = cleanify(request.form.get('ckeditor'))
        article.date = request.form.get('article_date')
        try:
            db.session.commit()
            if order.bonus_paid == 1:
                user = Users.query.filter(Users.card.contains(order.card_num)).first()
                email = user.email
                bonus_paid(email=email, order_num=order.order_num, bonus=order.bonus)
            return redirect(url_for('admin.edit_order', order_id=order.order_id))
        except Exception as exc:
            print(str(exc))
            return str(exc)
    return render_template('admin/edit_article.html', article=article)


@admin.route('/admin/delete_article/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required(1)
def delete_article(id):
    article = db.session.query(News).get(id)
    try:
        db.session.delete(article)
        db.session.commit()
        flash('Новость удалена', category='success')
        return redirect('/admin/news')
    except Exception as exc:
        print(str(exc))
        return str(exc)