import telebot, time
from telebot import types
import firebase_admin as fb
from firebase_admin import firestore
from secret import my_token

cred = fb.credentials.Certificate('my_credentials_certificate.json')
fb.initialize_app(cred, {'projectid': 'testbase-f402f'})
db = firestore.client()

def get_document(collection_id, document_id):
    return db.collection(collection_id).document(document_id).get().to_dict()

hot_meal = get_document('menu', 'hot_meal')
dessert = get_document('menu', 'desserts')
drink = get_document('menu', 'drinks')

bot = telebot.TeleBot(my_token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.full_name}! Для того, чтобы ознакомиться с нашим меню, нажмите /menu.')

@bot.message_handler(commands=['menu'])
def mainmenu(message):
    bot.send_message(message.chat.id, 'Выберите тип блюда:', reply_markup=menu())

tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))

docs_statistic = db.collection('statistic').stream()
list_stat = []
for doc in docs_statistic:
  list_stat.append(doc.id)

@bot.callback_query_handler(func=lambda call: True)
def info(call):
    if call.data == 'hot_meal':
        user = call.from_user.full_name
        time = tconv(call.message.date)
        button = call.data
        if user in list_stat:
            full = db.collection('statistic').document(user).get().to_dict()
            new = {time: button}
            result = full | new
        else:
            result = {time: button}
            list_stat.append(user)
        db.collection('statistic').document(user).set(result)

        bot.send_message(chat_id=call.message.chat.id, text=generate_message(hot_meal),
        reply_markup=to_home(), parse_mode='html')

    if call.data == 'dessert':
        user = call.from_user.full_name
        time = tconv(call.message.date)
        button = call.data
        if user in list_stat:
            full = db.collection('statistic').document(user).get().to_dict()
            new = {time: button}
            result = full | new
        else:
            result = {time: button}
            list_stat.append(user)
        db.collection('statistic').document(user).set(result)

        bot.send_message(
        chat_id=call.message.chat.id,
        text=generate_message(dessert),
        reply_markup=to_home(),
        parse_mode='html')

    if call.data == 'drink':
        user = call.from_user.full_name
        time = tconv(call.message.date)
        button = call.data
        if user in list_stat:
            full = db.collection('statistic').document(user).get().to_dict()
            new = {time: button}
            result = full | new
        else:
            result = {time: button}
            list_stat.append(user)
        db.collection('statistic').document(user).set(result)

        bot.send_message(
        chat_id=call.message.chat.id,
        text=generate_message(drink),
        reply_markup=to_home(),
        parse_mode='html')

    if call.data == 'back':
        user = call.from_user.full_name
        time = tconv(call.message.date)
        button = call.data
        if user in list_stat:
            full = db.collection('statistic').document(user).get().to_dict()
            new = {time: button}
            result = full | new
        else:
            result = {time: button}
            list_stat.append(user)
        db.collection('statistic').document(user).set(result)

        bot.send_message(chat_id=call.message.chat.id, text="Вы вернулись в меню", reply_markup=menu())

result = {}

docs_users = db.collection('users').stream()
users_list = []
for doc in docs_users:
  users_list.append(doc.id)

@bot.message_handler(content_types='text')
def archieve(message):
    user = message.from_user.full_name
    text = message.text
    message_time = tconv(message.date)
    if user in users_list:
        full_text = db.collection('users').document(user).get().to_dict()
        new = {message_time: text}
        result = full_text | new
    else:
        result = {message_time: text}
        users_list.append(user)
    if len(result.keys()) > 1000:
        result.clear()
    db.collection('users').document(user).set(result)

def menu():
    my_buttons = types.InlineKeyboardMarkup(row_width=3)
    button_hot_meal = types.InlineKeyboardButton(text='Горячие блюда', callback_data='hot_meal')
    button_dessert = types.InlineKeyboardButton(text='Десерты', callback_data='dessert')
    button_drink = types.InlineKeyboardButton(text='Напитки', callback_data='drink')
    my_buttons.add(button_hot_meal, button_dessert, button_drink)
    return my_buttons

def to_home():
    home = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data='back')
    home.add(button)
    return home

def generate_message(type):
    msg = ''
    if 'size' in type or 'price' in type:
        msg += f'<b>Блюдо: {type["name"]}\n</b>'
    if 'size' in type:
        msg += f'<b>Размер порции: {type["size"]}\n\n</b>'
    msg += type['to_print'] + '\n'
    if 'price' in type:
        msg += '\n'
        msg += f'<b>Цена: {type["price"]} BYN</b>'
    return msg

bot.polling(non_stop=True, interval=0)