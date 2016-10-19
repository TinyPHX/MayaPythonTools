#change the SkinCluster name and the affected joints name.  
#This is the basis for the skinning weights tool
#runs sloooooooooooooooooooooow for selections of larger verts.

#selection of verts
currentSelVerts=cmds.ls(sl=True,fl=True)

#for every vertex in the selection:
for i in range(len(currentSelVerts)):
    #check the weight for the joint that is recieving the weights
    checkRecieve=cmds.skinPercent('skinCluster25','%s'%(currentSelVerts[i]),transform='butterflyRoot_jnt',q=True )
    #check the weight for the joint that is giving the weights
    checkTake=cmds.skinPercent('skinCluster25','%s'%(currentSelVerts[i]),transform='legs_jnt',q=True)
    #make the joint change
    cmds.skinPercent('skinCluster25','%s'%(currentSelVerts[i]),tv=[('butterflyRoot_jnt',checkRecieve+checkTake),('legs_jnt',0.0)])