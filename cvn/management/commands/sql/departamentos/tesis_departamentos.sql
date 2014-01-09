/*-- Tesis doctorales con fecha de lectura en 2012 por departamentos. */
SELECT * FROM
(

SELECT UCASE(dep.nombre) AS "Departamento", 
      count(dep.nombre) AS "Tesis doctorales con fecha de lectura en 2012"

FROM mem12_GrupoInvest_departamento as dep
INNER JOIN mem12_GrupoInvest_investigador 
ON dep.id = mem12_GrupoInvest_investigador.departamento_id
INNER JOIN mem12_cvn_usuario
ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
INNER JOIN mem12_cvn_tesisdoctoral_usuario
ON mem12_cvn_tesisdoctoral_usuario.usuario_id = mem12_cvn_usuario.id
INNER JOIN mem12_cvn_tesisdoctoral
ON mem12_cvn_tesisdoctoral.id = mem12_cvn_tesisdoctoral_usuario.tesisdoctoral_id
WHERE YEAR(fecha_de_lectura)=2012 AND
       dep.mostrar != 0
GROUP BY dep.nombre

UNION ALL

SELECT UCASE(dep1.nombre) AS "Departamento", 0
FROM mem12_GrupoInvest_departamento AS dep1
WHERE 
(SELECT  count(dep2.nombre)
FROM mem12_GrupoInvest_departamento AS dep2
INNER JOIN mem12_GrupoInvest_investigador 
ON dep2.id = mem12_GrupoInvest_investigador.departamento_id
INNER JOIN mem12_cvn_usuario
ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
INNER JOIN mem12_cvn_tesisdoctoral_usuario
ON mem12_cvn_tesisdoctoral_usuario.usuario_id = mem12_cvn_usuario.id
INNER JOIN mem12_cvn_tesisdoctoral
ON mem12_cvn_tesisdoctoral.id = mem12_cvn_tesisdoctoral_usuario.tesisdoctoral_id
WHERE YEAR(fecha_de_lectura)=2012 AND 
		dep2.id = dep1.id
GROUP BY dep2.nombre) IS NULL
AND dep1.mostrar != 0
) DerivedTable

ORDER BY Departamento asc
/*INTO OUTFILE "/tmp/tesis_departamentos_2012.csv" FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';*/
