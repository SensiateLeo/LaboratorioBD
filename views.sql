--Function MD5 Generator
CREATE OR REPLACE FUNCTION password_hash (senha VARCHAR) RETURNS VARCHAR AS $$

DECLARE

	hash VARCHAR;

BEGIN
	hash = MD5(senha);
	RAISE INFO 'Original: {%}, MD5: {%}',senha,hash;
	return hash;
END; $$

LANGUAGE 'plpgsql';

--Alteração da coluna senha/Tabela Credencial
ALTER TABLE credencial ALTER COLUMN senha TYPE varchar(100);
--Iteração/Update Tabela Credencial
DO $$
DECLARE
   rec_cred  RECORD;
   cursor_cred  CURSOR FOR SELECT * FROM credencial;
BEGIN

	OPEN cursor_cred;

	LOOP

      FETCH cursor_cred INTO rec_cred;
      EXIT WHEN NOT FOUND;

		UPDATE credencial
		SET senha = password_hash(rec_cred.senha)
		WHERE CURRENT OF cursor_cred;

	END LOOP;
	CLOSE cursor_cred;
END $$;

INSERT INTO credencial VALUES
    ('adminCovid','superAdmin');

INSERT INTO funcionario VALUES
    (11111, 11111, '2020-06-08', 'Admin', 'adminCovid');

    CREATE OR REPLACE VIEW informacoes_gerais_covid AS
    select
    	P.id_pessoa as paciente,
    	P.nome as nome_pessoa,
    	P.idade,
    	P.sexo,
    	P.data_nasc,
    	P.cidade as Cidade,
    	P.cidade || '-' || P.estado || '-' || P.pais AS endereco_pessoa,
    	P.telefone_fixo || '-' || P.telefone_celular as Contato,
    	Atend.id_atendimento,
    	Atend.data as data_atendimento,
    	Atend.grau_avaliacao,
    	P.id_hospital,
    	H.nome as Hospital,
    	H.cidade || '-' || H.estado || '-' || H.pais AS endereco_hospital,
    	H.pais as pais_hospital,
    	H.qtd_funcionario,
    	H.qtd_leitos,
    	Atend.id_medico as medico_atendimento,
    	Med.crm,
    	Pront.id_prontuario,
    	A.resultado_positivo as amostras_positivas,
    	A.resultado_negativo as amostras_negativas
    	from pessoa P
    JOIN paciente Pac
    ON p.id_pessoa = Pac.id_paciente
    JOIN atendimento Atend
    ON Pac.id_paciente = Atend.id_paciente
    JOIN hospital H
    ON Pac.id_hospital = H.id_hospital
    JOIN medico Med
    ON Atend.id_medico = Med.id_medico
    JOIN prontuario Pront
    ON Pac.id_paciente=Pront.id_paciente
    JOIN (select id_paciente, sum(case when resultado = 'P' then 1 else 0 end) as resultado_positivo,sum(case when resultado = 'N' then 1 else 0 end) as resultado_negativo from amostra
    group by id_paciente) as A
    ON A.id_paciente = Pac.id_paciente
    order by P.id_pessoa;

CREATE OR REPLACE VIEW casosPositivos as
select count(A.id_paciente) as casos_positivos from
(select id_paciente from amostra where resultado = 'P'
group by id_paciente) as A;


CREATE OR REPLACE VIEW casosSuspeitos as
select count(A.id_paciente) from
(select id_paciente from amostra
group by id_paciente) as A;

CREATE OR REPLACE VIEW hospital_populoso as
select H.nome,C.quantidade_atendimentos
from
(select B.id_hospital, count(B.id_hospital) as quantidade_atendimentos from
(select A.id_paciente,
	P.id_hospital from
(select * from atendimento
where extract(month from data) = extract(month from (select current_date))-2) as A
JOIN paciente P
ON A.id_paciente = P.id_paciente) as B
group by id_hospital) as C
JOIN hospital H
ON C.id_hospital = H.id_hospital
order by quantidade_atendimentos DESC
limit 20;


CREATE OR REPLACE VIEW LabMaisAnalisados as
select L.nome,A.total_analises
from
(select id_laboratorio, count(id_laboratorio) as total_analises from amostra
where extract(month from data) = extract(month from (select current_date))-2
group by id_laboratorio
order by total_analises DESC) as A
JOIN laboratorio L
ON A.id_laboratorio = L.id_laboratorio
order by A.total_analises DESC
limit 20;

CREATE OR REPLACE VIEW cidadeMaisPositivos as
select A.cidade as Cidade,
sum(A.amostras_positivas) as Qtd_Casos_Positivos_COVID from
(select paciente,amostras_positivas,endereco_pessoa,cidade from informacoes_gerais_covid
 	where extract(month from data_atendimento) = extract(month from (select current_date))-2
 	group by paciente,amostras_positivas,cidade,endereco_pessoa) as A
group by cidade
order by Qtd_Casos_Positivos_COVID DESC
limit 20;

CREATE OR REPLACE VIEW CidadeMaisSuspeitos as
SELECT  PE.cidade as Cidade, count(A.id_amostra) as quantidade_suspeitos
	FROM PESQUISADOR Pes
	JOIN AMOSTRA A ON A.id_pesquisador = Pes.id_pesquisador
	JOIN PACIENTE PA ON PA.id_paciente = A.id_paciente
	JOIN PESSOA PE ON PE.id_pessoa = PA.id_paciente
WHERE extract(month from A.data) = extract(month from (select current_date))-2 and
	 (Cidade) != ''
GROUP BY PE.cidade ORDER BY quantidade_suspeitos DESC
LIMIT 20;

CREATE OR REPLACE VIEW Relatorio_1 as
    select
	P.nome,
	P.idade,
	P.sexo,
	P.data_nasc,
	concat(P.telefone_fixo,P.telefone_celular) as contato_telefonico,
	concat(P.cidade,concat(P.estado,P.pais)) as endereco,
	H.nome as Hospital
    from (select distinct(id_paciente) from amostra where resultado  = 'P') as A
	JOIN pessoa P
	ON A.id_paciente = P.id_pessoa
	JOIN hospital H
	ON P.id_hospital = H.id_hospital;

CREATE OR REPLACE VIEW Relatorio_2 as
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
    ON Z.id_hospital = H.id_hospital;

CREATE OR REPLACE VIEW Relatorio_3 as
select
H.cidade,
count(A.id_atendimento) as Qtd_Atendimentos,
count(distinct(A.paciente))Qtd_Pacientes_Distintos
from informacoes_gerais_COVID as A
JOIN hospital as H
ON A.id_hospital = H.id_hospital
group by H.cidade;

CREATE OR REPLACE VIEW Relatorio_3_Jan as
select
H.cidade,
count(A.id_atendimento) as Qtd_Atendimentos,
count(distinct(A.paciente))Qtd_Pacientes_Distintos
from informacoes_gerais_COVID as A
JOIN hospital as H
ON A.id_hospital = H.id_hospital
where extract (month from A.data_atendimento) = 01
group by H.cidade;

CREATE OR REPLACE VIEW Relatorio_3_Fev as
select
H.cidade,
count(A.id_atendimento) as Qtd_Atendimentos,
count(distinct(A.paciente))Qtd_Pacientes_Distintos
from informacoes_gerais_COVID as A
JOIN hospital as H
ON A.id_hospital = H.id_hospital
where extract (month from A.data_atendimento) = 02
group by H.cidade;

CREATE OR REPLACE VIEW Relatorio_3_Mar as
select
H.cidade,
count(A.id_atendimento) as Qtd_Atendimentos,
count(distinct(A.paciente))Qtd_Pacientes_Distintos
from informacoes_gerais_COVID as A
JOIN hospital as H
ON A.id_hospital = H.id_hospital
where extract (month from A.data_atendimento) = 03
group by H.cidade;

CREATE OR REPLACE VIEW Relatorio_3_Abr as
select
H.cidade,
count(A.id_atendimento) as Qtd_Atendimentos,
count(distinct(A.paciente))Qtd_Pacientes_Distintos
from informacoes_gerais_COVID as A
JOIN hospital as H
ON A.id_hospital = H.id_hospital
where extract (month from A.data_atendimento) = 04
group by H.cidade;


CREATE OR REPLACE VIEW Relatorio_Atendimentos_Completo as
select Rel.cidade,
		Rel.qtd_atendimentos,
		COALESCE(Jan.qtd_atendimentos,0) as Atendimentos_Janeiro,
		COALESCE(Fev.qtd_atendimentos,0) as Atendimentos_Fevereiro,
		COALESCE(Mar.qtd_atendimentos,0) as Atendimentos_Marco,
		COALESCE(Abr.qtd_atendimentos,0) as Atendimentos_Abril,
		Rel.qtd_pacientes_distintos
from Relatorio_3 as Rel
	LEFT JOIN Relatorio_3_Jan Jan
	on Rel.cidade = Jan.cidade
	LEFT JOIN Relatorio_3_Fev Fev
	on Rel.cidade = Fev.cidade
	LEFT JOIN Relatorio_3_Mar Mar
	on Rel.cidade = Mar.cidade
	LEFT JOIN Relatorio_3_Abr Abr
	on Rel.cidade = Abr.cidade;

CREATE OR REPLACE VIEW Relatorio_4 as
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
    ORDER BY A.data DESC;

CREATE OR REPLACE VIEW Relatorio_5 as
select
	L.nome,
	L.qtd_pesquisadores,
	concat(L.cidade,concat(L.estado,L.pais)) as endereco,
	A.qtd as qtd_amostras
	from (select id_laboratorio,count(id_amostra) as qtd from amostra group by id_laboratorio) as A
	JOIN laboratorio as L
	ON L.id_laboratorio = A.id_laboratorio;

CREATE OR REPLACE VIEW Relatorio_6 as
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
    ON pesquisador.id_pesquisador = amostra.id_pesquisador;
