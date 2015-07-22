#!/usr/bin/env python
# swap_po_in_py.py
#
# Copyright (C) 2015 Hugo A. Jimenez Hernandez
#   Released under the terms of the MIT License.
#
"""
Swap the string in source code with the new string after swapping msgid and msgstr in a Gettext PO file.

"""
import sys		
from os.path import join as os_path_join, splitext
from tempfile import mkstemp
from shutil import move
from os import remove, close
import io
class XCHG_translations:
	
	def __init__(self):
		self.root_path = ""
	def load_po(self,filename):
		try:
			from polib import pofile
			self.po = pofile(filename)
			print(self.po)
		except ImportError:
			print 'This script requires Polib.'
			print 'Download it at https://pypi.python.org/pypi/polib/'

	def get_path(self,filename):
		return os_path_join(self.root_path, filename)
	def get_type(self,filename):
		return splitext(filename)[1]		


 
	def set_root_path(self,path):
		self.root_path = path

	def replace(self,filename, lineno, esp_str,eng_str):

		#Create temp file
		if filename.endswith(".html.py"):
			filename = splitext(filename)[0]
		print("Fichero:%s " % (filename))
		src_file_path = self.get_path(filename)
		fh, dst_path = mkstemp()
		with io.open(src_file_path, 'r',encoding='utf-8') as src_file:
			code = src_file.readlines()
		

		if self.get_type(filename) == u'.html':
			import ipdb; ipdb.set_trace()			
			#import ipdb; ipdb.set_trace()
			pattern = u'{% trans '+ u'"'+esp_str+u'"' +u' %}'
			eng_pattern = u'{% trans '+ u'"'+eng_str+u'"' +u' %}'
			try:
						
				if pattern not in code[lineno-1]:
					pattern = u'{% trans '+ '\''+esp_str+'\'' +u' %}'
					eng_pattern = u'{% trans '+ u'\''+eng_str+u'\'' +u' %}'
				if eng_pattern not in code[lineno-1]:
					code[lineno-1] = code[lineno-1].replace(pattern,'{% trans '+'"'+eng_str+'"'+' %}')
					with io.open(dst_path,'w',encoding='utf-8') as dst_file:
						dst_file.writelines(code)
					#Remove original file
					remove(src_file_path)
					#Move new file
					move(dst_path, src_file_path)
			except UnicodeDecodeError:
				print (UnicodeDecodeError)	
		if 	self.get_type(filename) == u'.py':
			#import ipdb; ipdb.set_trace()
			pattern = u'_(' + '"' + esp_str + '"' + ')'
			eng_pattern = u'_(' + '"' + eng_str + '"' + ')'
			try:
				if pattern not in code[lineno-1]:							
					pattern = u'_(u' + '"' + esp_str + '"' + ')'
					eng_pattern = u'_(u' + '"' + eng_str + '"' + ')'
				if pattern not in code[lineno-1]:
					pattern = u'_(u' + '\'' + esp_str + '\'' + ')'
					eng_pattern = u'_(u' + '\'' + eng_str + '\'' + ')'
				if pattern not in code[lineno-1]:													
					pattern = u'_(' + '\'' + esp_str + '\'' + ')'
					eng_pattern = u'_(' + '\'' + eng_str + '\'' + ')'
				if eng_pattern not in code[lineno-1]:
					code[lineno-1] = code[lineno-1].replace(pattern,u'_('+'"'+eng_str+'"'+')')
					with io.open(dst_path,'w',encoding='utf-8') as dst_file:
						dst_file.writelines(code)
					#Remove original file
					remove(src_file_path)
					#Move new file
					move(dst_path, src_file_path)
			except UnicodeDecodeError:
				print (UnicodeDecodeError)	
import sys

try:
  from polib import pofile
except ImportError:
  print 'This script requires Polib.'
  print 'Download it at https://pypi.python.org/pypi/polib/'
  sys.exit(1)

if len(sys.argv) != 3:
  print 'USAGE: %s <PO file> <ROOT DIR>' % sys.argv[0]
  sys.exit(1)

filename = sys.argv[1]

XCHG=XCHG_translations()
XCHG.set_root_path(sys.argv[2])
XCHG.load_po(filename)

# Swap every unit, except the first one,
# which should be the gettext header.
valid_entries = [e for e in XCHG.po if e.occurrences]
valid_entries = [e for e in valid_entries if e.msgid]
for entry in valid_entries:
	esp = entry.msgid
	eng = entry.msgstr
	for occ in entry.occurrences:
		try:
				print (occ)
				XCHG.replace(occ[0],int(occ[1]),esp,eng)
		except IOError:
			print (IOError)
			pass



