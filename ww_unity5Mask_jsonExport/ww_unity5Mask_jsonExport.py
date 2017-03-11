'''
this tool takes a rig hierarchy(joints) and allows for checkbox masking on itself and other joints in the hierarchy.

-should display the dagpath to all joints and allow for checkboxing
-if a parent is unchecked, all it's children should be unchecked as well
-if a parent is checked, all it's children should be check-able
-need to find a way to order and distribute the checkbox list.  maybe as we see it in the outliner...
-need checkbox behavior that unchecks things marked as children...
'''
import maya.cmds as cmds
from functools import partial
import json
import os

widgets = {}

def ToolUI():
	if (cmds.window('window', exists = True)):
		cmds.deleteUI('window', window = True)
		
	#create window
	widgets['win'] = cmds.window('window', title = 'unity5 mask json exporter', w = 300, h = 400)
	
	#create top frame
	widgets['topFrame'] = cmds.frameLayout(l = 'display all joints', w = 300)
	widgets['topColumn'] = cmds.columnLayout(adjustableColumn = True)
	
	#create name field
	widgets['maskName'] = cmds.textFieldGrp()
	
	#create some text
	widgets['winTextTop'] = cmds.text(label = 'Joints with mask turned ON')
	
	#get the stuff for the topBox
	topBoxList = GetAllStuff(gui = True)
	
	#createTopBox (selection)
	widgets['selBox'] = cmds.textScrollList('selJntsList', numberOfRows = 15, allowMultiSelection = True, append = topBoxList)
	
	#create some more text
	widgets['winTextMid'] = cmds.text(label = 'Joints with mask turned OFF')
	
	#createBottomBox (deselection)
	widgets['deselBox'] = cmds.textScrollList('deselJntsList', numberOfRows = 15, allowMultiSelection = True)
	
	#create switch button
	widgets['switchButton'] = cmds.button(l = 'switch sides', w = 300, c = SwitchBtn_cmd)
	
	#create export button
	widgets['exportButton'] = cmds.button(l = 'export to JSON', w = 300, c = JsonExport_cmd)
	
	#show window
	cmds.showWindow(widgets['win'])
	
def PrintThing(*args):
	print "nothing here yet..."
	
def GetAllStuff(gui = True):
	allStuff = cmds.ls(dag = True, long = True)
	endList = []
	for each in allStuff:
		if '_grp' in each:
			if gui:
				if each.split('|')[1] == each.split('|')[-1]:
					endList.append(each.split('|')[-1])
				else:
					endList.append(each.split('|')[1] + '|' + each.split('|')[-1])
			else:
				endList.append(each[1:].replace('|','/'))
	return endList

def LoadJson(data, filePath):
	with open(filePath) as data_file:    
		data = json.load(data_file)
	
def SaveJson(data):
	prePath = cmds.workspace(q=True, dir=True)
	rootDir = prePath.split("scenes")[0]
	endDir = rootDir + '/data/unity_masks/'
	if not os.path.exists(endDir):
		os.mkdir(os.path.join(rootDir + '/data/', 'unity_masks'))
	filePath = endDir + cmds.textFieldGrp(widgets['maskName'], q = True, tx = True) + '.txt'
	toBeSaved = json.dumps(data, sort_keys = True, indent = 4, ensure_ascii = False)
	f = open(filePath, 'w')
	f.write(toBeSaved)
	f.close()
	
def JsonExport_cmd(*args):
	data = FormatJson()
	SaveJson(data)
	
def FormatJson(*args):
	weights_list = []
	theDagObjs_format = GetAllStuff(gui = False)
	checkDagObjs = GetAllStuff(gui = True)
	#every selectable thign in the TOP list right now
	for i in range(len(checkDagObjs)):
		try:
			cmds.textScrollList(widgets['selBox'], e = True, selectItem = checkDagObjs[i])
		except TypeError as te:
			print te
	#everythign in the toplist	
	selObj_topList = cmds.textScrollList(widgets['selBox'], q = True, selectItem = True)
	
	#check against everythign in the master list.  if in the top list, assign a weight of 1
	for i in range(len(checkDagObjs)):
		if checkDagObjs[i] in selObj_topList:
			weights_list.append(1)
		else:
			weights_list.append(0)
			
	for i in range(len(theDagObjs_format)):
		print "%s has a weight of %i" %(theDagObjs_format[i].split('/')[-1], weights_list[i])
	
	#build our export dictionary 
	finalDict_avMask = {}
	finalDict_master = {}
	
	prefab_subMask_dict = {}
	prefab_subMask_dict['fileID'] = 0
	
	mask_string = ''
	for i in range(104):
		mask_string += '0'
		
	blankInsertion_dict = {}
	blankInsertion_dict['m_Weight'] = 1
	blankInsertion_dict['m_Path'] = ''
	
	finalDict_list = []
	for i in range(len(theDagObjs_format)):
		finalDict_sub = {}
		finalDict_sub['m_Weight'] = weights_list[i]
		finalDict_sub['m_Path'] = theDagObjs_format[i]
		finalDict_list.append(finalDict_sub)
	
	finalDict_list.insert(0, blankInsertion_dict)
	
	finalDict_avMask['m_ObjectHideFlags'] = 0
	finalDict_avMask['m_PrefabParentObject'] = prefab_subMask_dict
	finalDict_avMask['m_PrefabInternal'] = prefab_subMask_dict
	finalDict_avMask['m_Name'] = 'SpacePug - Mask (%s)' %cmds.textFieldGrp(widgets['maskName'], q = True, tx = True)
	finalDict_avMask['m_Mask'] = mask_string
	finalDict_avMask['m_Elements'] = finalDict_list
	
	finalDict_master['AvatarMask'] = finalDict_avMask
	
	return finalDict_master
	
	
def SwitchBtn_cmd(*args):
	selItems_top = cmds.textScrollList(widgets['selBox'], q = True, si=True, ams=True)
	selItems_bottom = cmds.textScrollList(widgets['deselBox'], q = True, si=True, ams=True)
	
	#check topList.  if it's == None, then we are goign from bottom to top.
	if selItems_top != None:
		SwitchSides(selItems_top, top = True)
	elif selItems_bottom != None:
		SwitchSides(selItems_bottom, top = False)
	else:
		print("Nothing selected...")
		
def SwitchSides(selList, top = False):
	if top == False:
		for each in selList:
			cmds.textScrollList(widgets['selBox'], e = True, append = each)
			cmds.textScrollList(widgets['deselBox'], e = True, removeItem = each)
	else:
		for each in selList:
			cmds.textScrollList(widgets['deselBox'], e = True, append = each)
			cmds.textScrollList(widgets['selBox'], e = True, removeItem = each)
	