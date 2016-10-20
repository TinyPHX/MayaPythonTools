import maya.cmds as cmds
import maya.mel as mel

'''
take an object and make it a prop
- control structure should NOT interfere with any local rig stuff.  ie: jnts or deformers
'''
	
def propRigger(parList):
	#-get object from current selection
	propObj = cmds.ls(sl = True)[0]
	print "Making prop out of: ", propObj
	
	#-get parents, either from argument or from current selection
	if len(parList) == 0:
		parList = []
		for each in cmds.ls(sl = True):
			if not each == propObj:
				parList.append(each)
	
	for each in parList:	
		print 'Assigning "%s" as a parent to our prop.'%each
		
	#-build global control structure
	raw_globalCtrl = mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0 -s 8 -ch 0;')
	globalCtrl = cmds.rename(raw_globalCtrl, propObj[:-4] + '_prop_ctrl')
	globalCtrl_grp = cmds.group(em = True, n = propObj + '_prop_ctrl_grp')
	cmds.parent(globalCtrl, globalCtrl_grp)
	cmds.parentConstraint(globalCtrl, propObj, mo = True)
	cmds.scaleConstraint(globalCtrl, propObj, mo = True)
	
	# -build rig grp and parent everything under this group
	globalRigGrp = cmds.group(em = True, n = '%s_prop_rig_grp' %propObj[:-4])
	cmds.parent(globalCtrl_grp, globalRigGrp)
	cmds.parent(propObj, globalRigGrp)
	
	#-make new space matching attr "parentTo"
	formatEnum = ''
	for i in range(len(parList)):
		if i == 0:
			formatEnum += parList[i]
		else:
			formatEnum += ':%s' %parList[i]
			
	cmds.addAttr(globalCtrl, ln = 'parentTo', at = 'enum', en = formatEnum)
	cmds.setAttr('%s.parentTo'%globalCtrl, k = True)
	
	#-build nodal network for switching
	condNode_list = []
	parCon_list = []
	for i in range(len(parList)):
		parCon_list.append(cmds.parentConstraint(parList[i], globalCtrl_grp, mo = True)[0])
		condNode_list.append(cmds.createNode('condition', n = '%s_parentTo_%i_cond'%(propObj[:-4], i)))
		cmds.setAttr('%s.secondTerm'%condNode_list[i], i)
		cmds.connectAttr('%s.parentTo'%globalCtrl, '%s.firstTerm'%condNode_list[i], f = True)
		for n in ['R','G','B']:
			cmds.setAttr('%s.colorIfFalse%s'%(condNode_list[i], n), 0)
			cmds.setAttr('%s.colorIfTrue%s'%(condNode_list[i], n), 1)
		cmds.connectAttr('%s.outColor.outColorR'%condNode_list[i], '%s.%sW%i'%(parCon_list[i], parList[i], i), f = True)