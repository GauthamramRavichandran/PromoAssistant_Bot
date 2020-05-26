from backend.db_main import db

try:
	db.statistics.insert_one({'_id': 0,
	                          'Total Groups': 0,
	                          'Total Channels Registered': 0,
	                          'Total Channels Banned': 0,
	                          'Total Promos Done': 0,
	                          'Total Lists Created': 0})
except:
	pass


def get_next_list_num_db():
	return db.statistics.find_one_and_update({'_id': 0}, {'$inc': {'Total Lists Created': 1}},
	                                         return_document = True)


def get_stat_db():
	return db.statistics.find_one({'_id': 0})
