#ww_camCreater.py
#Creates a camera with the translation and rotational values of the perspective Camera
#by Wesley Wilson
#on 08/01/2014

#possible updates-
# create a GUI to select which camera to create camera from
# in aforementioned GUI, have an area to name the camera what YOU want.
# make the newly created camera the rendered camera
# tear off camera in new panel and rename that bitch something like "myNewCamPanel_01"

def camCreator(*args):
    import maya.cmds as cmds
    #select Perspective camera
    cmds.select('persp')
    perspCam=cmds.ls(sl=True)[0]

    #records the perspective camera's values into variables
    perspCam_TX=cmds.getAttr(perspCam+'.translateX')
    perspCam_TY=cmds.getAttr(perspCam+'.translateY')
    perspCam_TZ=cmds.getAttr(perspCam+'.translateZ')
    perspCam_RX=cmds.getAttr(perspCam+'.rotateX')
    perspCam_RY=cmds.getAttr(perspCam+'.rotateY')
    perspCam_RZ=cmds.getAttr(perspCam+'.rotateZ')
    perspCam_FCP=cmds.getAttr(perspCam+'.fcp')
    perspCam_NCP=cmds.getAttr(perspCam+'.ncp')
    
    #creates new camera and renames it, then saves the new name into a variable
    cmds.camera(dfg=True,jc=True)
    cmds.rename('camera1','render_cam_01')
    camName=cmds.ls(sl=True)[0]
    
    #applies the perspective camera's attributes to the newly created camera
    cmds.setAttr(camName+'.translateX',perspCam_TX)
    cmds.setAttr(camName+'.translateY',perspCam_TY)
    cmds.setAttr(camName+'.translateZ',perspCam_TZ)
    cmds.setAttr(camName+'.rotateX',perspCam_RX)
    cmds.setAttr(camName+'.rotateY',perspCam_RY)
    cmds.setAttr(camName+'.rotateZ',perspCam_RZ)
    cmds.setAttr(camName+'.fcp',perspCam_FCP)
    cmds.setAttr(camName+'.ncp',perspCam_NCP)
    
'''    
import ww_camCreater as wwcc
wwcc.camCreator()
'''
