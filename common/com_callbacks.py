from telegram import Bot
from telegram.utils.helpers import escape_markdown as e_m

from backend.db_stats import get_stat_db
from const.CONFIG import LOG_BOT_TKN, LOG_CHNL, SUPPORT_USERNAME
from common.com_decorators import nogroup
from common.com_kb_mks import kb_admins_markup, kbmenu_default_markup, settings_menu_markup
from const.PROMO_CONSTS import CHOICE
from common.com_bot_data import get_admins_list


@nogroup
def menu(update, context):
	try:
		if update.effective_user.id in get_admins_list(context):
			
			context.bot.send_message(chat_id = update.message.chat.id, text = "Menu",
			                         reply_markup = kb_admins_markup)
		else:
			context.bot.send_message(chat_id = update.message.chat.id, text = 'Menu',
			                         reply_markup = kbmenu_default_markup)
	
	except Exception as e:
		print(str(e))


def cancel(update, context):
	menu(update, context)
	return -1


if LOG_BOT_TKN:
	log_bot = Bot(token = LOG_BOT_TKN)


def log_this(text, markdown = False):
	if not LOG_BOT_TKN:
		return
	if markdown:
		log_bot.send_message(chat_id = LOG_CHNL, text = text, disable_web_page_preview = True, parse_mode = 'Markdown')
	else:
		log_bot.send_message(chat_id = LOG_CHNL, text = text, disable_web_page_preview = True)


def settings(update, context):
	context.bot.send_message(chat_id = update.message.chat.id, text = 'Settings', reply_markup = settings_menu_markup)
	return CHOICE


def check_channel_admin(bot, botid, chnlid):
	if bot.get_chat_member(chat_id = chnlid, user_id = botid).status == 'administrator':
		return True


'''def page_2_menu(update, context):
	context.bot.send_message(chat_id = update.message.chat.id, text = 'Next', reply_markup = page_2_markup)'''


def how_to(update, context):
	context.bot.send_message(text = f'Steps:'\
													f'\n0.Make me *admin* in promotions chnl and all the groups'\
													f'\n1.Forward me a post from the promotions (notifications) channel 🔔'\
													f'\n2.Send /configure@{e_m(context.bot.username)} and forward the reply msg to me'\
													f'\n3.Send the header (e.g.,Top Telegram chnls) and footer text (e.g.,Join now to promote) for the list'\
													f'\n4.After that, follow the same steps(2-6) for registering another group'\
													f'\n\n\t 🚁 Contact @{e_m(SUPPORT_USERNAME)} for assistance',
	                        chat_id = update.message.chat.id, parse_mode = 'Markdown', disable_web_page_preview = True)


def start(update, context):
	context.bot.send_message(text = "Hi! I'm your PromoAssistant\nI can help the admins of promogroup",
	                 chat_id = update.message.chat.id, reply_markup = kbmenu_default_markup)


def get_statistics(update, context):
	stats_info = get_stat_db()
	to_send = f'Statistics of {e_m(context.bot.username)}\n\n'
	for k, v in stats_info.items():
		if k == '_id':
			continue
		to_send += f"*{k}* :: {v}\n"
	to_send += f"\nOur Bots :: {e_m('@ASM_Scripts')}\nNews :: {e_m('@ASM_Official')}"
	update.message.reply_markdown(to_send)
	
	
def j_delete_msg(context):
	try:
		msg_obj = context.job.context
		if str(type(msg_obj)).endswith("Promise'>"):
			msg_obj = msg_obj.result()
		msg_obj.delete()
	except:
		pass