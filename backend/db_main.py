from pymongo import MongoClient

client = MongoClient()
# print(client.list_database_names())  # Databases
db = client.promo_assistant
print(db.collection_names())  # Collections


def load_bot_data_db():
	channel_list = []
	admins_list = []
	groups_list = []
	ban_id = []
	ban_name = []
	admins_find = db.admins.find()
	banned_find = db.banned_channels.find()
	# groups_find = db.groups.find()
	for i in admins_find:
		if i is not None:
			if i.get('channel id') not in channel_list:
				channel_list.append(i.get('channel id'))
			if i.get('_id') not in admins_list:
				admins_list.append(i.get('_id'))
			grps = i.get('groups')
			for grp in grps:
				if grp not in groups_list:
					groups_list.append(grp)

	for k in banned_find:
		if k is not None:
			ban_id.append(k.get('_id'))
			ban_name.append(k.get('name'))
	list_dict = {'channels': channel_list, 'admins': admins_list, 'groups': groups_list,
	             'ban_id': ban_id, 'ban_name': ban_name}
	return list_dict
