from backend.db_main import db
from const.con_classes import STATUS


def update_groups_db(adminid, groups, bot = None, name = 'A Promotional Group', header = 'Top Awesome Channels',
                     foot_text = 'Join Now', foot_url = 'https://t.me/ASM_Official', update = None, min_subs_req: int = 0):
	if update:
		db.groups.update_one({'_id': groups}, {'$set':
			                                       {'header': header,
			                                        'footer': {'text': foot_text, 'url': foot_url},
			                                        'name': name}})
	else:
		db.admins.update_one({'_id': adminid}, {'$push': {'groups': groups}})
		chanid = db.admins.find_one({'_id': adminid}).get('channel id')
		db.groups.insert_one({'_id': groups,
		                      'channel id': chanid,
		                      'bot': bot,
		                      'minimum subs required': min_subs_req,
		                      'header': header,
		                      'footer': {'text': foot_text,
		                                 'url': foot_url},
		                      'name': name,
		                      'status': STATUS.NEW})
		db.statistics.update_one({'_id': 0}, {'$inc': {'Total Groups': 1}})


def get_groupinfo_db(grpid):
	return db.groups.find_one({'_id': grpid})


def change_grp_status_db(groups: list, status: str):
	for grp in groups:
		db.groups.update_one({'_id': grp}, {'$set': {'status': status}})
