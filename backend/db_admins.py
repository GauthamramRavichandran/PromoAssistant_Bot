from backend.db_main import db


def insert_admin_db(adminid: int, username, chnlid: str, chnlname, chnlusername):
	try:
		db.admins.insert_one({
			'_id': adminid,
			'name': username,
			'channel name': chnlname,
			'channel id': chnlid,
			'channel username': chnlusername,
		})
		db.statistics.update_one({'_id': 0}, {'$inc': {'Total Admins': 1}})
	except Exception as e:
		print(str(e))


def insert_premium_chnls_db(adminid: int, user_data, num: int):
	if num == 1:
		db.admins.update_one({'_id': adminid},
		                     {'$set': {'premium_1': {'text': user_data['pre1_text'],
		                                             'url': user_data['pre1_url']}}})
	elif num == 2:
		db.admins.update_one({'_id': adminid},
		                     {'$set': {'premium_2': {'text': user_data['pre2_text'],
		                                             'url': user_data['pre2_url']}}})
	elif num == 3:
		db.admins.update_one({'_id': adminid},
		                     {'$set': {'premium_3': {'text': user_data['pre3_text'],
		                                             'url': user_data['pre3_url']}}})


def get_admin_db( adminid: int = None ):
	if adminid:
		return db.admins.find_one({'_id': adminid})
	return db.admins.find()


def update_pymnt_admin_db(adminid: int, paid: bool):
	db.admins.update_one({"_id": adminid}, {'$set': {'paid': paid}})


def insert_temp_admin_db(adminid: int):
	db.temp_admins.insert_one({'_id': adminid})


def get_temp_admin_db(adminid: int = None):
	if adminid:
		return db.temp_admins.find_one({'_id': adminid})
	return db.temp_admins.find()


def del_temp_admin_db(adminid: int):
	db.temp_admins.remove_one({'_id': adminid})
