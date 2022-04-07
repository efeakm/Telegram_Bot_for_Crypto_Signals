
from get_signals import get_signals
from telethon import TelegramClient
import time

api_id = 'TELEGRAM-ID'
api_hash = 'TELEGRAM-HASH'
username = 'TELEGRAM-USERNAME'
channel_invite_link = 'TELEGRAM-CHANNEL-LINK'

SECONDS_FOR_EACH_PERIOD = 900 #Checks signals every 15 min

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")

async def send_mess(message):
    await client.start()
    entity = await client.get_entity(channel_invite_link)
    await client.send_message(entity=entity, message=message)

#START MESSAGE
with client:
            client.loop.run_until_complete(send_mess(message='THE BOT HAS CONNECTED'))

while 1==1:
    longs, shorts = get_signals()
    
    if len(longs) > 0:
        
        MESSAGE = 'LONG ⬆️:'
        for sym in longs:
            MESSAGE = MESSAGE + f'\n {sym}'
        print(MESSAGE)


        with client:
            client.loop.run_until_complete(send_mess(message=MESSAGE))
                
    if len(shorts) > 0:
        
        MESSAGE = 'SHORT 🔻:'
        for sym in shorts:
            MESSAGE = MESSAGE + f'\n {sym}'
        print(MESSAGE)
                 
        with client:
            client.loop.run_until_complete(send_mess(message=MESSAGE))

    time.sleep(SECONDS_FOR_EACH_PERIOD)
