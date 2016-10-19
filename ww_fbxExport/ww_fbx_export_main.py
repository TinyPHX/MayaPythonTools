import maya.cmds as cmds
import maya.mel as mel
import os
import os.path
import json
from functools import partial

import ww_fbx_export_funcLib
from ww_fbx_export_funcLib import PrintFunction

#vars for the mel.eval calls, these should be function returns
exportFile_pyVar = ''
ww_fbx_export_funcLib.exportFile_mel = ''
animStart_pyVar = 1
ww_fbx_export_funcLib.animStart_mel = ''
animEnd_pyVa = 100
ww_fbx_export_funcLib.animEnd_mel = ''


varString_py = 'hotshits'
ww_fbx_export_funcLib.varString_mel = 'coolshits_2'

def DoTheStringThing(*args):
	ww_fbx_export_funcLib.MelStringFunction()
	print '\n' + ww_fbx_export_funcLib.varString_mel
	
fp = 'C:/Users/wwilson/Documents/maya/projects/TEST/assets/ww_fbx_export_funcLibxport_testing/01/spaceSwitch_export_001.fbx'
sel = [u'pSphere1', u'pSphere2', u'pSphere3', u'pCube1', u'pCube1_ctrl_grp_grp']
exportFile_pyVar = fp
ww_fbx_export_funcLib.exportFile_mel = 'newExportFile'
animStart_pyVar = 1
ww_fbx_export_funcLib.animStart_mel = 'animStart_melVar'
animEnd_pyVar = 100
ww_fbx_export_funcLib.animEnd_mel = 'animEnd_melVar'

def DoTheww_fbx_export_funcLibxportThing():
	ww_fbx_export_funcLib.ExportSelFbx(sel)
	
importFile_pyVar = fp
ww_fbx_export_funcLib.importFile_mel = 'newImportFile'
	
def DoTheFBXimportThing():
	ww_fbx_export_funcLib.ImportFbx(new = True)

widgets = {}

'''
printTheThing = ww_fbx_export_funcLib.PrintFunction()
print printTheThing
'''

PrintFunction()

def BuildUI():
	currentProj = cmds.workspace(q = True, fn = True)
	if (cmds.window('window', exists = True)):
		cmds.deleteUI('window', window = True)
		
	#create window
	widgets['win'] = cmds.window('window', title = 'FBX export tool', w = 400, h = 450)
	
	#create top frame
	widgets['topFrame'] = cmds.frameLayout(l = 'assemble files to build final FBX from', w = 400)
	
	#create top frame contents (text, spacers, text window, button)
	widgets['file_tsl'] = cmds.textScrollList('file_tsl', numberOfRows = 5)
	widgets['getFiles_btn'] = cmds.button('getFiles_btn', label = ' add files to list', c = partial(ww_fbx_export_funcLib.GetFiles, currentProj))
	
	#create bottom frame
	widgets['bottomFrame'] = cmds.frameLayout(l = 'build final FBX file', w = 400)
	
	#create bottom frame contents (text, spacers, button)
	widgets['spacer01'] = cmds.text("")
	widgets['buildFBX_btn'] = cmds.button('buildFBX_btn', l = 'commence-a-jigglin', c = DoTheStringThing)
	widgets['spacer02'] = cmds.text(" ")
	
	#show window
	cmds.showWindow(widgets['win'])