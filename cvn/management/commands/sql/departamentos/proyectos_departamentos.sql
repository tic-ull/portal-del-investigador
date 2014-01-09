/*-- Proyectos por departamentos
-- Actualmente: Con fecha de inicio en 2012 o vigentes con fecha de fin en 2012 o más.
*/

SELECT * FROM
(
SELECT UCASE(mem12_GrupoInvest_departamento.nombre) AS "Departamento", 
		count(mem12_cvn_proyecto_usuario.id) AS "Proyectos vigentes o con fecha de inicio en 2012"
	FROM mem12_cvn_proyecto
		 INNER JOIN mem12_cvn_proyecto_usuario
			ON mem12_cvn_proyecto.id = mem12_cvn_proyecto_usuario.proyecto_id
		 INNER JOIN mem12_cvn_usuario
			ON mem12_cvn_proyecto_usuario.usuario_id = mem12_cvn_usuario.id
	     INNER JOIN mem12_GrupoInvest_investigador 
			ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
		 INNER JOIN mem12_GrupoInvest_departamento
			ON mem12_GrupoInvest_departamento.id = mem12_GrupoInvest_investigador.departamento_id
		WHERE (YEAR(fecha_de_inicio)=2012 OR YEAR(fecha_de_fin)>=2012) AND
		              mem12_GrupoInvest_departamento.mostrar != 0

		GROUP BY mem12_GrupoInvest_departamento.nombre

UNION ALL

SELECT UCASE(dep1.nombre) AS "Departamento", 0
FROM mem12_GrupoInvest_departamento AS dep1
WHERE 
(SELECT  count(dep2.nombre)
FROM mem12_cvn_proyecto
		 INNER JOIN mem12_cvn_proyecto_usuario
			ON mem12_cvn_proyecto.id = mem12_cvn_proyecto_usuario.proyecto_id
		 INNER JOIN mem12_cvn_usuario
			ON mem12_cvn_proyecto_usuario.usuario_id = mem12_cvn_usuario.id
	     INNER JOIN mem12_GrupoInvest_investigador 
			ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
		 INNER JOIN mem12_GrupoInvest_departamento as dep2
			ON dep2.id = mem12_GrupoInvest_investigador.departamento_id
		 WHERE (YEAR(fecha_de_inicio)=2012 OR YEAR(fecha_de_fin)>=2012) AND
			   dep2.id = dep1.id
		 GROUP BY dep2.nombre) IS NULL
AND dep1.mostrar != 0
) DerivedTable

ORDER BY Departamento asc
/*INTO OUTFILE "/tmp/proyectos_departamentos_2012.csv" FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';*/
