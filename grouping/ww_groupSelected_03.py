#offset grouping script
#select everything you want to have grouped.  change the groupTwice variable to get one or two groups
#NO FREEZE TRANSFORMS!!!

import maya.cmds as cmds

groupTwice = True

currentSel = cmds.ls(sl=True)

for sel in currentSel:
    #make an empty group, parent it under sel, and set all its rots and trans to 0
    makeNull = cmds.group(em=True, n='%s_grp'%sel)
    cmds.parent(makeNull, sel)
    cmds.xform(t=(0,0,0), ro=(0,0,0))
    #unparent the empty group and parent sel under it, then set sel's rots and trans to 0
    cmds.parent(w=True)
    cmds.parent(sel,makeNull)
    cmds.xform(t=(0,0,0), ro=(0,0,0))
    
    #if groupTwice is set to True: perform the same thing using makeNull and another offset group
    if groupTwice:
        makeNullNull = cmds.group(em=True, n='%s_grp_grp'%sel)
        cmds.parent(makeNullNull, makeNull)
        cmds.xform(t=(0,0,0), ro=(0,0,0))
        #unparent the empty group and parent sel under it, then set sel's rots and trans to 0
        cmds.parent(w=True)
        cmds.parent(makeNull,makeNullNull)
        cmds.xform(t=(0,0,0), ro=(0,0,0))