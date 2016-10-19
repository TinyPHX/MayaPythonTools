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
removalList = ["nucleus1", "pfxHair1"]

#add any hair systems in the scene to the removalList
allHairSys_shapes = cmds.ls(type = 'hairSystem')
for each in allHairSys_shapes:
    hairSys_transList = cmds.listRelatives(each, p = True)
    if hairSys_transList:
        for every in hairSys_transList:
            removalList.append(every)
            

for item in removalList:
    if(item in cmds.ls()):
        cmds.delete(item)

# parent constraining the follicles to the newly made joints
faceGeo_shape = cmds.listRelatives(theFace_geo)[0]
attachedFollicles = cmds.listConnections(faceGeo_shape + '.worldMatrix')

#find the follicle we want
ourFollicle_list = []
for i in range(len(attachedFollicles)):
    ourFollicle_list.append(attachedFollicles[i])
    allConnections_trans =  cmds.listConnections(attachedFollicles[i] + '.translate')
    for each in allConnections_trans:
        if 'parentConstraint' in each:
            ourFollicle_list.remove(attachedFollicles[i])
            
cmds.parentConstraint(ourFollicle_list[0], newJoints[0], mo = False)