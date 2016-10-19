import maya.cmds as cmds
currentSel = cmds.ls(sl=True)

for i in range(len(currentSel)):
    cmds.select(currentSel[i])
    findShape = cmds.listRelatives(shapes=True, f=True)[0]
    cmds.select(findShape)
    cmds.setAttr(findShape + ".primaryVisibility",0)
    cmds.setAttr(findShape + ".castsShadows",0)
    cmds.setAttr(findShape + ".visibleInReflections",0) 