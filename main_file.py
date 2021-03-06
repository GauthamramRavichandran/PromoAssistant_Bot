from datetime import datetime
import logging
from telegram import BotCommand
from telegram.ext import Updater, messagequeue as mq, PicklePersistence
from telegram.utils.request import Request

from backend.db_list import del_expired_list
from common.com_bot_data import load_db_to_bot
from const.con_classes import MQBot
from const.CONFIG import PROMO_BOT_TKN, SERVER_IP_ADDR, PORT_NUM, NAME_OF_PEM_FILE, WEBHOOK_URL
from my_handlers import promo_group_regstr_hndlr, cancel_hndlr, chnl_admin_registr_hndlr, config_hndlr, crt_promo_hndlr, \
	dlt_promo_hndlr, settings_hndlr, shared_list_hndlr, strt_promo_hndlr, how_to_hndlr, stat_hndler, \
	inline_hndlr, unshared_list_hndlr, remove_chnl_hndlr

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR, filename = 'logs.log')

logger = logging.getLogger(__name__)
handlers_to_add = [promo_group_regstr_hndlr, settings_hndlr, dlt_promo_hndlr,
                   chnl_admin_registr_hndlr, config_hndlr, crt_promo_hndlr, shared_list_hndlr, strt_promo_hndlr,
                   how_to_hndlr, stat_hndler, inline_hndlr, unshared_list_hndlr, remove_chnl_hndlr, cancel_hndlr]


def main():
	my_persistence = PicklePersistence(filename = 'pickle_promo')
	q = mq.MessageQueue(all_burst_limit = 28, all_time_limit_ms = 3000)
	updater = Updater(bot = MQBot(token = PROMO_BOT_TKN, mqueue = q,
	                              request = Request(con_pool_size = 10)), use_context = True, persistence = my_persistence)
	
	j = updater.job_queue
	j.run_daily(time = datetime.time(datetime(12, 2, 1)), callback = del_expired_list, context = None)
	dispatcher = updater.dispatcher
	for hndlr in handlers_to_add:
		dispatcher.add_handler(hndlr)
	load_db_to_bot(context = dispatcher)
	
	# Exceptional Case #
	# dispatcher.add_handler(MessageHandler(Filters.text, exceptional))
	updater.bot.set_my_commands([BotCommand('start', 'start the bot'),
	                             BotCommand('remove', 'remove a channel'),
	                             BotCommand('shared', '#shared of current promo'),
	                             BotCommand('unshared', '#unshared of current promo'),
	                             BotCommand('configure', 'get the grpid'),
	                             BotCommand('cancel', 'stop current operation')])
	
	if SERVER_IP_ADDR:
		updater.start_webhook(listen = '127.0.0.1',
		                      port = PORT_NUM,
		                      url_path = PROMO_BOT_TKN.split(':')[-1],
		                      allowed_updates = ['message', 'callback_query'])
		updater.bot.set_webhook(url = WEBHOOK_URL,
		                        certificate = open(NAME_OF_PEM_FILE, 'rb'))
	else:
		updater.start_polling()
	
	updater.idle()


if __name__ == "__main__":
	main()