import maya.cmds as cmds

'''
__seperate single joint chain into two and make ctrl jnts and mainIK and mainFK control chains__
take single in chain and duplicate, remove all "twist" jnts.  this will be our dupChainMain and should just be shoulder, elbow, and wrist
we need to seperate this single chain into two seperate chains at the midpoint (elbow jnt).
make a new jnt with the elbow jnt name but with a "B" or something
delete(orientConstraint(MO = false)) the new jnt to the joint before the old elbow in the chain (this should make it have the right orientation)
delete(pointConstraint(MO = false)) the new jnt to the old elbow jnt (this should place it at the elbow jnt with the proper orientation)
parent all the jnts under the old elbow to the new elbow
duplicate each of the chains and remove the middle joints from each chain (we should just have the first joint and the last joint in these new chains)
make ANOTHER duplicate off of these new chains you just made (dupChain1) and remove the child joint from the chain (leaving just the first jnt)
connectAttr tX tY tZ rY and rZ from dupChain1 to the duplicate you just made (dupChain2)

__create ikspline solvers for the seperated chains__
make the EP curves for the ikSpline solvers (each should have just two cv's)
google search "curve python maya" for more info on this
create ikSpline solver using these newly made curves and going from the beginning of each chain to the end of each chain
create clusters for each of the cv's of each of the newly made curves and parentConstraint them to dupChain1's jnts.
at the same spots as the clusters, we should make spaceLocators, then move them off by some arbitrary amount in +Y (0.5 or so)
use these new space locators as the object up aim points for the advanced twist on our newly made ikSpline solvers
('twist_end_loc.worldMatrix[0]' is already connected to 'ikHandle1.dWorldUpMatrixEnd')
starting locator gets parent constrained to dupChain2
ending locator gets parent constrained to the last chain of the dupChain1

__parenting and organizing__this part gets muddy__
if you are going to make an IK or FK version and the switching, that should go here.

dupChainMain[shoulder] controls upperarm's dupChain1[0] (parent Constraint)
dupChainMain[elbow] controls upperarm's dupChain1[-1] (parent Constraint)
dupChainMain[elbow] controls lowerarm's dupChain1_grp (parent Constraint)
dupChainMain[elbow] controls lowerarm's dupChain1[-1] (parent Constraint)
'''

inChain = ['test_arm_01_jnt','test_arm_01_twist_01_jnt','test_arm_01_twist_02_jnt','test_arm_02_jnt','test_arm_02_twist_01_jnt','test_arm_02_twist_02_jnt','test_arm_03_jnt']
inChainA = [] # seperated at elbow (A and B)
inChainB = []
dupChain_main = [] #final duplicated chain
upArm_dupChain_01 = [] #control the splineIk's
lowArm_dupChain_01 = []
upArm_dupChain_02 = '' #rotX offset jnt (the secret of the twist)
lowArm_dupChain_02 = ''
ikTwistA_loc_list = []
ikTwistB_loc_list = []
ikTwistA_clstr_list = []
ikTwistB_clstr_list = []
dupChain = [] #workspace


#make main dup chain
for i in range(len(inChain)):
    if not '_twist_' in inChain[i]:
        cmds.select(inChain[i])
        newJnt = cmds.joint(rad = 0.65)
        cmds.parent(w=True)
        dupChain.append(newJnt)
#rename and add to proper list
for i in range(len(dupChain)):
    cmds.select(dupChain[i])
    newNameJnt = cmds.rename('mainChain_arm_%02i_jnt' %(i+1))
    dupChain_main.append(newNameJnt)
#parent properly
for i in range(len(dupChain_main)):
    if not i == 0:
        cmds.parent(dupChain_main[i], dupChain_main[i-1])


#seperate skinned chain at the elbow
origElbow = inChain[len(inChain)/2]
cmds.select(origElbow)
origElbow_parent = cmds.listRelatives(p=True)[0]

#making newjoint at origelbow parent and then snapping it to origelbow
cmds.select(origElbow_parent)
newJnt = cmds.joint(rad = 0.5)  #interesting tidbit - this new joint is NOT part of the skinning...
newNameJnt = cmds.rename(origElbow[:-4] + 'A_jnt')
cmds.delete(cmds.pointConstraint(origElbow, newNameJnt, mo = False))

#reorganize hierarchy
cmds.select(origElbow)
cmds.parent(w=True)

#append names to new joint lists that we use from here on out
#upper
cmds.select(inChain[0])
inChainA = cmds.listRelatives(ad = True, type = 'joint')
inChainA.append(inChain[0])
inChainA.reverse()

#lower
cmds.select(origElbow)
inChainB = cmds.listRelatives(ad = True, type = 'joint')
inChainB.append(origElbow)
inChainB.reverse()

#make dupChain_01
#upper
dupChain = []
for i in range(len(inChainA)):
    if not '_twist_' in inChainA[i]:
        cmds.select(inChainA[i])
        newJnt = cmds.joint(rad = 0.3)
        cmds.parent(w=True)
        dupChain.append(newJnt)
#rename and add to proper list
for i in range(len(dupChain)):
    cmds.select(dupChain[i])
    newNameJnt = cmds.rename('twistCtrl_upper_%02i_jnt' %(i+1))
    upArm_dupChain_01.append(newNameJnt)
#parent properly, then group everything
upArm_dupChain_grp = cmds.group(n = 'twistCtrl_upper_jnt_grp', em = True)
for i in range(len(upArm_dupChain_01)):
    if i == 0:
        cmds.delete(cmds.parentConstraint(upArm_dupChain_01[i], upArm_dupChain_grp, mo = False))
        cmds.parent(upArm_dupChain_01[i], upArm_dupChain_grp)
    else:
        cmds.parent(upArm_dupChain_01[i], upArm_dupChain_01[i-1])
        
#lower
dupChain = []
for i in range(len(inChainB)):
    if not '_twist_' in inChainB[i]:
        cmds.select(inChainB[i])
        newJnt = cmds.joint(rad = 0.3)
        cmds.parent(w=True)
        dupChain.append(newJnt)
#rename and add to proper list
for i in range(len(dupChain)):
    cmds.select(dupChain[i])
    newNameJnt = cmds.rename('twistCtrl_lower_%02i_jnt' %(i+1))
    lowArm_dupChain_01.append(newNameJnt)
#parent properly, then group everything
lowArm_dupChain_grp = cmds.group(n = 'twistCtrl_lower_jnt_grp', em = True)
for i in range(len(lowArm_dupChain_01)):
    if i == 0:
        cmds.delete(cmds.parentConstraint(lowArm_dupChain_01[i], lowArm_dupChain_grp, mo = False))
        cmds.parent(lowArm_dupChain_01[i], lowArm_dupChain_grp)
    else:
        cmds.parent(lowArm_dupChain_01[i], lowArm_dupChain_01[i-1])
        
#make dupChain_02 and connect to the appriopriate joint
#upper
dupChain = []
cmds.select(upArm_dupChain_grp)
newJnt = cmds.joint(rad = 0.4)
dupChain.append(newJnt)
#rename and add to proper list
for i in range(len(dupChain)):
    cmds.select(dupChain[i])
    upArm_dupChain_02 = cmds.rename('twistCtrl_upper_%02i_aim_jnt' %(i+1))
#connect trans and rot values
cmds.connectAttr(upArm_dupChain_01[0] + '.ry', upArm_dupChain_02 + '.ry', f = True)
cmds.connectAttr(upArm_dupChain_01[0] + '.rz', upArm_dupChain_02 + '.rz', f = True)
cmds.connectAttr(upArm_dupChain_01[0] + '.tx', upArm_dupChain_02 + '.tx', f = True)
cmds.connectAttr(upArm_dupChain_01[0] + '.ty', upArm_dupChain_02 + '.ty', f = True)
cmds.connectAttr(upArm_dupChain_01[0] + '.tz', upArm_dupChain_02 + '.tz', f = True)

#lower
dupChain = []
cmds.select(lowArm_dupChain_grp)
newJnt = cmds.joint(rad = 0.4)
dupChain.append(newJnt)
#rename and add to proper list
for i in range(len(dupChain)):
    cmds.select(dupChain[i])
    lowArm_dupChain_02 = cmds.rename('twistCtrl_lower_%02i_aim_jnt' %(i+1))
#connect trans and rot values
cmds.connectAttr(lowArm_dupChain_01[0] + '.ry', lowArm_dupChain_02 + '.ry', f = True)
cmds.connectAttr(lowArm_dupChain_01[0] + '.rz', lowArm_dupChain_02 + '.rz', f = True)
cmds.connectAttr(lowArm_dupChain_01[0] + '.tx', lowArm_dupChain_02 + '.tx', f = True)
cmds.connectAttr(lowArm_dupChain_01[0] + '.ty', lowArm_dupChain_02 + '.ty', f = True)
cmds.connectAttr(lowArm_dupChain_01[0] + '.tz', lowArm_dupChain_02 + '.tz', f = True)

#create ikSpline locators and move them off in the +Y
offsetAmnt = 2

#upper
for i in range(len(upArm_dupChain_01)):
    newLoc = cmds.spaceLocator()[0]
    cmds.delete(cmds.parentConstraint(upArm_dupChain_01[i], newLoc, mo = False))
    newLoc_name = cmds.rename('twist_upper_%02i_loc' %(i+1))
    ikTwistA_loc_list.append(newLoc_name)
    cmds.move(0,offsetAmnt,0, relative = True)
    if i == 0:
        cmds.parentConstraint(upArm_dupChain_02, newLoc_name, mo = True)
    else:
        cmds.parentConstraint(upArm_dupChain_01[-1], newLoc_name, mo = True)

#lower
for i in range(len(lowArm_dupChain_01)):
    newLoc = cmds.spaceLocator()[0]
    cmds.delete(cmds.parentConstraint(lowArm_dupChain_01[i], newLoc, mo = False))
    newLoc_name = cmds.rename('twist_lower_%02i_loc' %(i+1))
    ikTwistB_loc_list.append(newLoc_name)
    cmds.move(0,offsetAmnt,0, relative = True)
    if i == 0:
        cmds.parentConstraint(lowArm_dupChain_02, newLoc_name, mo = True)
    else:
        cmds.parentConstraint(lowArm_dupChain_01[-1], newLoc_name, mo = True)
        
#make ikSpline curve and clusters

#upper
upperPos1 = cmds.xform(upArm_dupChain_01[0], q = 1, t = 1, ws = 1)
upperPos2 = cmds.xform(upArm_dupChain_01[-1], q = 1, t = 1, ws = 1)
upperIk_crv = cmds.curve(n = 'upper_arm_crv', d = 1, p = [upperPos1, upperPos2])
newClstr01 = cmds.cluster(upperIk_crv + '.cv[0]', n = 'upper_arm_01_clstr', bs = True)
newClstr02 = cmds.cluster(upperIk_crv + '.cv[1]', n = 'upper_arm_02_clstr', bs = True)
cmds.parentConstraint(upArm_dupChain_01[0], newClstr01, mo = True)
cmds.parentConstraint(upArm_dupChain_01[-1], newClstr02, mo = True)  
for item in [newClstr01[1], newClstr02[1]]:
    ikTwistA_clstr_list.append(item)
    
#lower
lowerPos1 = cmds.xform(lowArm_dupChain_01[0], q = 1, t = 1, ws = 1)
lowerPos2 = cmds.xform(lowArm_dupChain_01[-1], q = 1, t = 1, ws = 1)
lowerIk_crv = cmds.curve(n = 'lower_arm_crv', d = 1, p = [lowerPos1, lowerPos2])
newClstr01 = cmds.cluster(lowerIk_crv + '.cv[0]', n = 'lower_arm_01_clstr', bs = True)
newClstr02 = cmds.cluster(lowerIk_crv + '.cv[1]', n = 'lower_arm_02_clstr', bs = True)
cmds.parentConstraint(lowArm_dupChain_01[0], newClstr01, mo = True)
cmds.parentConstraint(lowArm_dupChain_01[-1], newClstr02, mo = True)
for item in [newClstr01[1], newClstr02[1]]:
    ikTwistB_clstr_list.append(item)
    
#make ik spline and attach twist locators

#upper
upperArm_ik = cmds.ikHandle(n = 'upper_armTwist_ik', sj = inChainA[0], ee = inChainA[-1], c = upperIk_crv, solver = 'ikSplineSolver', ccv = False)[0]
cmds.setAttr(upperArm_ik + '.dTwistControlEnable', 1)
cmds.setAttr(upperArm_ik + '.dWorldUpType', 2) #set to object start/end
cmds.connectAttr( ikTwistA_loc_list[0] + '.worldMatrix[0]', upperArm_ik + '.dWorldUpMatrix', f = True)
cmds.connectAttr( ikTwistA_loc_list[-1] + '.worldMatrix[0]', upperArm_ik + '.dWorldUpMatrixEnd', f = True)

#lower
lowerArm_ik = cmds.ikHandle(n = 'lower_armTwist_ik', sj = inChainB[0], ee = inChainB[-1], c = lowerIk_crv, solver = 'ikSplineSolver', ccv = False)[0]
cmds.setAttr(lowerArm_ik + '.dTwistControlEnable', 1)
cmds.setAttr(lowerArm_ik + '.dWorldUpType', 2) #set to object start/end
cmds.connectAttr( ikTwistB_loc_list[0] + '.worldMatrix[0]', lowerArm_ik + '.dWorldUpMatrix', f = True)
cmds.connectAttr( ikTwistB_loc_list[-1] + '.worldMatrix[0]', lowerArm_ik + '.dWorldUpMatrixEnd', f = True)

# attach to main dup chain
cmds.parentConstraint(dupChain_main[0], upArm_dupChain_01[0], mo = True)
cmds.parentConstraint(dupChain_main[1], upArm_dupChain_01[1], mo = True)
cmds.parentConstraint(dupChain_main[1], lowArm_dupChain_grp, mo = True)
cmds.parentConstraint(dupChain_main[-1], lowArm_dupChain_01[1], mo = True)