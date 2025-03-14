from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_from_directory
from flask_ckeditor import upload_fail, upload_success
from flask_login import login_required
import os
from app.config import Config

from app.extensions import db, bcrypt
from app.models.users import Users
from app.models.orders import Orders
from app.models.items import Items
from app.models.prizes import Prizes
from app.models.ref import Ref
from app.models.news import News
from app.functions import role_required, save_picture
from app.email import send_registration_email, bonus_paid

admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=['POST', 'GET'])
@admin.route('/admin/', methods=['POST', 'GET'])
@admin.route('/admin/index', methods=['POST', 'GET'])
@login_required
@role_required(1)
def admin_dash():
    return render_template('admin/index.html')

@admin.route('/admin/users', methods=['POST', 'GET'])
@admin.route('/admin/users/<int:page>', methods = ['GET', 'POST'])
@login_required
@role_required(1)
def all_users(page = 1):
    # Гет запрос для фильтрации заказов
    query = request.args.get('query')

    users = db.session.query(Users).order_by(Users.card.desc()).paginate(page=page, per_page=25, error_out=False)

    if query:
        users = db.session.query(Users).order_by(Users.card.desc()).filter(
            (Users.card.like(f'%{query}%')) |
            (Users.phone.like(f'%{query}%')) |
            (Users.surname.like(f'%{query}%')) |
            (Users.name.like(f'%{query}%'))
        ).paginate(page=page, per_page=25, error_out=False)


    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Проверяем, что запрос от AJAX
        order_data = [{
            'card': user.card,
            'surname': user.surname,
            'name': user.name,
            'comment': user.comment,
            'phone': user.phone,
            'lvl': user.lvl,
            'totalmoney': user.totalmoney,
            'id': user.id
        } for user in users]
        print(order_data)
        return jsonify({'users': order_data})

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
            # if name and email and phone and card and password:
            #     send_registration_email(name, email, phone, card, password)
            return redirect(url_for('admin.all_users'))
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
    user = db.session.query(Users).get(id)
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
    user = db.session.query(Users).get(id)
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


@admin.route('/admin/add_order/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required(1)
def add_order(id):
    user = db.session.query(Users).get(id)
    user_card = user.card
    if request.method == 'POST':
        card = request.form.get('CARD_NUM')
        order_num = request.form.get('order_num')
        order_date = request.form.get('ORDER_DATE')
        shipment_date = request.form.get('SHIPMENT_DATE')
        payment_date = request.form.get('PAYMENT_DATE')
        bonus = request.form.get('BONUS')
        customer_name = request.form.get('CUSTOMER_NAME')
        order_sum = request.form.get('ORDER_SUM')
        address = request.form.get('ADDRESS')
        shop = request.form.get('SHOP')
        bonus_paid = False
        manual_add = True

        order = Orders(card_num=card, order_num=order_num, order_date=order_date, shipment_date=shipment_date, payment_date=payment_date,
                       bonus=bonus, customer_name=customer_name, order_sum=order_sum, address=address, shop=shop, bonus_paid=bonus_paid, manual_add=manual_add)

        try:
            db.session.add(order)
            db.session.commit()
            flash('Заказ добавлен!', category='success')
            return redirect(url_for('admin.edit_user', id=id))
        except Exception as exc:
            flash('Некорректно введены данные!', category='error')
            print(str(exc))
            print('беда')

    else:
        return render_template('admin/add_order.html', id=id, user_card=user_card)


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
    ref = db.session.query(Ref).get(id)
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
        file = request.files['image']
        if file:
            img = save_picture(file)
            title = request.form.get('title')
            type = request.form.get('type')
            description = request.form.get('description')
            content = request.form.get('content')
            article_date = request.form.get('article_date')

            print(f"📝 Полученные данные: title={title}, content={content}, date={article_date}")

            article = News(title=title, type=type, description=description, img=img, content=content, date=article_date)

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
        article.content = request.form.get('ckeditor')
        article.date = request.form.get('article_date')
        try:
            db.session.commit()
            flash('Новость изменена', category='success')
            return redirect(url_for('admin.edit_article', id=article.id))
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

@admin.route('/admin/upload_image', methods=['POST'])
@login_required
@role_required(1)
def upload_image():
    # if 'upload' not in request.files:
    #     return jsonify({'error': 'No file part'}), 400
    #
    # file = request.files['upload']
    #
    # if file.filename == '':
    #     return jsonify({'error': 'No selected file'}), 400
    #
    # if file:
    #     filename = file.filename
    #     filepath = os.path.join(Config.UPLOAD_PATH_FULL, filename)
    #     file.save(filepath)
    #     url = f"/admin/uploads/{filename}"
    #     return jsonify({'url': url})

    f = request.files.get('upload')
    if not f:
        return upload_fail(message="Файл не загружен.")  # Ошибка, если файл не передан

    # Сохраняем файл
    filepath = os.path.join(Config.UPLOAD_PATH_FULL, f.filename)
    f.save(filepath)

    # 📌 Формируем URL загруженного файла
    file_url = url_for('admin.uploaded_file', filename=f.filename, _external=True)

    return upload_success(file_url, filename=f.filename)  # Возвращаем JSON с URL

@admin.route('/admin/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(Config.UPLOAD_PATH_FULL, filename)