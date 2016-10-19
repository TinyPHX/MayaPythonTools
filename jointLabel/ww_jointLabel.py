# finds all the joints in the scene and turns on their labels.  The label is the name of the joint.  This will help when skinning.
import maya.cmds as cmds
currentSel = cmds.ls(type='joint')
for i in range(len(currentSel)):
    cmds.setAttr(currentSel[i]+'.type',18)
    cmds.setAttr(currentSel[i]+'.otherType','%s   \n   \n'%(currentSel[i]),type='string')
    cmds.setAttr(currentSel[i]+'.drawLabel',1)