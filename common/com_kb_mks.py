from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from const.con_my_emojis import e_no, e_yes, e_headphones, e_confused, e_email, e_bank, e_arrow_forward, e_hourglass, e_new, \
	e_gem, e_wrench, e_info, e_plus

kbmenu = [[KeyboardButton('Menu')]]
kbmenu_markup = ReplyKeyboardMarkup(kbmenu, resize_keyboard=True, one_time_keyboard=True)

finishmenu = [[KeyboardButton('Finish')]]
finishmenu_markup = ReplyKeyboardMarkup(finishmenu, resize_keyboard=True)

cancel_button = [[KeyboardButton('/cancel')]]
cancel_markup = ReplyKeyboardMarkup(cancel_button, resize_keyboard=True)

reset_button = [[KeyboardButton('Reset All')]]
reset_markup = ReplyKeyboardMarkup(reset_button, resize_keyboard=True, one_time_keyboard=True)

confirmmenu = [[KeyboardButton(f'{e_yes}Yes')],
               [KeyboardButton(f'{e_no}No')]]
confirmmenu_markup = ReplyKeyboardMarkup(confirmmenu, resize_keyboard=True, one_time_keyboard=True)

contact_us = [[InlineKeyboardButton(f'{e_headphones}Contact Us', url ='https://t.me/PromoAssistant_Support')]]
contact_us_markup = InlineKeyboardMarkup(contact_us, resize_keyboard=True)

yes_no_ban = [[InlineKeyboardButton(f'{e_yes}Yes', callback_data = 'bannedlist_1'),
               InlineKeyboardButton(f'{e_no}No', callback_data = 'bannedlist_0')]]
yes_no_ban_mk = InlineKeyboardMarkup(yes_no_ban)

kbmenu_default = [[KeyboardButton(f'Register for PromoGroup Admins')]]
''', KeyboardButton('Statistics')],
[KeyboardButton(f'{e_confused}How to')]]'''
kbmenu_default_markup = ReplyKeyboardMarkup(kbmenu_default, resize_keyboard=True, one_time_keyboard=True)

kb_admins = [[KeyboardButton('Open Registrations')],
             [KeyboardButton('Create list'), KeyboardButton('Delete list')]]
kb_admins_markup = ReplyKeyboardMarkup(kb_admins, resize_keyboard = True, one_time_keyboard = True)

'''page_2 = [[KeyboardButton(f'{e_wrench}Settings'), KeyboardButton('Bot Stats')],
          [KeyboardButton(f'{e_info}Request a feature')], [KeyboardButton(f'{e_confused}Help'), KeyboardButton('Menu')]]
page_2_markup = ReplyKeyboardMarkup(page_2, resize_keyboard = True, one_time_keyboard = True)'''

settings_menu = [[KeyboardButton('Edit Header and Footer')],
								 [KeyboardButton(f'{e_plus}Add Group')],
                 [KeyboardButton(f'{e_gem}Add Premium Channels')],
								 cancel_button[0]]
settings_menu_markup = ReplyKeyboardMarkup(settings_menu, resize_keyboard=True, one_time_keyboard=True)

confirm_mk = InlineKeyboardMarkup([[InlineKeyboardButton('Confirm', callback_data = 'c1'),
                                    InlineKeyboardButton('Cancel', callback_data = 'c0')]])

