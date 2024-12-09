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
               recipients=['damonjiuc@gmail.com'],
               text_body=render_template('email/partners_reg.txt',
                                         name=name, phone=phone, ref=ref),
               html_body=render_template('email/partners_reg.html',
                                         name=name, phone=phone, ref=ref))