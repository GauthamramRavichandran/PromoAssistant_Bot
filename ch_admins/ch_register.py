from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram.utils.helpers import escape_markdown as e_m

from backend.db_admins import get_temp_admin_db
from backend.db_chnls import add_new_channel_db
from backend.db_grps import get_groupinfo_db

from common.com_bot_data import get_admins_list
from common.com_callbacks import cancel
from common.com_kb_mks import confirm_mk, cancel_markup, kbmenu_default_markup, kb_admins_markup, contact_us_markup
from const.CONFIG import MY_ID, DESCR_LIMIT
from const.PROMO_CONSTS import DESCR, CONFIRM, FORWARD
from const.con_my_emojis import e_trophy
from const.con_classes import ValidationError
''' f'\n\nFormat :: \n#new | @Chnlname | Description here | Invitelink here', '''


def start_register_1(update, context):
	if update.message.chat.type == 'supergroup':
		update.message.reply_text(f'{context.bot.link}?start={update.message.chat.id}')
		return -1
	
	elif context.args and context.args[0]:
		try:
			context.user_data['grpid'] = int(context.args[0])
			grpinfo = get_groupinfo_db(context.user_data['grpid'])
			context.user_data['grpname'] = grpinfo.get('name')
			context.user_data['promochnid'] = grpinfo.get('channel id')
		except:
			update.message.reply_text('Invalid Link')
			return cancel(update, context)
		'''my_chnls = get_chnl_db(chanid = context.user_data['promochnid'], adminid = update.message.chat.id)
		chnl_btn = []
		for chnl in my_chnls:
			chnl_btn.append([InlineKeyboardButton(f"{chnl['name']}", callback_data = f"c_{chnl['_id']}")])
		chnl_btn.append([InlineKeyboardButton("Add New Channel", callback_data = "new")])
		update.message.reply_text("Select an option,", reply_markup = InlineKeyboardMarkup(chnl_btn))'''
		update.message.reply_text(f'To submit your channel to {context.user_data["grpname"]} ,'
		                          f'\nForward me a post from your channel', reply_markup = cancel_markup)
		return FORWARD
	
	else:
		if update.effective_user.id in get_admins_list(context):
			update.effective_message.reply_text(f"Hey there, {update.effective_user.first_name}", reply_markup = kb_admins_markup)
		elif get_temp_admin_db(update.effective_user.id):
			context.bot.send_message(text = "Hi! I'm your PromoAssistant\nI can help the admins of promogroup",
		                           chat_id = update.message.chat.id, reply_markup = kbmenu_default_markup)
		else:
			update.effective_message.reply_text("We currently allow only *selected candidates* to be registered."
			                                    "\nContact the developer if you have promogroup"
			                                    "\n\nPS. If you don't know what is a promogroup, then kindly *donot* contact us",
			                                    reply_markup = contact_us_markup, parse_mode = 'Markdown')
			
			
def start_register_2(update, context):
	try:
		if update.message.forward_from_chat.type != 'channel':
			raise ValidationError('Only Channels allowed')
		context.user_data['chnlid'] = update.message.forward_from_chat.id
		context.user_data['chnltitle'] = update.message.forward_from_chat.title
		if update.message.forward_from_chat.username is None:
			raise ValidationError("We are accepting only public channels as of now")
		context.user_data['chnlusnme'] = '@'+update.message.forward_from_chat.username
		'''banned = get_ban()
		if context.user_data['chnlid'] in banned[0] or context.user_data['chnlusnme'].lower() in banned[1]:
			update.message.reply_text('Oops! Your channel has been banned')
			return cancel(update, context)'''
		mem_count = context.bot.get_chat_members_count(context.user_data['chnlusnme'])
		min_subs_required = get_groupinfo_db(context.user_data['grpid']).get('minimum subs required', 0)
		if mem_count < min_subs_required and not (update.effective_user.id in get_admins_list(context)
		                                          or update.effective_user.id in MY_ID):
			raise ValidationError(f'Minimum Subs required for this promogroup -> {min_subs_required}')
		context.user_data['memcount'] = mem_count
		update.message.reply_text('Send the description,')
		return DESCR
	except ValidationError as v:
		update.message.reply_text(f'{v}', reply_markup = cancel_markup)


def start_register_3(update, context):
	got_descr = update.message.text
	if len(got_descr) > DESCR_LIMIT:
		update.message.reply_text(f'Description length should be lesser than {DESCR_LIMIT}\n{len(got_descr)}')
	else:
		context.user_data['descr'] = got_descr
		to_send = f"*Name* :: {e_m(context.user_data['chnltitle'])}" \
		    f"\n*Username* :: {e_m(context.user_data['chnlusnme'])}" \
		 f"\n*Subscribers* :: {context.user_data['memcount']}" \
		 f"\n*Description* :: \n{e_m(context.user_data['descr'])}" \
		       f"\n*Group* :: {e_m(context.user_data['grpname'])}"
		context.user_data['to_send'] = to_send
		update.message.reply_text(to_send, parse_mode = ParseMode.MARKDOWN, reply_markup = confirm_mk)
		return CONFIRM


def start_register_4(update, context):
	query = update.callback_query
	data = query.data
	if data[-1] == '1':
		query.message.edit_reply_markup(reply_markup = None)
		add_new_channel_db(chnlid = context.user_data['chnlid'], chnlname = context.user_data['chnlusnme'],
		                   adminid = query.message.chat.id, descr = context.user_data['descr'],
		                   memcount = context.user_data['memcount'], ingroup = context.user_data['grpid'],
		                   url = f'https://t.me/{context.user_data["chnlusnme"][1:]}')
		
		query.message.reply_text('Your channel has been successfully added')
		context.bot.send_message(text = f"{e_trophy} Channel Submitted Successfully {e_trophy} "
		                                f"\n{context.user_data['to_send']}",
		                         chat_id = context.user_data['grpid'], parse_mode = ParseMode.MARKDOWN,
		                         disable_notification = True, disable_web_page_preview = True)
		return cancel(update, context)
	else:
		query.message.edit_reply_markup(reply_markup = None)
		update.effective_message.reply_text('Ohk! You have cancelled the submission.'
		                                    '\n\nTo register again, open the register link from the group')
		return ConversationHandler.END