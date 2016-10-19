import maya.cmds as cmds

#get fileNodes into list variable
filesList = cmds.ls(type='file')
print filesList
print len(filesList)

#iterate through fileNodes list variable
for i in range(len(filesList)):
    cmds.select(filesList[i])
    #get file path for fileNodes[i]
    getFileNode = cmds.getAttr('%s.fileTextureName'%filesList[i])
    print '%s.fileTextureName'%filesList[i]
    print getFileNode
    
    #chop up the file path seperated by '/' character
    chopUp = getFileNode.split('/')
    #reattach filepath to local scope "sourceimages/filename.jpg"
    newPath = chopUp[-2] + '/' + chopUp[-1]
    print newPath
    
    #set filepath attribute to newPath variable.
    cmds.setAttr('%s.fileTextureName'%filesList[i],newPath,type='string')
