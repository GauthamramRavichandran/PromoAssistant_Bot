from datetime import datetime

from backend.db_admins import get_admin_db
from backend.db_main import db


def add_new_channel_db(chnlid, chnlname, memcount, adminid, ingroup, descr=None, url=None, permanent = 0):
	try:
		channelid = str(db.groups.find_one({'_id': ingroup}).get('channel id'))
		coll = db[channelid]
		if coll.find_one({'_id': chnlid}) and descr is None:
			coll.update_one({'_id': chnlid}, {'$set': {'eligible': 1, 'members count': memcount}})
		elif descr is not None:
			coll.update_one({'_id': chnlid}, {'$set': {
																				'name': chnlname,
																				'members count': memcount,
																				'adminid': adminid,
																				'description': descr,
																				'invitelink': url,
																				'eligible': 1,
																				'permanent': permanent,
																				'in group': ingroup,
																				'shared on': None,
																				'msgid': None}}, upsert = True)
			db.statistics.update_one({'_id': 0},
			                         {'$inc': {'Total Channels Registered': 1}})
			return True
	except Exception as e:
		print(e)


def remove_channel_db(groupid = None, chnl_id = None, chnl_name = None, rem_chnl_id = None):
	try:
		if groupid:
			chanid = db.groups.find_one({'_id': groupid}).get('channel id')
		elif chnl_id:
			chanid = chnl_id
		coll = db[chanid]
		if chnl_name:
			coll.delete_many({'name': str(chnl_name)})
		elif rem_chnl_id:
			coll.delete_many({'_id': rem_chnl_id})
		db.statistics.update_one({'_id': 0},
		                         {'$inc': {'Total Channels Registered' : -1}})
	except Exception as e:
		print(str(e))


def reg_channels_db(adminid, groupid):
	chnlid = get_admin_db(adminid).get('channel id')
	coll = db[chnlid]
	return coll.find({'in group': groupid, 'eligible': 1})


def update_shared_db(chnlid: int, msgid: int, time = datetime.now().replace(tzinfo = None), forwarded_from = None,
                     ingroup = None):
	if forwarded_from is None:
		coll = db[str(db.groups.find_one({'_id': ingroup}).get('channel id'))]
	else:
		coll = db[str(forwarded_from)]
	try:
		coll.update_one({'_id': chnlid}, {'$set': {'shared on': time, 'msgid': msgid}})
	except Exception as e:
		print(f'IN Update Shared\n{e}')
		
		
def check_shared_db(chnlid, grpid):
	return db[chnlid].find({'$and': [{'in group': grpid,
	                                  'shared on': {'$ne': None},
	                                  'msgid': {'$ne': None}}]})
		
		
def check_unshared_db(chnlid, grpid):
	return db[chnlid].find({'$and': [{'in group' : grpid,
	                                  'shared on':  None,
	                                  'msgid'    :  None}]})


def get_chnl_db(chanid, adminid):
	return db[chanid].find({'adminid': adminid})
