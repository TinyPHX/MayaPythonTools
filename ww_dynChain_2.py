'''
Auto Dynamic Chain Rig
Created by Wes Wilson
Last modified on 3/23/2015
Loosely based on a tutorial by Lester Banks 
webAddress
http://lesterbanks.com/2014/02/building-dynamic-joint-chains-maya-hair/

Notes:
    -Makes use of MEL, since the make selected curve dynamic module can only be called in MEL, not python.  Yet.
    -To use, just click on shelf button to launch GUI.  
    -Before running make sure there are no naming issues in the code below.
    -For scale constraint: Scale constraint from the scale_controller to the non-skinned geo, and the entire joints group.
    
     
Known issues:
    -Code isn't exactly optimized. 
    
'''

import sys
import maya.cmds as cmds
import maya.mel as mel

def makeDynChain_cmd(*args):
    #renaming variables and the MAIN selection variable.
    #This is what the follicles and hair system nodes should be named on creation.
    currentFolName='follicle1'
    currentHairSysName='hairSystem1'
    currentOutCrvGrpName='hairSystem1OutputCurves'
    #searches for existing follicle nodes then seperates them from their Shape node to get a list of pre-existing nodes.
    follicle=cmds.ls('dynChain_*_foll')
    #checks the number of follicles already in the scene and sets the renumberValue variable accordingly
    if follicle:
        renumberValue=len(follicle)+1
    else:
        renumberValue=01
                
    #All these use the renumberValue defined previously
    hairSystemName='dynChain_%02d_hSys'%(renumberValue)
    follicleName='dynChain_%02d_foll'%(renumberValue)
    ikHandleName='dynChain_%02d_ik'%(renumberValue)
    effectorName='dynChain_%02d_eff'%(renumberValue)
    inCrvName='dynChain_in_%02d_crv'%(renumberValue)
    inCrvBlendShapeName=inCrvName+'_BS'
    bsNodeName=inCrvName+'_BSnode'
    outCrvName='dynChain_out_%02d_crv'%(renumberValue)
    clstrCtrlName='dynSecondary_%02d'%(renumberValue)
   
    #empty lists used to create the clusters and cluster controllers
    ctrlList=[]
    clusterList=[]

    #The starting point of the code.  Last joint selected first and base joint selected last.
    #Starts with some basic input queries.
    dynChainBehavRad=cmds.radioButtonGrp('dynChainBehavior',q=True,sl=True)
    rootJntInput=cmds.textFieldGrp('rootJntSelInput',q=True,tx=True)
    endJntInput=cmds.textFieldGrp('endJntSelInput',q=True,tx=True)
    if endJntInput:
        endOfChain=endJntInput
    else:
        cmds.select(rootJntInput)
        autoEndJnt=cmds.listRelatives(ad=True)
        endOfChain=autoEndJnt[0]
    attractCrvValRaw=cmds.intSliderGrp('attractCrvSlider',q=True,v=True)
    attractCrvVal=attractCrvValRaw*.01
    hierarchyOn=cmds.checkBox('hierarchyBoul',q=True,v=True)
    
    #Find Parent joint of root joint in dynamic Chain.  Then unparents the chain from the other joint heirarchy
    cmds.select(rootJntInput)
    jntParent=cmds.listRelatives(p=True)
    if jntParent:
        cmds.parent(rootJntInput,w=True)
    cmds.select(endOfChain)
    cmds.select(rootJntInput,add=True)
    
    #create spline IK chain
    cmds.ikHandle(n=ikHandleName,sol='ikSplineSolver',roc=True,cra=False,pcv=True,snc=False,ccv=True,scv=False,ns=1,rtm=False,tws='linear')
    #find all associated parts to IK just created
    cmds.select(ikHandleName)
    findCrv=cmds.listConnections()
    getCurve=filter(lambda x: 'curve' in x, findCrv)[0]
    cmds.delete(ikHandleName)
    
    #rename input crv and shape node
    cmds.select(getCurve)
    cmds.rename(inCrvName)
    cmds.select(inCrvName)
    getChild=cmds.listRelatives(c=True)
    
    #create duplicate of input CRV
    cmds.duplicate(inCrvName,n=inCrvBlendShapeName)
    
    #make input crv dynamic
    cmds.select(inCrvName)
    mel.eval('makeCurvesDynamic "2" { "0", "0", "1", "1", "0" };')
    
    #Clean up and attribute setting from previous steps.
    cmds.select(inCrvName)
    cmds.parent(inCrvName,w=True)
    cmds.select(currentFolName)
    findParent=cmds.listRelatives(p=True)
    cmds.parent(findParent[0],rootJntInput)
    parentObjTransX=cmds.getAttr(findParent[0]+'.tx')
    cmds.setAttr(findParent[0]+".tx", 0)
    parentObjTransY=cmds.getAttr(findParent[0]+'.ty')
    cmds.setAttr(findParent[0]+".ty", 0)
    parentObjTransZ=cmds.getAttr(findParent[0]+'.tz')
    cmds.setAttr(findParent[0]+".tz", 0)
    parentObjRotX=cmds.getAttr(findParent[0]+'.rx')
    cmds.setAttr(findParent[0]+".rx", 0)
    parentObjRotY=cmds.getAttr(findParent[0]+'.ry')
    cmds.setAttr(findParent[0]+".ry", 0)
    parentObjRotZ=cmds.getAttr(findParent[0]+'.rz')
    cmds.setAttr(findParent[0]+".rz", 0)
    cmds.parent(findParent[0], w=True)
    cmds.parent(inCrvName,rootJntInput)
    cmds.setAttr(inCrvName+".tx",parentObjTransX)
    cmds.setAttr(inCrvName+".ty",parentObjTransY)
    cmds.setAttr(inCrvName+".tz",parentObjTransZ)
    cmds.setAttr(inCrvName+".rx",parentObjRotX)
    cmds.setAttr(inCrvName+".ry",parentObjRotY)
    cmds.setAttr(inCrvName+".rz",parentObjRotZ)
    cmds.parent(inCrvName,currentFolName)
    cmds.parent(inCrvBlendShapeName,rootJntInput)
    cmds.setAttr(inCrvBlendShapeName+".tx",parentObjTransX)
    cmds.setAttr(inCrvBlendShapeName+".ty",parentObjTransY)
    cmds.setAttr(inCrvBlendShapeName+".tz",parentObjTransZ)
    cmds.setAttr(inCrvBlendShapeName+".rx",parentObjRotX)
    cmds.setAttr(inCrvBlendShapeName+".ry",parentObjRotY)
    cmds.setAttr(inCrvBlendShapeName+".rz",parentObjRotZ)
    cmds.parent(inCrvBlendShapeName,currentFolName)
    cmds.makeIdentity(findParent[0], apply=True, t=True, r=True, s=True)
    cmds.select(currentHairSysName)
    cmds.rename(hairSystemName)
    cmds.select(hairSystemName)
    hairSysNameShape=cmds.listRelatives(c=True)
    cmds.setAttr(hairSysNameShape[0]+".startCurveAttract",attractCrvVal)
    cmds.setAttr(hairSysNameShape[0]+".attractionScale[1].attractionScale_Position",1)
    cmds.setAttr(hairSysNameShape[0]+".attractionScale[1].attractionScale_FloatValue",0.8)
    cmds.select(inCrvName)
    cmds.select(currentFolName)
    cmds.rename(follicleName)
    cmds.select(findParent[0])
    cmds.rename(inCrvName + '_grp')
    cmds.select(currentOutCrvGrpName)
    cmds.rename(outCrvName + '_grp')
    findChild=cmds.listRelatives(c=True)
    cmds.select(findChild[0])
    cmds.rename(outCrvName)
    cmds.setAttr(follicleName+'.visibility',0)
    
    #select joints again, then output crv to make the final IK spline solver
    cmds.select(endOfChain)
    cmds.select(rootJntInput,add=True)
    cmds.select(outCrvName,add=True)
    cmds.ikHandle(n=ikHandleName,sol='ikSplineSolver',roc=False,cra=False,pcv=False,snc=False,ccv=False,scv=False,ns=1,rtm=False,tws='linear')
    #find effector to rename it
    findEff=cmds.listConnections()
    getEffector=filter(lambda x: 'effector' in x, findEff)[0]
    cmds.select(getEffector)
    cmds.rename(effectorName)
    
    #setting up Blendshape
    cmds.select(inCrvBlendShapeName)
    cmds.select(inCrvName,add=True)
    cmds.blendShape(n=bsNodeName,o='local')
    cmds.setAttr(bsNodeName+'.'+inCrvBlendShapeName,1)
    
    #creating clusters for every CV on the BScurve
    curveName=cmds.ls(sl=True)[0]
    cvs=cmds.getAttr(inCrvName+'.cp',s=1)
    for i in range(cvs):
        try:
            clsBsName=inCrvName+'_%d_clst'%(i+1)
            cmds.select(inCrvBlendShapeName+'.cv[%d]'%(i))
            cmds.cluster(n=clsBsName,rel=True)
            clstrName=cmds.ls(sl=True)[0]
            cmds.setAttr(clstrName+'.visibility',0)
            clusterList.append(cmds.ls(sl=True)[0])
            cmds.select(inCrvName)
        except TypeError as te:
            print te
        except ValueError as ve:
            print ve
            
    #creating and connecting controllers and groups for the clusters just created.
    dynChainCtrlsGrp=[]
    for i in range(len(clusterList)):
        clsBsCtrlName=clstrCtrlName+'_ctrl_%d'%(i+1)
        ctrlCrv=cmds.circle(n=clsBsCtrlName,o=True,ch=False,nr=(0,0,1),r=0.05)
        ctrlList.append(clsBsCtrlName)
        currentClstr=clusterList[i]
        grp=cmds.group(n=clsBsCtrlName+'_grp',em=True)
        ctrlsHierarchyList=dynChainCtrlsGrp.append(grp)
        cmds.parent(grp,currentClstr)
        cmds.setAttr(grp + ".tx", 0)
        cmds.setAttr(grp + ".ty", 0)
        cmds.setAttr(grp + ".tz", 0)
        cmds.setAttr(grp + ".rx", 0)
        cmds.setAttr(grp + ".ry", 0)
        cmds.setAttr(grp + ".rz", 0)
        cmds.delete(cmds.parentConstraint(currentClstr,grp))
        cmds.parent(grp, w=True)
        cmds.makeIdentity(grp, apply=True, t=True, r=True, s=True)
        cmds.delete(cmds.parentConstraint(grp,ctrlCrv,mo=False))
        cmds.parent(ctrlCrv,grp)
        cmds.makeIdentity(ctrlCrv, apply=True, t=True, r=True, s=True)
        cmds.parentConstraint(ctrlCrv,currentClstr)
        #if the controller is the first one
        if clsBsCtrlName==ctrlList[0]:
            cmds.setAttr(clsBsCtrlName+'.visibility',0)
            if jntParent:
                cmds.parentConstraint(jntParent[0],clsBsCtrlName,mo=True)
        #the rest of the created controllers
        else:
            cmds.parentConstraint(clusterList[0],grp,mo=True)
    
    #reparent joint heirarchy back into rig and make dynChain attach like the radio button tells us to
    if jntParent:
        cmds.parent(rootJntInput,jntParent[0])
    cmds.select(follicleName)
    findFollShape=cmds.listRelatives(c=True)
    cmds.setAttr(findFollShape[0]+'.pointLock',dynChainBehavRad)
    
    #for hierarchy ON conditions.  Checks the input fields that are turned on by this option being checked o nthe GUI.
    if hierarchyOn:
        ctrlGrpName=cmds.textFieldGrp('ctrlGrpSelInput',q=True,tx=True)
        jntGrpName=cmds.textFieldGrp('jntGrpSelInput',q=True,tx=True)
        dynChainCtrlsGrpLen=len(dynChainCtrlsGrp)
        clusterListLen=len(clusterList)
        for i in range(dynChainCtrlsGrpLen):
            cmds.parent(dynChainCtrlsGrp[i],ctrlGrpName)
        for i in range(clusterListLen):
            cmds.parent(clusterList[i],jntGrpName)
        cmds.parent(ikHandleName,jntGrpName)
        cmds.parent(inCrvName+'_grp',jntGrpName)
        grpsList=cmds.ls('*_grp')        
        hairSysGrp=filter(lambda x: 'hairSystem' in x, grpsList)
        #If a hairsystem group does not exist, create one.  This should eventually be parented under the main character's grp.
        if not hairSysGrp:
            cmds.group(n='hairSystem_grp',em=True)
        cmds.parent(outCrvName+'_grp','hairSystem_grp')
        cmds.parent(hairSystemName,'hairSystem_grp')
        findNuc=cmds.ls(type='nucleus')
        cmds.select(findNuc)
        checkNucParent=cmds.listRelatives(p=True)
        if not checkNucParent:
            for i in range(len(findNuc)):
                cmds.parent(findNuc[i],'hairSystem_grp')
                
    #After the chain is made, this updates the box in the GUI looking for the root joint to be baked
    #with the root joint from the dyn chain creation function.
    cmds.textFieldGrp('lastDynChainRootName',e=True,tx=rootJntInput)
    
    #output.
    sys.stdout.write('Dyn Chain created.  Click "bake" to bake.')

#baking dynamic Chain command
def bakeDynChain_cmd(*args):
    #some basic inupt queries.
    checkDisNuc=cmds.checkBox('nucleusDisableBoul',q=True,v=True)
    rootJntFieldInput=cmds.textFieldGrp('lastDynChainRootName',q=True,tx=True)
    endJntCheck=cmds.checkBox('goToEndBoul',q=True,v=True)
    endJntFieldInput=cmds.textFieldGrp('endJntSelInput',q=True,tx=True)
    
    #bakes joints from input joint to end joint that might also be input.
    if rootJntFieldInput:
        cmds.select(rootJntFieldInput)
        findChild=cmds.listRelatives(ad=True,type='joint')
        totalJoints=[rootJntFieldInput]+findChild
        cmds.select(totalJoints)
        if not endJntCheck:
            cmds.select(endJntFieldInput)
            checkEndChild=cmds.listRelatives(ad=True,type='joint')
            checkEndChildLen=len(checkEndChild)
            if checkEndChildLen >= 1:
                totalEndJoints=[endJntFieldInput]+checkEndChild
            else:
                totalEndJoints=[endJntFieldInput]
            newTotalJnts=[]
            for i in range(len(totalJoints)):
                if totalJoints[i] not in totalEndJoints:
                    newTotalJnts.append(totalJoints[i])
            cmds.select(newTotalJnts)
    cmds.bakeSimulation(t=(0,500))
    
    #if disable nucleus was turned on, this would disable the nucleus.            
    if checkDisNuc:
        findNuc=cmds.ls(type='nucleus')
        cmds.select(findNuc)
        cmds.setAttr(findNuc[0]+'.enable',0)
        
    #output.
    sys.stdout.write('Dyn Chain baked. Smells like cookies.')

#turn on hierarchy selection
def hierarchyOn_cmd(*args):
    cmds.textFieldGrp('ctrlGrpSelInput',e=True,ed=True)
    cmds.textFieldGrp('jntGrpSelInput',e=True,ed=True)

#turn off hierarchy selection
def hierarchyOff_cmd(*args):
    cmds.textFieldGrp('ctrlGrpSelInput',e=True,ed=False)
    cmds.textFieldGrp('jntGrpSelInput',e=True,ed=False)
        
#turn on end Joint selection
def endJntOn_cmd(*args):
    cmds.textFieldGrp('endJntSelInput',e=True,ed=True)
    
#turn off end Joint selection
def endJntOff_cmd(*args):
    cmds.textFieldGrp('endJntSelInput',e=True,ed=False)
    
#prevents duplicate windows from popping up    
if cmds.window('dynChainCreator',exists=True):
    cmds.deleteUI('dynChainCreator',window=True)
    
#output upon running script
sys.stdout.write('DynChain creator by Wesley Wilson. Input joint names and click "create" to create a DynChain.')
    
#creates UI stuff
cmds.window('dynChainCreator',title=' Dynamic Chain')
cmds.rowColumnLayout(numberOfRows=20,p='dynChainCreator')
cmds.intSliderGrp('attractCrvSlider',label='Follicle curve attract value',field=True,min=0,max=100,v=80)
cmds.textFieldGrp('rootJntSelInput', label='Select root dynamic joint',pht="ex: R_arm_01_jnt")
cmds.checkBox('goToEndBoul',label=' Go to end of joint chain?', align='center',v=True,ofc=endJntOn_cmd,onc=endJntOff_cmd)
cmds.textFieldGrp('endJntSelInput', label='Select end dynamic joint',pht="ex: R_arm_04_jnt",ed=False)
cmds.radioButtonGrp('dynChainBehavior',label='Dynamic Chain behavior', labelArray3=['tail', 'inverted tail', 'linked chain'], numberOfRadioButtons=3,sl=1)
cmds.checkBox('hierarchyBoul',label=' Clean up hierarchy?', align='center',onc=hierarchyOn_cmd,ofc=hierarchyOff_cmd)
cmds.textFieldGrp('ctrlGrpSelInput', label='Select controls group',pht="ex: char_ctrl_grp",ed=False)
cmds.textFieldGrp('jntGrpSelInput', label='Select joints group',pht="ex: char_jnt_grp",ed=False)
cmds.button('makeDynamicChain',label='create Dynamic Chain',c=makeDynChain_cmd)
cmds.textFieldGrp('lastDynChainRootName', label='Bake simulation from joint',pht="Displays the last created chain's root joint.")
cmds.checkBox('nucleusDisableBoul',label=' Disable nucleus after baking?', align='center',v=True)
cmds.button('bakeDynamicChain',label='bake Dynamic Chain',c=bakeDynChain_cmd)

#spawn window.
cmds.showWindow('dynChainCreator')