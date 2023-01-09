import firebase_admin as fb
from firebase_admin import firestore
import pandas as pd

cred = fb.credentials.Certificate('my_credentials_certificate.json')
fb.initialize_app(cred, {'projectid': 'testbase-f402f'})
db = firestore.client()

df = pd.read_json('menu.json')
my_dict = df.to_dict('records')

for i in my_dict:
    for value in i.values():
        if value == 'hot_meals':
            db.collection('menu').document('hot_meal').set(i['buttons'][0])
        elif value == 'drinks':
            db.collection('menu').document('drinks').set(i['buttons'][0])
        elif value == 'dessert_meals':
            db.collection('menu').document('desserts').set(i['buttons'][0])

