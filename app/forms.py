from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import PasswordField, SubmitField, TelField, EmailField, DateField, FileField, IntegerField, StringField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class UserEditForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    phone = TelField('Телефон', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    birthday = DateField('Дата рождения', validators=[DataRequired()])
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