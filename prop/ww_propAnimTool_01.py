#By - Wesley Wilson
#last updated - 6/16/2014
#potential updates - 
#build a gui or series of prompts to input name of objects



#script used in animating props to smoothly transition from a parent constraint to no constraint.
#set up must be as follows-
#locator or some object with a parent constraint driving the master controller's group of the prop
#the locator object is parented or parent constrained to the character's hand/feet controller.
#must be on the frame you want to switch from controller to independent prop
import maya.cmds as mc

#record current time and one frame before into variables
nowTime=mc.currentTime(q=True)
thenTime=nowTime - 1

#record name of group to be keyframed and the locator/other master constrained object.  THESE STRINGS CHANGE WITH DIFFERENT PROJECTS
groupName='grp_ctrl_potion_strap_jnt_001_1'
locName='falc_attach_loc'

#records locators positional and rotation information and then sets the groups to the same, then set keyframe for that attribute
locTx=mc.getAttr(locName+'.translateX')
mc.setAttr(groupName+'.translateX',locTx)
mc.setKeyframe(groupName,at='translateX')
locTy=mc.getAttr(locName+'.translateY')
mc.setAttr(groupName+'.translateY',locTy)
mc.setKeyframe(groupName,at='translateY')
locTz=mc.getAttr(locName+'.translateZ')
mc.setAttr(groupName+'.translateZ',locTz)
mc.setKeyframe(groupName,at='translateZ')
locRx=mc.getAttr(locName+'.rotateX')
mc.setAttr(groupName+'.rotateX',locRx)
mc.setKeyframe(groupName,at='rotateX')
locRy=mc.getAttr(locName+'.rotateY')
mc.setAttr(groupName+'.rotateY',locRy)
mc.setKeyframe(groupName,at='rotateY')
locRz=mc.getAttr(locName+'.rotateZ')
mc.setAttr(groupName+'.rotateZ',locRz)
mc.setKeyframe(groupName,at='rotateZ')

#backwards one frame to set keyframe of 1 for the constraint switching attribute
mc.currentTime(thenTime,e=True)
mc.setKeyframe(groupName,attribute='blendParent1',v=1)

#forawrds back to switching frame to set keyframe of 0 for the constraint switching attribute
mc.currentTime(nowTime,e=True)
mc.setKeyframe(groupName,attribute='blendParent1',v=0)
