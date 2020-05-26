
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
		

		


