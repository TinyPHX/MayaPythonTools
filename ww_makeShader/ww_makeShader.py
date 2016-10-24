import maya.cmds as cmds
import random

def RemoveNS(inString):
	if ':' in inString:
		return inString.split(':')[-1]
	else:
		return inString

def CorrectNS(sel_list):
	new_sel_list = []
	sel_list_noNS = []
	NS_list = []
	allAssemblies = cmds.ls(assemblies = True)
	for each in allAssemblies:
		if ':' in each:
			splitName = each.split(':')[:-1]
			myNS = ''
			if len(splitName) > 1:
				for i in range(len(splitName)):
					if i == 0:
						myNS += splitName[i]
					else:
						myNS += ':' + splitName[i]
			else:
				myNS = splitName[0]
			NS_list.append(myNS)
			
	for each in sel_list:
		sel_list_noNS.append(RemoveNS(each))
		
	for i in range(len(NS_list)):
		for x in range(len(sel_list_noNS)):
			newString = NS_list[i] + ':' + sel_list_noNS[x]
			if (cmds.objExists(newString)):
				new_sel_list.append(newString)
		
	return new_sel_list
	
def MakeRandSurfaceShader(sel_list, name):
	newShader = cmds.shadingNode('surfaceShader', asShader = True, n = '%s_surfaceShader_mat'%name)
	cmds.setAttr('%s.outColor'%newShader, random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), type = 'double3')
	for sel in CorrectNS(sel_list):
		cmds.select(sel)
		cmds.hyperShade(assign = newShader)
	
	
	