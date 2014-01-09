/*----------------------------------------------------------------------------------------------
-- Investigadores por departamento a FECHA ACTUAL
----------------------------------------------------------------------------------------------*/
SELECT * FROM
(

SELECT UCASE(dep.nombre) AS "Departamento", 
		count(distinct(mem12_GrupoInvest_investigador.id)) AS "Investigadores en grupos de investigación a fecha actual"
	FROM mem12_GrupoInvest_departamento as dep
		 INNER JOIN mem12_GrupoInvest_investigador
			ON dep.id = mem12_GrupoInvest_investigador.departamento_id
		WHERE dep.mostrar != 0
		GROUP BY dep.nombre
				
UNION ALL

SELECT UCASE(dep1.nombre) AS "Departamento", 0
FROM mem12_GrupoInvest_departamento AS dep1
WHERE 
(SELECT	count(mem12_GrupoInvest_investigador.id)
 FROM mem12_GrupoInvest_departamento as dep2
	   INNER JOIN mem12_GrupoInvest_investigador
			ON dep2.id = mem12_GrupoInvest_investigador.departamento_id
 WHERE dep2.id = dep1.id 
 GROUP BY dep2.nombre) IS NULL
 AND dep1.mostrar != 0
) DerivedTable

ORDER BY Departamento asc

/*INTO OUTFILE "/tmp/investigadores_departamentos_2012.csv" FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';*/
