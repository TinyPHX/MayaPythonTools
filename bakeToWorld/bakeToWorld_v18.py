#bake a Childs t,r,s values to world Coordinates
#compatible with Maya 2012-2014
#version 1.8
#Steffen Richter
# copyright 2013 //all Rights reserved
#www.richter-steffen.com

import maya.cmds as cmds


selObj = cmds.ls(sl=True)

#Check if an object is selected
if selObj == []:
	cmds.confirmDialog(t='Warning!',message='Please Select min. one Child Object',ds='ok',icn='information')



bakeList = []
for n in selObj:
	
	#check if selected object is a child of an object			
	par = cmds.listRelatives(n,parent=True)
	if par == None:
		cmds.confirmDialog(t='Warning!',message='%s has no Parent Object' %n ,ds='ok',icn='information')
		
	else:
		#duplicate object 
								
		duplObj = cmds.duplicate(n,name=n+'_bakedToWorld',rc=True,rr=True)
		
		#delete doublicated children
		childrenTd = cmds.listRelatives(duplObj,c=True,pa=True)[1:]
		for c in childrenTd:
			cmds.delete(c)
		#unparent object,add constraints and append it to bake List	
		toBake = cmds.parent(duplObj,w=True)
		bakeList.append(toBake)
		cmds.parentConstraint(n,toBake,mo=False)
		cmds.scaleConstraint(n,toBake,mo=False)
		
		

#get Start and End Frame of Time Slider
startFrame = cmds.playbackOptions(q=True,minTime=True)
endFrame = cmds.playbackOptions(q=True,maxTime=True)

# bake Animation and delete Constraints

for i in bakeList:
	cmds.bakeResults(i, t=(startFrame,endFrame))
	cmds.delete(i[0] + '*Constraint*')