########################
#file: zbw_shapeScale.py
#Author: zeth willie
#Contact: zeth@catbuks.com, www.williework.blogspot.com
#Date Modified: 04/27/13
#To Use: type in python window  "import zbw_shapeScale as zss; zss.shapeScale()"
#Notes/Descriptions: Use to change the shape of a nurbsCurve by scaling the cv's
########################


import maya.cmds as cmds

widgets = {}

def shapeScaleUI():
    """UI for the script"""

    if (cmds.window("ssWin", exists=True)):
        cmds.deleteUI("ssWin", window=True)
        #cmds.winPref("shapeScaleWin", remove=True)

    widgets["win"] = cmds.window("ssWin", t="zbw_shapeScale", w=400, h=75, s=False)

    widgets["colLo"] = cmds.columnLayout("mainCLO", w=400, h=75)
    widgets["formLO"] = cmds.formLayout(nd=100, w=400)
    cmds.separator(h=10)
    widgets["slider"] = cmds.floatSliderGrp("slider", f=False, l="Scale", min=0.01, max=2, pre=3, v=1, adj=3, cal=([1, "left"], [2, "left"], [3, "left"]), cw=([1, 50], [2,220]), cc= shapeScaleExecute)
    cmds.separator(h=10)
    widgets["scaleFFG"] = cmds.floatFieldGrp(v1=100, pre= 1, l="Scale %", en1=True, w=110, cw=([1,50],[2,50]), cal=([1,"left"], [2,"left"]))
    widgets["scaleDoBut"] = cmds.button(l="Scale", w= 160, h=25, bgc=(.2,.4,.2), c=manualScale)
    widgets["trackerFFG"] = cmds.floatFieldGrp(l="Change", w=100, v1=100, pre=1, en1=False, cw=([1,45],[2,50]), cal=([1,"left"], [2,"right"]), bgc=(.2,.2,.2))
    widgets["clearBut"] = cmds.button(l="RESET", w=45, bgc=(.2,.2,.2), c=resetScale)

    widgets["origBut"] = cmds.button(l="ORIG", w=45, bgc=(.2,.2,.2), c=origScale)

    #attach to form layout
    cmds.formLayout(widgets["formLO"], e=True, attachForm=[(widgets["slider"], 'top', 5), (widgets["slider"], 'left', 5)])
    cmds.formLayout(widgets["formLO"], e=True, attachForm=[(widgets["scaleFFG"], 'top', 34), (widgets["scaleFFG"], 'left', 5)])
    cmds.formLayout(widgets["formLO"], e=True, attachForm=[(widgets["scaleDoBut"], 'top', 34), (widgets["scaleDoBut"], 'left', 120)])
    cmds.formLayout(widgets["formLO"], e=True, attachForm=[(widgets["clearBut"], 'top', 34), (widgets["clearBut"], 'left', 344)])
    cmds.formLayout(widgets["formLO"], e=True, attachForm=[(widgets["trackerFFG"], 'top', 5), (widgets["trackerFFG"], 'left', 290)])
    cmds.formLayout(widgets["formLO"], e=True, attachForm=[(widgets["origBut"], 'top', 34), (widgets["origBut"], 'left', 290)])

    cmds.showWindow(widgets["win"])
    cmds.window(widgets["win"], e=True, w=400, h=75)

def resetScale(*args):
    """resets the scale float field"""

    cmds.floatFieldGrp(widgets["trackerFFG"], e=True, v1=100)

def origScale(*args):
    """scales the object by the inverse of the currentScale (as measured by the tracker floatfield). So if everything was reset when you started it will
    undo all subsequent scaling operations"""

    currScale = cmds.floatFieldGrp(widgets["trackerFFG"], q=True, v1=True)
    scaleVal = 100/currScale
    # print "%s = factor"%factor
    # scaleVal = currScale * factor/100
    cmds.floatFieldGrp(widgets["trackerFFG"], e=True, v1=scaleVal*currScale)

    sel = cmds.ls(sl=True, type="transform")
    if sel:
        for obj in sel:
            #decide on object type
            objShape = cmds.listRelatives(obj, s=True)
            shapeType = cmds.objectType(objShape)

            cmds.select(cl=True)
            if shapeType == "nurbsSurface" or shapeType == "nurbsCurve":
                #get the components
                cvs = cmds.select((obj + ".cv[*]"))
                cmds.scale(scaleVal, scaleVal, scaleVal)
            elif shapeType == "mesh":
                #get the components
                cvs = cmds.select((obj + ".vtx[*]"))
                cmds.scale(scaleVal, scaleVal, scaleVal)
            else:
                cmds.warning("%s isn't a nurbs or poly object, so it was skipped")

    #clear and reselect all
    if sel:
        cmds.select(cl=True)
        cmds.select(sel)
        cmds.floatFieldGrp(widgets["scaleFFG"], e=True, v1=scaleVal*100)


def manualScale(*args):
    """uses the float field group to manually scale the object by that amount"""
    origScale = cmds.floatFieldGrp(widgets["trackerFFG"], q=True, v1=True)

    #get value from field
    scalePer = cmds.floatFieldGrp(widgets["scaleFFG"] , q=True, v1=True)
    scaleVal = scalePer/100
    #scaleShapes
    sel = cmds.ls(sl=True, type="transform")
    if sel:
        for obj in sel:
            #decide on object type
            objShape = cmds.listRelatives(obj, s=True)
            shapeType = cmds.objectType(objShape)

            cmds.select(cl=True)
            if shapeType == "nurbsSurface" or shapeType == "nurbsCurve":
                #get the components
                cvs = cmds.select((obj + ".cv[*]"))
                cmds.scale(scaleVal, scaleVal, scaleVal)
            elif shapeType == "mesh":
                #get the components
                cvs = cmds.select((obj + ".vtx[*]"))
                cmds.scale(scaleVal, scaleVal, scaleVal)
            else:
                cmds.warning("%s isn't a nurbs or poly object, so it was skipped")

    #clear and reselect all
    if sel:
        cmds.select(cl=True)
        cmds.select(sel)
        newScale = origScale * scaleVal
        cmds.floatFieldGrp(widgets["trackerFFG"], e=True, v1=newScale)

def shapeScaleExecute(*args):
    """takes the components of the selected obj and scales them according the slider"""

    origScale = cmds.floatFieldGrp(widgets["trackerFFG"], q=True, v1=True)

    oldScale = 100

    #get the selected obj
    sel = cmds.ls(sl=True, type="transform")

    #get the value from the slider
    scaleVal = cmds.floatSliderGrp(widgets["slider"] , q=True, v=True)

    if sel:
        for obj in sel:
            #decide on object type
            objShape = cmds.listRelatives(obj, s=True)
            shapeType = cmds.objectType(objShape)

            cmds.select(cl=True)
            if shapeType == "nurbsSurface" or shapeType == "nurbsCurve":
                #get the components
                cvs = cmds.select((obj + ".cv[*]"))
                cmds.scale(scaleVal, scaleVal, scaleVal)
                #fix scale adjuster
                newScale = oldScale * scaleVal
                cmds.floatFieldGrp(widgets["scaleFFG"], e=True, v1=newScale)
            elif shapeType == "mesh":
                #get the components
                cvs = cmds.select((obj + ".vtx[*]"))
                cmds.scale(scaleVal, scaleVal, scaleVal)
                #fix scale adjuster
                newScale = oldScale * scaleVal
                cmds.floatFieldGrp(widgets["scaleFFG"], e=True, v1=newScale)
            else:
                cmds.warning("%s isn't a nurbs or poly object, so it was skipped")

    #reset slider to 1, so we don't stack scalings
    cmds.floatSliderGrp(widgets["slider"], e=True, v=1)

    #clear and reselect all
    if sel:
        cmds.select(cl=True)
        cmds.select(sel)
        newScale = origScale * scaleVal
        cmds.floatFieldGrp(widgets["trackerFFG"], e=True, v1=newScale)

def shapeScale():
    """Use this to start the script!"""

    shapeScaleUI()