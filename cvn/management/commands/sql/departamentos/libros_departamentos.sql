/*----------------------------------------------------------------------------------------------
-- Capítulos de libros únicos por departamento en tabla Publicación-Usuario
----------------------------------------------------------------------------------------------*/
SELECT * FROM
(
SELECT nombre AS "Departamento", 
		COUNT(nombre) AS "Libros publicados en 2012" 
FROM (
	SELECT DISTINCT mem12_cvn_publicacion_usuario.publicacion_id, 
			mem12_GrupoInvest_departamento.nombre AS nombre
		FROM mem12_cvn_publicacion
			INNER JOIN mem12_cvn_publicacion_usuario
				ON mem12_cvn_publicacion.id = mem12_cvn_publicacion_usuario.publicacion_id 
			INNER JOIN mem12_cvn_usuario
				ON mem12_cvn_publicacion_usuario.usuario_id = mem12_cvn_usuario.id
			INNER JOIN mem12_GrupoInvest_investigador 
				ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
			INNER JOIN mem12_GrupoInvest_departamento
				ON mem12_GrupoInvest_departamento.id = mem12_GrupoInvest_investigador.departamento_id
			WHERE YEAR(fecha)=2012 AND 
						tipo_de_produccion="Libro" AND
						mem12_GrupoInvest_departamento.mostrar != 0
			GROUP BY  mem12_cvn_publicacion_usuario.publicacion_id, 
				mem12_GrupoInvest_departamento.nombre) DerivedTable1
GROUP BY nombre

UNION ALL

SELECT UCASE(dep1.nombre) AS "Departamento", 0
FROM mem12_GrupoInvest_departamento AS dep1
WHERE 
(SELECT  count(dep2.nombre)
FROM mem12_cvn_publicacion
			INNER JOIN mem12_cvn_publicacion_usuario
				ON mem12_cvn_publicacion.id = mem12_cvn_publicacion_usuario.publicacion_id 
			INNER JOIN mem12_cvn_usuario
				ON mem12_cvn_publicacion_usuario.usuario_id = mem12_cvn_usuario.id
			INNER JOIN mem12_GrupoInvest_investigador 
				ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
			INNER JOIN mem12_GrupoInvest_departamento AS dep2
				ON dep2.id = mem12_GrupoInvest_investigador.departamento_id
			WHERE YEAR(fecha)=2012 AND 
				  tipo_de_produccion="Libro" AND
				  dep2.id = dep1.id
			GROUP BY dep2.nombre) IS NULL
			AND dep1.mostrar != 0
) DerivedTable2

ORDER BY Departamento asc

/*INTO OUTFILE "/tmp/libros_departamentos_2012.csv" FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';*/
