""""
button @ rig
""""

import maya.cmds as cmds

from ..base import module
from ..base import control

from ..utils import joint
from ..utils import name

def build(
			attachFace,
			buttonObject,
			prefix = 'button',
			rigScale = 1.0,
			baseRig = None
			):
			
	"""
	@param attachFace: str, the face to attach the attach object to
	@param buttonObject: str, the attach object
	@param prefix: str, prefix to name new objects
	@param rigScale: float, scale factor for size of controls
	@param baseRig: baseRig: instance of base.module.Base class
	@return: dictionary with rig module objects
	"""
	
	# make rig module
	rigmodule = module.Module(prefix = prefix, baseObj = baseRig)
	
	#make attach groups
	#bodyAttachGrp = cmds.group(name=prefix + 'BodyAttach_grp', em = 1, p = rigmodule.topGrp)
	#baseAttachGrp = cmds.group(name=prefix + 'BaseAttach_grp', em = 1, p = rigmodule.topGrp)
	
	#make attach joints
	attachJoints = []
	
	for i in range(2):
		newJoint = cmds.joint(n = buttonObject + '_attach_%02i_jnt' %(i+1), rad = rigScale)
		attachJOints.append(newJoint)
		
	# attach joints to attach objects via skincluster
	cmds.skinCluster(attachJoints[1], buttonObject, tsb = True)
	
	# make controls
	attachCtrl = control.Control(prefix = prefix + "_01", translateTo = attachJoints[1], scale = rigScale, parent = rigmodule.topGrp, shape = 'circleY', lockChannels = [])
	
	#get the geo associated with the attach face object
	attachFace_geo = attachFace.split('.')[0]
	
	#follicle creation and crap node removal
	cmds.select(attachFace)
	mel.eval("createHair 1 8 2 0 0 0 0 0 0 1 2 2;")
	removalList = ['nucleus1', 'pfxHair1', 'hairSystem1']
	
	attachFace_geo_shape = cmds.listRelatives(attachFace_geo)[0]
	attachedFollicles = cmds.listConnections(attachFace_geo_shape + '.worldMatrix')
	
	follicleGrp = cmds.listRelatives(attachedFollicles[0] ,p = True)
	
	for item in removalList:
		if(item in cmds.ls()):
			cmds.delete(item)
			
	#attach controls to joints
	cmds.parentConstriant(attachCtrl.C, attachJoints[1] , mo = True)
	
	#attach joints to follicle
	cmds.parentConstraint(attachedFollicles[0], attachJoints[0], mo = False)
	
	#clean up
	cmds.parent(attachJoints[0], parts.jntsGrp)
	cmds.parent(attachCtrl.Off, parts.controlsGrp)
	cmds.parent(follicleGrp, parts.jntsGrp)
	
	
	return {'module':rigmodule}
	#return {'module':rigmodule, 'baseAttachGrp':baseAttachGrp, 'bodyAttachGrp':bodyAttachGrp}
	
	