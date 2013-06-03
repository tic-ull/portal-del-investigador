# -*- coding: utf-8 -*-

# Fichero con funciones auxiliares para las vistas

def formatDocumentIdent(data = None):
	""" 
	Función de ayuda que recibe un dato (NIE - NIF) y lo formatea para poder realizar
	las búsquedas. El formateo consiste en eliminar:
	  * guiones "-"
	  * puntos "." 
	
	Variables:
	- data: Documento de identificación a formatear.
	"""
	# Eliminar guiones del documento de identificacion
	if not data:
		return None
	# Eliminar espacios al principio o al final de la cadena
	data = data.strip()
	if ' ' in data:
		data = data.replace(' ','')
	if '-' in data:
		data = data.replace('-','')
	if '.' in data:
		data = data.replace('.','')
	return data
		

def searchDataUser(data = None):
	"""
		Función que devuelve un diccionario para buscar los datos de un usuario en la BBDD.
		Su principal uso es para comprobar que no se va a añadir un usuario que ya existe.
		
		Variables:
		- data:  Diccionario con los datos personales del usuario a añadir.
		
		Return: Diccionario de búsqueda.
	"""
	search_dic = {}
	if data.has_key('segundo_apellido'):
		search_dic['segundo_apellido'] = data['segundo_apellido']
	if data.has_key('primer_apellido'):
		search_dic['primer_apellido'] = data['primer_apellido']
	if data.has_key('nombre'):
		search_dic['nombre'] = data['nombre']
	# NOTE Algunos usuarios no tienen documento en el pdf duplicado y falla la búsqueda
	#if data.has_key('documento'):
	#	search_dic['documento'] = data['documento']
	return search_dic

	
	
	
