#applys UV checker texture through lambert material to selected object in scene
#made by Wesley Wilson
#date last modified: 04/24/2014



def applyUVchecker(*args):
    import maya.cmds as cmds
    selectedItems=(cmds.ls(sl=True))
    filePath='C:/Users/wwilson/Desktop/uvtemplate001-lg.jpg'
    #change filepath variable to where the texture you want to apply is
    name='UVtexture'
    #change name variable to whatever you want the materials name to be
    shader=cmds.shadingNode('lambert',name='%s_mat'%name,asShader=True)
    shading_group=cmds.sets(name='%s_SG'%name,renderable=True,noSurfaceShader=True,empty=True)
    texture_file=cmds.shadingNode('file',name='%s_file'%name,at=True)
    cmds.setAttr('%s.fileTextureName'%texture_file,filePath,typ='string')
    cmds.connectAttr('%s.outColor'%shader,'%s.surfaceShader'%shading_group)
    cmds.connectAttr('%s.outColor'%texture_file,'%s.color'%shader,f=True)
    cmds.select(selectedItems)
    cmds.hyperShade(a='%s_mat'%name)
    
    
    
"""
import UVchecker
UVchecker.applyUVchecker()
"""
