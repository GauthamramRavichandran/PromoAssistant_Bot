from random import choice
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown as e_m
from telegram.ext.dispatcher import run_async
from time import sleep

from backend.db_admins import get_admin_db
from backend.db_chnls import reg_channels_db, update_shared_db, check_shared_db
from backend.db_grps import get_groupinfo_db
from backend.db_list import insert_list_db, reset_registrations_db
from backend.db_stats import get_next_list_num_db

from common.com_bot_data import get_grps_list, get_admins_list
from common.com_callbacks import log_this
from common.com_kb_mks import kbmenu_markup
from const.con_my_emojis import e_star, e_tada, e_sparkles, e_dizzy, e_point_right, e_large_blue_diamond,\
e_sunny, e_globe, e_zap, e_moon, e_speaker, e_name_badge, e_spades, e_radio_button,\
e_gem, e_beginner, e_new
from const.CONFIG import MIN_CHNLS_PER_LIST

list_emojis = [e_star, e_tada, e_sparkles, e_dizzy, e_point_right, e_large_blue_diamond, e_sunny, e_globe,
               e_zap, e_moon, e_speaker, e_name_badge, e_spades, e_gem, e_beginner, e_radio_button, e_new]


@run_async
def create_list(update: Update, context):
	try:
		admin_info = get_admin_db(update.effective_user.id)
		for grp in admin_info['groups']:
			''' grp -> Group ID
					grp_info -> Group Dict '''
			grp_info = get_groupinfo_db(grp)
			if grp_info:
				header = grp_info['header']
				footer = grp_info['footer']
				chnls = reg_channels_db(adminid = update.effective_user.id, groupid = grp)
				chnl_list = []
				for j in chnls:
					chnl_list.append(j)
				chnl_list.sort(key = lambda x: x.get('members count'), reverse = True)
				if not chnl_list:
					context.bot.send_message(text = f"No Channels registered for the group {grp_info['name']}",
					                         chat_id = admin_info['_id'])
					continue
				
				#################################
				''' List Creation Logic  '''
				'''   quotient = No of Lists '''
				
				f = True
				num = MIN_CHNLS_PER_LIST//2
				quotient = 1
				remain = 0
				total = len(chnl_list)
				if total > MIN_CHNLS_PER_LIST:
					while f:
						quotient = total//num
						remain = total % num
						if quotient >= remain:
							f = False
						else:
							num += 1
				else:
					num = total
				num2 = num+1
				n = 0
				emoticon_1 = choice(list_emojis)
				for g in range(quotient):
					post = f'*'+e_m(str(header))+'*\n'+e_m(10*'━━')+'\n\n'
					if not remain:
						num2 = num
					else:
						remain -= 1
					to_send = {}
					
					for _ in range(num2):
						to_send.update({chnl_list[n].get('_id'): chnl_list[n].get('name')})
						post += f"{emoticon_1}[{chnl_list[n].get('name')[1:]}]({chnl_list[n].get('invitelink')})" \
						        f"\n\t\t\t\t\t\t*{chnl_list[n].get('description')}*\n\n"
						n += 1
					
					if admin_info.get('premium_1', []):
						post += f"\n\t[{admin_info['premium_1']['text']}]({admin_info['premium_1']['url']})"
						if admin_info.get('premium_2', []):
							post += f"\t|\t[{admin_info['premium_2']['text']}]({admin_info['premium_2']['url']})"
							if admin_info.get('premium_3', []):
								post += f"\t|\t[{admin_info['premium_3']['text']}]({admin_info['premium_3']['url']})"
					grpname = context.bot.get_chat(chat_id = grp).title
					post += f"\n{e_m(10*'━━')}\n[{footer['text']}]({footer['url']})"
					kb = [[InlineKeyboardButton(text = grpname, callback_data = 'prbt_1')],
					      [InlineKeyboardButton(text = 'Created by this bot', url = context.bot.get_me().link)]]
					context.bot.send_message(text = post, chat_id = admin_info['channel id'], parse_mode = 'Markdown',
					                         reply_markup = InlineKeyboardMarkup(kb), disable_web_page_preview = True)
					list_id = get_next_list_num_db()['Total Lists Created']
					insert_list_db(list_id = list_id, grpname = grp_info['name'], text = post)
					to_chnl = f"List {g + 1}\n" \
					          f"\t\t⏩ `@PromoAssistant_bot {list_id}`\n\n\t"
					to_chnl += '\n\t'.join(e_m(v) for v in to_send.values())
					context.bot.send_message(chat_id = admin_info['channel id'], text = to_chnl, parse_mode = 'Markdown')
					failed = 'Auto-Posting failed in these Channels::\nShare the list manually\n\n'
					for chnl in to_send.keys():
						try:
							shared = context.bot.send_message(text = post, chat_id = chnl, disable_web_page_preview = True,
							                                  parse_mode = 'Markdown')
							if str(type(shared)).endswith("Promise'>"):
								shared = shared.result()
								# Private chnls will have None as link
							context.bot.send_message(text = f"#shared|{to_send[chnl]}|{shared.link}", chat_id = grp,
							                         disable_notification = True, disable_web_page_preview = True)
							update_shared_db(chnlid = chnl, forwarded_from = admin_info['channel id'], time = shared.date,
							                 msgid = shared.message_id)
							sleep(0.1)  # Cooldown, prevents flooding
						except:
							failed += f"{to_send[chnl]}\n"
							sleep(0.2)  # Cooldown, prevents flooding
					if len(failed) > 80:
						context.bot.send_message(text = failed, chat_id = grp)
			log_this(f" List created for the admin {admin_info['_id']}\n{admin_info['channel username']}")
		else:
			context.bot.send_message(text = "You don't have any groups registered", chat_id = update.effective_user.id)
	except Exception as e:
		context.bot.send_message(chat_id = update.effective_user.id, text = f"Error occurred during list creation, \n\n{e}",
		                         reply_markup = kbmenu_markup)


def get_shared(update, context):
	if update.message.chat.type != 'supergroup':
		update.message.reply_text('This command only works in supergroup')
	elif update.effective_user.id not in get_admins_list(context):
		update.message.reply_text('Only admins can do that')
	elif update.message.chat_id not in get_grps_list(context):
		update.message.reply_text('This group is not registered with us')
	else:
		grpid = update.message.chat_id
		chnlid = get_groupinfo_db(grpid).get('channel id')
		shared_list = check_shared_db(chnlid = chnlid, grpid = grpid)
		if shared_list:
			shared_str = '#shared List ::\n\n'
			for j in shared_list:
				share = j.get('shared on')
				shared_str += f"[{j.get('name')}](https://t.me/{j.get('name')[1:]}/{j.get('msgid')})" \
				              f"\t {share:%d-%b %H:%M}\n"
			if len(shared_str) > 20:
				context.bot.send_message(text = shared_str, chat_id = update.message.chat.id,
				                         reply_to_message_id = update.message.message_id, parse_mode = 'Markdown', disable_web_page_preview = True)
				return
		context.bot.send_message(text = 'OOPS! No one shared the list yet', chat_id = update.message.chat.id,
		                        reply_to_message_id = update.message.message_id, parse_mode = 'Markdown')

# TODO get unshared list and send to admin. this function deeltes only if shared
def delete_lists(update, context):
	admin_info = get_admin_db(update.effective_user.id)
	for grp in admin_info['groups']:
		to_delete = check_shared_db(chnlid = admin_info['channel id'], grpid = grp)
		failed = f'Deletion Failed:\n\n'
		if to_delete:
			for chnl in to_delete:
				try:
					context.bot.delete_message(chat_id = chnl['_id'], message_id = chnl['msgid'])
					sleep(0.1)
				except Exception as e :
					failed += f"\n{chnl['name']} - {e}"
			if len(failed) > 30:
				context.bot.send_message(chat_id = grp, text = failed)
			else:
				context.bot.send_message(chat_id = grp,
				                         text = f'All lists deleted successfully')
	reset_registrations_db(update.effective_user.id, admin_info['groups'])