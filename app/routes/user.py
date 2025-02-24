from flask import Blueprint, render_template, redirect, flash, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import phpass

from app.extensions import db, bcrypt
from app.models.users import Users
from app.models.orders import Orders
from app.models.items import Items
from app.models.prizes import Prizes
from app.models.ref import Ref
from app.models.news import News
from app.forms import UserEditForm, UserLogin, Callback, MakeOrder, Feedback
from app.functions import save_picture
from app.email import user_callback_email, user_feedback_email, user_make_order_email


user = Blueprint('user', __name__)

@user.route('/user/login', methods=['POST', 'GET'])
def user_login():
    form = UserLogin()
    if form.validate_on_submit():
        login = form.login.data
        if login.isdigit():
            login = int(login)
            user = db.session.query(Users).filter_by(card=login).first()
            if not user:
                user = db.session.query(Users).filter_by(phone=login).first()
        else:
            user = db.session.query(Users).filter_by(email=login).first()
        if user.active == 0:
            flash('Ваш доступ в личный кабинет заблокирован', category='error')
            return redirect('user/login')
        if user.password.startswith('$P$B') and user and phpass.verify(form.password.data, user.password):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            try:
                db.session.commit()
                print('ok')
            except Exception as exc:
                print(str(exc))
                return str(exc)
            return redirect(next_page) if next_page else redirect('/user/')
        elif user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/user/')
        else:
            flash('Некорректные данные', category='error')
    return render_template('user/login.html', form=form)

@user.route('/user/', methods=['POST', 'GET'])
@login_required
def user_profile():
    user_in_lk = True if request.base_url.endswith('/user/') else False
    # Гет запрос для фильтрации заказов
    query = request.args.get('query')

    refs = db.session.query(Ref).order_by(Ref.id.desc()).filter_by(referer_card=current_user.card).all()
    news = db.session.query(News).order_by(News.id.desc()).all()
    for ref in refs:
        card = ref.referral_card
        print(card)
        userdata = db.session.query(Users).filter_by(card=card).first()
        name = ' '.join([userdata.name, userdata.surname])
        ref.name = name
    form = UserEditForm()
    form_callback = Callback()
    form_make_order = MakeOrder()
    form_feedback = Feedback()
    prizes = db.session.query(Prizes).filter_by(user_card=current_user.card).all()
    user_prizes = set()
    for prize in prizes:
        user_prizes.add(prize.type)

    orders = db.session.query(Orders).order_by(Orders.order_date.desc()).filter_by(card_num=current_user.card).all()

    stats = {'orders_count': 0, 'bonus_to_pay': 0, 'money_earned': 0}
    count_orders = 0
    for order in orders:
        count_orders += 1
        order.count = count_orders
        order.order_items = db.session.query(Items).filter_by(order_id=order.order_id).all()
        stats['orders_count'] += 1
        if order.payment_date is not None:
            stats['money_earned'] += order.bonus
            print(f'Дата доставки: {order.shipment_date} \t Дата выплаты: {order.payment_date}')
        elif order.shipment_date is not None:
            stats['bonus_to_pay'] += order.bonus
            print(f'Дата доставки: {order.shipment_date} \t Дата выплаты: {order.payment_date}')

    orders = orders[:6]

    if query:
        orders = db.session.query(Orders).order_by(Orders.order_date.desc()).filter_by(
            card_num=current_user.card).filter(
            (Orders.customer_name.like(f'%{query}%')) |
            (Orders.address.like(f'%{query}%'))
        ).all()


    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Проверяем, что запрос от AJAX
        order_data = [{
            'order_num': order.order_num,
            'customer_name': order.customer_name,
            'address': order.address,
            'order_date': order.order_date,
            'shipment_date': order.shipment_date,
            'order_sum': order.order_sum,
            'bonus': order.bonus,
            'bonus_paid': order.bonus_paid
        } for order in orders]
        print(order_data)
        return jsonify({'orders': order_data})

    if form.validate_on_submit():
        user = db.session.query(Users).get(form.id.data)
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
        return redirect('/user/login')
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

    return render_template('user/index.html', orders=orders, stats=stats, refs=refs, user_in_lk=user_in_lk, prizes=user_prizes, news=news,
                           form=form, form_callback=form_callback, form_make_order=form_make_order, form_feedback=form_feedback)


@user.route('/user/orders')
@login_required
def user_orders():
    orders = db.session.query(Orders).order_by(Orders.order_date.desc()).filter_by(card_num=current_user.card).all()
    count_orders = 0
    for order in orders:
        count_orders += 1
        order.count = count_orders
        order.order_items = db.session.query(Items).filter_by(order_id=order.order_id).all()
    return render_template('user/orders.html', orders=orders)

@user.route('/user/logout', methods =['POST', 'GET'])
@login_required
def user_logout():
    logout_user()
    return redirect('/user/login')