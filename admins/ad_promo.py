from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from admins.ad_lists import create_list, delete_lists
from backend.db_admins import get_admin_db
from backend.db_grps import change_grp_status_db

from const.con_classes import STATUS
from const.con_texts import new_pin_tx

from validation.v_ad_promo import valid_open_regstr, valid_create_list, valid_del_list


def start_regstr_promo(update: Update, context):
	admin_info = get_admin_db(update.effective_user.id)
	if admin_info.get('groups', []):
		update.effective_message.reply_text("You don't have any groups registered with us")
	else:
		if valid_open_regstr(admin_info['groups']):
			for grp in admin_info['groups']:
				context.bot.send_message(chat_id = grp, text = new_pin_tx,
				                         reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Register here',
				                                                                                    url = f'{context.bot.link}?start={grp}')]]))
			change_grp_status_db(admin_info['groups'], STATUS.REGISTRATION_OPEN)
			update.effective_message.reply_text("Registrations are open for all your groups")
		else:
			update.effective_message.reply_text("Current status of your groups doesn't allow opening registration"
			                                    "\nIt's either already open (or) previous list is not deleted yet")


def create_list_promo( update: Update, context ):
	admin_info = get_admin_db(update.effective_user.id)
	if admin_info.get('groups', []):
		update.effective_message.reply_text("You don't have any groups registered with us")
	else:
		if valid_create_list(admin_info['groups']):
			update.effective_message.reply_text("Gimme a minute, I'm creating the lists for you")
			create_list(update, context)
			change_grp_status_db(admin_info['groups'], STATUS.LIST_PUBLISHED)
			update.effective_message.reply_text("Shared the lists in channel")
		else:
			update.effective_message.reply_text("Current status of your groups doesn't allow creating list"
			                                    "\nIt's either new (or) previous list is not deleted (or) not started registration")
			

def delete_list_promo(update: Update, context):
	admin_info = get_admin_db(update.effective_user.id)
	if admin_info.get('groups', []):
		update.effective_message.reply_text("You don't have any groups registered with us")
	else:
		if valid_del_list(admin_info['groups']):
			update.effective_message.reply_text("Gimme a minute, I'm deleting the lists for you")
			delete_lists(update, context)
			change_grp_status_db(admin_info['groups'], STATUS.LIST_DELETED)
			update.effective_message.reply_text("Deleted the lists from the channels")
		else:
			update.effective_message.reply_text("Current status of your groups doesn't allow deleting list"
			                                    "\nIt's either new (or) list is already deleted (or) not started registration")
