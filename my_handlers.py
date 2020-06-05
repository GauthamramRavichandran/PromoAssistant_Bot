from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, Filters, CallbackQueryHandler, \
	InlineQueryHandler

from admins.ad_lists import get_shared, inlinequery_inlne_ck
from admins.ad_promo import start_regstr_promo, create_list_promo, delete_list_promo
from admins.ad_register import register, getname, check_group, set_header, foottext, footurl, configure_ck, \
	get_pre1_text, get_pre1_url, get_pre2_text, get_pre2_url, get_pre3_text, get_pre3_url, final_pre, add_group, \
	group_commands, settings, get_group
from ch_admins.ch_register import start_register_1, start_register_2, start_register_3, start_register_4
from common.com_callbacks import cancel, how_to, get_statistics
from const.PROMO_CONSTS import CONFIRMDELETE, NAME, ADDG, HEADER, FOOTTEXT, FOOTURL, CONFIRM, DESCR, FORWARD, PRE1_TEXT, \
	PRE1_URL, PRE2_TEXT, PRE2_URL, PRE3_TEXT, PRE3_URL, CHOICE, SELECT_GROUP

from dev.dev_ins_admin import activate_pre_ck, get_userid_from_forwrd

cancel_hndlr = CommandHandler('cancel', cancel)
inline_hndlr = InlineQueryHandler(inlinequery_inlne_ck)
promo_group_regstr_hndlr = ConversationHandler(
	entry_points = [MessageHandler(Filters.regex('Register for PromoGroup Admins'), register)],
	states = {
		NAME: [MessageHandler(Filters.forwarded, getname)],
		ADDG: [MessageHandler((Filters.text | Filters.forwarded) & ~Filters.command, check_group)],
		HEADER: [MessageHandler(Filters.text & (~Filters.command), set_header)],
		FOOTTEXT: [MessageHandler(Filters.text & (~Filters.command), foottext)],
		FOOTURL: [MessageHandler(Filters.text & (~Filters.command), footurl)]
	},
	fallbacks = [cancel_hndlr],
	allow_reentry = True,
	persistent = True,
	name = 'promogroup register'
)


settings_hndlr = ConversationHandler(
	entry_points=[MessageHandler(Filters.regex('.*Settings$'), settings)],
	states={
		CHOICE: [MessageHandler(Filters.regex('.*Edit Header and Footer$'), group_commands),
		         MessageHandler(Filters.regex('.*Add Group$'), add_group),
		         MessageHandler(Filters.regex('.*Add Premium Channels$'), get_pre1_text)],
		SELECT_GROUP: [MessageHandler(Filters.text & (~ Filters.command), get_group)],
		ADDG: [MessageHandler(Filters.text | Filters.forwarded, check_group)],
		HEADER: [MessageHandler(Filters.text & (~ Filters.command), set_header)],
		FOOTTEXT: [MessageHandler(Filters.text & (~ Filters.command), foottext)],
		FOOTURL: [MessageHandler(Filters.text & (~ Filters.command), footurl)],
		PRE1_TEXT: [MessageHandler(Filters.text & (~ Filters.command), get_pre1_url)],
		PRE1_URL: [MessageHandler(Filters.text & (~ Filters.command), get_pre2_text)],
		PRE2_TEXT: [MessageHandler(Filters.text & (~ Filters.command), get_pre2_url)],
		PRE2_URL: [MessageHandler(Filters.text & (~ Filters.command), get_pre3_text)],
		PRE3_TEXT: [MessageHandler(Filters.text & (~ Filters.command), get_pre3_url)],
		PRE3_URL: [MessageHandler(Filters.text & (~ Filters.command), final_pre)]
	},
	fallbacks=[cancel_hndlr],
	allow_reentry=True,
	persistent = True,
	name = 'settings conv.'
)
menu_hndlr = MessageHandler(Filters.regex('.*Menu$'), start_register_1)
how_to_hndlr = MessageHandler(Filters.regex('.*How to$'), how_to)
strt_promo_hndlr = MessageHandler(Filters.regex('^Open Registrations$'), start_regstr_promo)
crt_promo_hndlr = MessageHandler(Filters.regex('^Create list$'), create_list_promo)
dlt_promo_hndlr = MessageHandler(Filters.regex('^Delete list$'), delete_list_promo)
shared_list_hndlr = CommandHandler('getshared', get_shared)
config_hndlr = CommandHandler('configure', configure_ck)
stat_hndler = MessageHandler(Filters.regex('.*Statistics'), get_statistics)

chnl_admin_registr_hndlr = ConversationHandler(
	entry_points = [CommandHandler('start', start_register_1)],
	states = {
		FORWARD: [MessageHandler(Filters.forwarded, start_register_2)],
		DESCR: [MessageHandler(Filters.text & (~ Filters.command), start_register_3)],
		CONFIRM: [CallbackQueryHandler(start_register_4)]
	},
	fallbacks = [cancel_hndlr],
	allow_reentry = True,
	persistent = True,
	name = 'channel register conv.'
)

ins_premium_conv_hndlr = ConversationHandler(
	entry_points = [CommandHandler('insert', get_userid_from_forwrd)],
	states = {
		FORWARD : [MessageHandler(Filters.forwarded, activate_pre_ck)]
	},
	fallbacks = [cancel_hndlr],
	allow_reentry = True,
	persistent = True,
	name = 'Premium conv.')
