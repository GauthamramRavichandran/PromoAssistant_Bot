import logging
from telegram import BotCommand
from telegram.ext import Updater, messagequeue as mq
from telegram.utils.request import Request

from const.con_classes import MQBot
from const.CONFIG import PROMO_BOT_TKN, SERVER_IP_ADDR, PORT_NUM, NAME_OF_PEM_FILE, WEBHOOK_URL
from my_handlers import promo_group_regstr_hndlr, cancel_hndlr, chnl_admin_registr_hndlr, config_hndlr, crt_promo_hndlr, \
	dlt_promo_hndlr, settings_hndlr, shared_list_hndlr, strt_promo_hndlr, how_to_hndlr, stat_hndler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR, filename = 'logs.log')

logger = logging.getLogger(__name__)
handlers_to_add = [promo_group_regstr_hndlr, cancel_hndlr, chnl_admin_registr_hndlr, config_hndlr, crt_promo_hndlr, \
                   dlt_promo_hndlr, settings_hndlr, shared_list_hndlr, strt_promo_hndlr, how_to_hndlr, stat_hndler]


def main():
	
	q = mq.MessageQueue(all_burst_limit = 28, all_time_limit_ms = 3000)
	updater = Updater(bot = MQBot(token = PROMO_BOT_TKN, mqueue = q,
	                              request = Request(con_pool_size = 10)), use_context = True)
	
	# j = updater.job_queue >>>>
	dispatcher = updater.dispatcher
	for hndlr in handlers_to_add:
		dispatcher.add_handler(hndlr)
	# dispatcher.add_handler(InlineQueryHandler(inlinequery)) >>>>
	# dispatcher.add_error_handler(error_handle)
	
	# Exceptional Case #
	# dispatcher.add_handler(MessageHandler(Filters.text, exceptional))
	updater.bot.set_my_commands([BotCommand('start', 'start the bot'),
	                             BotCommand('getshared', '#shared of current promo'),
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