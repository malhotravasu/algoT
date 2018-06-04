import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from fetch import setup_firestore

if __name__ == '__main__':
	db = setup_firestore()
	users_ref = db.collection(u'MSFT')
	docs = users_ref.get()
	for doc in docs:
		print(u'{} => {}'.format(doc.id, doc.to_dict()))