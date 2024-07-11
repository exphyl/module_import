# Author: Sohail Ali
# Date: 12.13.16
# Updated: 12.15.16
# Module_Import.py
# This application will take a list of modules and attempt to install them if they are not already installed

# 12.15.16, added the functionality to import sub modules from a module
# mods = {'netifaces': None, 'nmap': None} # Dict of modules to import
# Key is module name
# Value is what to import from Key e.g from BS4 import beautifulsoup

def os_check():
	import platform
	osp = {'system': platform.system(),
			'node': platform.node(),
			'release': platform.release(),
			'version': platform.version(),
			'machine': platform.machine(),
			'processor': platform.processor()}
	return osp

# if a module attempting to be imported is not installed, this function will attempt to install the module
def install_module(module): 
	import os
	val = os.system("python -m pip install --user " + module)
	return val
	
# this function checks to see if a module is already installed, if it is not
# then it will attempt to install the module and then checks to see if the module is installed again.
def check_module(module, subitem): 
	try:
		if subitem == None:
			__import__(module)
			x = 1
		else:
			__import__(module, fromlist=[subitem])
			x = 1
	except ImportError:
		print "Attempting to install %s" % module
		install_module(module)
		try:
			if subitem == None:
				__import__(module)
			else:
				__import__(module, fromlist=[subitem])
		except ImportError:
			print "There was an error, please manually install the module: %s" % module
		x = 0
	return (module, subitem, x)

# this function imports the module and returns a dict with the module name as the key
# and the imported module as the value. There is probably a cleaner way to do this.
def import_module(imported):
	i_mod = {}
	for k,v in imported.iteritems():
		if v == None:
			i_mod[k] = __import__(k)
		if v is not None:
			i_mod[k] = __import__(k, fromlist=[v]) 
	return i_mod

#old import_module function
# def import_module(imported):
# 	i_mod = {}
# 	for k,v in imported.iteritems():
# 		if v == 1:
# 			i_mod[k] = __import__(k, fromlist=[subitem]) 
# 	return i_mod
	

# this function verifies that all the modules that needed to be imported were imported.  	
def verified(mods):
	imported = {}
	x = 0
	for m,s in mods.iteritems():
		mod, sub, val = check_module(m,s)
		imported[mod] = mod, sub, val			
#	for m,s,i in imported.values():
	for m,s,i in imported.values():
		x += i
	if x == len(imported):
		return (imported,True)
	else:
		return False
		
# this function takes the checks return from verified() for a true or false value  
def checker(mods):		
	try:
		i, v = verified(mods)
		return i,v
	except:
		v = verified(mods)
		return v

# this function takes the return from the checker() function and if a True value is returned
# it builds a dict of modules
def module(checked):
	if checked is not False:
		i_mod = {}
		imported = {}
		for x, val in checked[0].iteritems():
			i = 0
			for m in val:
				if m is None:
					s = m
				if m is not None:
					#print m
					try:
						m += 1
					except:
						if i != 1:
						#	print m
							mod = m
							imported[mod] = None
						if i == 1:
						#	print "sub module: " + str(m)
							s = m
							imported[mod] = s
					#i_mod = mi.import_module(m,s)
				i += 1
		i_mod = import_module(imported)
	return i_mod
#just a test edit.