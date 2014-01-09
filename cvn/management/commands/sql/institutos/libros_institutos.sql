/*----------------------------------------------------------------------------------------------
-- Capítulos de libros únicos por instituto en tabla Publicación-Usuario
----------------------------------------------------------------------------------------------*/
SELECT * FROM
(
SELECT nombre AS "Instituto", 
		COUNT(nombre) AS "Libros publicados en 2012" 
FROM (
	SELECT DISTINCT mem12_cvn_publicacion_usuario.publicacion_id, 
			mem12_GrupoInvest_instituto.nombre AS nombre
		FROM mem12_cvn_publicacion
			INNER JOIN mem12_cvn_publicacion_usuario
				ON mem12_cvn_publicacion.id = mem12_cvn_publicacion_usuario.publicacion_id 
			INNER JOIN mem12_cvn_usuario
				ON mem12_cvn_publicacion_usuario.usuario_id = mem12_cvn_usuario.id
			INNER JOIN mem12_GrupoInvest_investigador 
				ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
			INNER JOIN mem12_GrupoInvest_instituto
				ON mem12_GrupoInvest_instituto.id = mem12_GrupoInvest_investigador.instituto_id
			WHERE YEAR(fecha)=2012 AND 
						tipo_de_produccion="Libro" AND
						mem12_GrupoInvest_instituto.mostrar != 0
			GROUP BY  mem12_cvn_publicacion_usuario.publicacion_id, 
				mem12_GrupoInvest_instituto.nombre) DerivedTable1
GROUP BY nombre

UNION ALL

SELECT UCASE(ins1.nombre) AS "Instituto", 0
FROM mem12_GrupoInvest_instituto AS ins1
WHERE 
(SELECT  count(ins2.nombre)
FROM mem12_cvn_publicacion
			INNER JOIN mem12_cvn_publicacion_usuario
				ON mem12_cvn_publicacion.id = mem12_cvn_publicacion_usuario.publicacion_id 
			INNER JOIN mem12_cvn_usuario
				ON mem12_cvn_publicacion_usuario.usuario_id = mem12_cvn_usuario.id
			INNER JOIN mem12_GrupoInvest_investigador 
				ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
			INNER JOIN mem12_GrupoInvest_instituto AS ins2
				ON ins2.id = mem12_GrupoInvest_investigador.instituto_id
			WHERE YEAR(fecha)=2012 AND 
				  tipo_de_produccion="Libro" AND
				  ins2.id = ins1.id
			GROUP BY ins2.nombre) IS NULL
			AND ins1.mostrar != 0
) DerivedTable2

ORDER BY Instituto asc

/*INTO OUTFILE "/tmp/libros_institutos_2012.csv" FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';*/
