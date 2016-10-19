#the selection order should be [face, attach object]
#the attach object should be ONTOP of the grid at center of world with clean trans and rots
#the attach object should also be FACING up (+y)

currentSel = cmds.ls(sl=True)

theFace = currentSel[0]
theAttachObject = currentSel[1]

#get the geo associated with theFace
theFace_geo = currentSel[0].split('.')[0]

#deselect everything to start the joint creation
cmds.select(cl=True)

newJoints = []
for i in range(2):
    newJoint = cmds.joint(n = theAttachObject + '_attach_%02i_jnt' %(i+1), rad = 0.2)
    newJoints.append(newJoint)

#attach joint to attach object
cmds.skinCluster(newJoints[1], theAttachObject, tsb = True)

theControl = cmds.circle(n = newJoints[1] + '_ctrl', ch = False, radius = 0.5, nr=(0, 1, 0))[0]
theControl_grp = cmds.group(n = newJoints[1] + '_ctrl_grp')

cmds.parentConstraint(newJoints[0], theControl_grp, mo = True)
cmds.parentConstraint(theControl, newJoints[1], mo = True)

#make follicle from the selected face and remove the CRAP noone needs :)
cmds.select(theFace)
mel.eval("createHair 1 8 2 0 0 0 0 0 0 2 1 2;")
removalList = ["nucleus1", "pfxHair1", "hairSystem1"]

for item in removalList:
    if(item in cmds.ls()):
        cmds.delete(item)

# parent constraining the follicles to the newly made joints
faceGeo_shape = cmds.listRelatives(theFace_geo)[0]
attachedFollicles = cmds.listConnections(faceGeo_shape + '.worldMatrix')       

cmds.parentConstraint(attachedFollicles[0], newJoints[0], mo = False)