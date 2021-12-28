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

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
token_http = '5056457780:AAETIRlqs1vbg3BtzvAjFxkgI6xgzus3kAc'

api_id = 5276077
api_hash = '29e2e425fc4419b0bf57b029bdd325df'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=token_http)
from time import sleep

#GRUPO = '-1274793802'


with client:
    real_id, peer_type = utils.resolve_id(-1274793802)
    print('Iniciando bot')
    while True:
        notas = NotasSocin.objects.last()
        config = ConfiguracaoSocin.get_solo()
        configs_email = ConfiguracaoEmail.get_solo()
        configs_email.refresh_from_db()
        if configs_email.telegram_notas_presas:
            print('Habilitado,procurando notas...')
            config.refresh_from_db()
            if notas and notas.valor >= config.quantidade_para_ativar_envio and notas.data > timezone.now() + timedelta(minutes=2):
                print('Nota encontrada,enviando...')
                msg = f'*** ALERTA ***\n NOTAS PRESAS SOCIN \nQUANTIDADE: {notas.valor}'
                client.send_message(types.PeerChannel(real_id),msg)
                sleep(300)
                sleep(2)
            else:
                sleep(5)
        print('Não encontrou')


#client.log_out()
#client.run_until_disconnected()

# with client:
     # client.loop.run_until_complete(main())
