import maya.cmds as cmds
import maya.mel as mel

#make a new file
cmds.file(new = True, f = True)

#remove crap function
def CleanRemove(object):
    if(object in cmds.ls()):
        cmds.delete(object)

theName = 'newNurbsSurface_01'
theNumU = 1
theNumV = 10
theControlNum = 5

newNurbsSurface = cmds.nurbsPlane(n = theName,ax = (0,1,0), w = theNumU, lr = theNumV, d = 3, u = theNumU, v = theNumV, ch = 0)[0]

cmds.select(newNurbsSurface)
mel.eval("createHair %s %s 2 0 0 0 0 5 0 1 1 1;" %(theNumU, theNumV))

#we need to remove the extra crap now
removalList = ["nucleus1", "pfxHair1", "hairSystem1"]

for i in range(theNumV):
    removalList.append("curve%i" %(i + 1))

for item in removalList:
    CleanRemove(item)
    
#get the follicles associated with this nurbs surface
nurbsShape = cmds.listRelatives(newNurbsSurface)[0]
attachedFollicles = cmds.listConnections(nurbsShape + '.worldMatrix')

for i in range(len(attachedFollicles)):
    follicle = cmds.rename(attachedFollicles[i], theName + '_%02i_follicle' %(i+1))
    cmds.select(follicle)
    cmds.joint(n = theName + 'follicle_%02i_jnt' %(i+1))

#make control joints
cmds.select(cl = True)
locList = []
for i in range(theControlNum):
    newLoc = cmds.spaceLocator()
    locList.append(newLoc)
    if i == 0:
        cmds.move((theNumV/2), z = True)
    if i == (theControlNum - 1):
        cmds.move(-(theNumV/2), z = True)
        
#move the rest of the "joints" to their new spots
for i in range(len(locList)):
    if (i > 0) & (i < (len(locList) - 1)):
        print locList[i]
        cmds.pointConstraint(locList[0], locList[i], mo = False)
        cmds.pointConstraint(locList[len(locList) - 1], locList[i], mo = False)
