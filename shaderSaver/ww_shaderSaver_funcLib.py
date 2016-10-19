#ww_shaderSaver_funcLib

import maya.cmds as cmds
import os
import os.path
import json

def getAllShaders_list(*args):
	allSG = cmds.ls(type = 'shadingEngine')
	allShaders = []
	for each in allSG:
		if 'SG' in each:
			allShaders.append(each[:-2])
	return allShaders
	
def getShaderfromObjSel(selObj):
	selObj_shape = cmds.listRelatives(selObj, shapes = True)[0]
	selObj_SG = cmds.listConnections(selObj_shape, type = 'shadingEngine')[0]
	return selObj_SG[:-2]
	
def getSGfromShader(shader = None):
	if shader:
		if cmds.objExists(shader):
			sgq = cmds.listConnections(shader, d = True, et = True, t = 'shadingEngine')
			if sgq:
				return sgq[0]
	return None
	
def assignObjectListToShader(objList = None, shader = None):
	# assign selection to the shader
	shaderSG = getSGfromShader(shader)
	if objList:
		if shaderSG:
			cmds.sets(objList, e = True, forceElement = shaderSG)
		else:
			print 'The provided shader didn\'t return a shaderSG'
	else:
		print 'Please select one or more objects'
		
def assignSelectionToShader(shader = None):
	sel = cmds.ls(sl = True, l = True)
	if sel:
		assignObjectListToShader(sel, shader)
		
def getJsonFileName(currentProj, fileName):
	return currentProj + '/data/shaderSaver/' + fileName
	
def LoadJson(filePath):
	with open(filePath) as data_file:
		data = json.load(data_file)
		return data
	
def SaveJson(data, filePath):
	toBeSaved = json.dumps(data, sort_keys = True, indent = 4, ensure_ascii = False)
	f = open(filePath, 'w')
	f.write(toBeSaved)
	f.close()
	
def FormatDataJson(shaderData, objectData):
	endDict = {}
	for i in range(len(objectData)):
		endDict[objectData[i]] = shaderData[i]
	return endDict
	
def ConnectShaders(objSel, jsonFile):
	allInfo = LoadJson(jsonFile)
	print allInfo
	for i in range(len(objSel)):
		cmds.select(objSel[i])
		assignSelectionToShader(allInfo[objSel[i]])