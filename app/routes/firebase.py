from flask import Blueprint, request, jsonify
from firebase_admin import messaging
from app.extensions import db
from app.models.users import Users
from app.models.notifications import Notifications


firebase = Blueprint('firebase', __name__)

@firebase.route('/firebase/', methods=['POST', 'GET'])
def firebase_test():
    try:
        # data = request.json
        # token = data['token']
        # message_title = data['title']
        # message_body = data['body']
        token = 'eKwELyeeQx-7RSWjw19Em1:APA91bF1MzMUypcx07QyjwTXFvyd1zfUuGtJfFMPF-DFYa0YX4jAv0cDZyXDpVSB7s8KO5K27isNZv1MH_Pcb5jGKpktZSU1LhETljurkSnVg_vU90CPfU4'
        message_title = 'test kek'
        message_body = 'test kek test kek test kek'

        message = messaging.Message(
            notification=messaging.Notification(
                title=message_title,
                body=message_body,
            ),
            token=token,
        )

        response = messaging.send(message)
        return jsonify({'success': True, 'response': response}), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def send_notification(data):
    tokens = data[0]
    message_title = data[1]
    message_body = data[2]

    for token in tokens:
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=message_title,
                    body=message_body,
                ),
                token=token,
            )

            response = messaging.send(message)
            return jsonify({'success': True, 'response': response}), 200

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500



# возвращает все токены юзера
@firebase.route('/firebase/token/<int:card>', methods=['POST', 'GET'])
def get_tokens(card):
    tokens = db.session.query(Notifications.token).filter(Notifications.card == card).all()
    for i in range(len(tokens)):
        tokens[i] = str(tokens[i])[2:-3]
    return  tokens

# возвращает имя юзера
@firebase.route('/firebase/name/<int:card>', methods=['POST', 'GET'])
def get_name(card):
    name = str(db.session.query(Users.name).filter(Users.card == card).first())[2:-3]
    return  name


# уведомления о выигрыше: {{name}}, поздравляем
# id юзера
# название приза
def send_prizes_notification(card, prize):
    tokens = get_tokens(card)
    name = get_name(card)
    title = f'{name}, поздравляем!'
    body = f'Вы выиграли {prize}! Менеджер свяжется с Вами'
    return [tokens, title, body]

# уведомления выплаты бонуса
# id юзера
# номер заказа
def send_order_notification(card, order_num):
    tokens = get_tokens(card)
    title = f'Бонус выплачен'
    body = f'Осуществлена выплата по заказу {order_num}'
    return [tokens, title, body]

# напоминание о покупке (не хватает до next lvl)
# id юзера
# оставшаяся сумма
def send_purchase_reminder_notification(card, money_left):
    tokens = get_tokens(card)
    name = get_name(card)
    title = f'{name}, осталось немного!!'
    body = f'До следующего уровня Вам не хватает {money_left} рублей'
    return [tokens, title, body]

# уведомление о повышении уровня
# карта юзера
# уровень юзера
# скидка юзера
def send_lvlup_notification(card, lvl, discount):
    tokens = get_tokens(card)
    name = get_name(card)
    title = f'Ваш новый уровень {lvl}!'
    body = f'{name}, поздравляем с повышением уровня! Новый процент вознаграждения составляет {discount}%'
    return [tokens, title, body]


@firebase.route('/firebase/bday/<int:card>', methods=['POST', 'GET'])
def send_birthday_notification(card):
    tokens = get_tokens(card)
    name = get_name(card)
    title = f'{name}, с Днем рождения!'
    body = f'Команда "PRO Дизайн" поздравляет Вас! И желает еще большего количества бонусов'
    return [tokens, title, body]