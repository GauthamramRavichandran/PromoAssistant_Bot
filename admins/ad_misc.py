from backend.db_admins import get_admin_db
from backend.db_chnls import remove_channel_db


def remove_channel(update, context):
	if context.args:
		chnlid = get_admin_db(update.effective_user.id).get('channel id')
		remove_channel_db(chnl_id = chnlid, rem_chnl_id = context.args[0])
		update.effective_message.reply_text("Channel removed successfully")
	else:
		update.effective_message.reply_text("Not enough parameters"
		                                    "\nExample: /remove chnlid")
