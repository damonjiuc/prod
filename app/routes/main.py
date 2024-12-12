from flask import Blueprint, render_template, send_from_directory, current_app
import os
from ..forms import Partnership, Contacts
from app.email import send_partnership_email, send_contacts_email


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main/index.html')

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

    return render_template('main/partners.html', form=form)


@main.route('/trading')
def trading():
    form = Partnership()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        ref = form.ref.data
        send_partnership_email(name, phone, ref)

    return render_template('main/trading.html', form=form)


@main.route('/retail')
def retail():
    return render_template('main/retail.html')


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
    return render_template('main/contacts.html', form=form)