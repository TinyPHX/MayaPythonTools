# This module will make a range of motion animation for joints in the scene.
# That animation should be used to help in skinning a character and not for evil
#
# @auth - Wesley Wilson :)
# @datelastmodified - 04/17/2014

import maya.cmds as cmds
cmds.currentTime(0,update=True,edit=True)
jntList=cmds.ls(type='joint')
ctrlList=cmds.ls(type='curve')
RXv=0.0
RYv=0.0
RZv=0.0
TXv=0.0
TYv=0.0
TZv=0.0
CurrentTime=cmds.currentTime(q=True)
FirstKey=5
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
    negTime=(bothTime/2)
    negRotX=((cmds.floatFieldGrp('rotate_XYZgrp',q=True,v=True)[0])*-2)
    negRotY=((cmds.floatFieldGrp('rotate_XYZgrp',q=True,v=True)[1])*-2)
    negRotZ=((cmds.floatFieldGrp('rotate_XYZgrp',q=True,v=True)[2])*-2)
    cmds.setKeyframe(attribute=('rotateX','rotateY','rotateZ'))
    cmds.setKeyframe(attribute=('rotateX','rotateY','rotateZ'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[1])
    cmds.currentTime(cmds.intFieldGrp('RangeCounter',q=True,v=True)[0],update=True,edit=True)
    cmds.rotate(cmds.floatFieldGrp('rotate_XYZgrp',q=True,v=True)[0],cmds.floatFieldGrp('rotate_XYZgrp',q=True,v=True)[1],cmds.floatFieldGrp('rotate_XYZgrp',q=True,v=True)[2],r=True,eu=True)
    cmds.setKeyframe(attribute=('rotateX','rotateY','rotateZ'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[0])
    cmds.currentTime(negTime,update=True,edit=True)
    cmds.rotate(negRotX,negRotY,negRotZ,r=True)
    updateTime()

#Translate button - keys the current time adn the animrange value with original translates then translates and keys at firstkey value
#then moves to 3rd value and negative translates and keys
def translate_cmd(*args):
    bothTime=(cmds.intFieldGrp('RangeCounter',q=True,v=True)[1])+(cmds.intFieldGrp('RangeCounter',q=True,v=True)[0])
    negTime=(bothTime/2)
    negTransX=((cmds.floatFieldGrp('translate_XYZgrp',q=True,v=True)[0])*-1)
    negTransY=((cmds.floatFieldGrp('translate_XYZgrp',q=True,v=True)[1])*-1)
    negTransZ=((cmds.floatFieldGrp('translate_XYZgrp',q=True,v=True)[2])*-1)
    cmds.setKeyframe(attribute=('translateX','translateY','translateZ'))
    cmds.setKeyframe(attribute=('translateX','translateY','translateZ'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[1])
    cmds.currentTime(cmds.intFieldGrp('RangeCounter',q=True,v=True)[0],update=True,edit=True)
    cmds.move(cmds.floatFieldGrp('translate_XYZgrp',q=True,v=True)[0],cmds.floatFieldGrp('translate_XYZgrp',q=True,v=True)[1],cmds.floatFieldGrp('translate_XYZgrp',q=True,v=True)[2],a=True,ls=True)
    cmds.setKeyframe(attribute=('translateX','translateY','translateZ'),t=cmds.intFieldGrp('RangeCounter',q=True,v=True)[0])
    cmds.currentTime(negTime,update=True,edit=True)
    cmds.move(negTransX,negTransY,negTransZ,a=True,ls=True)
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
    RXv=0.0
    RYv=0.0
    RZv=0.0
    TXv=0.0
    TYv=0.0
    TZv=0.0
    cmds.floatFieldGrp('rotate_XYZgrp',e=True, value1=RXv, value2=RYv, value3=RZv)
    cmds.floatFieldGrp('translate_XYZgrp',e=True, value1=TXv, value2=TYv, value3=TZv)
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
cmds.floatFieldGrp('rotate_XYZgrp',numberOfFields=3, label='Rotate     ',ann=rotateGrpAnn, value1=RXv, value2=RYv, value3=RZv)
cmds.button('translate_btn',label='translate',c=translate_cmd)
cmds.floatFieldGrp('translate_XYZgrp',numberOfFields=3, label='Translate  ',ann=translateGrpAnn, value1=TXv, value2=TYv, value3=TZv)
cmds.button('reset_btn',label='Reset Time and Values',ann=resetBtnAnn,c=reset_cmd)
cmds.intFieldGrp('RangeCounter',numberOfFields=2, label='First value change',extraLabel='Total range',ann=RangeCounterAnn,enable1=False,enable2=False, value1=FirstKey, value2=AnimRange)

#spawns the hell beast.
cmds.showWindow('motionRange')