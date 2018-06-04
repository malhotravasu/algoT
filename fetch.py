import requests
import threading
import time
import random
import sched
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
def setup_firestore():
  cred = credentials.Certificate('permissions.json')
  firebase_admin.initialize_app(cred)
  db = firestore.client()
  return db


def get_put_data(db):
  while True:
    URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=1min&apikey=T6KFH1HD8IOSZZDW'
    r = requests.get(url = URL)
    data_dump = r.json()['Time Series (1min)']
    document_name = next(iter(data_dump))
    if ('16:00:00' in document_name):
      break
    document_data = data_dump[document_name]
    put_data(db, document_name, document_data)
    print('Sleeping')
    time.sleep(60)

def put_data(db, document_name, document_data):
  doc = db.collection('MSFT').document(document_name)
  doc.set(document_data)
  print('Data Set')


if __name__ == '__main__':
  db = setup_firestore()
  get_put_data(db)