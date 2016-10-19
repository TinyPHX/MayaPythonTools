import maya.cmds as cmds

currentActualTime = cmds.currentTime(q=True)

copyKeys = cmds.copyKey()
pasteKeys = cmds.pasteKey(t=(currentActualTime,currentActualTime),f=(currentActualTime,currentActualTime),o='insert',copies=1,connect=False,valueOffset=2)