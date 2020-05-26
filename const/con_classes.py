from telegram import Bot
from telegram.error import TimedOut, BadRequest
from telegram.ext import BaseFilter, messagequeue as mq

from common.com_bot_data import get_admins_list


class MQBot(Bot):
	def __init__(self, is_queued_def = True, mqueue = None, *args, **kwargs):
		super(MQBot, self).__init__(*args, **kwargs)
		self._is_messages_queued_default = is_queued_def
		self._msg_queue = mqueue or mq.MessageQueue()
	
	def __del__(self):
		try:
			self._msg_queue.stop()
		except:
			pass
	
	# super(MQBot, self).__del__()
	
	@mq.queuedmessage
	def send_message(self, *args, **kwargs):
		try:
			return super(MQBot, self).send_message(*args, **kwargs)
		except TimedOut:
			return self.send_message(*args, **kwargs)
		except BadRequest:
			pass


class ValidationError(Exception):
	def __init__(self, message):
		super().__init__(message)


class STATUS:
	NEW = 'NEW'
	REGISTRATION_OPEN = 'REGISTRATION_OPEN'
	LIST_PUBLISHED = 'LIST_PUBLISHED'
	LIST_DELETED = 'LIST_DELETED'
	
# FIXME use decs instead, context can't be send in filter
'''class FilterAdmins(BaseFilter):
	def filter(self, message):
		try:
			return message.from_user.id in get_admins_list(context = context)
		except:
			return False


filter_admins = FilterAdmins()


class FFilterAdmins(BaseFilter):
	def filter(self, message):
		try:
			return message.from_user.id in f_admins_list
		except:
			return False


f_filter_admins = FFilterAdmins()


class FilterGroups(BaseFilter):
	def filter(self, message):
		return message.chat.id in groups_list


filter_groups = FilterGroups()


class FFilterGroups(BaseFilter):
	def filter(self, message):
		return message.chat.id in f_groups_list


f_filter_groups = FFilterGroups()'''