#Joint Chain creation script
#easily and painlessly create joint chains that are named, numbered, and oriented exactly how you would like them to be.
#created by Wesley Wilson on 03/16/15
#last modified on 06/11/2015

'''
how to:
    1. run script, opening GUI and creating locators for the start and end joints
    2. move the locators to where you want them, but do not orient them, this will be done automatically later.
    DON'T freeze transforms or center pivots of locators!
    3. specify the facing angle for the joints (usually X), the number of joints wanted, and the naming convention to be used
    4. create locators, then place them were you want those corresponding joints
    DON'T freeze transforms or center pivots of locators!
    5. if you want joints mirrored select appropriate box and define options for joint mirroring
    6. once happy with locator placement, simply click the joint creation button
    7. for MORE joint chains, close script and relaunch.

to do:
    -make an IK option. using simple IKRP, maybe a spline IK in later builds...
    -make an IK/FK switching rig, with all appropriate setups needed for that.
    -make stretchy IK rig.
    -Automatic controller creation, maybe even auto constraining?  
     Would probably need a slider to control scale of controllers.  
     Maybe the scale operation happens on all the 
     joints you have selected.  And ONLY them. 
    '''
import maya.cmds as cmds
from sys import stdout
radioBoxAnn='Select the facing angle for your joint chain.'
intGrpAnn='Input the total amount(incluing the root and end) of joints you would like to create.'
textFieldAnn='Input the base name to be used in this joint chain.'
mirrorBoulAnn='Click to mirror joints on creation.  Enables or Disables options below.'
mirrorAxisAnn='Select the mirror axis for your joint chain.'
mirrorFuncAnn='Select the mirror function for your joint chain.\nBehavior will reverse the rotation axis, so when you rotate it reverses the movement on the mirrored chain.\nOrientation will match the axis from the original side, effectively doing the opposite of behavior when rotating.'
globalJntsList=[]

#locator creation function.  Also creates aim constraints for the locators.
def createLoc_cmd(*args):
    locatorList=[]
    updatedJntName=cmds.textFieldGrp('inputName_grp',q=True,tx=True)
    updatedInptVal=(cmds.intFieldGrp('inputValue_grp',q=True,value1=True))-2
    facingQuery=cmds.radioButtonGrp('inputFacing_grp',q=True,sl=True)
    #determines facing angle from radiobox
    if facingQuery==1:
        boxValue=[1,0,0]
        invertBoxVal=[-1,0,0]
    elif facingQuery==2:
        boxValue=[0,1,0]
        invertBoxVal=[0,-1,0]
    elif facingQuery==3:
        boxValue=[0,0,1]
        invertBoxVal=[0,0,-1]
    #create inbetween locators and turn on local rotation axis
    renameRoot = cmds.rename(makeRoot,updatedJntName+'_loc01')
    locatorList.append(renameRoot)
    renameEnd = cmds.rename(makeEnd,updatedJntName+'_loc%02i'%(updatedInptVal+2))
    for i in range(updatedInptVal):
        locTransOffset=i*2
        makeLoc=cmds.spaceLocator(n=updatedJntName+'_loc%02i'%(i+2),a=True)
        locatorList.append(cmds.ls(sl=True)[0])
        cmds.select(makeLoc)
        cmds.toggle(la=True)
    locatorList.append(renameEnd)
    #simple math formula to determine the weighting to be used during the point constraint process
    weightOffset=[]
    for i in range(updatedInptVal+2):
        calc=i/(updatedInptVal+1.0)
        weightOffset.append(calc)
    #aim and point constraint creation, we will remove the point constraint after we create it
    for i in range (updatedInptVal+1):
        try:
            cmds.pointConstraint(locatorList[-1],updatedJntName+'_loc%02i'%(i+1),mo=False,w=weightOffset[i])
            cmds.pointConstraint(locatorList[0],updatedJntName+'_loc%02i'%(i+1),mo=False,w=(1-weightOffset[i]))
            cmds.pointConstraint(locatorList[0],locatorList[-1],updatedJntName+'_loc%02i'%(i+1),e=True,rm=True)
            cmds.aimConstraint(updatedJntName+'_loc%02i'%(i+2),updatedJntName+'_loc%02i'%(i+1),aim=boxValue)
        except ValueError as ve:
            print ve
        except RuntimeError as re:
            print re
    cmds.aimConstraint(locatorList[-2],locatorList[-1],aim=invertBoxVal)
    cmds.aimConstraint(locatorList[1],locatorList[0],aim=boxValue)
    stdout.write("Place locators then click 'create joint chain'")

#joint creation function.
def createJnt_cmd(*args):
    cmds.floatSliderGrp('jointScaleSlider',e=True,en=True)
    jntsList=[]
    updatedJntName=cmds.textFieldGrp('inputName_grp',q=True,tx=True)
    updatedInptVal=cmds.intFieldGrp('inputValue_grp',q=True,value1=True)
    mirrorCheck=cmds.checkBox('mirrorBoul',q=True,v=True)
    parentCheck=cmds.checkBox('parentBoul',q=True,v=True)
    cmds.select(clear=True)
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
        mirrorJntsList=[]
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
        
        for i in range(len(jntsList)):
            newInstance=jntsList[i].replace(checkMirrorNameSearch,checkMirrorNameReplace)
            mirrorJntsList.append(newInstance)
            
    
    #parenting functionality.    
    if parentCheck==True:
        parentObject=cmds.textFieldGrp('parentChain_grp',q=True,tx=True)
        if mirrorCheck==True:
            mirroredParentJnt=jntsList[0].replace(checkMirrorNameSearch,checkMirrorNameReplace)
            cmds.parent(mirroredParentJnt,parentObject)
        cmds.parent(jntsList[0],parentObject)
        
    #output on function completion.
    if parentCheck==True:
        if mirrorCheck==True:
            stdout.write("Joint chain created and mirrored with %i joints and parented under %s. \n"%(updatedInptVal,parentObject))
        else:
            stdout.write("Joint chain created with %i joints and parented under %s. \n"%(updatedInptVal,parentObject))
    elif mirrorCheck==True:
        stdout.write("Joint chain created and mirrored with %i joints. \n"%(updatedInptVal))
    else:
        stdout.write("Joint chain created with %i joints. \n"%(updatedInptVal))
    
    #updated joint list for use with radius control slider   
    for i in range(len(jntsList)):
        globalJntsList.append(jntsList[i])
    if mirrorCheck==True:    
        for i in range(len(mirrorJntsList)):
            globalJntsList.append(mirrorJntsList[i])
    
    return globalJntsList

#radius control Slider functionality
def jointScale_cmd(*args):
    radiusValue=cmds.floatSliderGrp('jointScaleSlider',q=True,v=True)
    for i in range(len(globalJntsList)):
        cmds.setAttr(globalJntsList[i]+".radius",radiusValue)
                  
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
    
#turn on the parenting options, you big baby.    
def ParentOn_cmd(*args):
    cmds.textFieldGrp('parentChain_grp',e=True,ed=True)
    
#turn off the parenting options, you rebel.    
def ParentOff_cmd(*args):
    cmds.textFieldGrp('parentChain_grp',e=True,ed=False)
    
#edit the scale of locators
def scaleLoc_cmd(*args):
    scaleValue=cmds.floatSliderGrp('locScaleSlider',q=True,v=True)
    locatorShapeList=cmds.ls(type="locator")
    for i in range(len(locatorShapeList)):
        cmds.select(locatorShapeList[i])
        locatorList=cmds.listRelatives(p=True)
        cmds.select(locatorList)
        cmds.xform(scale=(scaleValue,scaleValue,scaleValue))
        cmds.select(cl=True)

    
#prevents duplicate windows from popping up    
if cmds.window('jointCreator',exists=True):
    cmds.deleteUI('jointCreator',window=True)
  
#creates UI stuff
cmds.window('jointCreator',title='Joint Chain Creator')
cmds.rowColumnLayout(numberOfRows=20,p='jointCreator')
cmds.radioButtonGrp('inputFacing_grp',label='Facing axis', labelArray3=['X', 'Y', 'Z'], numberOfRadioButtons=3,ann=radioBoxAnn)
cmds.radioButtonGrp('inputFacing_grp',e=True,sl=1)
cmds.intFieldGrp('inputValue_grp',numberOfFields=1, label='Number of joints to make',value1=3,ann=intGrpAnn)
cmds.textFieldGrp('inputName_grp', label='Name for joint chain',pht="ex: R_arm",ann=textFieldAnn)
cmds.button('makeLocs',label='create locators',c=createLoc_cmd)
cmds.floatSliderGrp('locScaleSlider',field=True, label='scale locators', minValue=0, maxValue=10, fieldMinValue=-100, fieldMaxValue=100, value=1, cc=scaleLoc_cmd )
cmds.checkBox('mirrorBoul',label=' Mirror joint chain?', align='center',rs=True,onc=mirrorOn_cmd,ofc=mirrorOff_cmd,ann=mirrorBoulAnn)
cmds.radioButtonGrp('mirrorAxis',label='Mirror axis', labelArray3=['XY', 'YZ', 'XZ'], numberOfRadioButtons=3,ed=False,ann=mirrorAxisAnn)
cmds.radioButtonGrp('mirrorAxis',e=True,sl=2)
cmds.radioButtonGrp('mirrorFunc',label='Mirror by', labelArray2=['Behavior', 'Orientation'], numberOfRadioButtons=2,ed=False,ann=mirrorFuncAnn)
cmds.radioButtonGrp('mirrorFunc',e=True,sl=1)
cmds.textFieldGrp('mirrorNameSearch_grp', label='Search for',pht="ex: R_",ed=False)
cmds.textFieldGrp('mirrorNameReplace_grp', label='Replace with',pht="ex: L_",ed=False)
cmds.checkBox('parentBoul',label=' Parent joint chain?', align='center',rs=True,onc=ParentOn_cmd,ofc=ParentOff_cmd)
cmds.textFieldGrp('parentChain_grp', label='Parent chain under',pht="ex: ROOT_jnt",ed=False)
cmds.button('makeJnts',label='create joint chain',c=createJnt_cmd)
cmds.floatSliderGrp('jointScaleSlider',field=True, label='joint radius', minValue=0, maxValue=50, fieldMinValue=-100, fieldMaxValue=100, value=1 ,cc=jointScale_cmd ,en=False)


#makes the initial locators to be the start and end joints
makeRoot = cmds.spaceLocator(n='rootJoint_loc')
cmds.toggle(la=True)
cmds.move(1,0,0)
makeEnd = cmds.spaceLocator(n='endJoint_loc')
cmds.toggle(la=True)
cmds.move(-1,0,0)

#spawns the hell beast.
cmds.showWindow('jointCreator')
stdout.write("joint chain creator by Wesley Wilson.  Manipulate locators to beginning and end points, then specify parameters. \n")