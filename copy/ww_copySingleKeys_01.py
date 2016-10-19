#graph editor keyframe copier.
#by Wesley Wilson
#on 02/24/15
#edited on 02/25/15

#To use:  In GraphEditor, select the keyframes you want to copy, then go to the time you want them pasted and run this script.


"""
This script copies the selected keyframes and pastes them at the current time in the grapheditor.
This script currently only works with one selected keyframe per channel on multiple channels and objects.
This script does allow you to copy and paste multiple keyframes over various objects, but does not allow you to copy and paste multipl keyframes within the same channel.
"""

import maya.cmds as cmds
import sys

#record the current time int oan aptly named variable
currentActualTime = cmds.currentTime(q=True)
#record the current list of selected keyframes into an aptly named variable
allKeys = cmds.keyframe(q=True, n=True)

#the working bits. We find keyframe's channel and object and then the keyframe's value.  We then re set new keyframes at the currentTime.
for i in range (len(allKeys)):
     currentSelKey = allKeys[i]
     splitKey = currentSelKey.split("_")
     choppedObject = splitKey[:-1]
     currentObject = "_".join(choppedObject)
     currentChannel = splitKey[-1]
     currentValue=cmds.keyframe(q=True,at=currentChannel,vc=True)
     cmds.setKeyframe(currentObject,at=currentChannel,t=currentActualTime,v=currentValue[i]) 
     
#output the amount of keyframes copied and pasted.
sys.stdout.write("Copied %i keyframes. Lil' John got the rhythm make the booty go POP."%(len(allKeys)))