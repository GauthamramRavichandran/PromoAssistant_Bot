from datetime import datetime, timedelta

from backend.db_admins import get_admin_db
from backend.db_main import db


def insert_list_db(list_id, grpname, captions=None, photo_id = None, markup= None, text = None):
	expire = datetime.now().replace(minute = 0, second = 0, microsecond = 0, tzinfo = None) + timedelta(days = 7)
	if photo_id:
		db.lists.insert_one({'_id': list_id,
	                       'photo': photo_id,
	                       'grpname': grpname,
		                     'captions': captions,
	                       'markup': markup,
		                     'expires on': expire})
	else:
		db.lists.insert_one({'_id': list_id,
		                     'grpname': grpname,
		                     'text': text,
		                     'expires on': expire})
		
		
def get_list_db(list_id):
	return db.lists.find_one({'_id': list_id})
def del_expired_list(bot, job):
	expired = datetime.now()
	db.lists.delete_many({'expires on': {'$lt': expired}})
def update_shared_db(chnlid, msgid, time = datetime.now().replace(tzinfo = None), forwarded_from = None, ingroup = None):
	if forwarded_from is None:
		coll = db[str(db.references.find_one({'_id': ingroup}).get('channel id'))]
	else:
		coll = db[str(forwarded_from)]
	try:
		coll.update_one({'_id': chnlid}, {'$set': {'shared on': time, 'msgid': msgid}})
	except Exception as e:
		print(f'IN Update Shared\n{e}')
		
		
def reset_registrations_db(adminid, grps):
	chnlid = get_admin_db(adminid).get('channel id')
	coll = db[chnlid]
	for grp in grps:
		coll.update_many({'in group': grp}, {'$set': {'eligible': 0, 'shared on': None, 'msgid': None}})
		# coll.update_many({'in group': grp, 'permanent': 1}, {'$set': {'eligible': 1}})
	db.statistics.update_one({'_id': 0},
	                         {'$inc': {'Total Promos Done': len(grps)}})
