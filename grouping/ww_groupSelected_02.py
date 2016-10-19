'''

Grouping Tool [oGRP]

Instructions: This will group selected objects twice.  Once under a locator and then the locator under a group.

'''

import maya.cmds as mc

selObj = mc.ls(sl=True)

for all in selObj:
    grp = mc.group(em=True)
    loc = mc.spaceLocator()
    mc.setAttr(loc[0]+".localScaleX",0.001)
    mc.setAttr(loc[0]+".localScaleY",0.001)
    mc.setAttr(loc[0]+".localScaleZ",0.001)
    
    rnm_grp = mc.rename(grp, all + "_grp")
    rnm_loc = mc.rename(loc,all + "_loc")
    
    mc.parent(rnm_grp, all)
    
    mc.setAttr(rnm_grp + ".tx", 0)
    mc.setAttr(rnm_grp + ".ty", 0)
    mc.setAttr(rnm_grp + ".tz", 0)
    mc.setAttr(rnm_grp + ".rx", 0)
    mc.setAttr(rnm_grp + ".ry", 0)
    mc.setAttr(rnm_grp + ".rz", 0)
    
    mc.parent(rnm_loc, all)
    
    mc.setAttr(rnm_loc + ".tx", 0)
    mc.setAttr(rnm_loc + ".ty", 0)
    mc.setAttr(rnm_loc + ".tz", 0)
    mc.setAttr(rnm_loc + ".rx", 0)
    mc.setAttr(rnm_loc + ".ry", 0)
    mc.setAttr(rnm_loc + ".rz", 0)
    
    mc.delete(mc.parentConstraint(all, rnm_grp))
    
    mc.delete(mc.parentConstraint(all, rnm_loc))
    
    mc.parent(rnm_grp, w=True)
    
    mc.parent(rnm_loc, w=True)
    
    mc.parent(all, rnm_loc)
    
    mc.parent(rnm_loc, rnm_grp)
    
    mc.makeIdentity(rnm_loc, apply=True, t=True, r=True, s=True)