########################################################################
#                                                                      #
#             ns_animBlockTool.py                                      #
#                                                                      #
#             Version 1.0 , last modified 2012-04-15                   #
#                                                                      #
#             Copyright (C) 2012  Nicholas Silveira                    #
#                                                                      #
#             Email: nicholas.silveira@gmail.com                       #
#                                                                      #
########################################################################


'''

I N S T A L L A T I O N::

Step 1:
Copy "ns_animBlockTool.py" to your Maya plugins directory.
Windows: C:\Users\UserName\Documents\maya\scripts

Step 2:
Run this in Python Script Editor or creat a Shelf Button.

import ns_animBlockTool
ns_animBlockTool.animBlockGUI()


If you have any problems email me at...
nicholas.silveira@gmail.com

'''

import maya.cmds as cmds



'''
========================================================================
---->  Progress Bar  <----
========================================================================
'''

def progressBar (windowName, value, *args):
    
    if (cmds.window ('progressWindow', q=True, exists=True)):
        cmds.deleteUI('progressWindow')
            
    else:
            
        progressWindow = cmds.window('progressWindow', title = windowName)
        cmds.columnLayout()

        progressControl = cmds.progressBar(width=300, beginProgress=True, maxValue= value)
        cmds.showWindow( progressWindow )

        return progressControl
    
    

'''
========================================================================
---->  Create New Attribute  <----
========================================================================
'''
   
def createAttr (name, attrName, value, *args):
    
    cmds.addAttr (name, ln= attrName, at='double', min= value [0], max= value [1])
    cmds.setAttr (name + '.' + attrName, e=True, keyable= True)

    return name + '.' + attrName
    
    
    
'''
========================================================================
---->  Create Block  <----
========================================================================
'''

def createBlocks (*args):

    ''' -Query GUI Values- '''
    horizontalCount = cmds.intField( 'horizontalCount', q=True, value=True)
    verticalCount = cmds.intField( 'verticalCount', q=True, value=True)
    blockScaling = cmds.floatField( 'blockScaling', q=True, value=True)
    blockSpacing = cmds.floatField( 'blockSpacing', q=True, value=True)
    blockBevel = cmds.intField( 'blockBevel', q=True, value=True)
    addCollision = cmds.checkBox('addCollision', q=True, value=True)
    
    
    ''' -Create Geo Grp- '''
    if cmds.objExists ('blockMainGeo_grp'):
        blockMainGeoGrp = 'blockMainGeo_grp'
        
    else:
        blockMainGeoGrp = cmds.group (n= 'blockMainGeo_grp', em=True)
        
        
    ''' -Create Rig Grp- '''
    if cmds.objExists ('blockMainRig_grp'):
        blockMainRigGrp = 'blockMainRig_grp'
        
    else:
        blockMainRigGrp = cmds.group (n= 'blockMainRig_grp', em=True)
        
        
    ''' -Create Controller Grp- '''
    if cmds.objExists ('blockController_grp'):
        blockControllerGrp = 'blockController_grp'
        
    else:
        blockControllerGrp = cmds.group (n= 'blockController_grp', em=True)
        
        
    ''' -Create Geo Layer- '''
    if cmds.objExists ('blockGeo_layer'):
        blockGeoLayer = 'blockGeo_layer'
        
    else:
        blockGeoLayer = cmds.createDisplayLayer (n= 'blockGeo_layer')
        
        
    ''' -Create Controller Layer- '''
    if cmds.objExists ('blockController_layer'):
        blockControllerLayer = 'blockController_layer'
        
    else:
        blockControllerLayer = cmds.createDisplayLayer (n= 'blockController_layer')
        
    cmds.editDisplayLayerMembers (blockControllerLayer, blockControllerGrp)
        
        
        
    ''' -Build Controller- '''
    if cmds.objExists ('blockTop*_controller'):
        cmds.select ('blockTop*_controller')
        versionCount = cmds.ls (sl=True)
        versionCount = len(versionCount) + 1
        versionCount = str(versionCount)
             
    else:
            versionCount = '1'
        
    
    blockTopScaleX = (blockScaling * horizontalCount * 0.5) + ((horizontalCount - 1) * blockSpacing * 0.5) + blockScaling
    blockTopScaleZ = (blockScaling * verticalCount * 0.5) + ((verticalCount - 1) * blockSpacing * 0.5) + blockScaling

    blockTopController = cmds.curve (n= 'blockTop' + versionCount + '_controller', p= [(-blockTopScaleX, 0, -blockTopScaleZ),
                                                                                            (blockTopScaleX, 0, -blockTopScaleZ),
                                                                                            (blockTopScaleX, 0, blockTopScaleZ),
                                                                                            (-blockTopScaleX, 0, blockTopScaleZ),
                                                                                            (-blockTopScaleX, 0, -blockTopScaleZ)],
                                                                                             d=1)


    
    

    blockController = cmds.circle (n= 'block' + versionCount + '_controller', nr= [0, 1, 0], r= blockScaling, ch= False) [0]
    radiusScaleAttr = createAttr (blockController, 'radiusScale', [0,1])
    
    
    cmds.setAttr (blockController + '.translateY', blockScaling * 10)
    cmds.makeIdentity (blockController, apply=True, t=True, r=True, s=True, n=0)
    
    cmds.parent (blockController, blockTopController)
    cmds.parent (blockTopController, blockControllerGrp)
    
    
    
    blockRigTop = cmds.group (n= 'blockRigTop' + versionCount + '_grp', p= blockMainRigGrp, em=True)
    cmds.parentConstraint (blockTopController, blockRigTop, mo=True)
    cmds.scaleConstraint (blockTopController, blockRigTop, mo=True)
    
    

    blockCount = horizontalCount * verticalCount
    
    
    ''' -Progress Bar- '''
    progressName = progressBar ('Building Blocks', blockCount)

    
    for block in range(blockCount):
        
        ''' -Block Count- '''
        if cmds.objExists ('block*_geo'):
             cmds.select ('block*_geo')
             blockVersion = cmds.ls (sl=True)
             blockVersion = len(blockVersion) + 1
             blockVersion = str(blockVersion)
            
        else:
            blockVersion = '1'


        blockGeoGrp = cmds.group (n= 'blockGeo' + blockVersion + '_grp', p= blockMainGeoGrp, em=True)
        blockRigGrp = cmds.group (n= 'blockRig' + blockVersion + '_grp', p= blockRigTop, em=True)
        
        ''' -Create Block- '''
        blockGeo = cmds.polyCube (n= 'block' + blockVersion + '_geo',
                                  w= blockScaling,
                                  h= blockScaling,
                                  d= blockScaling,
                                  ch=False) [0]
                                  
        cmds.parent (blockGeo, blockGeoGrp)
        cmds.editDisplayLayerMembers (blockGeoLayer, blockGeo)
    
    
        ''' -Extrude the Top poly- '''
        extrudeTop = cmds.polyExtrudeFacet (blockGeo + '.f[1]') [0]
        cmds.setAttr (extrudeTop + ".localScale", 0.7, 0.7, 0.7, type= 'double3')
        cmds.setAttr (extrudeTop + ".localTranslate", 0, 0, blockScaling * 0.05, type= 'double3')
          
        
        ''' -Translate Block to Ground Level- '''
        blockTop = cmds.xform (blockGeo + '.f[9]', ws=True,q=True,t=True)
        cmds.setAttr (blockGeo + '.translateY', -blockTop [1])
        
        
        
        ''' -Setup Distance- '''
        blockBaseLoc = cmds.spaceLocator (n= 'blockBase' + blockVersion + '_loc') [0]
        blockEndLoc = cmds.spaceLocator (n= 'blockEnd' + blockVersion + '_loc') [0]
        blockTopLoc = cmds.spaceLocator (n= 'blockTop' + blockVersion + '_loc') [0]
        blockLoc = cmds.spaceLocator (n= 'block' + blockVersion + '_loc') [0]
        
        cmds.parent (blockBaseLoc, blockEndLoc, blockLoc, blockTopLoc, blockRigGrp)
        
        cmds.parentConstraint (blockController, blockTopLoc, blockEndLoc)
        cmds.setAttr (blockTopLoc + '.translateY', blockScaling * 10)
        
        
        
        
        ''' -Create Top Collision- '''
        if addCollision == True:
            
            collisionBlockGeo = cmds.duplicate (blockGeo, n= 'collisionBlock' + blockVersion + '_geo') [0]
            cmds.delete (collisionBlockGeo + '.f[0]', collisionBlockGeo + '.f[2:5]')
            
            cmds.makeIdentity (collisionBlockGeo, apply=True, t=True, r=True, s=True, n=0)
            cmds.makeIdentity (collisionBlockGeo)
            
            cmds.delete (collisionBlockGeo, ch=True)
            
            
            ''' -Collision Dynamics- '''
            collisionDyn = cmds.rigidBody (collisionBlockGeo, n= 'collisionBlock' + blockVersion + '_dyn', active=False)
            cmds.hide (collisionBlockGeo)
            
            cmds.pointConstraint (blockLoc, collisionBlockGeo)

            

        
        ''' -Zero Out Block Values- '''
        cmds.makeIdentity (blockGeo, apply=True, t=True, r=True, s=True, n=0)
        cmds.makeIdentity (blockGeo)
        
        cmds.delete (blockGeo, ch=True)
        
        
        ''' -Create and Place Joints- '''
        cmds.select (cl=True)
        blockBaseJnt = cmds.joint (n= 'blockBase' + blockVersion + '_jnt')
        blockBottom = cmds.xform (blockGeo + '.f[0]', ws=True,q=True,t=True)
        cmds.setAttr (blockBaseJnt + '.translateY', blockBottom [1])
        
        blockEndJnt = cmds.joint (n= 'blockEnd' + blockVersion + '_jnt')
        cmds.setAttr (blockEndJnt + '.translateY', -blockBottom [1])
        
        cmds.setAttr (blockBaseJnt + '.radius', blockScaling * 0.1)
        cmds.setAttr (blockEndJnt + '.radius', blockScaling * 0.1)
        
        cmds.parentConstraint (blockLoc, blockEndJnt)
        cmds.parent (blockBaseJnt, blockRigGrp)
        
        
        ''' -Skin Block to Joints- '''
        blockSkin = cmds.skinCluster (blockGeo, blockBaseJnt, blockEndJnt,n= 'block' + blockVersion + '_skin') [0]
    
        cmds.skinPercent (blockSkin,
                          blockGeo + '.vtx[0:1]',
                          blockGeo + '.vtx[6:7]',
                          transformValue= [(blockBaseJnt, 1), (blockEndJnt, 0)])
        
        cmds.skinPercent (blockSkin,
                          blockGeo + '.vtx[2:5]',
                          blockGeo + '.vtx[8:11]',
                          transformValue= [(blockBaseJnt, 0), (blockEndJnt, 1)])
        
        
        ''' -Bevel the Block- '''
        if blockBevel >= 1:
            cmds.polyBevel (blockGeo + '.e[0:19]',
                            offset= 0.08,
                            offsetAsFraction= 1,
                            autoFit= 1,
                            segments= blockBevel,
                            worldSpace= 1,
                            uvAssignment=0,
                            fillNgons=1,
                            mergeVertices= 1,
                            mergeVertexTolerance= 0.0001,
                            smoothingAngle= 30,
                            miteringAngle= 180,
                            angleTolerance= 180, ch=1)
            
            cmds.bakePartialHistory( blockGeo, prePostDeformers=True )


        
        
        
        ''' -Radius Scale- '''
        try:
            blockScaleCurve1 = blockScaleCurve1
            
            blockEndConstraint = cmds.parentConstraint (blockEndLoc, name=True, q=True)
            blockEndAlias = con = cmds.parentConstraint (blockEndLoc, weightAliasList=True, q=True)

            blockEndConstraint1 = blockEndConstraint + '.' + blockEndAlias [0]
            blockEndConstraint2 = blockEndConstraint + '.' + blockEndAlias [1]
            
            cmds.connectAttr (blockScaleCurve1 + '.output', blockEndConstraint1)
            cmds.connectAttr (blockScaleCurve2 + '.output', blockEndConstraint2)
            
            

        except:
            blockEndConstraint = cmds.parentConstraint (blockEndLoc, name=True, q=True)
            blockEndAlias = con = cmds.parentConstraint (blockEndLoc, weightAliasList=True, q=True)
            
            blockEndConstraint1 = blockEndConstraint + '.' + blockEndAlias [0]
            blockEndConstraint2 = blockEndConstraint + '.' + blockEndAlias [1]
            
            cmds.setDrivenKeyframe (blockEndConstraint1, cd= radiusScaleAttr, dv= 0,v= 1)
            cmds.setDrivenKeyframe (blockEndConstraint1, cd= radiusScaleAttr, dv= 1,v= 0)
            
            cmds.setDrivenKeyframe (blockEndConstraint2, cd= radiusScaleAttr, dv= 0,v= 0)
            cmds.setDrivenKeyframe (blockEndConstraint2, cd= radiusScaleAttr, dv= 1,v= 1)
            
            blockScaleCurve1 = cmds.listConnections(blockEndConstraint1, source=True, type="animCurve") [0]
            blockScaleCurve2 = cmds.listConnections(blockEndConstraint2, source=True, type="animCurve") [0]

        
        
        
        
        ''' -Find Distance- '''
        blockDistance = cmds.shadingNode ('distanceBetween', asUtility=True, name = 'block' + blockVersion + '_distance')
        
        blockBaseLocShape = cmds.listRelatives (blockBaseLoc, shapes=True) [0]
        blockEndLocShape = cmds.listRelatives (blockEndLoc, shapes=True) [0]

        
        cmds.connectAttr (blockBaseLocShape + '.worldPosition [0]', blockDistance + '.point1')
        cmds.connectAttr (blockEndLocShape + '.worldPosition [0]', blockDistance + '.point2')
        
        
        ''' -Translate Box Anim- '''
        cmds.setDrivenKeyframe (blockLoc + '.translateY', cd= blockDistance + '.distance', dv= blockScaling * 10,v= blockScaling * 0)
        cmds.setDrivenKeyframe (blockLoc + '.translateY', cd= blockDistance + '.distance', dv= blockScaling * 9.8,v= -blockScaling * 0.2)
        
        cmds.setDrivenKeyframe (blockLoc + '.translateY', cd= blockDistance + '.distance', dv= blockScaling * 5.2,v= blockScaling * 5.2)
        cmds.setDrivenKeyframe (blockLoc + '.translateY', cd= blockDistance + '.distance', dv= blockScaling * 5,v= blockScaling * 5) 
        
        cmds.setDrivenKeyframe (blockLoc + '.translateY', cd= blockDistance + '.distance', dv= blockScaling * 0.2,v= -blockScaling * 0.2)
        cmds.setDrivenKeyframe (blockLoc + '.translateY', cd= blockDistance + '.distance', dv= blockScaling * 0,v= blockScaling * 0)
        

        ''' -Block Layout- '''
        blockScaling2 = blockScaling + blockSpacing
        

        if block == 0:
            traX = ((horizontalCount -1) * -0.5 * blockScaling2)
            traZ = ((verticalCount -1) * -0.5 * blockScaling2)
            
            
            cmds.setAttr (blockRigGrp + '.translate', traX, 0, traZ)
            horizontalCountDown1 = horizontalCount -1
            horizontalCountDown2 = horizontalCount
            verticalCountDown = 0
            
        else:
            if horizontalCountDown1 == 0:
                horizontalCountDown1 = horizontalCount
                horizontalCountDown2 = horizontalCount
                verticalCountDown = verticalCountDown - 1
                
                
            horizontalCountDown1 = horizontalCountDown1 -1
            horizontalCountDown2 = horizontalCountDown2 -1
            
            traX = (((horizontalCount -1) * -0.5 + horizontalCountDown2) * blockScaling2)
            traZ = (((verticalCount -1) * -0.5 - verticalCountDown) * blockScaling2)
            
            cmds.setAttr (blockRigGrp + '.translate', traX, 0, traZ)   
        
        
        
        cmds.parentConstraint (blockController, blockTopLoc, mo=True)
        
        

        cmds.hide (blockRigGrp)
        cmds.progressBar (progressName, e=True, step= 1)
        
        


    ''' -Close Progress Bar- '''
    progressBar ('', 0)
    
    

'''
========================================================================
---->  Create Block  <----
========================================================================
'''
    
def deleteBlocks (*args):
    if cmds.objExists ('blockMainGeo_grp'):
        cmds.delete ('blockMainGeo_grp')
    
    if cmds.objExists ('blockMainRig_grp'):
        cmds.delete ('blockMainRig_grp')
    
    if cmds.objExists ('blockController_grp'):
        cmds.delete ('blockController_grp')

    

    
'''
========================================================================
---->  Create GUI  <----
========================================================================
'''

def animBlockGUI():

    if (cmds.window ('animBlockWindow', q=True, exists=True)):
        cmds.deleteUI('animBlockWindow')



    animBlockWindow = cmds.window ('animBlockWindow' , title= 'NS Anim Block Tool v1.0',wh=(400,700))
    tab = cmds.tabLayout ()



    ''' Create Block Layout '''
    createTab =  cmds.columnLayout (adj=True)
    
    cmds.rowColumnLayout ('createRow1',nc=2,columnWidth=[(1,100),(2,50)])
    cmds.text (label = ' Horizontal Count:', width=20, height=26, align='left')
    cmds.intField ('horizontalCount', value=2, min= 1)
    
    cmds.text (label = ' Vertical Count:', width=20, height=26, align='left')
    cmds.intField ('verticalCount', value=2, min= 1)
    
    cmds.text (label = ' Block Scaling:', width=20, height=26, align='left')
    cmds.floatField ('blockScaling', value=1, precision=2)
    
    cmds.text (label = ' Block Spacing:', width=20, height=26, align='left')
    cmds.floatField ('blockSpacing', value=0, precision=2)
    
    cmds.text (label = ' Block Bevel:', width=20, height=26, align='left')
    cmds.intField ('blockBevel', value= 0, min= 0)
    
    cmds.text (label = ' Add Collision:', width=20, height=26, align='left')
    cmds.checkBox ('addCollision', label= '', value=False, align="left")
    
    cmds.setParent('..')
    cmds.button (label= 'Create Blocks', align='center', c= createBlocks)
    cmds.button (label= 'Delete Blocks', align='center', c= deleteBlocks)
    cmds.setParent(tab)
    
    
    ''' Info Block Layout '''
    infoTab =  cmds.columnLayout (adj=True)
    cmds.scrollField( editable=False, wordWrap=True, ww= False, text='####################################################\n' +
                                                                      '#                                                  #\n' +
                                                                      '#      ns_animBlockTool.py                         #\n' +
                                                                      '#                                                  #\n' +
                                                                      '#      Version 1.0 , last modified 2012-04-15      #\n' +
                                                                      '#                                                  #\n' +
                                                                      '#      Copyright (C) 2012  Nicholas Silveira       #\n' +
                                                                      '#                                                  #\n' +
                                                                      '#      Email: nicholas.silveira@gmail.com          #\n' +
                                                                      '#                                                  #\n' +
                                                                      '####################################################')
    cmds.setParent(tab)



    ''' Tab layout '''
    cmds.tabLayout (tab, edit=True, tabLabel=((createTab,"Create Blocks"),
                                              (infoTab,"Info")))
    cmds.showWindow( animBlockWindow )















