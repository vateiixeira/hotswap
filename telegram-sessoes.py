from datetime import timedelta
from django.utils import timezone
from telethon import TelegramClient, events, sync
from telethon.tl import types
from telethon.tl.functions.contacts import ResolveUsernameRequest
import os,sys

import django
from django.conf import settings
from decouple import config

# if config('SYSTEM_TYPE') == 'linux':
#      sys.path.append('/root/betlol-api')
# else:
#      sys.path.append("C:\dev\api-bet")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
django.setup()

# Now this script or any imported module can use any part of Django it needs.

import django
from telethon import utils

django.setup()

from my_project.core.models import NotasSocin,ConfiguracaoSocin,ConfiguracaoEmail
from django.utils import timezone
from datetime import timedelta
from decouple import config

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
token_http = config('TOKEN_BOT','')

api_id = config('API_ID')
api_hash = config('API_SECRET')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=token_http)
from time import sleep

#GRUPO = '-1274793802'

#client.log_out()
#client.run_until_disconnected()

# with client:
     # client.loop.run_until_complete(main())


import asyncio
import websockets

ws_url = "ws://192.168.1.222/ws/sessoes/"

async def command_receiver():
    real_id, peer_type = utils.resolve_id(-1274793802)
    async with websockets.connect(ws_url) as websocket:
        while True:
            message = await websocket.recv()
            client.send_message(types.PeerChannel(real_id),message)    


with client:
    client.loop.run_until_complete(command_receiver())