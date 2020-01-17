import cx_Oracle
import time


def conecta():
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
            a.object_id = c.object_id
            group by  b.inst_id,session_id ,b.osuser , terminal ,
            machine, program,os_user_name ,blocking_session,module
            order by inst_id,session_id"""    )
    result=cursor.fetchall()
    return result




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




