#Pose Saver tool for Maya 
#by: Wesley Wilson on 11/25/2015
 
'''
to use:
	COPYING:
		- select all control curves to be saved to file
		- name the text file you want outputted something descriptive.  You will have to navigate to this later
		- click button to save pose information.  
		
		Script saves to the current project's data folder inside a poseSaves folder.
	
	PASTING:
		- select all control curves AND joints to be compared and changed by text file
		- determine the time slide distance in the int field
		- click button to start pasting procedure.  
		
		Script opens a file dialogue box where you navigate to the text file corresponding to the pose you want.
		Once selected, the script searches the current selection for different transform values from those from the pose text file.
		If there is a difference in a specific channel, keyframes are set at the current time at the current values and then at the 
		current time (+ the time slide distance amount defined earlier) with the changed values from the text file.

future stuff:
	- add support for namespaces (on save, the controller/joint names are recorded sans the nameSpace.  on load, the controller/joint names are read from the currentSel sans the nameSpace)
	- add support for more channels/ custom channels.  Not sure HOW this would work right now.
	- add support for animated groups or blendshape's or just mesh transformations
'''
	

import maya.cmds as cmds
import json
import os

#global animation check var
CHECKANIM = True

#prevents duplicate windows from popping up	
if cmds.window('poseSaver',exists=True):
	cmds.deleteUI('poseSaver',window=True)

def GetName(inName):
	if ':' in inName:
		return inName.split(':')[-1]
	else:
		return inName

#copy KeyFrames function
def copyPose(*args):
	allCurves = cmds.ls(sl=True)
	
	#this is what the file will be named
	poseName = cmds.textFieldGrp('poseName_grp',q=True,tx=True)
	
	#this is what we will be saving
	saveDict = {}
	
	for i in range(len(allCurves)):
		#find keyable attrs
		allValDicts = []
		cntrlObj = GetName(allCurves[i])
		for attrName in cmds.listAttr(allCurves[i], k = True):
			valDict = {}
			valDict[attrName] = cmds.getAttr('%s.%s'%(allCurves[i], attrName))
			allValDicts.append(valDict)
		
		saveDict[cntrlObj] = allValDicts
	
	#find current workpath
	prePath = cmds.workspace(q=True,dir=True)
	trimPath=prePath.find('/',41)
	dataPath = prePath[:trimPath] + '/data/'
	folderPath = dataPath + '/poseSaves/'
	
	#check to see if folder already exists
	ifExist = os.path.exists(folderPath)
	if not ifExist:
		#make folder to store .txt files if one does not already exist
		os.mkdir(os.path.join(dataPath, 'poseSaves'))
		
	fullPath = folderPath + poseName + '.txt'
	
	toBeSaved = json.dumps(saveDict, sort_keys=True, ensure_ascii=True, indent=2)
	f=open(fullPath, 'w')
	
	#the actual save
	f.write(toBeSaved)
	f.close()
		
		
#paste KeyFrames function
def pastePose(*args):
	#currentTime
	crntTime=cmds.currentTime(q=True)
	
	#check if animation = yes
	CHECKANIM = CheckAnimBtn()
	
	#slideAmount
	slideAmnt = cmds.intFieldGrp('slideTime_grp',q=True,v=True)[0]
	print slideAmnt
	
	#filePath
	fileTypes = '*.txt'
	fileName = cmds.fileDialog2(ds=2, fileFilter = fileTypes, fileMode=1, caption="Paste Pose",okc = 'Load')[0]
	print fileName
	
	#selection of things you want the pose pasted to
	currentSel = cmds.ls(sl=True)
	
	#fullPath = prePath[:trimPath]+'//data/poseSaves/'+fileName+'.txt'
	if os.path.exists(fileName):
		#if the file at a specific path exists, then open it and attach information from it to variables
		f=open(fileName)
		dataFile = json.load(f)
		
		for i in range(len(currentSel)):
			currentSel_name = GetName(currentSel[i])	
			#findAttrs
			attrs = cmds.listAttr(currentSel[i], k = True)
			currentDict = dataFile[currentSel_name]
			for x in range(len(currentDict)):
				for key in currentDict[x]:
					#print "key: %s, value: %s"%(key, currentDict[x][key])
					#check if the currently selected object has an attr that matches the name of the key we have stored
					if cmds.listAttr(currentSel[i], st = key):
						#check current value and compare with new value
						currentVal = cmds.getAttr('%s.%s'%(currentSel[i], key))
						if not currentVal == currentDict[x][key]:
							try:
								if CHECKANIM: #yes/True
									cmds.setKeyframe('%s.%s'%(currentSel[i], key))
									cmds.currentTime(crntTime + slideAmnt, update = True, edit = True)
								cmds.setAttr('%s.%s'%(currentSel[i], key), currentDict[x][key])
								if CHECKANIM: #yes/True
									cmds.setKeyframe('%s.%s'%(currentSel[i], key))
									cmds.currentTime(crntTime, update = True, edit = True)
							except RuntimeError as re:
								print re
				

#check animCheck_btn
def CheckAnimBtn(*args):
	currentAnimBtn_val = cmds.radioButtonGrp('animCheck_btn', q = True,  sl = True)
	if currentAnimBtn_val == 1: #yes
		cmds.intFieldGrp('slideTime_grp', e = True, enable = True)
		CHECKANIM = True
	else:
		cmds.intFieldGrp('slideTime_grp', e = True, enable = False)
		CHECKANIM = False
		
	return CHECKANIM

#show GUI function

def showGUI():
	cmds.window('poseSaver',title='Pose Saver by Wesley Wilson')
	cmds.rowColumnLayout(numberOfRows=20,p='poseSaver')
	
	cmds.radioButtonGrp('animCheck_btn', label = 'Set keyframes?', labelArray2 = ['yes','no'], numberOfRadioButtons = 2, sl = 1, cc = CheckAnimBtn)
	cmds.textFieldGrp('poseName_grp', label='Name for this pose',pht="ex: HIKI_H1_001")
	cmds.button('copyPose_btn',label='Save Pose', c=copyPose)
	cmds.intFieldGrp('slideTime_grp',numberOfFields = 1, label='Duration of transition', enable = False)
	cmds.button('loadPose_btn',label='Load Pose', c=pastePose)
	
	cmds.showWindow('poseSaver')