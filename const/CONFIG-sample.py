# Rename this file to CONFIG.py

DESCR_LIMIT = 35
SUPPORT_USERNAME = ''  # # Ex: PromoAssistant_Support (without adding '@')
MIN_CHNLS_PER_LIST = 20

PROMO_BOT_TKN = ''

# if you're gonna use webhooks
PORT_NUM = 1234
SERVER_IP_ADDR = ''
NAME_OF_PEM_FILE = 'self-signed.pem'
WEBHOOK_URL = f'https://{SERVER_IP_ADDR}:443/{PROMO_BOT_TKN.split(":")[-1]}'
# ====================================================================================

LOG_BOT_TKN = ''
LOG_CHNL = ''
