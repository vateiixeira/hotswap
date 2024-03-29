from django.utils import timezone
from my_project.core.models import ConfiguracaoEmail, ConfiguracaoSocin, NotasSocin, Profile
from celery import shared_task
from my_project.atendimento.models import Atendimento
from my_project.chamado.models import Chamado
from .emails import send_mail, send_mail_notas_presas
from datetime import datetime, timedelta
from .dates import normalized


@shared_task
def envia_email_atendimento(atendimento_id):
    atendimento = Atendimento.object.filter(id=atendimento_id)
    config = ConfiguracaoEmail.get_solo()
    
    if not atendimento:
        return 
    if not config.send_novos_atendimentos:
        return

    atendimento = atendimento.last()

    subject =  f'[ATENDIMENTO] #{atendimento.id} - {atendimento.setor}'
    
    context = {
        'title': f'[ATENDIMENTO] #{atendimento.id} - {atendimento.setor}',
        'dados': {
            'Problema': atendimento.problema,
            'Setor' : atendimento.setor,
            'Solicitante' : atendimento.solicitante,
            'Loja' : atendimento.loja,
            'Responsável' : atendimento.responsavel or 'Não atribuido',
        }
    }
    if not atendimento.responsavel:
        to = list(Profile.objects.filter(filiais=atendimento.loja,cargo__in=[Profile.CARGO_TECNICO,Profile.CARGO_GERENCIA_TI]).values_list('user__email',flat=True))
        if not to:
            return
    else:
        to = [atendimento.responsavel.email]

    send_mail(subject,to,context)

@shared_task
def envia_email_chamado(chamado_id):
    chamado = Chamado.object.filter(id=chamado_id)
    config = ConfiguracaoEmail.get_solo()
    
    if not chamado:
        return 
    if not config.send_novos_chamados:
        return

    chamado = chamado.last()

    fornecedor = chamado.fornecedor or ''

    subject =  f'[CHAMADO] #{chamado.id} - {fornecedor}'
    
    context = {
        'title': f'[CHAMADO] #{chamado.id} - {fornecedor}',
        'dados': {
            'Número': chamado.chamado,
            'Modelo' : chamado.modelo,
            'Serial' : chamado.serial,
            'Criado por' : chamado.user,
            'Loja' : chamado.loja,
            'Quantidade': chamado.quantidade,
            'Defeito' : chamado.defeito,
            'Status': chamado.status,
        }
    }

    if chamado.justificativa:
        context['dados']['Justificativa'] = chamado.justificativa

    if chamado.valor:
        context['dados']['Valor'] = chamado.valor

    if chamado.fornecedor:
        context['dados']['Fornecedor'] = chamado.fornecedor

    to = list(Profile.objects.filter(filiais=chamado.loja,cargo__in=[Profile.CARGO_TECNICO,Profile.CARGO_GERENCIA_TI]).values_list('user__email',flat=True))
    if not to:
        return
        
    send_mail(subject,to,context)

@shared_task
def envia_email_notas_presas():
    
    config = ConfiguracaoEmail.get_solo()

    config_banco = ConfiguracaoSocin.get_solo()

    if '' in [config_banco.user,config_banco.password, config_banco.database,config_banco.host]:
        return
    
    if not config.send_notas_presas:
        return 

    if len(config.notas_presas) < 1:
        return

    import mysql.connector   

    try:
        cnx = mysql.connector.connect(user=config_banco.user, password=config_banco.password,
                                host=config_banco.host,
                                database=config_banco.database)
    except Exception as ex:
        print(ex)
        print('error')
        return

    cursor = cnx.cursor()
    script = "select count(*) from exp_imp_movimento where data_movimento= CURDATE() and situacao_movimento=1 and tipo_movimento=1;"
    cursor.execute(script) 
    for i in cursor:
        quantidade = i[0]
   
    #import random
    # quantidade = random.randint(490,510)
    # print(quantidade)
    # print(config.notas_presas)
    
    if quantidade >= config_banco.quantidade_para_ativar_envio:
        
        if not config_banco.ultimo_envio_email_massa:         
            config_banco.ultimo_envio_email_massa = timezone.now()
            config_banco.save()
            subject = f'{quantidade} notas presas SOCIN'            
            send_mail_notas_presas(subject,config.notas_presas,normalized(timezone.now()),quantidade)
        
        if config_banco.ultimo_envio_email_massa and config_banco.ultimo_envio_email_massa + timedelta(minutes=config_banco.intervalo_entre_envios) < timezone.now():
            config_banco.ultimo_envio_email_massa = timezone.now()
            config_banco.save()
            subject = f'{quantidade} notas presas SOCIN'            
            send_mail_notas_presas(subject,config.notas_presas,normalized(timezone.now()),quantidade)


@shared_task
def notas_socin():
    import mysql.connector
    from mysql.connector import Error
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    socin = ConfiguracaoSocin.get_solo()
    channel_layer = get_channel_layer()
    try:
        cnx = mysql.connector.connect(user=socin.user, password=socin.password,
                                host=socin.host,
                                database=socin.database,
                                connect_timeout=2)
        cursor = cnx.cursor()
        script = "select count(*) from exp_imp_movimento where data_movimento= CURDATE() and situacao_movimento=1 and tipo_movimento=1;"
        cursor.execute(script) 
        for i in cursor:
            data = i[0]
            NotasSocin.objects.create(
                valor = data
            )
            async_to_sync(channel_layer.group_send)(
                    'socin',
                    {'type': 'chat_message', 'message': data}
                )  
    except Exception as exc:
        async_to_sync(channel_layer.group_send)(
                    'socin',
                    {'type': 'chat_message', 'message': 'error'}
                )
        raise exc  

@shared_task
def exclui_notas_socin():
    from django.utils import timezone
    NotasSocin.objects.filter(data__date__lt=timezone.now()).delete()

@shared_task
def sessoes_travadas():
    from my_project.core.conexao_oracle import Sessoes,stats
    from my_project.core.models import ConfiguracaoSessoes,SessoesBlock
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    from django.utils import timezone
    from datetime import timedelta
    
    con = Sessoes()
    blocks = {}
    config = ConfiguracaoSessoes.get_solo()
    channel_layer = get_channel_layer()
    while True:
        config.refresh_from_db()
        data = con.run()
        if len(data['origem']) > 0:
            #print(data['bloqueados'])
            print(data['origem'])
            print(data['origem_data'])
            for lock in data['origem']:
                if blocks.get(lock,None):
                    if blocks.get(lock,None)[0] + timedelta(minutes=config.minutos) < timezone.now():
                        if blocks.get(lock,None) and blocks.get(lock,None)[1]:
                            SessoesBlock.objects.get_or_create(
                                session_id =blocks[lock][1][stats['session_id']],
                                usuario =blocks[lock][1][stats['usuario']],
                                terminal =blocks[lock][1][stats['terminal']],
                                maquina =blocks[lock][1][stats['maquina']],
                                programa =blocks[lock][1][stats['programa']],
                                os_username =blocks[lock][1][stats['os']],
                                #sessao_bloqueada =blocks[lock][1][stats['sessao_bloqueada']],
                                data= blocks.get(lock,None)[0],
                            )
                            # aqui precisa ir pro channel no redis para notificar front e telegram
                        else:
                            print('Nao achou data para gravar o lock.')                            
                else:
                    blocks[lock] = [timezone.now(),data['origem_data'].get(lock,None)]
            print(blocks)
            print('-'*50)
        else:
            blocks = {}
            # aqui precisa excluir channel para sair notificacao do front
        if data['origem_data']:
            msg = [
                {            
                'title': f"{data['origem_data'][x][3]} | {data['origem_data'][x][4]}",#"VILLEFORT\\ADM-CONTAB09",
                'description': f"{data['origem_data'][x][1]} - {data['origem_data'][x][5]}",#"ana.ferreira - ADM-CONTAB09",
                'done': False,
                } for x in data['origem_data']
            ]
        else:
            msg = []
        print('Executando')
        print(msg)
        qtd = len(data['bloqueados'])
        async_to_sync(channel_layer.group_send)(
                    'sessoes',
                    {'type': 'chat_message', 'message': msg, 'qtd': qtd}
                )