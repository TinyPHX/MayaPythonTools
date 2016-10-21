import maya.cmds as cmds
import random

def MakeRandSurfaceShader(sel_list, name):
	newShader = cmds.shadingNode('surfaceShader', asShader = True, n = '%s_surfaceShader_mat'%name)
	cmds.setAttr('%s.outColor'%newShader, random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), type = 'double3')
	for sel in sel_list:
		cmds.select(sel)
		cmds.hyperShade(assign = newShader)
	
	
	