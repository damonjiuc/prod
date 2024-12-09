from flask_mail import Message
from app import mail
from flask import render_template

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_partnership_email(name, phone, ref):
    send_email('[prod.ru] New Partner Registration',
               sender='no-reply@prod.ru',
               recipients=['damonjiuc@gmail.com', 'partners@prod.ru'],
               text_body=render_template('email/partners_reg.txt',
                                         name=name, phone=phone, ref=ref),
               html_body=render_template('email/partners_reg.html',
                                         name=name, phone=phone, ref=ref))

def send_registration_email(name, email, phone, card, password):
    send_email('[prod.ru] Ваш личный кабинет партнера успешно создан',
               sender='no-reply@prod.ru',
               recipients=[email],
               text_body=render_template('email/registration_confirm.txt',
                                         name=name, email=email, phone=phone, card=card, password=password),
               html_body=render_template('email/registration_confirm.html',
                                         name=name, email=email, phone=phone, card=card, password=password))

def bonus_paid(email, order_num, bonus):
    send_email(f'[prod.ru] Бонус за заказ {order_num} выплачен',
               sender='no-reply@prod.ru',
               recipients=[email],
               text_body=render_template('email/bonus_paid.txt',
                                         order_num=order_num, bonus=bonus),
               html_body=render_template('email/bonus_paid.html',
                                         order_num=order_num, bonus=bonus))