import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Firebase Authentication
def setup_firestore():
  cred = credentials.Certificate('permissions.json')
  firebase_admin.initialize_app(cred)
  db = firestore.client()
  return db

def dump_data(db):
  URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=1min&apikey=T6KFH1HD8IOSZZDW'
  response = requests.get(url = URL)
  json_data = json.loads(response.text)
  if 'Time Series (1min)' in json_data:
    data_dump = response.json()['Time Series (1min)']
    document_name = next(iter(data_dump))
  document_data = data_dump[document_name]
  put_data(db, document_name, document_data)

# Actual dumping into Firestore
def put_data(db, document_name, document_data):
  doc = db.collection('MSFT').document(document_name)
  doc.set(document_data)
  print('Data Set', {document_name: document_data})

if __name__ == '__main__':
  db = setup_firestore()
  dump_data(db)