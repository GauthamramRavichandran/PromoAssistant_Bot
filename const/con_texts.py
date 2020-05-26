from const.con_my_emojis import e_tada, e_arrow_forward, e_scroll, e_lost, e_envelope
from const.CONFIG import DESCR_LIMIT

new_pin_tx = f'''
		{e_tada}{e_tada}{e_tada}

	Registrations has started
  Rules,
    1. Channel should be public
    2. Description should be lesser than {DESCR_LIMIT}

  Register your channel using the below link,'''

new_button_pin_tx = f'''
		{e_tada}{e_tada}{e_tada}

	Registrations has started

{e_arrow_forward}Format:
	#new|@channelusername|Description in 3 words|Invitelink/publiclink

	If you've already registered a channel with us,
		 send #join|@channelusername'''

# || for link
pub_pin_tx = f"{e_scroll}List has been published in the notification channel\n\n\t\t||" \
          f"\n\nWe request channel admins to post the list asap if not posted by our bot\nAlso report #shared here if posted manually"


join_now_tx = f'{e_envelope}\n\tJoin our channel to know about latest happenings of this bot as well as others we have' \
                f"\n\nAlso, after joining, you won't get this annoying message{e_lost}"
