#make FK match what IK is
#This takes the skin joints' worldspace translates and local rotations and then appklies them to the appropriate FK controls
#thus snapping the FK controls to the skin joints' current location.  This is the same location as the IK joints. 

#select the Ik controller with '01' as its number.

  
import maya.cmds as cmds
#given the current selection, grab all of the IK control curves and put them into a list
#cmds.select('R_armIK_01_ctrl')
currentSel = cmds.ls(sl=True)[0]
IK_ctrls=[]
for i in range(10):
    tryNum = currentSel.replace('_01_','_%02i_'%i)

    try:
        cmds.select(tryNum)
        IK_ctrls.append(cmds.ls(sl=True)[0])
    except ValueError as ve:
        print ve

#given all the IK control curves, find all the bind joints using the IK control curves name as a starting point
bind_jnts=[]
for i in IK_ctrls:
    ikRemove = i.replace('IK_','_')
    makeJnt = ikRemove.replace('_ctrl','_jnt')
    bind_jnts.append(makeJnt)

#given all the IK control curves, find all the FK control curves using the IK control curves name as a starting point
FK_ctrls=[]
for i in IK_ctrls:
    switchIKFK = i.replace('IK_','FK_')
    FK_ctrls.append(switchIKFK)

#take the bind joint rotates (and in one instance the IK curves translates) and apply them to the FK curves
for i in range(len(bind_jnts)):
    cmds.select(bind_jnts[i])
    getRot = cmds.xform(q=True,ro=True)
    if i == 0:
        cmds.select(IK_ctrls[i])
        getTrans = cmds.xform(q=True,t=True)
    cmds.select(FK_ctrls[i])
    cmds.xform(ro=(getRot[0],getRot[1],getRot[2]))
    if i == 0:
        cmds.xform(t=(getTrans[0],getTrans[1],getTrans[2]))