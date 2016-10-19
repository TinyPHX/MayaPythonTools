'''
Script to import crease set data from a spcific text file/group of text files
How to use-
1.    Import the scene you want, can have NO namespaces on the skinned geo you want to recrease
2.    Don't need to select geo or anything, but geo you want to recrease must have same name as when it was creased
3.    Click the button.  Warning will pop up if geo isn't found in the scene, but script should still work
4.    For the love of Pete, make sure the path is the same as the crease files you are lookign to import.  The best way to do this is 
      by saving the file you are importing crease data into inside the same directory as the file you are getting the crease info from.
'''


import maya.cmds as cmds
import json
import os
#find current workspace
prePath=cmds.workspace( q=True, dir=True)
#find project name from the workspace path(projectPath variable)
trimPath=prePath.find('/',41)
firstCut=prePath.find('/',35)+1
lastCut=prePath.find('/',firstCut)
projectPath=prePath[firstCut:lastCut]
#Within a given nnumber range(1-10):
for i in range(10):
    #attach the number to the full path (thus creating a path to all the potential files)      
    fullPath=prePath[:trimPath]+'/data/creaseData/'+ projectPath + '_0%d'%(i)+'.txt'
    if os.path.exists(fullPath):
        #if the file at a specific path exists, then open it and attach information from it to variables
        #if the file at a specific path does NOT exist, then it will keep going down the path
        f=open(fullPath)
        dataFile=json.load(f)
        value=dataFile[-1]
        creaseSel=dataFile[:-1]
        numbOfEdges=len(creaseSel)
        #for all the edges in the variables creaseSel, select them and then apply the crease at the specified crease value
        #if the edges in the files found don't exist, their will be a value error(no object found) but the script will keep going
        for i in creaseSel:
            try:
                cmds.select(creaseSel)
                cmds.polyCrease(ch=True,v=value)
            except ValueError as e:
                print (e)