"""
=====================================================================
    Tool for saving and loading skinWeights in Maya

    (c) 2013 - 2015 by Thomas Bittner
    thomasbittner@hotmail.de

    source the file and then run: showUI()


=====================================================================
    
"""




import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.mel
import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtCore, QtGui
import shiboken



def showUI():
    global mainWin
    mainWin = bSkinSaverUI()
    mainWin.show()


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(ptr), QtGui.QWidget)


class bSkinSaverUI(QtGui.QDialog):
    def __init__(self, parent=getMayaWindow()):
        super(bSkinSaverUI, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)

        tab_widget = QtGui.QTabWidget()
        objectsTab = QtGui.QWidget()
        verticesTab = QtGui.QWidget()
        
        tab_widget.addTab(objectsTab, "Objects")
        tab_widget.addTab(verticesTab, "Vertices")
        self.descLabel = QtGui.QLabel("(C) 2015 by Thomas Bittner", parent=self)       
        self.setWindowTitle('bSkinSaver 1.0')
        
        self.objectsFileLine = QtGui.QLineEdit('', parent=self)
        self.selectObjectsFileButton = QtGui.QPushButton("Set File", parent=self)
        self.saveObjectsButton = QtGui.QPushButton("Save Weights from selected Objects", parent=self)
        self.loadObjectsButton = QtGui.QPushButton("Load", parent=self)
        self.loadObjectsSelectionButton = QtGui.QPushButton("Load to Selected Object", parent=self)

        objectsLayout = QtGui.QVBoxLayout(objectsTab)
        objectsLayout.setAlignment(QtCore.Qt.AlignTop)
        objectsLayout.setSpacing(3)
        objectsFileLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        objectsFileLayout.addWidget(self.objectsFileLine)
        objectsFileLayout.addWidget(self.selectObjectsFileButton)    
        objectsLayout.addLayout(objectsFileLayout)
        
        objectsButtonLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        objectsButtonLayout.setSpacing(0)
        objectsButtonLayout.addWidget(self.saveObjectsButton)
        objectsButtonLayout.addWidget(self.loadObjectsButton)
        objectsButtonLayout.addWidget(self.loadObjectsSelectionButton)

        objectsLayout.addLayout(objectsButtonLayout)
        
        self.verticesFileLine = QtGui.QLineEdit('', parent=self)
        self.selectVerticesFileButton = QtGui.QPushButton("Set File", parent=self)
        self.saveVerticesButton = QtGui.QPushButton("Save Weights from selected Vertices", parent=self)
        self.loadVerticesButton = QtGui.QPushButton("Load onto selected Object", parent=self)
        
        verticesLayout = QtGui.QVBoxLayout(verticesTab)
        verticesLayout.setAlignment(QtCore.Qt.AlignTop)
        verticesLayout.setSpacing(3)
        verticesFileLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        verticesFileLayout.addWidget(self.verticesFileLine)
        verticesFileLayout.addWidget(self.selectVerticesFileButton)        
        verticesLayout.addLayout(verticesFileLayout)
        
        verticesButtonLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        verticesButtonLayout.setSpacing(0)
        verticesButtonLayout.addWidget(self.saveVerticesButton)
        verticesButtonLayout.addWidget(self.loadVerticesButton)
        verticesLayout.addLayout(verticesButtonLayout)
        
        
        self.layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self) 
        self.layout.addWidget(tab_widget)
        self.layout.addWidget(self.descLabel)
        self.resize(400, 10)
        
        #select files
        self.connect(self.selectObjectsFileButton, QtCore.SIGNAL("clicked()"), self.selectObjectsFile)        
        self.connect(self.selectVerticesFileButton, QtCore.SIGNAL("clicked()"), self.selectVerticesFile)        

        self.connect(self.saveObjectsButton, QtCore.SIGNAL("clicked()"), self.saveObjects)        
        self.connect(self.loadObjectsButton, QtCore.SIGNAL("clicked()"), self.loadObjects)                        
        self.connect(self.loadObjectsSelectionButton, QtCore.SIGNAL("clicked()"), self.loadObjectsSelection)   
                            
        self.connect(self.saveVerticesButton, QtCore.SIGNAL("clicked()"), self.saveVertices)        
        self.connect(self.loadVerticesButton, QtCore.SIGNAL("clicked()"), self.loadVertices)                        
                
    def selectObjectsFile(self):
        fileResult = cmds.fileDialog2()
        if fileResult != None:
            self.objectsFileLine.setText(fileResult[0])

    def selectVerticesFile(self):
        fileResult = cmds.fileDialog2()
        if fileResult != None:       
            self.verticesFileLine.setText(fileResult[0])

    
    def loadObjects(self):
        bLoadSkinValues (False, str(self.objectsFileLine.text()))
        
    def loadObjectsSelection(self):
        bLoadSkinValues (True, str(self.objectsFileLine.text()))
        
    def saveObjects(self):
        bSaveSkinValues(str(self.objectsFileLine.text()))
         
    def loadVertices(self):
        bLoadVertexSkinValues (str(self.verticesFileLine.text()))
        
    def saveVertices(self):   
        bSaveVertexSkinValues(str(self.verticesFileLine.text()))

    

bSkinPath = OpenMaya.MDagPath()
def bFindSkinCluster(objectName):    
    it = OpenMaya.MItDependencyNodes(OpenMaya.MFn.kSkinClusterFilter)
    while not it.isDone():
        fnSkinCluster = OpenMayaAnim.MFnSkinCluster(it.item())
        fnSkinCluster.getPathAtIndex(0,bSkinPath)
                
        if OpenMaya.MFnDagNode(bSkinPath.node()).partialPathName() == objectName or OpenMaya.MFnDagNode(OpenMaya.MFnDagNode(bSkinPath.node()).parent(0)).partialPathName() == objectName:
            return it.item()
        it.next()
    return False



def bLoadVertexSkinValues(inputFile):

    line = ''
    joints = []
    weights = []
    splittedStrings = []
    splittedWeights = []
    weightDoubles = OpenMaya.MDoubleArray()
    selectionList = OpenMaya.MSelectionList()
    vertexCount = 0;

    OpenMaya.MGlobal.getActiveSelectionList( selectionList );
    node = OpenMaya.MDagPath()
    component = OpenMaya.MObject()
    selectionList.getDagPath( 0, node, component );

    if not node.hasFn(OpenMaya.MFn.kTransform):
        print 'select a skinned object'



    NewTransform = OpenMaya.MFnTransform (node)
    if not NewTransform.childCount() or not NewTransform.child(0).hasFn(OpenMaya.MFn.kMesh):
        print 'select a skinned object..'

    mesh = NewTransform.child(0);
    objectName = OpenMaya.MFnDagNode(mesh).name()
    skinCluster = bFindSkinCluster(objectName)
    if not skinCluster.hasFn(OpenMaya.MFn.kSkinClusterFilter):
        print 'select a skinned object'

    fnSkinCluster = OpenMayaAnim.MFnSkinCluster(skinCluster)
    input = open(inputFile, 'r')

    joints = []
    weightLines = []
    filePosition = 0
    while True:
        line = input.readline().strip()
        if not line:
            break

        if filePosition == 0:
            vertexCount = int(line)
            filePosition = 1
        elif filePosition == 1:
            if not line.startswith("========"):
                joints.append(line)
            else:
                filePosition = 2;        
        elif filePosition == 2:
            weightLines.append(line)

    if OpenMaya.MItGeometry(node).count() != vertexCount:
        print "vertex counts don't match, result might be bad"



    # joints..
    influenceArray = OpenMaya.MDagPathArray()
    influenceStringArray = []
    influenceMapArray = OpenMaya.MIntArray()
    jointsMapArray = OpenMaya.MIntArray()

    infCount = fnSkinCluster.influenceObjects(influenceArray)
    for i in range(infCount):
        influenceStringArray.append(OpenMaya.MFnDagNode(influenceArray[i]).name())      
        influenceMapArray.append(-1)
        for k in range(len(joints)):
            if influenceStringArray[i] == joints[k]:
                influenceMapArray[i] = k

    for i in range(len(joints)):
        jointsMapArray.append(-1);

    allInfluencesInScene = True
    influenceInScene = False
    for i in range(len(joints)):
        influenceInScene = False
        for k in range(len(influenceStringArray)):
            if influenceStringArray[k] == joints[i]:
                influenceInScene = True
                jointsMapArray[i] = k

        if not influenceInScene:
            allInfluencesInScene = False
            print joints[i], ' is missing in the skinCluster'

    if not allInfluencesInScene:
        print 'There are influences missing'
        return

    extraInfluencesCount = 0

    for i in range(len(influenceStringArray)):
        jointInInfluences = False
        for k in range(len(joints)):
            if joints[k] == influenceStringArray[i]:
                jointInInfluences = True
        if not jointInInfluences:
            jointsMapArray.append(i)
            extraInfluencesCount += 1

    #load points
    fnVtxComp = OpenMaya.MFnSingleIndexedComponent()
    vtxComponents = OpenMaya.MObject()
    vtxComponents = fnVtxComp.create( OpenMaya.MFn.kMeshVertComponent )

    for i in range(len(weightLines)):
        splittedStrings = weightLines[i].split(':');
        if len(splittedStrings) > 1:
            fnVtxComp.addElement(int(splittedStrings[0]))
            splittedWeights = splittedStrings[1].split(' ')
            for k in range(len(splittedWeights)):
                weightDoubles.append(float(splittedWeights[k]))

            weightDoubles += [0] * extraInfluencesCount


    #SET WEIGHTS 
    fnSkinCluster.setWeights(bSkinPath, vtxComponents, jointsMapArray, weightDoubles, 0)

    # select the vertices
    pointSelectionList = OpenMaya.MSelectionList()
    pointSelectionList.add(OpenMaya.MDagPath(node),vtxComponents);
    OpenMaya.MGlobal.setActiveSelectionList(pointSelectionList);



def bSaveVertexSkinValues(inputFile):
    print 'saving Vertex skinWeights.. '

    selection = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList( selection );
    iterate = OpenMaya.MItSelectionList(selection);
    while not iterate.isDone():
        dagPath = OpenMaya.MDagPath()
        component = OpenMaya.MObject();
        iterate.getDagPath(dagPath, component);
        skinCluster = bFindSkinCluster(OpenMaya.MFnDagNode(dagPath).partialPathName())
        fnSkinCluster = OpenMayaAnim.MFnSkinCluster(skinCluster);
        iterate.next()

        if skinCluster.hasFn(OpenMaya.MFn.kSkinClusterFilter):
            output = open(inputFile, 'w')
            output.write(str(OpenMaya.MItGeometry(bSkinPath).count()) + '\n')

            fnVtxComp = OpenMaya.MFnSingleIndexedComponent()
            vtxComponents = OpenMaya.MObject();
            vtxComponents = fnVtxComp.create( OpenMaya.MFn.kMeshVertComponent );

            WeightArray = OpenMaya.MFloatArray()
            meshIter = OpenMaya.MItMeshVertex ( dagPath, component)
            while not meshIter.isDone():
                fnVtxComp.addElement( meshIter.index());
                meshIter.next()

            vertexCount = meshIter.count();
            scriptUtil = OpenMaya.MScriptUtil()
            infCountPtr = scriptUtil.asUintPtr()     
            fnSkinCluster.getWeights(bSkinPath, vtxComponents, WeightArray, infCountPtr)
            infCount = OpenMaya.MScriptUtil.getUint(infCountPtr)

            weightCheckArray = []
            for i in range(infCount):
                weightCheckArray.append(False)

            for i in range(vertexCount):
                for k in range(infCount):
                    if not weightCheckArray[k] and WeightArray[((i * infCount) + k)]:
                        weightCheckArray[k] = True

            #joints.. 
            InfluentsArray = OpenMaya.MDagPathArray()
            fnSkinCluster.influenceObjects(InfluentsArray);
            for i in range(infCount):
                if (weightCheckArray[i]):
                    output.write(OpenMaya.MFnDagNode(InfluentsArray[i]).name() + '\n')

            output.write('============\n')

            counter = 0;
            weightArrayString = []
            meshIter = OpenMaya.MItMeshVertex (dagPath, component)
            while not meshIter.isDone():
                weightArrayString = str(meshIter.index()) + ':'

                for k in range(infCount):
                    if weightCheckArray[k] == True:
                        weightArrayString += str(WeightArray[(counter * infCount) + k]) + ' '

                output.write(weightArrayString + '\n')
                counter += 1
                meshIter.next()

            output.close()
            iterate.next()




def bSaveSkinValues(inputFile):

    output = open(inputFile, 'w')

    selection = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selection)

    iterate = OpenMaya.MItSelectionList(selection)

    while not iterate.isDone():
        node = OpenMaya.MDagPath()
        component = OpenMaya.MObject()
        iterate.getDagPath (node, component)
        if not node.hasFn(OpenMaya.MFn.kTransform):
            print OpenMaya.MFnDagNode(node).name() + ' is not a Transform node (need to select transform node of polyMesh)'
        else:
            objectName = OpenMaya.MFnDagNode(node).name()
            newTransform = OpenMaya.MFnTransform(node)
            for childIndex in range(newTransform.childCount()):
                childObject = newTransform.child(childIndex)
                if childObject.hasFn(OpenMaya.MFn.kMesh) or childObject.hasFn(OpenMaya.MFn.kNurbsSurface) or childObject.hasFn(OpenMaya.MFn.kCurve):
                    skinCluster = bFindSkinCluster(OpenMaya.MFnDagNode(childObject).partialPathName())
                    if skinCluster is not False:
                        bSkinPath = OpenMaya.MDagPath()
                        fnSkinCluster = OpenMayaAnim.MFnSkinCluster(skinCluster)
                        fnSkinCluster.getPathAtIndex(0,bSkinPath)
                        influenceArray = OpenMaya.MDagPathArray()
                        fnSkinCluster.influenceObjects(influenceArray)
                        influentsCount = influenceArray.length()
                        #output.write(bSkinPath.partialPathName() + '\n')
                        output.write(objectName + '\n')

                        for k in range(influentsCount):
                            jointTokens = str(influenceArray[k].fullPathName()).split('|')
                            jointTokens = jointTokens[len(jointTokens)-1].split(':')
                            output.write(jointTokens[len(jointTokens)-1] + '\n')

                        output.write('============\n')

                        vertexIter = OpenMaya.MItGeometry(bSkinPath)

                        saveString = ''
                        counterValue = 0
                        while not vertexIter.isDone():
                            counterValue = counterValue + 1
                            vertex = vertexIter.component()

                            scriptUtil = OpenMaya.MScriptUtil()
                            infCountPtr = scriptUtil.asUintPtr()     
                            vtxComponents = OpenMaya.MObject()     
                            weightArray = OpenMaya.MDoubleArray()  

                            fnSkinCluster.getWeights(bSkinPath, vertex, weightArray, infCountPtr)

                            saveString = ''

                            for j in range(OpenMaya.MScriptUtil.getUint(infCountPtr)):
                                saveString += str(weightArray[j])
                                saveString += ' '

                            output.write(saveString + '\n')

                            vertexIter.next()
                        output.write('\n')


        iterate.next()

    output.close()
    print "done saving weights"





def bSkinObject(objectName, joints, weights):

    if not cmds.objExists(objectName):
        print objectName, " doesn't exist - skipping. "
        return
    
    allInfluencesInScene = True;
    jointsCheck = [] 
    for i in range(len(joints)):
        jointsCheck = joints[i]

    sceneJointTokens = []
    fileJointTokens = []

    it = OpenMaya.MItDependencyNodes ( OpenMaya.MFn.kJoint);
    # quick check:
    for jointIndex in range(len(joints)):
        jointHere = False;
        it = OpenMaya.MItDependencyNodes ( OpenMaya.MFn.kJoint)
        while not it.isDone():                
            sceneJointTokens = str(OpenMaya.MFnDagNode(it.item()).fullPathName()).split('|')
            if str(joints[jointIndex]) == str(sceneJointTokens[len(sceneJointTokens) - 1]):
                jointHere = True;

            it.next()

        if not jointHere:
            allInfluencesInScene = False;
            print 'missing influence: ', joints[jointIndex]



    if not allInfluencesInScene:
        print objectName, " can't be skinned because of missing influences."
        return

    #maya.mel.eval("undoInfo -st 0")

    
    if type(bFindSkinCluster(objectName)) != type(True):
        maya.mel.eval("DetachSkin " + objectName)

    cmd = "select "
    for i in range(len(joints)):
        cmd += " " + joints[i]

    cmd += " " + objectName
    maya.mel.eval(cmd)

    maya.mel.eval("skinCluster -tsb -mi 10");
    maya.mel.eval("select `listRelatives -p " + objectName + "`");
    maya.mel.eval("refresh")
    #maya.mel.eval("undoInfo -st 1")

    skinCluster = bFindSkinCluster(objectName)
    fnSkinCluster = OpenMayaAnim.MFnSkinCluster(skinCluster)
    InfluentsArray = OpenMaya.MDagPathArray()
    fnSkinCluster.influenceObjects(InfluentsArray)

    bSkinPath = OpenMaya.MDagPath()
    fnSkinCluster.getPathAtIndex(fnSkinCluster.indexForOutputConnection(0),bSkinPath)

    weightStrings = []
    vertexIter = OpenMaya.MItGeometry (bSkinPath)

    weightDoubles = OpenMaya.MDoubleArray()


    singleIndexed = True;
    vtxComponents = OpenMaya.MObject()
    fnVtxComp = OpenMaya.MFnSingleIndexedComponent()
    fnVtxCompDouble = OpenMaya.MFnDoubleIndexedComponent()

    
    if bSkinPath.node().apiType() == OpenMaya.MFn.kMesh:
        vtxComponents = fnVtxComp.create( OpenMaya.MFn.kMeshVertComponent )
    elif bSkinPath.node().apiType() == OpenMaya.MFn.kNurbsSurface:
        singleIndexed = False
        vtxComponents = fnVtxCompDouble.create( OpenMaya.MFn.kSurfaceCVComponent )
    elif bSkinPath.node().apiType() == OpenMaya.MFn.kNurbsCurve:
        vtxComponents = fnVtxComp.create( OpenMaya.MFn.kCurveCVComponent )
   
    #mapping joint-indices
    influenceIndices = OpenMaya.MIntArray()
    checkInfluences = []

    for k in range(InfluentsArray.length()):
        checkInfluences.append(0)
    for i in range(len(joints)):
        influenceIndices.append(-1)

    for i in range(len(joints)):
        fileJointTokens = joints[i].split('|')

        for k in range(InfluentsArray.length()):

            sceneJointTokens = str(OpenMaya.MFnDagNode(InfluentsArray[k]).fullPathName()).split('|')
            if fileJointTokens[len(fileJointTokens) - 1] == sceneJointTokens[len(sceneJointTokens) - 1]:  # changed from joints
                influenceIndices[i] = k
                checkInfluences[k] = 1        

    counterValue = 0;
    if not singleIndexed:
        currentU = 0
        currentV = 0

        cvsU = OpenMaya.MFnNurbsSurface(bSkinPath.node()).numCVsInU()
        cvsV = OpenMaya.MFnNurbsSurface(bSkinPath.node()).numCVsInV()
        formU = OpenMaya.MFnNurbsSurface(bSkinPath.node()).formInU()
        formV = OpenMaya.MFnNurbsSurface(bSkinPath.node()).formInV()
	
        if formU == 3:
            cvsU -= 3
        if formV == 3:
            cvsV -= 3
    
    
    vertexIter = OpenMaya.MItGeometry (bSkinPath)
    while not vertexIter.isDone():
        weightStrings = []
        if singleIndexed:
            fnVtxComp.addElement(counterValue)
        else:
            fnVtxCompDouble.addElement(currentU, currentV)
            currentV += 1;
            if currentV >= cvsV:
                currentV = 0
                currentU += 1

        weightStrings = weights[counterValue].split(' ');
        for i in range(len(weightStrings)):
            weightDoubles.append(float(weightStrings[i]))
        counterValue += 1
        vertexIter.next()

    #SET WEIGHTS 
    print "setting weights for  ", objectName
    fnSkinCluster.setWeights(bSkinPath, vtxComponents, influenceIndices,weightDoubles, 0)
    #Maya.mel.eval("skinPercent -normalize true " + fnSkinCluster.name() + " " + objectName)

    influenceIndices.clear();
    weightDoubles.clear();



def bLoadSkinValues(loadOnSelection, inputFile):
    joints = []
    weights = []
    PolygonObject = ""


    if loadOnSelection == True:
        selectionList = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(selectionList)
        node = OpenMaya.MDagPath()
        component = OpenMaya.MObject()
        if selectionList.length():
            selectionList.getDagPath( 0, node, component )
            if node.hasFn(OpenMaya.MFn.kTransform):
	            NewTransform = OpenMaya.MFnTransform (node)
	            if NewTransform.childCount():
		            if NewTransform.child(0).hasFn(OpenMaya.MFn.kMesh):
			            PolygonObject = str(OpenMaya.MFnDagNode(NewTransform.child(0)).partialPathName())



    if loadOnSelection and len(PolygonObject) == 0:
        print "You need to select a polygon object"
        return

    input = open(inputFile, 'r')

    FilePosition = 0
    while True:
        line = input.readline()
        if not line:
            break

        line = line.strip()

        if FilePosition is not 0:
            if not line.startswith("============"):
                if FilePosition is 1:
                    joints.append(line) 
                elif FilePosition is 2:
                    if len(line) > 0:
                        weights.append(line)
                    else:
                        bSkinObject(PolygonObject, joints, weights)
                        PolygonObject = ""
                        joints = []
                        weights = []
                        FilePosition = 0
                        if loadOnSelection == True:
                            break

            else: # it's ========
                FilePosition = 2

        else: #FilePosition is 0
            if not loadOnSelection:
                PolygonObject = line
            FilePosition = 1;
            
            if cmds.objExists(PolygonObject):
                maya.mel.eval("select " + PolygonObject)
                maya.mel.eval("refresh")






