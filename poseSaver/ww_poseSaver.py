#Pose Saver tool for Maya 
#by: Wesley Wilson on 11/25/2015
 
'''
to use:
    COPYING:
        - select all control curves to be saved to file
        - name the text file you want outputted something descriptive.  You will have to navigate to this later
        - click button to save pose information.  
        
        Script saves to the current project's data folder inside a poseSaves folder.
    
    PASTING:
        - select all control curves AND joints to be compared and changed by text file
        - determine the time slide distance in the int field
        - click button to start pasting procedure.  
        
        Script opens a file dialogue box where you navigate to the text file corresponding to the pose you want.
        Once selected, the script searches the current selection for different transform values from those from the pose text file.
        If there is a difference in a specific channel, keyframes are set at the current time at the current values and then at the 
        current time (+ the time slide distance amount defined earlier) with the changed values from the text file.

future stuff:
    - add support for namespaces (on save, the controller/joint names are recorded sans the nameSpace.  on load, the controller/joint names are read from the currentSel sans the nameSpace)
    - add support for more channels/ custom channels.  Not sure HOW this would work right now.
    - add support for animated groups or blendshape's or just mesh transformations
'''
    

import maya.cmds as cmds
import json
import os

#prevents duplicate windows from popping up    
if cmds.window('poseSaver',exists=True):
    cmds.deleteUI('poseSaver',window=True)


#copy KeyFrames function
def copyPose(*args):
    #get all joints and curves into lists
    #allJoints = cmds.ls(type = 'joint')
    allCurves = cmds.ls(sl=True)
	print allCurves
	print "Got here!"
    
    #this is what the file will be named
    poseName = cmds.textFieldGrp('poseName_grp',q=True,tx=True)
    print poseName
    
    #this is what we will be saving
    saveDict = {}
    '''
    for i in range(len(allJoints)):
        cmds.select(allJoints[i])
        getTrans = cmds.xform(q=True,t=True)
        getRots = cmds.xform(q=True,ro=True)
        getScales = cmds.xform(q=True,s=True,r=True)
        
        saveDict[allJoints[i]] = getTrans + getRots + getScales
    '''    
    for i in range(len(allCurves)):
        cmds.select(allCurves[i])
        getTrans = cmds.xform(q=True,t=True)
        getRots = cmds.xform(q=True,ro=True)
        getScales = cmds.xform(q=True,s=True,r=True)
        
        saveDict[allCurves[i]] = getTrans + getRots + getScales
    
    #find current workpath
    prePath = cmds.workspace(q=True,dir=True)
    trimPath=prePath.find('/',41)
    dataPath = prePath[:trimPath] + '/data/'
    folderPath = dataPath + '/poseSaves/'
    
    #check to see if folder already exists
    ifExist = os.path.exists(folderPath)
    if not ifExist:
        #make folder to store .txt files if one does not already exist
        os.mkdir(os.path.join(dataPath, 'poseSaves'))
        
    fullPath = folderPath + poseName + '.txt'
    
    toBeSaved = json.dumps(saveDict, sort_keys=True, ensure_ascii=True, indent=2)
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
    
    #selection of things you want the pose pasted to
    currentSel = cmds.ls(sl=True)
      
    #fullPath = prePath[:trimPath]+'//data/poseSaves/'+fileName+'.txt'
    if os.path.exists(fileName):
        #if the file at a specific path exists, then open it and attach information from it to variables
        f=open(fileName)
        dataFile = json.load(f)
        
        for i in range(len(currentSel)):
            #load dictionary data using current selection as a key
            loadTrans = dataFile[currentSel[i]][0:3]
            loadRots = dataFile[currentSel[i]][3:6]
            loadScales = dataFile[currentSel[i]][6:9]
            
            #check that data against current transform values for that currentSel object
            cmds.select(currentSel[i])
            checkTrans = cmds.xform(q=True,t=True)
            checkRots = cmds.xform(q=True,ro=True)
            checkScales = cmds.xform(q=True,s=True,r=True)
            
            XYZdict = {1:'X', 2:'Y', 3:'Z'}
            
            #change transform values to pasteValues recieved from text file if they don't match the current values
            for n in range(len(XYZdict)):
                if not checkTrans[n] == loadTrans[n]:
                    print 'setting key on %s.translate%s'%(currentSel[i],XYZdict[n+1]) 
                    try:
                        #set keyFrame at current Time
                        cmds.setKeyframe(currentSel[i] + '.translate%s'%XYZdict[n+1])
                        #change currentTime by offset variable amount
                        cmds.currentTime(crntTime + slideAmnt, update = True, edit = True)
                        #change relevant attribute channels and set a keyframe
                        cmds.setAttr(currentSel[i] + '.translate%s'%XYZdict[n+1],loadTrans[n])
                        cmds.setKeyframe(currentSel[i] + '.translate%s'%XYZdict[n+1])
                        #go back to proper time that transition should occur at
                        cmds.currentTime(crntTime, update = True, edit = True)
                    except RuntimeError as re:
                        print re
                
                if not checkRots[n] == loadRots[n]:
                    print 'setting key on %s.rotate%s'%(currentSel[i],XYZdict[n+1])
                    try:
                        #set keyFrame at current Time
                        cmds.setKeyframe(currentSel[i] + '.rotate%s'%XYZdict[n+1])
                        #change currentTime by offset variable amount
                        cmds.currentTime(crntTime + slideAmnt, update = True, edit = True)
                        #change relevant attribute channels and set a keyframe
                        cmds.setAttr(currentSel[i] + '.rotate%s'%XYZdict[n+1],loadRots[n])
                        cmds.setKeyframe(currentSel[i] + '.rotate%s'%XYZdict[n+1])
                        #go back to proper time that transition should occur at
                        cmds.currentTime(crntTime, update = True, edit = True)
                    except RuntimeError as re:
                        print re
                        
                if not checkScales[n] == loadScales[n]:
                    print 'setting key on %s.scale%s'%(currentSel[i],XYZdict[n+1])   
                    try:
                        #set keyFrame at current Time
                        cmds.setKeyframe(currentSel[i] + '.scale%s'%XYZdict[n+1])
                        #change currentTime by offset variable amount
                        cmds.currentTime(crntTime + slideAmnt, update = True, edit = True)
                        #change relevant attribute channels and set a keyframe
                        cmds.setAttr(currentSel[i] + '.scale%s'%XYZdict[n+1],loadScales[n])
                        cmds.setKeyframe(currentSel[i] + '.scale%s'%XYZdict[n+1])
                        #go back to proper time that transition should occur at
                        cmds.currentTime(crntTime, update = True, edit = True)  
                    except RuntimeError as re:
                        print re

#show GUI function
def showGUI():
    cmds.window('poseSaver',title='Pose Saver by Wesley Wilson')
    cmds.rowColumnLayout(numberOfRows=20,p='poseSaver')
    
    cmds.textFieldGrp('poseName_grp', label='Name for this pose',pht="ex: HIKI_H1_001")
    cmds.button('copyPose_btn',label='Save this Pose', c=copyPose)
    cmds.intFieldGrp('slideTime_grp',numberOfFields = 1, label='Duration of transition')
    cmds.button('loadPose_btn',label='Load this Pose', c=pastePose)
    
    cmds.showWindow('poseSaver')
	
def printThing():
	print "the thing!"
	
print "what the hell?"
                        