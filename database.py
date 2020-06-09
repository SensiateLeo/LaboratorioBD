def autenticar(cursor,login,senha):
    cursor.execute("select * from credencial where login = " + "'" + login + "'" + " and senha = " + "'" + senha + "'")
    row = cursor.fetchone()
    return row

def verifica_Tipo(cursor,login):
    cursor.execute("select departamento from funcionario where login = " + "'" + login + "'")
    row = cursor.fetchone()
    return row[0]

#============RELATÓRIOS================================

def relatorio_historicoPessoal(cursor):
    cursor.execute("select * from Relatorio_1 limit 20")
    row = cursor.fetchall()
    return row

def relatorio_historicoHospitais(cursor):
    cursor.execute("select * from Relatorio_2 limit 20")
    row = cursor.fetchall()
    return row

def relatorio_historicoAtendimentos(cursor):
    cursor.execute("select * from Relatorio_3 limit 20")
    row = cursor.fetchall()
    return row

def relatorio_historicoAmostras(cursor):
    cursor.execute("select * from Relatorio_4 limit 20")
    row = cursor.fetchall()
    return row

def relatorio_historicoLaboratorios(cursor):
    cursor.execute("select * from Relatorio_5 limit 20")
    row = cursor.fetchall()
    return row

def relatorio_historicoPesquisadores(cursor):
    cursor.execute("select * from Relatorio_6 limit 20")
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

'''

postgreSQL_select_historico_pessoal = """
    select
	P.nome,
	P.idade,
	P.sexo,
	P.data_nasc,
	concat(P.telefone_fixo,P.telefone_celular) as contato_telefonico,
	concat(P.cidade,concat(P.estado,P.pais)) as endereco,
	P.id_hospital,
	H.nome as Hospital
	from (select distinct(id_paciente) from amostra where resultado  = 'P') as A
	JOIN pessoa P
	ON A.id_paciente = P.id_pessoa
	JOIN hospital H
	ON P.id_hospital = H.id_hospital
    """

    postgreSQL_select_historico_hospitais = """
    select
	H.nome,
	concat(H.cidade,concat(H.estado,H.pais)),
	H.qtd_funcionario,
	H.qtd_leitos,
	Z.qtd_atendimentos,
	Z.qtd_pacientes
    from hospital H
    JOIN (select X.id_hospital,sum(X.qtd_atendimento) as qtd_atendimentos,count(X.id_paciente) as qtd_pacientes from 
    (select P.id_hospital,A.qtd_atendimento,A.id_paciente
    from (select count(id_atendimento) as qtd_atendimento,id_paciente from atendimento group by id_paciente) as A
    JOIN paciente as P
    ON P.id_paciente=A.id_paciente) as X group by X.id_hospital) as Z
    ON Z.id_hospital = H.id_hospital
    """

    postgreSQL_select_historico_amostra = """
    select 
	P.nome,
	P.idade,
	P.sexo,
	concat(P.cidade,concat(P.estado,P.pais)) as endereco,
	A.data,
	A.resultado,
	A.id_laboratorio
    from amostra A
    JOIN pessoa P
    ON P.id_pessoa = A.id_paciente
    ORDER BY A.data DESC
    """

    postgreSQL_select_historico_laboratorios="""
    select
	L.nome,
	L.qtd_pesquisadores,
	concat(L.cidade,concat(L.estado,L.pais)) as endereco,
	A.qtd as qtd_amostras
	from (select id_laboratorio,count(id_amostra) as qtd from amostra group by id_laboratorio) as A
	JOIN laboratorio as L
	ON L.id_laboratorio = A.id_laboratorio
    """

    postgreSQL_select_historico_pesquisadores = """
    select 
	pessoa.nome,
	funcionario.registro_institucional,
	funcionario.data_contratacao,
	amostra.id_amostra,
	amostra.data,
	amostra.resultado
	from pesquisador
    JOIN pessoa
    ON pesquisador.id_pesquisador = pessoa.id_pessoa
    JOIN funcionario
    ON funcionario.id_funcionario = pesquisador.id_pesquisador
    JOIN amostra
    ON pesquisador.id_pesquisador = amostra.id_pesquisador
    """

'''
