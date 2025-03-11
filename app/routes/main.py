from flask import Blueprint, render_template, send_from_directory, current_app, make_response, request, redirect
import os
import socket
from app.forms import Partnership, Contacts
from app.email import send_partnership_email, send_contacts_email
from app.main import update
from app.extensions import db
from app.models.news import News


main = Blueprint('main', __name__)

@main.route('/')
def index():
    if not request.cookies.get('ref'):
        ref = request.args.get('r')
        if ref:
            response = make_response(redirect('/'))
            response.set_cookie('ref', str(ref), max_age=60 * 60 * 24 * 365 * 2)
            return response
    return render_template('main/index.html', active_page='index')

@main.route('/cookie')
def cookie(ref):
    pass

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.config['ROOT'],'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@main.route('/partners', methods=['POST', 'GET'])
def partners():
    form = Partnership()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        ref = form.ref.data
        send_partnership_email(name, phone, ref)

    return render_template('main/partners.html', form=form, active_page='partners')


@main.route('/trading')
def trading():
    form = Partnership()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        ref = form.ref.data
        send_partnership_email(name, phone, ref)

    return render_template('main/trading.html', form=form, active_page='trading')


@main.route('/retail')
def retail():
    return render_template('main/retail.html', active_page='retail')


@main.route('/contacts', methods=['POST', 'GET'])
def contacts():
    form = Contacts()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        email = form.email.data
        message = form.message.data
        ref = form.ref.data
        send_contacts_email(name, phone, email, message, ref)
    return render_template('main/contacts.html', form=form, active_page='contacts')

@main.route('/policy')
def policy():
    return render_template('main/policy.html')

@main.route('/blog', methods = ['GET', 'POST'])
@main.route('/blog/<int:page>', methods = ['GET', 'POST'])
def blog(page = 1):
    posts = db.session.query(News).order_by(News.id.desc()).paginate(page=page, per_page=1, error_out=False)
    title = f'PRO Дизайн - Блог - Страница #{page}'
    return render_template('main/blog.html', title=title, posts=posts)

@main.route('/upd')
def update_orders():
    update()
    return 'ok'

@main.route('/ip')
def ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip