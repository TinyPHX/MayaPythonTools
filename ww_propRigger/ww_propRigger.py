import maya.cmds as cmds
import maya.mel as mel

'''
take an object and make it a prop
- control structure should NOT interfere with any local rig stuff.  ie: jnts or deformers
'''
def RemoveNameSpace(inString):
	if ':' in inString:
		return inString.split(':')[-1]
	else:
		return inString
	
def MakePropComplex(propObj):
	parList = cmds.ls(sl = True)
	#-get parents, either from argument or from current selection
	if len(parList) == 0:
		parList = []
		for each in cmds.ls(sl = True):
			if not each == propObj:
				parList.append(each)
	
	for each in parList:
		if not each == propObj:
			print 'Assigning "%s" as a parent to our prop.'%each
		
	parList_noNS = []
	for every in parList:
		parList_noNS.append(RemoveNameSpace(every))
		
	# -find the main control deep inside propObj
	propObj_allChildren = cmds.listRelatives(propObj)
	print propObj_allChildren
	for allChild in propObj_allChildren:
		if '_ctrl' in allChild:
			propObj_ctrlsGrp = allChild
	propObj_ctrlsGrpKids = cmds.listRelatives(propObj_ctrlsGrp)
	print propObj_ctrlsGrpKids
	for allKid in propObj_ctrlsGrpKids:
		if '_main' in allKid:
			propObj_mainCtrlGrp = allKid
		
	#-build global control structure
	raw_globalCtrl = mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0 -s 8 -ch 0;')
	globalCtrl = cmds.rename(raw_globalCtrl, propObj_mainCtrlGrp[:-4] + '_prop_ctrl')
	globalCtrl_grp = cmds.group(em = True, n = propObj + '_prop_ctrl_grp')
	cmds.parent(globalCtrl, globalCtrl_grp)
	cmds.parentConstraint(globalCtrl, propObj_mainCtrlGrp, mo = True)
	cmds.scaleConstraint(globalCtrl, propObj_ctrlsGrp, mo = True)
	
	# -build rig grp and parent everything under this group
	globalRigGrp = cmds.group(em = True, n = '%s_prop_rig_grp' %propObj[:-4])
	cmds.parent(globalCtrl_grp, globalRigGrp)
	cmds.parent(propObj, globalRigGrp)
	
	#-make new space matching attr "parentTo"
	formatEnum = ''
	for i in range(len(parList)):
		print i
		print parList[i]
		print parList_noNS[i]
		if not parList[i] == propObj:
			if i == 0:
				break
			if i == 1:
				formatEnum += parList_noNS[i]
			else:
				formatEnum += ':%s' %parList_noNS[i]
			
	cmds.addAttr(globalCtrl, ln = 'parentTo', at = 'enum', en = formatEnum)
	cmds.setAttr('%s.parentTo'%globalCtrl, k = True)
	
	#-build nodal network for switching
	condNode_list = []
	parCon_list = []
	for i in range(len(parList)):
		if not parList[i] == propObj: 
			parCon_list.append(cmds.parentConstraint(parList[i], globalCtrl_grp, mo = True)[0])
			condNode_list.append(cmds.createNode('condition', n = '%s_parentTo_%i_cond'%(propObj[:-4], (i-1))))
			cmds.setAttr('%s.secondTerm'%condNode_list[i-1], (i-1))
			cmds.connectAttr('%s.parentTo'%globalCtrl, '%s.firstTerm'%condNode_list[i-1], f = True)
			for n in ['R','G','B']:
				cmds.setAttr('%s.colorIfFalse%s'%(condNode_list[i-1], n), 0)
				cmds.setAttr('%s.colorIfTrue%s'%(condNode_list[i-1], n), 1)
			cmds.connectAttr('%s.outColor.outColorR'%condNode_list[i-1], '%s.%sW%i'%(parCon_list[i-1], parList_noNS[i], (i-1)), f = True)

def MakePropSimple(propObj):
	parList = cmds.ls(sl = True)
	#-get parents, either from argument or from current selection
	if len(parList) == 0:
		parList = []
		for each in cmds.ls(sl = True):
			if not each == propObj:
				parList.append(each)
	
	for each in parList:
		if not each == propObj:
			print 'Assigning "%s" as a parent to our prop.'%each
		
	parList_noNS = []
	for every in parList:
		parList_noNS.append(RemoveNameSpace(every))
			
		
	#-build global control structure
	raw_globalCtrl = mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0 -s 8 -ch 0;')
	globalCtrl = cmds.rename(raw_globalCtrl, propObj[:-4] + '_prop_ctrl')
	globalCtrl_grp = cmds.group(em = True, n = propObj + '_prop_ctrl_grp')
	cmds.parent(globalCtrl, globalCtrl_grp)
	cmds.parentConstraint(globalCtrl, propObj, mo = True)
	#cmds.scaleConstraint(globalCtrl, propObj, mo = True)
	
	# -build rig grp and parent everything under this group
	globalRigGrp = cmds.group(em = True, n = '%s_prop_rig_grp' %propObj[:-4])
	cmds.parent(globalCtrl_grp, globalRigGrp)
	cmds.parent(propObj, globalRigGrp)
	
	#-make new space matching attr "parentTo"
	formatEnum = ''
	for i in range(len(parList)):
		print i
		print parList[i]
		print parList_noNS[i]
		if not parList[i] == propObj:
			if i == 0:
				break
			if i == 1:
				formatEnum += parList_noNS[i]
			else:
				formatEnum += ':%s' %parList_noNS[i]
			
	cmds.addAttr(globalCtrl, ln = 'parentTo', at = 'enum', en = formatEnum)
	cmds.setAttr('%s.parentTo'%globalCtrl, k = True)
	
	#-build nodal network for switching
	condNode_list = []
	parCon_list = []
	for i in range(len(parList)):
		if not parList[i] == propObj: 
			parCon_list.append(cmds.parentConstraint(parList[i], globalCtrl_grp, mo = True)[0])
			condNode_list.append(cmds.createNode('condition', n = '%s_parentTo_%i_cond'%(propObj[:-4], (i-1))))
			cmds.setAttr('%s.secondTerm'%condNode_list[i-1], (i-1))
			cmds.connectAttr('%s.parentTo'%globalCtrl, '%s.firstTerm'%condNode_list[i-1], f = True)
			for n in ['R','G','B']:
				cmds.setAttr('%s.colorIfFalse%s'%(condNode_list[i-1], n), 0)
				cmds.setAttr('%s.colorIfTrue%s'%(condNode_list[i-1], n), 1)
			cmds.connectAttr('%s.outColor.outColorR'%condNode_list[i-1], '%s.%sW%i'%(parCon_list[i-1], parList_noNS[i], (i-1)), f = True)
		
def propRigger(parList):
	#-get object from current selection
	propObj = cmds.ls(sl = True)[0]
	print "Making prop out of: ", propObj
	
	#check propObj
	if '_grp' in propObj:
		MakePropComplex(propObj)
	else:
		MakePropSimple(propObj)