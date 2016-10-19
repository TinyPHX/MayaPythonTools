# This module will make a range of motion animation for joints in the scene.
# That animation should be used to help in skinning a character and not for evil
#
# @auth - Wesley Wilson :)
# @datelastmodified - 08/11/2016

import maya.cmds as cmds
cmds.currentTime(0,update=True,edit=True)
jntList=cmds.ls(type='joint')
#ctrlList=cmds.ls(type='curve')
RotVal = 0.0
TransVal = 0.0
CurrentTime=cmds.currentTime(q=True)
FirstKey=5
SecondKey = FirstKey * 2
AnimRange=20
NEWfirstKey=(CurrentTime)+(FirstKey)
NEWanimRange=(CurrentTime)+(AnimRange)
RangeCounterAnn='First value change is the frame where the inputs from above will be keyed. \nTotal range is the total range of the animation.'
rotateGrpAnn='Animate relative rotations, then inverted rotational values. \nIE: 15 then -15'
translateGrpAnn='Animate absolute translations, then inverted translation values. \nIE: 5 then -5\nWill transform absolutely, so copy current transform values into fields.'
resetBtnAnn='Resets current time to 0, RangeCounter to 5 and 20, and all transform values to 0.0'

#Rotate button - keys the current time and the animrange value with original rotations then rotates and keys at firstkey value 
#then moves to 3rd value and negative rotates and keys
def rotate_cmd(*args):
    bothTime=(cmds.intFieldGrp('RangeCounter',q=True,v=True)[1])+(cmds.intFieldGrp('RangeCounter',q=True,v=True)[0])
    ActualRot = cmds.floatFieldGrp('rotate_XYZgrp',q=True,v=True)[0]
    negRot = ((cmds.floatFieldGrp('rotate_XYZgrp',q=True,v=True)[0])*-2)
    
    #X
    queryTime = cmds.currentTime(q=True)
    cmds.setKeyframe(attribute=('rotateX'))
    cmds.setKeyframe(attribute=('rotateX'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[1])
    cmds.currentTime(cmds.intFieldGrp('RangeCounter',q=True,v=True)[0],update=True,edit=True)
    cmds.rotate(ActualRot,0,0,r=True,eu=True)
    cmds.setKeyframe(attribute=('rotateX'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[0])
    cmds.currentTime((cmds.intFieldGrp('RangeCounter',q=True,v=True)[1] - FirstKey),update=True,edit=True)
    cmds.rotate(negRot,0,0,r=True)
    cmds.currentTime(bothTime,update=True,edit=True)
    updateTime()
    
    #Y
    queryTime = cmds.currentTime(q=True)
    cmds.setKeyframe(attribute=('rotateY'))
    cmds.setKeyframe(attribute=('rotateY'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[1])
    cmds.currentTime(cmds.intFieldGrp('RangeCounter',q=True,v=True)[0],update=True,edit=True)
    cmds.rotate(0,ActualRot,0,r=True,eu=True)
    cmds.setKeyframe(attribute=('rotateY'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[0])
    cmds.currentTime((cmds.intFieldGrp('RangeCounter',q=True,v=True)[1] - FirstKey),update=True,edit=True)
    cmds.rotate(0,negRot,0,r=True)
    cmds.currentTime(bothTime,update=True,edit=True)
    updateTime()
    
    #Z
    queryTime = cmds.currentTime(q=True)
    cmds.setKeyframe(attribute=('rotateZ'))
    cmds.setKeyframe(attribute=('rotateZ'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[1])
    cmds.currentTime(cmds.intFieldGrp('RangeCounter',q=True,v=True)[0],update=True,edit=True)
    cmds.rotate(0,0,ActualRot,r=True,eu=True)
    cmds.setKeyframe(attribute=('rotateZ'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[0])
    cmds.currentTime((cmds.intFieldGrp('RangeCounter',q=True,v=True)[1] - FirstKey),update=True,edit=True)
    cmds.rotate(0,0,negRot,r=True)
    cmds.currentTime(bothTime,update=True,edit=True)
    updateTime()

#Translate button - keys the current time adn the animrange value with original translates then translates and keys at firstkey value
#then moves to 3rd value and negative translates and keys
def translate_cmd(*args):
    bothTime=(cmds.intFieldGrp('RangeCounter',q=True,v=True)[1])+(cmds.intFieldGrp('RangeCounter',q=True,v=True)[0])
    ActualTrans = cmds.floatFieldGrp('translate_XYZgrp',q=True,v=True)[0]
    negTrans = ((cmds.floatFieldGrp('translate_XYZgrp',q=True,v=True)[0])*-2)
    
    print "TransX: this is the current time: %i" %(cmds.currentTime(q=True))
    print "TransX: this is bothTime: %i"%(bothTime)
    print "TransX: this is the negative time: %i"%((bothTime/2)+(cmds.currentTime(q=True)))
    
    #X
    queryTime = cmds.currentTime(q=True)
    cmds.setKeyframe(attribute=('translateX'))
    cmds.setKeyframe(attribute=('translateX'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[1])
    cmds.currentTime(cmds.intFieldGrp('RangeCounter',q=True,v=True)[0],update=True,edit=True)
    cmds.move(ActualTrans,0,0,r=True,ls=True)
    cmds.setKeyframe(attribute=('translateX'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[0])
    cmds.currentTime((cmds.intFieldGrp('RangeCounter',q=True,v=True)[1] - FirstKey),update=True,edit=True)
    cmds.move(negTrans,0,0,r=True,ls=True)
    cmds.currentTime(bothTime,update=True,edit=True)
    updateTime()
    
    #Y
    queryTime = cmds.currentTime(q=True)
    cmds.setKeyframe(attribute=('translateY'))
    cmds.setKeyframe(attribute=('translateY'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[1])
    cmds.currentTime(cmds.intFieldGrp('RangeCounter',q=True,v=True)[0],update=True,edit=True)
    cmds.move(0,ActualTrans,0,r=True,ls=True)
    cmds.setKeyframe(attribute=('translateY'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[0])
    cmds.currentTime((cmds.intFieldGrp('RangeCounter',q=True,v=True)[1] - FirstKey),update=True,edit=True)
    cmds.move(0,negTrans,0,r=True,ls=True)
    cmds.currentTime(bothTime,update=True,edit=True)
    updateTime()
    
    #Z
    queryTime = cmds.currentTime(q=True)
    cmds.setKeyframe(attribute=('translateZ'))
    cmds.setKeyframe(attribute=('translateZ'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[1])
    cmds.currentTime(cmds.intFieldGrp('RangeCounter',q=True,v=True)[0],update=True,edit=True)
    cmds.move(0,0,ActualTrans,r=True,ls=True)
    cmds.setKeyframe(attribute=('translateZ'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[0])
    cmds.currentTime((cmds.intFieldGrp('RangeCounter',q=True,v=True)[1] - FirstKey),update=True,edit=True)
    cmds.move(0,0,negTrans,r=True,ls=True)
    cmds.currentTime(bothTime,update=True,edit=True)
    updateTime()
    
#selects joints in the scene as they are selected in the tool window and informs you that you did just do something   
def selectionTask():
    selItems=cmds.textScrollList('jointScrollList',q=1,si=True,ams=True)
    cmds.select(clear=True)
    for sItem in selItems:
        cmds.select(sItem,add=True)
    print('You just selected something, sucka')
    
#update the values in the animrange fields.  You can't be trusted with these values.
def updateTime(*args):
    cmds.currentTime(cmds.intFieldGrp('RangeCounter',q=True,v=True)[1],update=True,edit=True)
    CurrentTime=cmds.currentTime(q=True)
    OldTime1=cmds.intFieldGrp('RangeCounter',q=True,v1=True)
    OldTime2=cmds.intFieldGrp('RangeCounter',q=True,v2=True)
    NEWfirstKey=(CurrentTime)+(FirstKey)
    NEWanimRange=(CurrentTime)+(AnimRange)
    cmds.intFieldGrp('RangeCounter',e=True,value1=NEWfirstKey,value2=NEWanimRange)
 
#resets all fields. 
# all. fields.
def reset_cmd(*args):
    RotVal = 0.0
    TransVal = 0.0
    cmds.floatFieldGrp('rotate_XYZgrp',e=True, value1=RotVal)
    cmds.floatFieldGrp('translate_XYZgrp',e=True, value1=TransVal)
    cmds.intFieldGrp('RangeCounter',e=True,value1=FirstKey,value2=AnimRange)
    cmds.currentTime(0,edit=True,update=True)
    print('You got it, Boss!')

#prevents duplicate windows from popping up    
if cmds.window('motionRange',exists=True):
    cmds.deleteUI('motionRange',window=True)

#creates UI stuff
cmds.window('motionRange',title='Range of Motion Tool')
cmds.rowColumnLayout(numberOfRows=7,p='motionRange')
cmds.textScrollList('jointScrollList',numberOfRows=15, allowMultiSelection=True,append=jntList,sc=selectionTask)
cmds.button('rotate_btn',label='rotate',c=rotate_cmd)
cmds.floatFieldGrp('rotate_XYZgrp',numberOfFields=1, label='Rotate     ',ann=rotateGrpAnn, value1=RotVal)
cmds.button('translate_btn',label='translate',c=translate_cmd)
cmds.floatFieldGrp('translate_XYZgrp',numberOfFields=1, label='Translate  ',ann=translateGrpAnn, value1=TransVal)
cmds.intFieldGrp('RangeCounter',numberOfFields=2, label='First value change',extraLabel='Total range',ann=RangeCounterAnn,enable1=False,enable2=False, value1=FirstKey, value2=AnimRange)
cmds.button('reset_btn',label='Reset Time and Values',ann=resetBtnAnn,c=reset_cmd)

#spawns the hell beast.
cmds.showWindow('motionRange')