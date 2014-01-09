/* Asistencia a congresos de investigadores por institutos */

SELECT * FROM
(

SELECT UCASE(mem12_GrupoInvest_instituto.nombre) AS "Instituto", 
		count(mem12_cvn_congreso_usuario.id) AS "Asistencia a congresos de investigadores en 2012"
	FROM mem12_cvn_congreso
		 INNER JOIN mem12_cvn_congreso_usuario
			ON mem12_cvn_congreso.id = mem12_cvn_congreso_usuario.congreso_id
		 INNER JOIN mem12_cvn_usuario
			ON mem12_cvn_congreso_usuario.usuario_id = mem12_cvn_usuario.id
	     INNER JOIN mem12_GrupoInvest_investigador 
			ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
		 INNER JOIN mem12_GrupoInvest_instituto
			ON mem12_GrupoInvest_instituto.id = mem12_GrupoInvest_investigador.instituto_id
		WHERE (YEAR(fecha_realizacion)=2012 OR YEAR(fecha_finalizacion)=2012) AND
		              mem12_GrupoInvest_instituto.mostrar != 0

		GROUP BY mem12_GrupoInvest_instituto.nombre

UNION ALL

SELECT UCASE(ins1.nombre) AS "Instituto", 0
FROM mem12_GrupoInvest_instituto AS ins1
WHERE 
(SELECT  count(ins2.nombre)
FROM mem12_cvn_congreso
		 INNER JOIN mem12_cvn_congreso_usuario
			ON mem12_cvn_congreso.id = mem12_cvn_congreso_usuario.congreso_id
		 INNER JOIN mem12_cvn_usuario
			ON mem12_cvn_congreso_usuario.usuario_id = mem12_cvn_usuario.id
	     INNER JOIN mem12_GrupoInvest_investigador 
			ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
		 INNER JOIN mem12_GrupoInvest_instituto as ins2
			ON ins2.id = mem12_GrupoInvest_investigador.instituto_id
		 WHERE (YEAR(fecha_realizacion)=2012 OR YEAR(fecha_finalizacion)=2012) AND
			   ins2.id = ins1.id
		 GROUP BY ins2.nombre) IS NULL
AND ins1.mostrar != 0
) DerivedTable

ORDER BY Instituto asc
/*INTO OUTFILE "/tmp/congresos_institutos_2012.csv" FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';*/

