#make IK match what FK is
#make skin joints temporarily drive position of the end and beginning of chain.  do the middle manually - for now.

#select FK controller with '01' number

#Given current selection, find and place in list all FK controls related to current selection
#cmds.select('R_armFK_01_ctrl')
currentSel = cmds.ls(sl=True)[0]
FK_ctrls=[]
for i in range(10):
    tryNum = currentSel.replace('_01_','_%02i_'%i)

    try:
        cmds.select(tryNum)
        FK_ctrls.append(cmds.ls(sl=True)[0])
    except ValueError as ve:
        print ve

#given all the IK control curves, find all the FK control curves using the IK control curves name as a starting point
IK_ctrls=[]
for i in FK_ctrls:
    switchIKFK = i.replace('FK_','IK_')
    IK_ctrls.append(switchIKFK)

# select first and last FK controls and then make IK controls match placement.    
for i in range(len(FK_ctrls)):
    if i != 1:    
        cmds.select(FK_ctrls[i])
        getRot = cmds.xform(q=True,ro=True)
        getTrans = cmds.xform(q=True,t=True,ws=True)
        cmds.select(IK_ctrls[i])
        cmds.xform(ro=(getRot[0],getRot[1],getRot[2]))
        cmds.xform(t=(getTrans[0],getTrans[1],getTrans[2]),ws=True)