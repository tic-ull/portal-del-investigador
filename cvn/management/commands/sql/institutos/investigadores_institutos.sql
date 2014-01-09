/*----------------------------------------------------------------------------------------------
-- Investigadores por instituto a FECHA ACTUAL
----------------------------------------------------------------------------------------------*/
SELECT * FROM
(

SELECT UCASE(ins.nombre) AS "Instituto", 
		count(distinct(mem12_GrupoInvest_investigador.id)) AS "Investigadores en grupos de investigación a fecha actual"
	FROM mem12_GrupoInvest_instituto as ins
		 INNER JOIN mem12_GrupoInvest_investigador
			ON ins.id = mem12_GrupoInvest_investigador.instituto_id
		WHERE ins.mostrar != 0
		GROUP BY ins.nombre
				
UNION ALL

SELECT UCASE(ins1.nombre) AS "Instituto", 0
FROM mem12_GrupoInvest_instituto AS ins1
WHERE 
(SELECT	count(mem12_GrupoInvest_investigador.id)
 FROM mem12_GrupoInvest_instituto as ins2
	   INNER JOIN mem12_GrupoInvest_investigador
			ON ins2.id = mem12_GrupoInvest_investigador.instituto_id
 WHERE ins2.id = ins1.id 
 GROUP BY ins2.nombre) IS NULL
 AND ins1.mostrar != 0
) DerivedTable

ORDER BY Instituto asc

/*INTO OUTFILE "/tmp/investigadores_institutos_2012.csv" FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';*/
