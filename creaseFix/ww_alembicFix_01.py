'''
Alembic Cache Subdivision fix Tool.
Created by Wesley Wilson
on 7/16/2014

future update notes - 
-could include the ability to do it for multiple meshes.
-could make a gui with a viewlist that lets you visually select the shape nodes/meshes you want affected.
-could include a prompt to ask if you want to create this node on the selected mesh's shape node when you apply creases.
 The prompt could search to see if that mesh already has an attribute like this on the shape node.
'''

import maya.cmds as cmds

##Works off of the selected mesh.  Saves the selected mesh into a variable
selMesh=cmds.ls(sl=True)
listShape=cmds.listRelatives(selMesh,s=True)

##Finds the selected mesh's shape node and puts that into another variable, then selects that node.
selShape=listShape[0]
cmds.select(selShape)

##Creates a new attribute within the shape node then sets the boolean value to true(1).
cmds.addAttr(ln="SubDivisionMesh",at='bool')
cmds.setAttr(selShape+".SubDivisionMesh",k=True,e=True)
cmds.setAttr(selShape+".SubDivisionMesh",1)