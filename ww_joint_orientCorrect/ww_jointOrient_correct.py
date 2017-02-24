#reorient joints
#this script assumes you have a hierarchy of joints that are all @ 0 rotations with really messed up orients.
#it further assumes all the joints are exactly where they need to be.

#to use - select the root joint in the hierarchy and grab all children joints using "select hierarchy"
'''
record old jnt's joint orient
make new empty group and snap it to the old jnt, paste the old jnt's joint orient vals into the rots of the new grp
make a new joint and parent it to new grp.  0 the trans and rots of the new jnt.
unparent new joint and delete the empty grp
parent to the correct parent joint.  
'''

currentSel = cmds.ls(sl=True)
for i in range(len(currentSel)):
    jnt_oX = cmds.getAttr('%s.jointOrientX' %currentSel[i])
    jnt_oY = cmds.getAttr('%s.jointOrientY' %currentSel[i])
    jnt_oZ = cmds.getAttr('%s.jointOrientZ' %currentSel[i])
    jnt_rad = cmds.getAttr('%s.radius' %currentSel[i])
    jnt_parJnt = cmds.listRelatives(currentSel[i], p = True)[0]
    
    newGrp = cmds.group(em = True)
    newJnt = cmds.joint(rad = (jnt_rad + 0.5), n = currentSel[i][:-4] + '_NEWjnt')
    
    '''
    for each in [currentSel[i], newJnt]:
        cmds.setAttr(each + '.displayLocalAxis', 1)
    '''
    
    cmds.delete(cmds.pointConstraint(currentSel[i], newGrp, mo = False))
    cmds.setAttr('%s.rotateX'%newGrp, jnt_oX)
    cmds.setAttr('%s.rotateY'%newGrp, jnt_oY)
    cmds.setAttr('%s.rotateZ'%newGrp, jnt_oZ)
    
    cmds.parent(newJnt ,w=True)
    cmds.delete(newGrp)
    
    if jnt_parJnt[-4:] == '_jnt':
        cmds.parent(newJnt, jnt_parJnt[:-4] + '_NEWjnt')



