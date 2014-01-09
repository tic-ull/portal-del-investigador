/*-- Tesis doctorales con fecha de lectura en 2012 por institutos. */
SELECT * FROM
(

SELECT UCASE(ins.nombre) AS "Instituto", 
      count(ins.nombre) AS "Tesis doctorales con fecha de lectura en 2012"

FROM mem12_GrupoInvest_instituto as ins
INNER JOIN mem12_GrupoInvest_investigador 
ON ins.id = mem12_GrupoInvest_investigador.instituto_id
INNER JOIN mem12_cvn_usuario
ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
INNER JOIN mem12_cvn_tesisdoctoral_usuario
ON mem12_cvn_tesisdoctoral_usuario.usuario_id = mem12_cvn_usuario.id
INNER JOIN mem12_cvn_tesisdoctoral
ON mem12_cvn_tesisdoctoral.id = mem12_cvn_tesisdoctoral_usuario.tesisdoctoral_id
WHERE YEAR(fecha_de_lectura)=2012 AND
       ins.mostrar != 0
GROUP BY ins.nombre

UNION ALL

SELECT UCASE(ins1.nombre) AS "Instituto", 0
FROM mem12_GrupoInvest_instituto AS ins1
WHERE 
(SELECT  count(ins2.nombre)
FROM mem12_GrupoInvest_instituto AS ins2
INNER JOIN mem12_GrupoInvest_investigador 
ON ins2.id = mem12_GrupoInvest_investigador.instituto_id
INNER JOIN mem12_cvn_usuario
ON mem12_cvn_usuario.documento = mem12_GrupoInvest_investigador.nif
INNER JOIN mem12_cvn_tesisdoctoral_usuario
ON mem12_cvn_tesisdoctoral_usuario.usuario_id = mem12_cvn_usuario.id
INNER JOIN mem12_cvn_tesisdoctoral
ON mem12_cvn_tesisdoctoral.id = mem12_cvn_tesisdoctoral_usuario.tesisdoctoral_id
WHERE YEAR(fecha_de_lectura)=2012 AND 
		ins2.id = ins1.id
GROUP BY ins2.nombre) IS NULL
AND ins1.mostrar != 0
) DerivedTable

ORDER BY Instituto asc
/*INTO OUTFILE "/tmp/tesis_institutos_2012.csv" FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';*/
