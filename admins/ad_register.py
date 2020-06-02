from re import search
from telegram import ReplyKeyboardRemove, MessageEntity, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from backend.db_admins import insert_admin_db, get_admin_db
from backend.db_grps import update_groups_db, get_groupinfo_db
from backend.db_admins import insert_premium_chnls_db, get_temp_admin_db

from common.com_bot_data import get_admins_list, get_chnls_list, append_admins, append_chnl, \
	get_grps_list, append_grps
from common.com_callbacks import log_this, j_delete_msg, cancel
from common.com_decorators import nogroup
from common.com_kb_mks import reset_markup, cancel_markup, kbmenu_markup, settings_menu_markup

from const.con_classes import ValidationError
from const.con_my_emojis import e_info, e_confused, e_success
from const.PROMO_CONSTS import CONFIRMDELETE, NAME, ADDG, HEADER, FOOTTEXT, FOOTURL, PRE1_TEXT, PRE1_URL, PRE2_TEXT, \
	PRE2_URL, PRE3_TEXT, PRE3_URL, SELECT_GROUP, CHOICE


@nogroup
def register(update, context):
	if update.effective_user.id in get_admins_list(context):
		update.message.reply_text('It seems you have already registered\n'
		                          'Do you want to reset everything?\n\n'
		                          f'{e_info}PS. If you send "Reset All", everything will be deleted, '
		                          f'no confirmations will be asked', reply_markup=reset_markup)
		return CONFIRMDELETE
	if not get_admin_db(update.effective_user.id):
		update.effective_message.reply_text("You can't register, pls confirm with @ys0serious that you have a promogroup."
		                                    "\nSo that I can let you register")
		return ConversationHandler.END
	update.message.reply_text('We can begin the registration process right away')
	context.bot.send_message(text = e_info+'Forward a message/post from your promotions channel',
	                         chat_id = update.effective_user.id, reply_markup=cancel_markup)
	return NAME


# FIXME fix it
'''def confirmation(update, context):
	if search('.*Reset All', update.message.text):
		update.message.reply_text("You've initiated a resetting process.\nWiping your data",
		                          reply_markup=ReplyKeyboardRemove())
		update.message.reply_text('pls wait...')
		wipe_from_base(update.message.chat.id)
		reset_lists(update, context)
		update.message.reply_text('Who are you then?')
	return cancel(update, context)'''


def getname(update, context):
	try:
		if update.effective_message.forward_from_chat.type == 'channel':
			chanid = str(update.effective_message.forward_from_chat.id)
			if not update.effective_message.forward_from_chat.username:
				raise Exception('Only public channels allowed')
			if chanid in get_chnls_list(context):
				raise Exception("There's already a channel\nWe can't add this")
			append_chnl(chnlid = chanid, context = context)
			append_admins(adminid = update.effective_user.id, context = context)
			insert_admin_db(adminid = update.effective_user.id,
			                username = update.message.chat.username, chnlid = chanid,
			                chnlname = update.effective_message.forward_from_chat.title,
			                chnlusername = f'@{update.effective_message.forward_from_chat.username}')
			log_this(f': New Admin :\nAdmin (#{update.effective_user.id}) inserted')
			update.message.reply_text("Add me as admin in this channel if you haven't done yet")
			update.message.reply_text('Send me the group id')
			update.message.reply_text("To know your group id,"
			                          "\n1. Add me into your group as an admin "
			                          f"\n2. Send /configure@{context.bot.username} in group"
			                          "\n3. Group ID will be sent to your group"
			                          "\n4. Forward me the message", reply_markup = cancel_markup)
			return ADDG
		raise Exception('Only Channels allowed')
	except Exception as e:
		update.message.reply_text(e_confused+str(e))


# FIXME add_grp
def add_group(update, context):
	admininfo = get_admin_db(update.effective_user.id)
	if not admininfo.get('groups'):
		update.message.reply_text("You haven't added any groups yet")
		update.message.reply_text("Send 'Register for PromoGroup Admins' > 'Reset All' and start the registration process from the top")
		return ConversationHandler.END
	else:
		update.message.reply_text('Send me the group id')
		update.message.reply_text("To know your group id,"
		                          "\n1. Add me into your group as an admin "
		                          f"\n2. Send /configure@{context.bot.username} in group"
		                          "\n3. Group ID will be sent to your group"
		                          "\n4. Forward me the message", reply_markup = cancel_markup)
		return ADDG


def configure_ck(update, context):
	try:
		if update.message.chat.type != 'supergroup':
			raise ValidationError("I'm compatible only in supergroup")
		msg_info = context.bot.send_message(text = 'Give me a sec!', chat_id = update.message.chat.id)
		if str(type(msg_info)).endswith("Promise'>"):
			msg_info = msg_info.result()
		msg_info.delete()
		msg_obj = context.bot.send_message(text = f"{msg_info.chat.id} | GroupID" \
		                                          f"\n\nNote for Admin : " \
		                                          f"\n\t\tForward me this message in private",
		                                   chat_id = update.message.chat.id)
		context.job_queue.run_once(j_delete_msg, 150, context = msg_obj)
	except ValidationError as v:
		update.message.reply_text(str(v))


def check_group(update, context):
	user_data = context.user_data
	try:
		grpid = update.message.text.split('|', maxsplit = 1)[0].strip()
		msg = context.bot.send_message(text=e_success+'Successfully integrated', chat_id=grpid)
		if str(type(msg)).endswith("Promise'>"):
			msg = msg.result()
		if not msg:
			raise ValidationError(f'Check whether our bot @{context.bot.username} is added as admin in this group')
		if msg.chat.id in get_grps_list(context):
			raise ValidationError("This group is already registered with us"
			                      "\nSend the group ID, that's not registered already")
		if msg.chat.type != 'supergroup':
			raise ValidationError('Only Supergroups allowed')
		
		user_data['group'] = msg.chat.id
		user_data['title'] = str(msg.chat.title)
		update.message.reply_text('Now add header text for your promolist\n '
		                          'Criteria :: One line and not longer than 35letters')
		return HEADER
	
	except ValidationError as v:
		update.message.reply_text(f'{e_confused}{v}\nAnd then forward me the same message again')
	except Exception as e:
		update.message.reply_text(f'{e_confused}{e}')


def set_header(update, context):
	user_data = context.user_data
	try:
		msg = update.message.text.strip()
		if not len(msg.split('\n')) > 1:
			if len(msg) < 38:
				user_data['header'] = msg
				update.message.reply_text(msg)
				update.message.reply_text('Now add footer text for your promolist\n '
				                          'Criteria :: One line and not longer than 35letters')
				return FOOTTEXT
			raise Exception('Header should be lesser than 35 words\nYour length : '+str(len(msg)))
		raise Exception('Only one line is allowed')
	except Exception as e:
		update.message.reply_text(f'{e_confused}\n{e}')


def foottext(update, context):
	try:
		msg = update.message.text.strip()
		if len(msg.split('\n')) > 1:
			raise Exception('Only one line is allowed')
		if len(msg) > 38:
			raise Exception('Footer should be lesser than 35 words\nYour length : '+str(len(msg)))
		
		for i in update.message.text:
			if i in '()[]':
				raise Exception('Sorry, your text contains restricted letters -> ()[]')
		context.user_data['text'] = update.message.text
		update.message.reply_text('Now send the invitelink of this group\nOnly URL allowed')
		return FOOTURL
	
	except Exception as e:
		update.message.reply_text(f'{e_confused}\n{e}')


def footurl(update, context):
	user_data = context.user_data
	try:
		for i in update.message.text:
			if i in '()[]':
				raise ValidationError('Sorry, your text contains restricted letters -> ()[]')
		dictt = update.message.parse_entities(MessageEntity.ALL_TYPES)
		for key in dictt.keys():
			if key.type == 'url':
				user_data['url'] = dictt[key]
				break
		if 'url' not in user_data:
			raise ValidationError('URL not found')
		update_grp = True
		if not user_data.get('edit', 0):
			update_grp = None
			append_grps(user_data['group'], context = context)
			
		update_groups_db(adminid=update.message.chat.id, groups=user_data['group'],
		                 header=user_data['header'], name=user_data['title'],
		                 foot_text=user_data['text'], foot_url=user_data['url'], update = update_grp)
		log_this(f'AdminID :: {update.message.chat.id}'
		         f"\nHeader :: {user_data['header']}"
		         f"\nFooter :: {user_data['text']}"
		         f"\nURL :: {user_data['url']}")
		if user_data.get('edit', None):
			update.message.reply_text('Footer edited successfully', reply_markup=kbmenu_markup)
			del user_data['edit']
			return cancel(update, context)
		update.message.reply_text('Footer added successfully')
		update.message.reply_text('Next Group')
		return add_group(update, context)
	except ValidationError as f:
		update.message.reply_text(f'Error :: {f}')
	except Exception as e:
		update.message.reply_text(f'{e_confused}\n{e}')


def get_pre1_text(update, context):
	update.message.reply_text('Premium users can add upto 3 premium channels\nFree users can add only one premium channel')
	update.message.reply_text('Now, Send the text of the Premium-1 Channel')
	return PRE1_TEXT


def get_pre1_url(update, context):
	context.user_data['pre1_text'] = update.message.text.strip()
	if len(context.user_data['pre1_text'].split(' ')) >= 3:
		update.message.reply_text("Your text won't be fully visible\nSo keep it short")
		return PRE1_TEXT
	for i in context.user_data['pre1_text']:
		if i in '()[]':
			update.message.reply_text('Text should not contain any of these chars -> ()[]')
			return PRE1_TEXT
	update.message.reply_text('Send the url of the Premium-1 Channel')
	return PRE1_URL


def get_pre2_text(update, context):
	context.user_data['pre1_url'] = update.message.text.strip()
	if not context.user_data['pre1_url'].startswith('http') and not context.user_data['pre1_url'].startswith('t.me'):
		update.message.reply_text('Only LINKS allowed')
		return PRE1_URL
	insert_premium_chnls_db(adminid = update.message.chat_id, user_data = context.user_data, num = 1)
	update.message.reply_text('Premium-1 channel inserted successfully')
	if update.message.chat_id in get_admins_list(context):
		update.message.reply_text("I'm sorry,you can't add anymore premium channels")
		update.message.reply_text("Buy premium to activate 2 more slots")
		return cancel(update, context)
	update.message.reply_text('Send the text of the Premium-2 Channel')
	return PRE2_TEXT


def get_pre2_url(update, context):
	context.user_data['pre2_text'] = update.message.text.strip()
	if len(context.user_data['pre2_text'].split(' ')) > 3:
		update.message.reply_text("Your text won't be fully visible\nSo keep it short")
		return
	for i in context.user_data['pre2_text']:
		if i in '()[]':
			update.message.reply_text('Text should not contain any of these chars -> ()[]')
			return
	update.message.reply_text('Send the url of the Premium-2 Channel')
	return PRE2_URL


def get_pre3_text(update, context):
	context.user_data['pre2_url'] = update.message.text.strip()
	if not context.user_data['pre2_url'].startswith('http') and not context.user_data['pre2_url'].startswith('t.me'):
		update.message.reply_text('Only LINKS allowed')
		return
	insert_premium_chnls_db(adminid = update.message.chat_id, user_data = context.user_data, num = 2)
	update.message.reply_text('Premium-2 channel inserted successfully')
	update.message.reply_text('Send the text of the Premium-3 Channel')
	return PRE3_TEXT


def get_pre3_url(update, context):
	context.user_data['pre3_text'] = update.message.text.strip()
	if len(context.user_data['pre3_text'].split(' ')) > 3:
		update.message.reply_text("Your text won't be fully visible\nSo keep it short")
		return
	for i in context.user_data['pre3_text']:
		if i in '()[]':
			update.message.reply_text('Text should not contain any of these chars -> ()[]')
			return
	update.message.reply_text('Send the url of the Premium-3 Channel')
	return PRE3_URL


def final_pre(update, context):
	context.user_data['pre3_url'] = update.message.text.strip()
	if not context.user_data['pre3_url'].startswith('http') and not context.user_data['pre3_url'].startswith('t.me') :
		update.message.reply_text('Only LINKS allowed')
		return
	insert_premium_chnls_db(adminid = update.message.chat_id, user_data = context.user_data, num = 3)
	update.message.reply_text('Premium-3 channel inserted successfully')
	update.message.reply_text('Premium Channels have been added successfully\n'
	                          '\nIf you wanna change anything, you have to do it before scheduling lists')
	return cancel(update, context)


def settings(update, context):
	context.bot.send_message(chat_id = update.message.chat.id, text = 'Settings',
	                         reply_markup = settings_menu_markup)
	return CHOICE


def group_commands(update, context):
	admininfo = get_admin_db(update.effective_user.id)
	grps = admininfo.get('groups')
	if not grps or not grps[0]:
		update.message.reply_text("You haven't added any groups yet")
		return ConversationHandler.END
	
	elif search('.*Edit', update.message.text):
		context.user_data['edit'] = True
		# kbgrpmenu = [[]] >>>>
	kbgrpmenu = [[]]
	# reserved for future releases >>>>
	'''else:
		context.user_data['edit'] = False
		kbgrpmenu = [[KeyboardButton('All Groups')]]
		context.user_data['channel'] = admininfo.get('channel id')
		context.user_data['channel_username'] = admininfo.get('channel username')
		context.user_data['premium_1'] = admininfo.get('premium_1', [])
		context.user_data['premium_2'] = admininfo.get('premium_2', [])
		context.user_data['premium_3'] = admininfo.get('premium_3', [])'''
	context.user_data['groups'] = []
	context.user_data['adminid'] = update.effective_user.id
	context.user_data['group_dict'] = {}
	for grp in grps:
		if not context.user_data['edit']:
			continue
		context.user_data['groups'].append(grp)
		context.user_data['group_dict'].update({grp: get_groupinfo_db(grp)})
		kbgrpmenu.append([KeyboardButton(str(grp)+' | '+str(context.user_data['group_dict'][grp].get('name')))])
	# reserved for future releases >>>>
	'''if len(kbgrpmenu) < 2:
		update.message.reply_text('Lists have been scheduled/posted in all groups'
		                          '\nWait till it finishes')
		return cancel(update, context)'''
	kbgrpmenu.append([KeyboardButton('/cancel')])
	kbgrpmenu_markup = ReplyKeyboardMarkup(kbgrpmenu, resize_keyboard = True, one_time_keyboard = True)
	context.bot.send_message(chat_id = update.message.chat_id, text = 'Select a Group', reply_markup = kbgrpmenu_markup)
	return SELECT_GROUP


def get_group(update, context):
	msg = update.message.text.split('|')[0].strip()
	if search('.*All Groups', msg):
		context.user_data['select_group'] = 'All Groups'
	elif msg[1:].isdigit() and (int(msg) in context.user_data['groups']):
		context.user_data['select_group'] = int(msg)
		
	if 'select_group' not in context.user_data:
		update.message.reply_text('Invalid Text\nSelect from the buttons')
	else:
		if context.user_data['edit']:
			context.user_data['group'] = context.user_data['select_group']
			context.user_data['title'] = str(update.message.text.split('|')[-1].strip())
			update.message.reply_text('Now add header text for your promolist'
																'\n Criteria :: One line and not longer than 35letters')
			return HEADER
		# reserved for future releases >>>>
		'''update.message.reply_text(text = 'What should I do now?',
		                          reply_markup = domenu_markup)
		return DO_WHAT'''