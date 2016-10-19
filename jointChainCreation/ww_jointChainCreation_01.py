#Joint Chain creation script
#easily and painlessly create joint chains that are named, numbered, and oriented exactly how you would like them to be.
#created by Wesley Wilson on 03/16/15

'''
how to:
    1. run script, opening GUI
    2. specify the facing angle for the joints (usually X), the number of joints wanted, and the naming convention to be used
    3. create locators, then place them were you want those corresponding joints
    DON'T freeze transforms or center pivots of locators!
    4. once happy with locator placement, simply click the joint creation button
    5. for MORE joint chains, close script and relaunch.
'''
import maya.cmds as cmds
radioBoxAnn='Select the facing angle for your joint chain.'
intGrpAnn='Input the amount of joints you would like to create.'
textFieldAnn='Input the base name to be used in this joint chain.'

#locator creation function.  Also creates aim constraints for the locators.
def createLoc_cmd(*args):
    updatedJntName=cmds.textFieldGrp('inputName_grp',q=True,tx=True)
    updatedInptVal=cmds.intFieldGrp('inputValue_grp',q=True,value1=True)
    facingQuery=cmds.radioButtonGrp('inputFacing_grp',q=True,sl=True)
    #determines facing angle from radiobox
    if facingQuery==1:
        boxValue=[1,0,0]
    elif facingQuery==2:
        boxValue=[0,1,0]
    elif facingQuery==3:
        boxValue=[0,0,1]
    #create locators and turn on local rotation axis
    for i in range(updatedInptVal):
        locTransOffset=i*2
        makeLoc=cmds.spaceLocator(n=updatedJntName+'_loc%02i'%(i+1),a=True)
        cmds.move(locTransOffset,0,0,r=True)
        cmds.select(makeLoc)
        cmds.toggle(la=True) 
    #aim constraint creation
    for i in range (updatedInptVal):
        try:
            cmds.aimConstraint(updatedJntName+'_loc%02i'%(i+2),updatedJntName+'_loc%02i'%(i+1),aim=boxValue)
        except ValueError as ve:
            print ve
  
#joint creation function.  Also deletes the locators and creates a proper hierarchy for the joints.
def createJnt_cmd(*args):
    cmds.select(clear=True)
    updatedJntName=cmds.textFieldGrp('inputName_grp',q=True,tx=True)
    updatedInptVal=cmds.intFieldGrp('inputValue_grp',q=True,value1=True)
    for i in range(updatedInptVal):
        try:
            cmds.select(updatedJntName+'_loc%02i'%(i+1),add=True)
        except ValueError as ve:
            print ve
    locSel=cmds.ls(sl=True)
    #grabs the translate and rotate values from each locator and stores them into variables
    for i in range(len(locSel)):
        cmds.select(locSel[i])
        recordLocTX=cmds.getAttr(locSel[i]+'.translateX')
        recordLocTY=cmds.getAttr(locSel[i]+'.translateY')
        recordLocTZ=cmds.getAttr(locSel[i]+'.translateZ')
        recordLocRX=cmds.getAttr(locSel[i]+'.rotateX')
        recordLocRY=cmds.getAttr(locSel[i]+'.rotateY')
        recordLocRZ=cmds.getAttr(locSel[i]+".rotateZ")
        cmds.select(clear=True)
        #make dem joints
        cmds.joint(n=updatedJntName+'_%02i_jnt'%(i+1),p=(recordLocTX,recordLocTY,recordLocTZ),o=(recordLocRX,recordLocRY,recordLocRZ))
        cmds.select(locSel[i])
    cmds.select(clear=True)
    #parents the joints properly
    for i in range(updatedInptVal):
        try:
            jntSel=cmds.select(updatedJntName+'_%02i_jnt'%(i+1),add=True)
        except ValueError as ve:
            print ve
    currentSelJnt=cmds.ls(sl=True)
    invertCurrentSelJnt= currentSelJnt[::-1]
    for i in range(updatedInptVal):
        try:
            jntParent=cmds.parent(invertCurrentSelJnt[i],invertCurrentSelJnt[i+1])
        except ValueError as ve:
            print ve
        except IndexError as ie:
            print ie
    #deletes locators.  We won't need them anymore.
    cmds.select(locSel)
    cmds.delete()
    
#prevents duplicate windows from popping up    
if cmds.window('jointMaker',exists=True):
    cmds.deleteUI('jointMaker',window=True)
    
#creates UI stuff
cmds.window('jointMaker',title='joint Chain Maker')
cmds.rowColumnLayout(numberOfRows=7,p='jointMaker')
cmds.radioButtonGrp('inputFacing_grp',label='Facing axis', labelArray3=['X', 'Y', 'Z'], numberOfRadioButtons=3,ann=radioBoxAnn)
cmds.intFieldGrp('inputValue_grp',numberOfFields=1, label='Number of joints to make',value1=3,ann=intGrpAnn)
cmds.textFieldGrp('inputName_grp', label='Name for joint chain  ',pht="ex: R_arm",ann=textFieldAnn)
cmds.button('makeLocs',label='create locators',c=createLoc_cmd)
cmds.button('makeJnts',label='create joint chain',c=createJnt_cmd)

#spawns the hell beast.
cmds.showWindow('jointMaker')