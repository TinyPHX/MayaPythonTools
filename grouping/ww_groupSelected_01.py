'''

Grouping Tool [oGRP]

Instructions: This will group selected objects.

'''

import maya.cmds as mc

selObj = mc.ls(sl=True)

for all in selObj:
    grp = mc.group(em=True)
    
    rnm_grp = mc.rename(grp, all + "_grp")
    
    mc.parent(rnm_grp, all)
    
    mc.setAttr(rnm_grp + ".tx", 0)
    mc.setAttr(rnm_grp + ".ty", 0)
    mc.setAttr(rnm_grp + ".tz", 0)
    mc.setAttr(rnm_grp + ".rx", 0)
    mc.setAttr(rnm_grp + ".ry", 0)
    mc.setAttr(rnm_grp + ".rz", 0)
    
    mc.delete(mc.parentConstraint(all, rnm_grp))
    
    mc.parent(rnm_grp, w=True)
    
    mc.parent(all, rnm_grp)
    
    mc.makeIdentity(all, apply=True, t=True, r=True, s=True)