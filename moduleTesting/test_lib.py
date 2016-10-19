'''
lib test module
'''
import maya.cmds as cmds
import maya.mel as mel
import sys
'''
functionLib = 'C:/Users/wwilson/Documents/maya/scripts/moduleTesting'
for each in sys.modules.keys():
	if 'test_main' in each:
		print each
		del sys.modules[each]

import test_main
'''
def FindVar(str):
	return str

def SomeInfo(info):
	return info

def Thingy01(input):
	print "Here we are."
	print "%s" %returned_info
	print input
	
returned_info = SomeInfo('cluckcluck')
someVar_py = 'colonel'
someVar_mel = 'sanders'

def MelStringFunction():
	mel.eval('string $%s = `python "someVar_py"`;'%someVar_mel)
	mel.eval('print $%s;'%someVar_mel)
