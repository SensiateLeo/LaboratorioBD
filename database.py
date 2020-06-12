def autenticar(cursor,login,senha):
    cursor.execute("select * from credencial where login = " + "'" + login + "'" + " and senha = " + "'" + senha + "'")
    row = cursor.fetchone()
    return row

def verifica_Tipo(cursor,login):
    cursor.execute("select departamento from funcionario where login = " + "'" + login + "'")
    row = cursor.fetchone()
    return row[0]

#============RELATÓRIOS================================

def relatorio_historicoPessoal(cursor, nome):
    if(nome == ''):
        cursor.execute("select * from Relatorio_1 limit 20")
        row = cursor.fetchall()
    else:
        cursor.execute("select * from Relatorio_1 where nome = '"+nome+"'")
        row = cursor.fetchall()
    return row

def relatorio_historicoHospitais(cursor, nome):
    if (nome == ''):
        cursor.execute("select * from Relatorio_2 limit 20")
        row = cursor.fetchall()
    else:
        cursor.execute("select * from Relatorio_2 where nome = '" + nome + "'")
        row = cursor.fetchall()
    return row

def relatorio_historicoAtendimentos(cursor, nome):
    if (nome == ''):
        cursor.execute("select * from Relatorio_3 limit 20")
        row = cursor.fetchall()
    else:
        cursor.execute("select * from Relatorio_3 where cidade = '" + nome + "'")
        row = cursor.fetchall()
    return row

def relatorio_historicoAmostras(cursor, valor):
    if (valor == ''):
        cursor.execute("select * from Relatorio_4 limit 20")
        row = cursor.fetchall()
    else:
        cursor.execute("select * from Relatorio_4 where data = '" + valor + "'")
        row = cursor.fetchall()
    return row

def relatorio_historicoLaboratorios(cursor, nome):
    if (nome == ''):
        cursor.execute("select * from Relatorio_5 limit 20")
        row = cursor.fetchall()
    else:
        cursor.execute("select * from Relatorio_5 where nome = '" + nome + "'")
        row = cursor.fetchall()
    return row

def relatorio_historicoPesquisadores(cursor, nome):
    if (nome == ''):
        cursor.execute("select * from Relatorio_6 limit 20")
        row = cursor.fetchall()
    else:
        cursor.execute("select * from Relatorio_6 where nome = '" + nome + "'")
        row = cursor.fetchall()
    return row

#============OVERVIEW================================

def overview_casosPositivos(cursor):
    cursor.execute("select * from casosPositivos")
    row = cursor.fetchone()
    return row[0]

def overview_casosSuspeitos(cursor):
    cursor.execute("select * from casosSuspeitos")
    row = cursor.fetchone()
    return row[0]

def overview_HopistalPopuloso(cursor):
    cursor.execute("select * from hospital_populoso")
    row = cursor.fetchall()
    return row

def overview_LabMaisAnalisados(cursor):
    cursor.execute("select * from LabMaisAnalisados")
    row = cursor.fetchall()
    return row

def overview_CidadesMaisPositivos(cursor):
    cursor.execute("select * from cidadeMaisPositivos")
    row = cursor.fetchall()
    return row

def overview_CidadesMaisSuspeitos(cursor):
    cursor.execute("select * from CidadeMaisSuspeitos")
    row = cursor.fetchall()
    return row

#============SIMULAÇÕES================================
def getMaxIDAmostra(cursor):
    cursor.execute("select max(id_amostra) from amostraCC")
    row = cursor.fetchone()
    return row[0]+1

def insertAmostra(cursor,date,resultado,idLaboratorio,idPaciente,idPesquisador):
    table = 'amostraCC'
    pesquisa = "INSERT INTO " + table + " VALUES (" + str(getMaxIDAmostra(cursor)) + ",'" + date + "','" + resultado + "'," + str(idLaboratorio) + ',' + str(idPaciente) + ',' + str(idPesquisador) + ')'
    print(pesquisa)
    cursor.execute(pesquisa)

def resetAmostra(cursor):
    cursor.execute('DROP TABLE IF EXISTS amostraCC')
    cursor.execute('CREATE TABLE IF NOT EXISTS amostraCC as select * from amostra')

def showAmostra(cursor):
    cursor.execute('SELECT * FROM amostraCC order by id_amostra DESC')
    row = cursor.fetchmany(20)
    return row

def updateAmostra(cursor,id_amostra,data,resultado):
    update = 'UPDATE amostraCC '
    update+= '''SET data = ''' + "'"+ str(data) + "'"
    update+= ''',resultado = ''' + "'" + str(resultado) + "'"
    update+= ''' WHERE id_amostra = ''' + str(id_amostra)
    print(update)
    cursor.execute(update)

def getAmostra(cursor,id_amostra):
    pesquisa = 'select * from amostraCC where id_amostra = ' + str(id_amostra)
    print(pesquisa)
    cursor.execute(pesquisa)
    row = cursor.fetchone()
    return row

def getMaxIDAtendimento(cursor):
    cursor.execute("select max(id_atendimento) from atendimentoCC")
    row = cursor.fetchone()
    return row[0]+1

def insertAtendimento(cursor,date,grau_avalicao,observacoes,idMedico,idPaciente,idProntuario):
    table = 'atendimentoCC'
    pesquisa = "INSERT INTO " + table + " VALUES (" + str(getMaxIDAtendimento(cursor)) + ",'" + date + "','" + grau_avalicao + "','" +observacoes +"',"+ str(idMedico) + ',' + str(idPaciente) + ',' + str(idProntuario) + ')'
    print(pesquisa)
    cursor.execute(pesquisa)

def resetAtendimento(cursor):
    cursor.execute('DROP TABLE IF EXISTS atendimentoCC')
    cursor.execute('CREATE TABLE IF NOT EXISTS atendimentoCC as select * from atendimento')

def showAtendimento(cursor):
    cursor.execute('SELECT * FROM atendimentoCC order by id_atendimento DESC')
    row = cursor.fetchmany(20)
    return row

def updateAtendimento(cursor,id_atendimento,data,grau_avaliacao,observacoes):
    update = 'UPDATE atendimentoCC '
    update+= '''SET data = ''' + "'"+ str(data) + "'"
    update+= ''',grau_avaliacao = ''' + "'" + str(grau_avaliacao) + "'"
    update += ''',observacoes = ''' + "'" + str(observacoes) + "'"
    update+= ''' WHERE id_atendimento = ''' + str(id_atendimento)
    print(update)
    cursor.execute(update)

def getAtendimento(cursor,id_atendimento):
    pesquisa = 'select * from atendimentoCC where id_atendimento = ' + str(id_atendimento)
    print(pesquisa)
    cursor.execute(pesquisa)
    row = cursor.fetchone()
    return row

def getMaxIDProntuario(cursor):
    cursor.execute("select max(id_prontuario) from prontuarioCC")
    row = cursor.fetchone()
    return row[0]+1

def insertProntuario(cursor,id_paciente):
    table = 'prontuarioCC'
    pesquisa = "INSERT INTO " + table + " VALUES (" + str(getMaxIDProntuario(cursor)) + "," + str(id_paciente) + ')'
    print(pesquisa)
    cursor.execute(pesquisa)

def resetProntuario(cursor):
    cursor.execute('DROP TABLE IF EXISTS prontuarioCC')
    cursor.execute('CREATE TABLE IF NOT EXISTS prontuarioCC as select * from prontuario')

def showProntuario(cursor):
    cursor.execute('SELECT * FROM prontuarioCC order by id_prontuario DESC')
    row = cursor.fetchmany(20)
    return row

def updateProntuario(cursor,id_prontuario,id_paciente):
    update = 'UPDATE prontuarioCC '
    update+= '''SET id_paciente = ''' + "'"+ str(id_paciente) + "'"
    update+= ''' WHERE id_prontuario = ''' + str(id_prontuario)
    print(update)
    cursor.execute(update)

def getProntuario(cursor,id_prontuario):
    pesquisa = 'select * from prontuarioCC where id_prontuario = ' + str(id_prontuario)
    print(pesquisa)
    cursor.execute(pesquisa)
    row = cursor.fetchone()
    return row