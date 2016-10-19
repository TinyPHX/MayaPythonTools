#offset grouping script
#select everything you want to have grouped.  change the groupTwice variable to get one or two groups
#NO FREEZE TRANSFORMS!!!
import maya.cmds as cmds

groupTwice = False

currentSel = cmds.ls(sl=True)

#single selection grouping function        
def superGroup(sel):
    makeNull = cmds.group(em = True, n = '%s_grp'%sel)
    cmds.parent(makeNull, sel)
    cmds.xform(t = (0,0,0), ro = (0,0,0))
    cmds.parent(w=True)
    cmds.parent(sel, makeNull)
    cmds.xform(t = (0,0,0), ro = (0,0,0))
            

#for everything in the current selection: run function with sel = currentSel[i]    
for sel in currentSel:
    superGroup(sel)
    
    #if groupTwice is set to True: make sel = the group that was just made and enter function again
    if groupTwice:
        cmds.select('%s_grp'%sel)
        sel = cmds.ls(sl=True)[0]
        
        superGroup(sel)
        
        cmds.select(currentSel)