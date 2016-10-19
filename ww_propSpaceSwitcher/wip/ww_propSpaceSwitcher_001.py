"""
ww_propSpaceSwitcher

by: Wesley Wilson
on: 9/23/2016


This tool builds a useful and robust seamless space switching system 

"""
#build a building function that sets up the attributes and nodal networks for switching
#as well as the necessary scriptJob and scriptNode as needed
#build the action function that gets called by the scriptJob
#this action function should be initialized by the scriptNode on scene load and then called
#by the scriptJob when the switch attribute gets updated

#doesn't work at all with animation.  need some way to set keyframes on everything being affected by the switching.  Things like the group witht he offset amount need to be keyed, as does the switch node
#need to do research on how autokeyframe can be tracked.  perhaps I can write another scirptJob to load that looks for setting keys on this particular attribute, then it sets keys on all other attributes
#the above statement will not be a thing. i think 


import maya.cmds as cmds
from functools import partial

def loadTest():
	"loaded!"
	
def reload():
	#reloadFile
	fileToReload = 'C:\Users\wwilson\Documents\maya\projects\TEST\scenes\spaceswitching_testing\03\propTool_maker_wip\propSwitching_test_001.ma'.replace('\\','/')
	cmds.file( fileToReload, open = True, force = True )

def actionFunc(propObj, parList):
	propObj_grp = '%s_grp' %propObj
	switchNode = '%s_switch'%propObj
	
def buildFunc(propObj, parList):
	propObj_ctrl = '%s_ctrl' %propObj
	propObj_ctrl_grp = '%s_grp_grp' %propObj_ctrl
	#build switch attribute and populate with parent list content
	parList_string = ''
	for i in range(len(parList)):
		if i > 0:
			parList_string += ':'
		parList_string += parList[i]
	cmds.select(propObj_ctrl)
	cmds.addAttr(ln = 'parentTo', at = 'enum', en = parList_string)
	cmds.setAttr(propObj_ctrl + '.parentTo', e = True, keyable = True)
	
	#build nodal network using parList
	switchNode = cmds.createNode('choice', n = '%s_switch_choice' %propObj)
	for i in range(len(parList)):
		cmds.createNode('condition', n = '%s_parCon_cond' %parList[i])
		cmds.connectAttr('%s.selector' %switchNode, '%s_parCon_cond.firstTerm' %parList[i], f = True)
		cmds.setAttr('%s_parCon_cond.secondTerm' %parList[i], i)
		cmds.setAttr('%s_parCon_cond.colorIfTrueR' %parList[i], 1)
		cmds.setAttr('%s_parCon_cond.colorIfFalseR' %parList[i], 0)
		parCon = cmds.parentConstraint(parList[i], propObj_ctrl_grp, n = '%s_parCon' %propObj_ctrl_grp, mo = True)[0]
		cmds.connectAttr( '%s_parCon_cond.outColor.outColorR' %parList[i], '%s.%sW%i' %(parCon, parList[i], i), f = True)
		
	#buildScriptNode and populate with scriptJob function which calls the action function
	importScript = 'import maya.cmds as cmds\ncmds.scriptJob( attributeChange = ["%s.parentTo", "newLoc = cmds.spaceLocator()\\ncmds.delete(cmds.parentConstraint(\'%s_grp\', newLoc, mo = False))\\ncmds.setAttr(\'%s.selector\', cmds.getAttr(\'%s.parentTo\'))\\ncmds.delete(cmds.pointConstraint(newLoc, \'%s_grp\', mo = False))\\ncmds.delete(cmds.orientConstraint(newLoc, \'%s_grp\', mo = False))\\ncmds.delete(newLoc)\\ncmds.select(\'%s\')"], protected = True)' %(propObj_ctrl, propObj_ctrl, switchNode, propObj_ctrl, propObj_ctrl, propObj_ctrl, propObj_ctrl)
	
	cmds.scriptNode(st = 1, bs = importScript, n = '%s_switch_scriptNode' %propObj, stp = 'python')