from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import PasswordField, SubmitField, TelField, EmailField, DateField, FileField, IntegerField, StringField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_login import current_user


class Partnership(FlaskForm):
    """ Заявка на партнерство """
    name = StringField('Имя', validators=[DataRequired()])
    phone = TelField('Телефон', validators=[DataRequired()])
    ref = StringField('Реф') #, default=lambda: current_user.birthday
    submit = SubmitField('Подать заявку')


class Contacts(FlaskForm):
    """ Форма в контактах """
    name = StringField('Имя', validators=[DataRequired()])
    phone = TelField('Телефон', validators=[DataRequired()])
    email = EmailField('E-mail', default=lambda: current_user.email)
    message = StringField('Сообщение')
    ref = StringField('Реф') #, default=lambda: current_user.birthday
    submit = SubmitField('Связаться')


class UserEditForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()], default=lambda: current_user.id)
    phone = TelField('Телефон', validators=[DataRequired()], default=lambda: current_user.phone)
    email = EmailField('E-mail', validators=[DataRequired()], default=lambda: current_user.email)
    birthday = DateField('Дата рождения', validators=[DataRequired()], default=lambda: current_user.birthday)
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    avatar = FileField('Загрузите аватар', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Изменить')


class UserLogin(FlaskForm):
    """ Form to login users """
    login = StringField('Логин', validators=[DataRequired(), Length(min=2, max=56)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')