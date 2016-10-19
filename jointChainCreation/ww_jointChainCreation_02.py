#Joint Chain creation script
#easily and painlessly create joint chains that are named, numbered, and oriented exactly how you would like them to be.
#created by Wesley Wilson on 03/16/15

'''
how to:
    1. run script, opening GUI
    2. specify the facing angle for the joints (usually X), the number of joints wanted, and the naming convention to be used
    3. create locators, then place them were you want those corresponding joints
    DON'T freeze transforms or center pivots of locators!
    4. if you want joints mirrored select appropriate box and define options for joint mirroring
    5. once happy with locator placement, simply click the joint creation button
    6. for MORE joint chains, close script and relaunch.
'''
import maya.cmds as cmds
from sys import stdout
radioBoxAnn='Select the facing angle for your joint chain.'
intGrpAnn='Input the amount of joints you would like to create.'
textFieldAnn='Input the base name to be used in this joint chain.'
mirrorBoulAnn='Click to mirror joints on creation.  Enables or Disables options below.'
mirrorAxisAnn='Select the mirror axis for your joint chain.'
mirrorFuncAnn='Select the mirror function for your joint chain.\nBehavior will reverse the rotation axis, so when you rotate it reverses the movement on the mirrored chain.\nOrientation will match the axis from the original side, effectively doing the opposite of behavior when rotating.'

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
    stdout.write("Place locators then click 'create joint chain'")
  
#joint creation function.  Also deletes the locators, can mirror with several options, and creates a proper hierarchy for the joints.
def createJnt_cmd(*args):
    jntsList=[]
    cmds.select(clear=True)
    updatedJntName=cmds.textFieldGrp('inputName_grp',q=True,tx=True)
    updatedInptVal=cmds.intFieldGrp('inputValue_grp',q=True,value1=True)
    mirrorCheck=cmds.checkBox('mirrorBoul',q=True,v=True)
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
        jntsList.append(cmds.ls(sl=True)[0])
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
    cmds.select(clear=True)
    
    #mirroring functionality.    
    if mirrorCheck==True:
        checkmirrorFunc=cmds.radioButtonGrp('mirrorFunc',q=True,sl=True)
        if checkmirrorFunc==2:
            mirrorBehav=False
        else:
            mirrorBehav=True
        checkMirrorAxis=cmds.radioButtonGrp('mirrorAxis',q=True,sl=True)
        if checkMirrorAxis==1:
            mirrorXYBoul=True
            mirrorYZBoul=False
            mirrorXZBoul=False
        elif checkMirrorAxis==2:
            mirrorXYBoul=False
            mirrorYZBoul=True
            mirrorXZBoul=False
        else:
            mirrorXYBoul=False
            mirrorYZBoul=False
            mirrorXZBoul=True
        checkMirrorNameSearch=cmds.textFieldGrp('mirrorNameSearch_grp',q=True,tx=True)
        checkMirrorNameReplace=cmds.textFieldGrp('mirrorNameReplace_grp',q=True,tx=True)
        cmds.select(jntsList[0])
        cmds.mirrorJoint(mxy=mirrorXYBoul,myz=mirrorYZBoul,mxz=mirrorXZBoul,mb=mirrorBehav,sr=(checkMirrorNameSearch,checkMirrorNameReplace))
        cmds.select(clear=True)
        stdout.write("Joint chain created and mirrored with %i joints."%(updatedInptVal))
    else:
        stdout.write("Joint chain created with %i joints."%(updatedInptVal))

                  
#turn on the mirroring options    
def mirrorOn_cmd(*args):
    cmds.radioButtonGrp('mirrorAxis',e=True,ed=True)
    cmds.radioButtonGrp('mirrorFunc',e=True,ed=True)
    cmds.textFieldGrp('mirrorNameSearch_grp',e=True,ed=True)
    cmds.textFieldGrp('mirrorNameReplace_grp',e=True,ed=True)

#turn off the mirroring options, you need to make up your mind.    
def mirrorOff_cmd(*args):
    cmds.radioButtonGrp('mirrorAxis',e=True,ed=False)
    cmds.radioButtonGrp('mirrorFunc',e=True,ed=False)
    cmds.textFieldGrp('mirrorNameSearch_grp',e=True,ed=False)
    cmds.textFieldGrp('mirrorNameReplace_grp',e=True,ed=False)
    
#prevents duplicate windows from popping up    
if cmds.window('jointCreator',exists=True):
    cmds.deleteUI('jointCreator',window=True)
    
#creates UI stuff
cmds.window('jointCreator',title='Joint Chain Creator')
cmds.rowColumnLayout(numberOfRows=10,p='jointCreator')
cmds.radioButtonGrp('inputFacing_grp',label='Facing axis', labelArray3=['X', 'Y', 'Z'], numberOfRadioButtons=3,ann=radioBoxAnn)
cmds.radioButtonGrp('inputFacing_grp',e=True,sl=1)
cmds.intFieldGrp('inputValue_grp',numberOfFields=1, label='Number of joints to make',value1=3,ann=intGrpAnn)
cmds.textFieldGrp('inputName_grp', label='Name for joint chain',pht="ex: R_arm",ann=textFieldAnn)
cmds.button('makeLocs',label='create locators',c=createLoc_cmd)
cmds.checkBox('mirrorBoul',label=' Mirror joint chain?', align='center',rs=True,onc=mirrorOn_cmd,ofc=mirrorOff_cmd,ann=mirrorBoulAnn)
cmds.radioButtonGrp('mirrorAxis',label='Mirror axis', labelArray3=['XY', 'YZ', 'XZ'], numberOfRadioButtons=3,ed=False,ann=mirrorAxisAnn)
cmds.radioButtonGrp('mirrorAxis',e=True,sl=2)
cmds.radioButtonGrp('mirrorFunc',label='Mirror by', labelArray2=['Behavior', 'Orientation'], numberOfRadioButtons=2,ed=False,ann=mirrorFuncAnn)
cmds.radioButtonGrp('mirrorFunc',e=True,sl=1)
cmds.textFieldGrp('mirrorNameSearch_grp', label='Search for',pht="ex: R_",ed=False)
cmds.textFieldGrp('mirrorNameReplace_grp', label='Replace with',pht="ex: L_",ed=False)
cmds.button('makeJnts',label='create joint chain',c=createJnt_cmd)

#spawns the hell beast.
cmds.showWindow('jointCreator')
stdout.write("joint chain creator by Wesley Wilson.")