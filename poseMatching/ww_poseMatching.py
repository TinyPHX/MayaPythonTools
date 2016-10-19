file -f -new;
// untitled // 
commandPort -securityWarning -name commandportDefault;
// Error: line 1: Could not open command port commandportDefault because that name is in use. // 
// mental ray for Maya 2015 
// Mental ray for Maya: using startup file C:/Program Files/Autodesk/mentalrayForMaya2015//maya.rayrc.
// mental ray for Maya: setup
// mental ray for Maya: initialize
// mental ray for Maya: register extensions
// mental ray Node Factory: loaded
// mental ray for Maya: successfully registered
// mental ray for Maya: loading startup file: C:/Program Files/Autodesk/mentalrayForMaya2015//maya.rayrc
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/abcimport.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/abcimport.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/AdskShaderSDKWrappers.mi
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/architectural.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/architectural.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/base.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/base.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/basehair.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/basehair.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/bifrostMR.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/bifrostMR.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/bifrostphenMR.mi
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/builtin_bsdf.mi
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/builtin_object_light.mi
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/contour.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/contour.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/layering.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/layering.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/layering_phen.mi
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/mrptex.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/mrptex.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/paint.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/paint.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/physics.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/physics.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/production.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/production.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/subsurface.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/subsurface.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/surfaceSampler.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/surfaceSampler.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/userdata.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/userdata.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/useribl.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/useribl.dll
// generating Maya nodes...
// parsing C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/include/xgenMR.mi
// loading C:/Program Files/Autodesk/mentalrayForMaya2015/shaders/xgenMR.dll
// generating Maya nodes...
// AbcExport v1.0 using Alembic 1.5.4 (built May  8 2014 13:47:10)
// AbcImport v1.0 using Alembic 1.5.4 (built May  8 2014 13:47:10)
updateRendererUI;
updateRendererUI;
selectMode -object; selectType -handle 0 -ikHandle 0 -joint 0 -nurbsCurve 1 -cos 1 -stroke 1 -nurbsSurface 0 -polymesh 0 -subdiv 0 -plane 0 -lattice 0 -cluster 0 -sculpt 0 -nonlinear 0 -particleShape 0 -emitter 0 -field 0 -spring 0 -rigidBody 0 -fluid 0 -hairSystem 0 -follicle 0 -nCloth 0 -nRigid 0 -dynamicConstraint 0 -rigidConstraint 0 -collisionModel 0 -light 0 -camera 0 -texture 0 -ikEndEffector 0 -locator 0 -dimension 0;selectType -byName gpuCache 0;
createModelPanelMenu modelPanel1;
createModelPanelMenu modelPanel2;
createModelPanelMenu modelPanel3;
createModelPanelMenu modelPanel4;
buildPanelPopupMenu scriptEditorPanel1;
evalDeferred "showWindow scriptEditorPanel1Window;";
showWindow scriptEditorPanel1Window;
/*dSBRMBMI*/python("import maya.app.general.shelfEditorWindow as myTempSEW\nmyTempSEW.doIt(selectedShelfButton='shelfButton36')\ndel myTempSEW");
import maya.app.general.shelfEditorWindow as myTempSEW
myTempSEW.doIt(selectedShelfButton='shelfButton36')
del myTempSEW
global string $gShelfTopLevel; string $tmp=$gShelfTopLevel;
// Result: MayaWindow|toolBar2|MainShelfLayout|formLayout14|ShelfLayout // 
if(! `exists shelfLabel_uiToMel` ) {source "shelfLabel.mel";};
selectCurrentExecuterControl;
Z:\Casino Core\SORT LATER\Logo\3d_test\A
# Error: invalid syntax
#   File "<maya console>", line 2
#     Z:\Casino Core\SORT LATER\Logo\3d_test\A
#      ^
# SyntaxError: invalid syntax # 
commandScrollFieldPromptForFile "Save Selected" "C:/Users/wwilson/Documents/maya/2015-x64/prefs/scriptEditorTemp" 1 "python";
np_getPrimaryProjectFileRules 0;
// Result: Scenes scene scenes Templates templates assets Images images images Source Images sourceImages sourceimages Render Data renderData renderData Clips clips clips Sound sound sound Scripts scripts scripts Disk Cache diskCache data Movies movie movies Translator Data translatorData data AutoSave autoSave autosave // 
(u"C:/Users/wwilson/Documents/maya/scripts/FKIK_switching/ww_FKIK_switching.py").replace("\\","/");
# Result: C:/Users/wwilson/Documents/maya/scripts/FKIK_switching/ww_FKIK_switching.py # 
// Result: C:/Users/wwilson/Documents/maya/scripts/FKIK_switching/ww_FKIK_switching.py // 
shelfButtonPMO "MayaWindow|toolBar2|MainShelfLayout|formLayout14|ShelfLayout|Custom||popupMenu68" 1 "shelfButton41" "/*dSBRMBMI*/";
/*dSBRMBMI*/python("import maya.app.general.shelfEditorWindow as myTempSEW\nmyTempSEW.doIt(selectedShelfButton='shelfButton41')\ndel myTempSEW");
import maya.app.general.shelfEditorWindow as myTempSEW
myTempSEW.doIt(selectedShelfButton='shelfButton41')
del myTempSEW
global string $gShelfTopLevel; string $tmp=$gShelfTopLevel;
// Result: MayaWindow|toolBar2|MainShelfLayout|formLayout14|ShelfLayout // 
if(! `exists shelfLabel_uiToMel` ) {source "shelfLabel.mel";};
shelfButtonPMO "MayaWindow|toolBar2|MainShelfLayout|formLayout14|ShelfLayout|Custom||popupMenu66" 1 "shelfButton39" "/*dSBRMBMI*/";
/*dSBRMBMI*/python("import maya.app.general.shelfEditorWindow as myTempSEW\nmyTempSEW.doIt(selectedShelfButton='shelfButton39')\ndel myTempSEW");
import maya.app.general.shelfEditorWindow as myTempSEW
myTempSEW.doIt(selectedShelfButton='shelfButton39')
del myTempSEW
global string $gShelfTopLevel; string $tmp=$gShelfTopLevel;
// Result: MayaWindow|toolBar2|MainShelfLayout|formLayout14|ShelfLayout // 
if(! `exists shelfLabel_uiToMel` ) {source "shelfLabel.mel";};
shelfButtonPMO "MayaWindow|toolBar2|MainShelfLayout|formLayout14|ShelfLayout|Custom||popupMenu65" 1 "shelfButton38" "/*dSBRMBMI*/";
/*dSBRMBMI*/python("import maya.app.general.shelfEditorWindow as myTempSEW\nmyTempSEW.doIt(selectedShelfButton='shelfButton38')\ndel myTempSEW");
import maya.app.general.shelfEditorWindow as myTempSEW
myTempSEW.doIt(selectedShelfButton='shelfButton38')
del myTempSEW
global string $gShelfTopLevel; string $tmp=$gShelfTopLevel;
// Result: MayaWindow|toolBar2|MainShelfLayout|formLayout14|ShelfLayout // 
if(! `exists shelfLabel_uiToMel` ) {source "shelfLabel.mel";};
shelfButtonPMO "MayaWindow|toolBar2|MainShelfLayout|formLayout14|ShelfLayout|Custom||popupMenu57" 1 "shelfButton30" "/*dSBRMBMI*/";
/*dSBRMBMI*/python("import maya.app.general.shelfEditorWindow as myTempSEW\nmyTempSEW.doIt(selectedShelfButton='shelfButton30')\ndel myTempSEW");
import maya.app.general.shelfEditorWindow as myTempSEW
myTempSEW.doIt(selectedShelfButton='shelfButton30')
del myTempSEW
global string $gShelfTopLevel; string $tmp=$gShelfTopLevel;
// Result: MayaWindow|toolBar2|MainShelfLayout|formLayout14|ShelfLayout // 
if(! `exists shelfLabel_uiToMel` ) {source "shelfLabel.mel";};
commandScrollFieldPromptForFile "Save Selected" "C:/Users/wwilson/Documents/maya/2015-x64/prefs/scriptEditorTemp" 1 "python";
np_getPrimaryProjectFileRules 0;
// Result: Scenes scene scenes Templates templates assets Images images images Source Images sourceImages sourceimages Render Data renderData renderData Clips clips clips Sound sound sound Scripts scripts scripts Disk Cache diskCache data Movies movie movies Translator Data translatorData data AutoSave autoSave autosave // 
commandScrollFieldPromptForFile "Save Selected" "C:/Users/wwilson/Documents/maya/2015-x64/scripts/" 1 "mel";
np_getPrimaryProjectFileRules 0;
// Result: Scenes scene scenes Templates templates assets Images images images Source Images sourceImages sourceimages Render Data renderData renderData Clips clips clips Sound sound sound Scripts scripts scripts Disk Cache diskCache data Movies movie movies Translator Data translatorData data AutoSave autoSave autosave // 
(u"C:/Users/wwilson/Documents/maya/scripts/poseMatching/ww_poseMatching.py").replace("\\","/");
# Result: C:/Users/wwilson/Documents/maya/scripts/poseMatching/ww_poseMatching.py # 
// Result: C:/Users/wwilson/Documents/maya/scripts/poseMatching/ww_poseMatching.py // 
