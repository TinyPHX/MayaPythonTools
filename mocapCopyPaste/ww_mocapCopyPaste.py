'''
Make this thing work for MOCAP animation and my autorig system.  it's TAIGHT.

to use:
    we assume you are working with mocap.  if not, then go away.  This is not for you.
    also we assume you have baked all the trans rot and scale keys for the duration of the aniamtion you want to work with.
    Also - the first frame must be a t-pose, the rest should be your mocap aniamtion
    select one joint in the rig, any joint will do, then name the file you want to export.
    click to export.
    
    in your aniamtion file, you must select all the FK controls on the rig you are workign with.
    load the tool again, then you go to the txt file you exported in the above steps
    on import, it will go through all your selections and apply the animation to the rig in a new anim layer set to override
    any aniamtion you do after this, you must do on a new aniamtion layer ontop of this layer.

future stuff:
    BLEGH
'''

#Pose Saver tool for Maya 
#by: Wesley Wilson on 11/25/2015
    

import maya.cmds as cmds
import json
import os

#prevents duplicate windows from popping up    
if cmds.window('poseSaver',exists=True):
    cmds.deleteUI('poseSaver',window=True)


#copy KeyFrames function
def copyPose(*args):
    
    # bake simulation (or assume it is already baked)
    
    # find anim duration (assumes you have anim starting at first frame and the all trans rot and scale keys were baked)
    checkObj = cmds.ls(sl=True)[0]
    print checkObj
    numKeys = cmds.keyframe(checkObj,at='translateX',q=True,kc=True)
    print numKeys
    animLen = int(cmds.keyframe('%s.translateX'%checkObj,time=((numKeys-1),numKeys),query=True)[0])
    
    #get all joints and curves into lists
    allJoints = cmds.ls(type = 'joint')
    allCurves = cmds.ls(sl=True)
    
    #this is what the file will be named
    poseName = cmds.textFieldGrp('poseName_grp',q=True,tx=True)
    
    #this is what we will be saving
    saveList = []
    frameJntSaveDict = {}
    frameCrvSaveDict = {}
    for frame in range(animLen + 1):
        frameSaveDict = {}
        cmds.currentTime(frame, e=True)
        for i in range(len(allJoints)):
            cmds.select(allJoints[i])
            getTrans = cmds.xform(q=True,t=True)
            getRots = cmds.xform(q=True,ro=True)
            getScales = cmds.xform(q=True,s=True,r=True)
            
            frameSaveDict[allJoints[i]] = getTrans + getRots + getScales
        
        for i in range(len(allCurves)):
            cmds.select(allCurves[i])
            getTrans = cmds.xform(q=True,t=True)
            getRots = cmds.xform(q=True,ro=True)
            getScales = cmds.xform(q=True,s=True,r=True)
            
            frameSaveDict[allCurves[i]] = getTrans + getRots + getScales
        saveList.append(frameSaveDict)
    
    #find current workpath
    prePath = cmds.workspace(q=True,dir=True)
    trimPath=prePath.find('/',41)
    dataPath = prePath[:trimPath] + '/data'
    folderPath = dataPath + '/poseSaves/'
    
    #check to see if folder already exists
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
        
    fullPath = folderPath + poseName + '.txt'
    
    toBeSaved = json.dumps(saveList, sort_keys=True, ensure_ascii=True, indent=2)
    f=open(fullPath, 'w')
    
    #the actual save
    f.write(toBeSaved)
    f.close()
        
        
#paste KeyFrames function
def pastePose(*args):
    #currentTime
    crntTime=cmds.currentTime(q=True)
    
    #slideAmount
    slideAmnt = cmds.intFieldGrp('slideTime_grp',q=True,v=True)[0]
    print slideAmnt
    
    #filePath
    fileTypes = '*.txt'
    fileName = cmds.fileDialog2(ds=2, fileFilter = fileTypes, fileMode=1, caption="Paste Pose",okc = 'Load')[0]
    print fileName
    
    #new animation layer to paste this stuff on
    cmds.animLayer('importAnimLayer',o = True, aso = True)
    
    #selection of things you want the pose pasted to
    currentSel = cmds.ls(sl=True)
    #find all joints in the scene
    allJnts = cmds.ls(type='joint')
    
    #create and populate controlsDict
    controlsDict = {}
    jntsDict={}
    for sel in currentSel:
        cmds.select(sel)
        for jnt in allJnts:
            findAttr = cmds.attributeQuery(jnt ,node = sel, ex=True, ln = True)
            if findAttr:
                controlsDict[findAttr] = sel #control object is the value and the joint its attached to is the key
                cmds.select(jnt)
                jntsDict[findAttr] = cmds.xform(q=True,t=True)
                
    
    #fullPath = prePath[:trimPath]+'//data/poseSaves/'+fileName+'.txt'
    if os.path.exists(fileName):
        #if the file at a specific path exists, then open it and attach information from it to variables
        f=open(fileName)
        dataFile = json.load(f)
        
        for num in range(len(dataFile)):
            cmds.currentTime(crntTime + num + 1, update = True, edit = True)
            for key in controlsDict:
                #load dictionary data using current selection as a key
                loadTrans = dataFile[num][key][0:3]
                loadRots = dataFile[num][key][3:6]
                loadScales = dataFile[num][key][6:9]
                
                #check that data against current transform values for that currentSel object
                cmds.select(controlsDict[key])
                checkTrans = cmds.xform(q=True,t=True)
                checkRots = cmds.xform(q=True,ro=True)
                checkScales = cmds.xform(q=True,s=True,r=True)
                
                XYZdict = {1:'X', 2:'Y', 3:'Z'}
                
                #change transform values to pasteValues recieved from text file if they don't match the current values
                for n in range(len(XYZdict)):
                    print 'setting key on %s.translate%s'%(controlsDict[key],XYZdict[n+1]) 
                    try:
                        #set keyFrame at current Time
                        #cmds.setKeyframe(currentSel[i] + '.%s%s'%(TRSdict[x+1],XYZdict[n+1]))
                        #change currentTime by offset variable amount
                        cmds.setAttr(controlsDict[key] + '.translate%s'%XYZdict[n+1],(loadTrans[n] - jntsDict[key][n]))
                        cmds.setKeyframe(controlsDict[key] + '.translate%s'%XYZdict[n+1],al = 'importAnimLayer')
                    except RuntimeError as re:
                        print re
                        
                #change rotate values to pasteValues recieved from text file if they don't match the current values
                for n in range(len(XYZdict)):
                    print 'setting key on %s.rotate%s'%(controlsDict[key],XYZdict[n+1]) 
                    try:
                        #set keyFrame at current Time
                        #cmds.setKeyframe(currentSel[i] + '.%s%s'%(TRSdict[x+1],XYZdict[n+1]))
                        #change currentTime by offset variable amount
                        cmds.setAttr(controlsDict[key] + '.rotate%s'%XYZdict[n+1],loadRots[n])
                        cmds.setKeyframe(controlsDict[key] + '.rotate%s'%XYZdict[n+1],al = 'importAnimLayer')
                    except RuntimeError as re:
                        print re
                        
                #change scale values to pasteValues recieved from text file if they don't match the current values
                for n in range(len(XYZdict)):
                    print 'setting key on %s.scale%s'%(controlsDict[key],XYZdict[n+1]) 
                    try:
                        #set keyFrame at current Time
                        #cmds.setKeyframe(currentSel[i] + '.%s%s'%(TRSdict[x+1],XYZdict[n+1]))
                        #change currentTime by offset variable amount
                        cmds.setAttr(controlsDict[key] + '.scale%s'%XYZdict[n+1],loadScales[n])
                        cmds.setKeyframe(controlsDict[key] + '.scale%s'%XYZdict[n+1],al = 'importAnimLayer')
                    except RuntimeError as re:
                        print re


#show GUI function
def showGUI():
    cmds.window('poseSaver',title='Pose Saver by Wesley Wilson')
    cmds.rowColumnLayout(numberOfRows=20,p='poseSaver')
    
    cmds.checkBox('anim_checkBox', label='Would you like to save an animation?')
    cmds.textFieldGrp('poseName_grp', label='Name for this pose',pht="ex: HIKI_H1_001")
    cmds.button('copyPose_btn',label='Save this Pose', c=copyPose)
    cmds.intFieldGrp('slideTime_grp',numberOfFields = 1, label='Duration of transition')
    cmds.button('loadPose_btn',label='Load this Pose', c=pastePose)
    
    cmds.showWindow('poseSaver')
    
showGUI()
                        