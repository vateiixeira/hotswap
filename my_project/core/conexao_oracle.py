from datetime import timedelta
import cx_Oracle
import time
from django.utils import timezone
from my_project.core.models import ConfiguracaoSessoes,SessoesBlock


stats = {
        'session_id':1,
        'usuario':2,
        'terminal':3,
        'maquina':4,
        'programa':5,
        'os':6,
        'sessao_bloqueada':7,
    }

class Sessoes():

    cursor = None
    connection = None
    stats = {
        'session_id':1,
        'usuario':2,
        'terminal':3,
        'maquina':4,
        'programa':5,
        'os':6,
        'sessao_bloqueada':7,
    }

    def __init__(self) -> None:
        self.make()

    def make(self):
        uid="VILLE5"
        pwd="g00gl3"
        db="(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = villep-scan.villefort.lan)(PORT = 1521))(LOAD_BALANCE = YES)(CONNECT_DATA = (SERVER = DEDICATED)(SERVICE_NAME = CEMAPROD)(FAILOVER_MODE = (TYPE = SELECT)(METHOD = BASIC)(RETRIES = 180)(DELAY = 5))))"  # string de conexão do Oracle, configurado no


        self.connection=cx_Oracle.connect(uid + "/" + pwd + "@" + db)
    
    def run(self):
        cursor=self.connection.cursor()

        cursor.execute(
                """select  b.inst_id,session_id "SECAO",b.osuser "USUARIO", terminal "TERMINAL",
                machine"MAQUINA", program"PROGRAMA",os_user_name ,blocking_session"SECAO_BLOQUEADA",module

                from
                gv$locked_object a,
                gv$session b,
                dba_objects c 
                where b.sid = a.session_id and
                a.object_id = c.object_id            
                group by  b.inst_id,session_id ,b.osuser , terminal ,
                machine, program,os_user_name ,blocking_session,module
                order by inst_id,session_id""")
        # blocking_session is not null
        result = cursor.fetchall()
        cursor.close()
        # cursos = litsta
        bloqueados = []
        origem = []
        origem_data = {}
        for i in result:
            if i[self.stats['sessao_bloqueada']] != None:
                bloqueados.append(i)
                origem.append(i[self.stats['sessao_bloqueada']])
            if i[self.stats['session_id']] in origem and i[self.stats['session_id']] not in origem:
                origem_data[i[self.stats['session_id']]]= i                
            
        return {
            'bloqueados': bloqueados,
            'origem': origem,
            'origem_data': origem_data,
        }


def oracle_sessoes():
    con = Sessoes()
    blocks = {}
    config = ConfiguracaoSessoes.get_solo()
    while True:
        config.refresh_from_db()
        data = con.run()
        if len(data['origem']) > 0:
            #print(data['bloqueados'])
            print(data['origem'])
            for lock in data['origem']:
                if blocks.get(lock,None):
                    if blocks.get(lock,None) + timedelta(minutes=config.minutos) < timezone.now():
                        SessoesBlock.objects.create(
                            session_id =data['origem_data'][lock][stats['session_id']],
                            usuario =data['origem_data'][lock][stats['usuario']],
                            terminal =data['origem_data'][lock][stats['terminal']],
                            maquina =data['origem_data'][lock][stats['maquina']],
                            programa =data['origem_data'][lock][stats['programa']],
                            os_username =data['origem_data'][lock][stats['os']],
                            sessao_bloqueada =data['origem_data'][lock][stats['sessao_bloqueada']],
                            data= blocks.get(lock,None),
                        )
                        # aqui precisa ir pro channel no redis para notificar front e telegram
                else:
                    blocks[lock] = timezone.now()
            print(blocks)
            print('-'*50)
        else:
            blocks = {}
            # aqui precisa excluir channel para sair notificacao do front

        time.sleep(10)

def convert(mes):
    if mes == 1:
        return 'jan'
    elif mes == 2:
        return 'feb'
    elif mes == 3:
        return 'mar'
    elif mes == 4:
        return 'apr'
    elif mes == 5:
        return 'may'
    elif mes == 6:
        return 'jun'
    elif mes == 7:
        return 'jul'
    elif mes == 8:
        return 'aug'
    elif mes == 9:
        return 'sep'
    elif mes == 10:
        return 'oct'
    elif mes == 11:
        return 'nov'
    elif mes == 12:
        return 'dec'




