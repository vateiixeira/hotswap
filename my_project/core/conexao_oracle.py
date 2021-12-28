import cx_Oracle
import time


def conecta():
    stats = {
        'session_id':1,
        'usuario':2,
        'terminal':3,
        'maquina':4,
        'programa':5,
        'os':6,
        'sessao_bloqueada':7,
    }
    uid="VILLE5"
    pwd="g00gl3"
    db="(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = villep-scan.villefort.lan)(PORT = 1521))(LOAD_BALANCE = YES)(CONNECT_DATA = (SERVER = DEDICATED)(SERVICE_NAME = CEMAPROD)(FAILOVER_MODE = (TYPE = SELECT)(METHOD = BASIC)(RETRIES = 180)(DELAY = 5))))"  # string de conexão do Oracle, configurado no


    connection=cx_Oracle.connect(uid + "/" + pwd + "@" + db)
    cursor=connection.cursor()

    cursor.execute(
            """select  b.inst_id,session_id "SECAO",b.osuser "USUARIO", terminal "TERMINAL",
            machine"MAQUINA", program"PROGRAMA",os_user_name ,blocking_session"SECAO_BLOQUEADA",module

            from
            gv$locked_object a,
            gv$session b,
            dba_objects c 
            where b.sid = a.session_id and
            a.object_id = c.object_id and
            
            group by  b.inst_id,session_id ,b.osuser , terminal ,
            machine, program,os_user_name ,blocking_session,module
            order by inst_id,session_id""")
    # blocking_session is not null
    result = cursor.fetchall()
    cursor.close()
    print(type(result))
    bloqueados = []
    origem = []
    origem_data = []
    for i in result:
        if i[stats['sessao_bloqueada']] != None:
            bloqueados.append(i)
            origem.append(i[stats['session_id']])
        if i[stats['session_id']] in origem:
            origem_data.append(i)
        
    return {
        'bloqueados': bloqueados,
        'origem': origem,
        'origem_data': origem_data,
    }


def oracle_sessoes():
    while True:
        time.sleep(10)
        data = conecta()
        if len(data['bloqueados']) > 0:
            print(data['bloqueados'])
            print(data['origem'])
            print(data['origem_data'])
            print('-'*50)

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




