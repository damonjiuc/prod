from flask import Blueprint, render_template, send_from_directory, current_app
import os
from ..forms import Partnership
from app.email import send_partnership_email


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
        if name and phone:
            send_partnership_email(name, phone, ref)

    return render_template('main/partners.html', form=form)


@main.route('/trading')
def trading():
    return render_template('main/trading.html')


@main.route('/retail')
def retail():
    return render_template('main/retail.html')


@main.route('/contacts')
def contacts():
    return render_template('main/retail.html')