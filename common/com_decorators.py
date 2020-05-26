from functools import wraps
# FIXME
from common.com_bot_data import get_grps_list, get_admins_list
from common.com_kb_mks import contact_us_markup
from const.CONFIG import MY_ID
from const.con_classes import ValidationError


def nogroup(func):
	@wraps(func)
	def wrapped(update, context, *args, **kwargs):
		try:
			if update.message.chat.type == 'private':
				return func(update, context, *args, **kwargs)
			update.message.reply_text('This command/function only works in private')
			return
		except :
			return
	return wrapped


def onlyme(func):
	@wraps(func)
	def wrapped(update, context, *args, **kwargs):
		try:
			if update.effective_user.id in MY_ID:
				return func(update, context, *args, **kwargs)
			return
		except Exception as e:
			update.message.reply_text(str(e))
			return
	return wrapped


def testing(func):
	@wraps(func)
	def wrapped(update, context, *args, **kwargs):
		try:
			return func(update, context, *args, **kwargs)
		except ValidationError as v:
			update.message.reply_text(f'{v}')
			return
		except Exception as e:
			print(str(e))
			return
	return wrapped


def only_paid(func):
	@wraps(func)
	def wrapped(update, context, *args, **kwargs):
		try:
			chat_id = update.message.chat_id
			if chat_id in get_grps_list(context):
				return func(update, context, *args, **kwargs)
			if update.message.chat.type == 'private' and (chat_id in get_admins_list(context) or chat_id in MY_ID):
				return func(update, context, *args, **kwargs)
			else:
				context.bot.send_message(text = "This function is available only for paid version 💰",
				                 chat_id = update.message.chat_id, reply_markup = contact_us_markup)
				return
		except Exception as e:
			print(f'Only paid - > {e}')
			return
	return wrapped
