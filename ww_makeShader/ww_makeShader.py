import maya.cmds as cmds
import random

def RemoveNS(inString):
	if ':' in inString:
		return inString.split(':')[-1]
	else:
		return inString

def CorrectNS(inString):
	#returns the correct namespace to use in this scene given the incoming geo
	ns_list = []
	allAssemblies = cmds.ls(assemblies = True)
	
	for each in allAssemblies:
		if ':' in each:
			splitName = each.split(':')[:-1]
			for i in range(len(splitName)):
				if i == 0:
					ns = splitName[i]
				if not i == 0:
					ns += ':%s'%splitName[i]
			ns_list.append(ns)
	
	for i in range(len(ns_list)):
		#check if obj exists using current index ns and some sel_object without the namespace
		trialObj = RemoveNS(inString)
		if cmds.objExists('%s:%s'%(ns_list[i], trialObj)):
			return ns_list[i]
	
	#if we get this far without exiting the function, then we have no namespace matches, therefore should return an empty string
	return ''

def MakeRandSurfaceShader(sel_list, name):
	#new nodes
	newShader = cmds.shadingNode('surfaceShader', asShader = True, n = '%s_surfaceShader_mat'%name)
	newRGBtoHSV = cmds.createNode('rgbToHsv', n = '%s_surfaceShader_rgbhsv'%name)
	newHSVtoRGB = cmds.createNode('hsvToRgb', n = '%s_surfaceShader_hsvrgb'%name)
	newSatMult = cmds.createNode('multiplyDivide', n = '%s_surfaceShader_multDiv'%name)
	
	#connections for new nodes
	cmds.connectAttr('%s.outHsv'%newRGBtoHSV, '%s.input1'%newSatMult, f = True)
	cmds.connectAttr('%s.outHsv.outHsvS'%newRGBtoHSV, '%s.input2.input2Y'%newSatMult, f = True)
	cmds.connectAttr('%s.output'%newSatMult, '%s.inHsv'%newHSVtoRGB, f = True)
	cmds.connectAttr('%s.outRgb'%newHSVtoRGB, '%s.outColor'%newShader, f = True)
	
	#setting attributes
	cmds.setAttr('%s.operation'%newSatMult, 2) #divide
	cmds.setAttr('%s.inRgb'%newRGBtoHSV, random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), type = 'double3')
	
	#assignment to geo
	for sel in sel_list:
		sel_noNS = RemoveNS(sel)
		sel_NS = CorrectNS(sel)
		if sel_NS == '':
			appendedSel = sel_noNS
		else:
			appendedSel = '%s:%s'%(sel_NS, sel_noNS)
		cmds.select(appendedSel)
		cmds.hyperShade(assign = newShader)
	
	
	