# makes the torn off window the active view then plays the animation.  
# Preventing the need to constantly click on it to make it active, then click play.  
# Now you just click on this instead...
#
# the name of the panel will vary
# Could make it so if the active view was the persp cam view then the animation would automatically stop.
# Could make it so any time the torn off view is made active the animation starts.
# Could make it so that when the torn off view is created it records the name of that Panel.

from maya.cmds import currentTime
from maya.cmds import modelEditor
from maya.cmds import play
##import maya.cmds as mc
currentTime(0,e=True)
modelEditor("modelPanel8",e=True,av=True)
play(forward=True)