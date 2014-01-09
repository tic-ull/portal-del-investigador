/*
-- convenios por institutos
-- TODO
-- Revisar criterios de fechas
-- Actualmente: Con fecha de inicio en 2012
-- Ver si hay que hacer la vigencia hasta o cubriendo 2012

-- OJO ACTUALMENTE LA BBDD no tiene apenas información. La consulta solo devuelve 2 filas
*/

SELECT * FROM
(
	SELECT UCASE(mem12_GrupoInvest_instituto.nombre) AS "Instituto", 
			count(mem12_cvn_convenio_usuario.id) AS "Convenios vigentes o con fecha de inicio en 2012"
	FROM mem12_cvn_convenio
		 INNER JOIN mem12_cvn_convenio_usuario
			ON mem12_cvn_convenio.id = mem12_cvn_convenio_usuario.convenio_id
		 INNER JOIN mem12_cvn_usuario
			ON mem12_cvn_convenio_usuario.usuario_id = mem12_cvn_usuario.id
		 INNER JOIN mem12_GrupoInvest_investigador 
			ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
		 INNER JOIN mem12_GrupoInvest_instituto
			ON mem12_GrupoInvest_instituto.id = mem12_GrupoInvest_investigador.instituto_id
	WHERE (YEAR(fecha_de_inicio) = 2012 
		   OR
		   (duracion_anyos < 100 AND
			YEAR(INTERVAL (duracion_anyos * 365 + duracion_meses * 12 + duracion_dias) DAY + fecha_de_inicio) >= 2012)
		   OR /* caso de dato erróneo */
			(duracion_anyos >= 100 AND
			YEAR(INTERVAL (duracion_meses * 12 + duracion_dias) DAY + fecha_de_inicio) >= 2012)
		   OR /* caso de dato erróneo */
			(duracion_anyos >= 2012)
			)
			AND
		   mem12_GrupoInvest_instituto.mostrar != 0

	GROUP BY mem12_GrupoInvest_instituto.nombre

	UNION ALL

	SELECT UCASE(ins1.nombre) AS "Instituto", 0
	FROM mem12_GrupoInvest_instituto AS ins1
	WHERE 
		(SELECT  count(ins2.nombre)
		FROM mem12_cvn_convenio
				 INNER JOIN mem12_cvn_convenio_usuario
					ON mem12_cvn_convenio.id = mem12_cvn_convenio_usuario.convenio_id
				 INNER JOIN mem12_cvn_usuario
					ON mem12_cvn_convenio_usuario.usuario_id = mem12_cvn_usuario.id
				 INNER JOIN mem12_GrupoInvest_investigador 
					ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
				 INNER JOIN mem12_GrupoInvest_instituto as ins2
					ON ins2.id = mem12_GrupoInvest_investigador.instituto_id
				 WHERE YEAR(fecha_de_inicio)=2012 AND
					   ins2.id = ins1.id
				 GROUP BY ins2.nombre) IS NULL
		AND ins1.mostrar != 0
) DerivedTable

ORDER BY Instituto asc
/*INTO OUTFILE "/tmp/convenios_institutos_2012.csv" FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';*/
