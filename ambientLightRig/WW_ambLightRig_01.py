#Creates an Ambient Light soft lighting setup for rendering/test rendering
#Requires that your materials are MIA_materialX.  This requirement might 
#change in the future.  Also, requires that they all be selected.  This requirement
#will likely not change.
#by-Wesley Wilson
#on-6/23/14

import maya.cmds as cmds
#name of the lambert to be created. All other names are driven from this variable.
LambertName='ambientShader_lambert'

#select materials and assign to a list variable
selectedMaterials=cmds.ls(sl=True)

#creates the new lambert and assigns it a color of white
newLambert = cmds.shadingNode('lambert',name='%s'%LambertName,asShader=True)
cmds.setAttr('%s.color'%LambertName,1,1,1,typ='double3')

#creates an ambient light and turns its ambient shade off
cmds.ambientLight(n='%s_ambLight'%LambertName,ambientShade=0)

#takes selected materials and turns on AO and then connects the lambert to that material
for selected in selectedMaterials:
    cmds.setAttr('%s.ao_on'%selected,1)
    cmds.setAttr('%s.ao_samples'%selected,24)
    cmds.connectAttr('%s.color'%LambertName,'%s.ao_ambient'%selected,f=True)