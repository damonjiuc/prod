from flask import Blueprint, render_template, send_from_directory, current_app
import os


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main/index.html')

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.config['ROOT'],'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')