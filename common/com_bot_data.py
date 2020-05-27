# TODO get data from db
from backend.db_main import load_bot_data_db


def load_db_to_bot(context):
	# context.bot_data
	db_dict = load_bot_data_db()
	# list_dict = {'channels': channel_list, 'admins': admins_list, 'groups': groups_list,
	# 	             'ban_id': ban_id, 'ban_name': ban_name}
	context.bot_data['groups'] = db_dict['groups']
	context.bot_data['chnls'] = db_dict['channels']
	context.bot_data['admins'] = db_dict['admins']
	context.bot_data['banid'] = db_dict['ban_id']
	context.bot_data['banname'] = db_dict['ban_name']
	print('Data loaded from DB to bot_data')


def get_grps_list(context):
	return context.bot_data.get('groups', [])


def append_grps(grpid, context):
	if 'groups' in context.bot_data:
		context.bot_data['groups'].append(grpid)
	else:
		context.bot_data['groups'] = [grpid]
		
	
def get_admins_list(context):
	return context.bot_data.get('admins', [])


def append_admins(adminid, context):
	if 'admins' in context.bot_data:
		context.bot_data['admins'].append(adminid)
	else:
		context.bot_data['admins'] = [adminid]


def get_chnls_list(context):
	return context.bot_data.get('chnls', [])


def append_chnl(chnlid, context):
	if 'chnls' in context.bot_data:
		context.bot_data['chnls'].append(chnlid)
	else:
		context.bot_data['chnls'] = [chnlid]
		

		


