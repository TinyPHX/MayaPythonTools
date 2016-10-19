# Animation Scaling script for use in exporting animations into Unity that will be scaled in the game engine
# Created by Wesley Wilson on 1/20/2015


# There needs to be animation on each channel for this to work (tranX, Y, and Z)
# Infact, its better if you don't do this until after the animation is baked and ready for export into Unity

import maya.cmds as cmds
# currently only works on one selected object
currentSel = cmds.ls(sl=True)[0]

# finds time parameters
currentMinTime=cmds.playbackOptions(q=True,minTime=True)
currentMaxTime=cmds.playbackOptions(q=True,maxTime=True)

# place each attribute key value and the time for those keys into variables
currentAttr=["tx","ty","tz"]
currentKeysTime_X=cmds.keyframe(currentSel+".translateX",time=(currentMinTime,currentMaxTime),q=True)
currentKeysTime_Y=cmds.keyframe(currentSel+".translateY",time=(currentMinTime,currentMaxTime),q=True)
currentKeysTime_Z=cmds.keyframe(currentSel+".translateZ",time=(currentMinTime,currentMaxTime),q=True)
currentTranX=cmds.keyframe(currentSel,q=True,at=currentAttr[0],vc=True)
currentTranY=cmds.keyframe(currentSel,q=True,at=currentAttr[1],vc=True)
currentTranZ=cmds.keyframe(currentSel,q=True,at=currentAttr[2],vc=True)

# multiplication factor
multFactor=.5

# new key values
newTranX=[]
newTranY=[]
newTranZ=[]

# print each attributes values and then multiply them all by the value change number and then reprint the values to show the changes
print "tranX_______"
print currentTranX
for i in range(len(currentTranX)):
    modifiedKey = currentTranX[i] * multFactor
    newTranX.append(modifiedKey)
print newTranX
print "tranY________"
print currentTranY
for i in range(len(currentTranY)):
    modifiedKey = currentTranY[i] * multFactor
    newTranY.append(modifiedKey)
print newTranY
print "tranZ________"
print currentTranZ
for i in range(len(currentTranZ)):
    modifiedKey = currentTranZ[i] * multFactor
    newTranZ.append(modifiedKey)
print newTranZ

# set the NEW keys in place of the old translation keys
for i in range(len(newTranX)):
    cmds.setKeyframe(currentSel,e=True,at='tx',v=newTranX[i],t=currentKeysTime_X[i])
for i in range(len(newTranY)):
    cmds.setKeyframe(currentSel,e=True,at='ty',v=newTranY[i],t=currentKeysTime_Y[i])
for i in range(len(newTranZ)):
    cmds.setKeyframe(currentSel,e=True,at='tz',v=newTranZ[i],t=currentKeysTime_Z[i])