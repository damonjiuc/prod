from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db, bcrypt
from ..models.users import Users
from ..models.orders import Orders
from ..models.items import Items
from ..models.prizes import Prizes
from ..models.ref import Ref
from ..forms import UserEditForm, UserLogin, Callback, MakeOrder, Feedback
from ..functions import save_picture
from app.email import user_callback_email, user_feedback_email, user_make_order_email


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
        if user.active == 0:
            flash('Ваш доступ в личный кабинет заблокирован', category='error')
            return redirect(url_for('main.index'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user.user_profile'))
        else:
            flash('Некорректные данные', category='error')
    return render_template('user/login.html', form=form)

@user.route('/user/', methods=['POST', 'GET'])
@login_required
def user_profile():
    user_in_lk = True if request.base_url.endswith('/user/') else False
    refs = Ref.query.order_by(Ref.id.desc()).filter_by(referer_card=current_user.card).all()
    form = UserEditForm()
    form_callback = Callback()
    form_make_order = MakeOrder()
    form_feedback = Feedback()
    prizes = Prizes.query.filter_by(user_id=current_user.id).all()
    user_prizes = set()
    for prize in prizes:
        user_prizes.add(prize.type)
    orders = Orders.query.order_by(Orders.order_date.desc()).filter_by(card_num=current_user.card).all() # .limit(6)
    stats = {'orders_count': 0, 'bonus_to_pay': 0, 'money_earned': 0}

    for order in orders:
        order.order_items = Items.query.filter_by(order_id=order.order_id).all()
        stats['orders_count'] += 1
        if order.payment_date is not None:
            stats['money_earned'] += order.bonus
            print(f'Дата доставки: {order.shipment_date} \t Дата выплаты: {order.payment_date}')
        elif order.shipment_date is not None:
            stats['bonus_to_pay'] += order.bonus
            print(f'Дата доставки: {order.shipment_date} \t Дата выплаты: {order.payment_date}')

    orders = orders[:6]

    if form.validate_on_submit():
        user = Users.query.get(form.id.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.phone=form.phone.data
        user.email=form.email.data
        user.birthday=form.birthday.data
        if form.avatar.data:
            avatar_filename = save_picture(form.avatar.data)
            user.avatar=avatar_filename
        user.password=hashed_password
        try:
            db.session.commit()
        except Exception as exc:
            print(str(exc))
            flash('Некорректные данные', category='error')
        return redirect(url_for('user.user_login'))
    if form_callback.validate_on_submit():
        name = form_callback.callback_name.data
        phone = form_callback.callback_phone.data
        user_callback_email(current_user.card, name, phone)
    if form_feedback.validate_on_submit():
        name = form_feedback.feedback_name.data
        text = form_feedback.feedback_text.data
        user_feedback_email(current_user.card, name, text)
    if form_make_order.validate_on_submit():
        name = form_make_order.make_order_name.data
        phone = form_make_order.make_order_phone.data
        text = form_make_order.make_order_phone.data
        user_make_order_email(current_user.card, name, phone, text)

    return render_template('user/index.html', orders=orders, stats=stats, refs=refs, user_in_lk=user_in_lk, prizes=user_prizes,
                           form=form, form_callback=form_callback, form_make_order=form_make_order, form_feedback=form_feedback)


@user.route('/user/orders')
@login_required
def user_orders():
    orders = Orders.query.order_by(Orders.order_date.desc()).filter_by(card_num=current_user.card).all()
    for order in orders:
        order.order_items = Items.query.filter_by(order_id=order.order_id).all()
    return render_template('user/orders.html', orders=orders)

@user.route('/user/logout', methods =['POST', 'GET'])
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('main.index'))