'''
Skinned Mesh crease recreation script.
Prerequisites - must have crease sets on skinned mesh seperated by object and crease value, no namespaces on skinned object name,
    Project must be set like thus (C:\Users\wwilson\Documents\maya\projects\PROJECTNAME), need a pretty defualt maya folder setup,
    Use when initially creasing geometry and not after creases are already present, currently can't handle more than 10 crease files
    per project.
Does not work with multiple crease nodes.  Only one per mesh to be exported, please.
    
How to use - 
1.    When making creases- select edges to crease, then create a crease set.  For name- use projectname followed by "_0#" (ex: WIND_01,
      WIND_02,etc.).  This script will only load files in a specific folder with the name of the project as the name of the file.
2.    Crease the edges like normal, using the crease tool
3.    Select the crease set in the outliner, then run script (one instance per crease set)
'''
import os
import maya.cmds as cmds
import json
#get current selection (crease set)
currentSel=cmds.ls(sl=True)
creaseSetName=currentSel[0]
#select children of current selection (edges)
cmds.select(currentSel,ne=False)
selChild=cmds.ls(sl=True)
#get crease value of edges
creaseValue=cmds.polyCrease(q=True,v=True)
valueList=[creaseValue[0]]

#store the creaseset information into variable (the selected edges and the crease value)
toSave=selChild + valueList

#find current workpath
prePath=cmds.workspace( q=True, dir=True)
trimPath=prePath.find('/',41)
dataPath=prePath[:trimPath]+'/data/'
folderPath=dataPath + '/creaseData/'

#check to see if folder exists already
ifExist=os.path.exists(folderPath)
if not ifExist:
    #make folder to store .txt files
    os.mkdir(os.path.join(dataPath,'creaseData'))
    fullPath=folderPath + creaseSetName + ".txt"
    toBeSaved=json.dumps(toSave,sort_keys=True,ensure_ascii=True,indent=2)
    f=open(fullPath,"w")
    #save crease set information to a .txt file in the folder
    f.write(toBeSaved)
    f.close()

else:
    #if the folder already exists, just save the crease set
    fullPath=folderPath + creaseSetName + ".txt"
    toBeSaved=json.dumps(toSave,sort_keys=True,ensure_ascii=True,indent=2)
    f=open(fullPath,"w")
    #save crease set information to a .txt file in the folder
    f.write(toBeSaved)
    f.close()
