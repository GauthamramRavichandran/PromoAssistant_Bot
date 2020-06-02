from backend.db_admins import insert_temp_admin_db

from common.com_kb_mks import cancel_markup
from common.com_decorators import onlyme
from const.PROMO_CONSTS import FORWARD


@onlyme
def get_userid_from_forwrd( update, context ):
	update.effective_message.reply_text('Forward me a message from the user', reply_markup = cancel_markup)
	return FORWARD


def activate_pre_ck( update, context ):
	if update.message['forward_from']:
		user_id = update.effective_message.forward_from.id
		insert_temp_admin_db(user_id)
		update.message.reply_text("Inserted into temp_admins")
		return -1
	else:
		update.message.reply_text("I can't find the info of the user from the forwarded message."
		                          "\nAsk the user to change his/her privacy settings"
		                          "\nGo to Settings>Privacy and Security>"
		                          "Under Privacy, Forwarded Messages> Change it to Everybody")
		update.message.reply_text("Forward the message once the user has changed the settings")