import maya.cmds as cmds
import maya.mel as mel

#helper function
def CleanRemove(object):
    if(object in cmds.ls()):
        cmds.delete(object)

#build ribbon rig function
def MakeRibbon(name, numU, numV, numCtrls):
	#all the groups for cleanup
	ribbonJntsGrp = cmds.group(em = True, n = name + '_ribbon_jnts_grp')
	ribbonMeshGrp = cmds.group(em = True, n = name + '_ribbon_geo_grp')
	ribbonCtrlsGrp = cmds.group(em = True, n = name + '_ribbon_ctrls_grp')
	ribbonMasterGrp = cmds.group(em = True, n = name + '_ribbon_grp')
	
	for grp in [ribbonJntsGrp, ribbonMeshGrp, ribbonCtrlsGrp]:
		cmds.select(grp)
		cmds.parent(grp, ribbonMasterGrp)
		
	newNurbsSurface = cmds.nurbsPlane(n = name, ax = (0,1,0), w = numU, lr = numV, d = 3, u = numU, v = numV, ch = False)[0]
	cmds.parent(newNurbsSurface, ribbonMeshGrp)
	cmds.select(newNurbsSurface)
	mel.eval("createHair %s %s 2 0 0 0 0 5 0 1 1 1;" %(numU, numV))
	
	#remove extra crap
	removalList = ['nucleus1', 'pfxHair1','hairSystem1']
	
	for i in range(numV):
		removalList.append("curve%i" %(i + 1))
		
	for item in removalList:
		CleanRemove(item)
		
	#get the follicles associated with this nurbs surface
	nurbsShape = cmds.listRelatives(newNurbsSurface)[0]
	attachedFollicles = cmds.listConnections(nurbsShape + '.worldMatrix')
	
	#find and rename follocle's group, then stash it in the jnts grp
	cmds.select(attachedFollicles[0])
	follicleGrp = cmds.listRelatives(ap = True)[0]
	new_follicleGrp = cmds.rename(follicleGrp, name + '_follicle_grp')
	cmds.parent(new_follicleGrp, ribbonJntsGrp)
	
	for i in range(len(attachedFollicles)):
		follicle = cmds.rename(attachedFollicles[i], name + '_%02i_follicle' %(i+1))
		cmds.select(follicle)
		follicleJnt = cmds.joint(n = name + '_%02i_follicle_jnt' %(i+1), rad = 0.6)
		
	#make control joints
	cmds.select(cl = True)
	jntList = []
	for i in range(numCtrls):
		newJnt = cmds.joint(n = name + 'skin_%02i_jnt'%(i + 1), rad = 1)
		jntList.append(newJnt)
		cmds.parent(newJnt, ribbonJntsGrp)
		if i == 0:
			cmds.move((numV/2), z = True)
		if i == (numCtrls - 1):
			cmds.move(-(numV/2), z = True)
		cmds.hide(newJnt)
		cmds.select(cl=True)
		
	#move the rest of the joints to their new spots
	denomerator = float(len(jntList) - 1)
	for i in range(len(jntList)):
		if (i > 0) & (i < (len(jntList) - 1)):
			numerator = float(i)
			cmds.pointConstraint(jntList[0], jntList[i], mo = False)
			cmds.pointConstraint(jntList[-1], jntList[i], mo = False)
			cmds.setAttr(jntList[i] + "_pointConstraint1." + jntList[0] + "W0", (1 - (numerator/denomerator)))
			cmds.setAttr(jntList[i] + "_pointConstraint1." + jntList[-1] + "W1", (numerator/denomerator))
			cmds.delete(jntList[i] + "_pointConstraint1")
			
	#grab all the joints and skin them to the surface. this is the magic.
	cmds.select(jntList)
	cmds.select(newNurbsSurface, add = True)
	
	skin = cmds.skinCluster(n = name + '_ribbon_skinCluster', mi = 3, dr = 6, tsb = True, sm = 1)[0]
	
	#make some control objects for the joints
	cubePoints = [(0.5, -0.5, 0.5), (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5)]
	
	for i in range(len(jntList)):
		cmds.curve(d = 1, p = cubePoints)
		cubeCtrl = cmds.ls(sl = True)[0]
		ctrlObject = cmds.rename(cubeCtrl, name + '_%02i_ctrl'%(i+1))
		grp = cmds.group(ctrlObject)
		ctrlObject_grp = cmds.rename(grp, name + '_%02i_ctrl_grp'%(i+1))
		cmds.parent(ctrlObject_grp, ribbonCtrlsGrp)
		#move into position
		cmds.delete(cmds.pointConstraint(jntList[i], ctrlObject_grp, mo = False))
		#establish connection
		cmds.parentConstraint(ctrlObject, jntList[i], mo = True)
		
	#make master control for placement, shoudl not be used for actual deformations
	masterCtrl = cmds.circle()[0]
	new_masterCtrl = cmds.rename(masterCtrl, name + '_ribbon_master_ctrl')
	masterCtrlGrp = cmds.group(new_masterCtrl, n = new_masterCtrl + '_grp')
	cmds.move(0,0,-(numV/2))
	cmds.parent(masterCtrlGrp, ribbonMasterGrp)
	
	cmds.parentConstraint(new_masterCtrl, ribbonCtrlsGrp, mo = True)