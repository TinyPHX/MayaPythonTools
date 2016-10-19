-----------------------------------
Simple Tools Asset Manager v.0.9.6
-----------------------------------
Updated on September 22nd, 2013
-------------

To install, 
1. unzipped simpleTools.zip.
2. from maya shelf menu, load the shelf file shelf_Simple_Tools.mel located under ../simpleTools/shelves.
3. click on the asset manager shelf button.

-------------
PyQT.
-------------

SimpleTools comes pre-bundled with pyqt version for Maya.

If you are already using pyqt, you might want to make sure you source the pre-bundled version to avoid problems.

-------------
Tutorials
-------------

https://vimeo.com/album/2000558

Check out the tutorials, they'll get you going.

-------------
Trial version
-------------
If you have the free trial version, it will limit the number of project, sections, subsections and containers you're able to create.
All other feature are exactly the same

-------------
Contact
-------------
clapperboy@videotron.ca
use "Simple Tools Asset Manager v.0.9.6" as subject to get faster response

---------------------
v.0.9.3 release note
---------------------
added feature:
Main window will retains it's size in free window mode.
Ability to create a container from the current scene.
Trial version
---------------------
v.0.9.4 release note
---------------------
Fixed bug in WIP and improved wip workflow.
added overwrite wip capability
added rename wip capability

Added new manage texture feature.
If checked, from the preferences menu. 
It will make sure texture filepath are pointing in the containers sourceimages folder.
If the file doesn't exists, it will be copied over and the link of the texture node will be changed accordingly.
If the texture node use image sequence, it will copy all related images providing they use this naming convention <name>.#.<format>
it supports any number padding.
---------------------
v.0.9.5 release note
---------------------
Support maya 2014

snapshot ui. 
It has a new Lighting menu with options and High Quality Rendering under Renderers menu.
You can use hotkey 6 and 7 to toggle inbetween default and all light inside the ui viewport.
When opening the ui, The focus has changed to the viewport allowing you to use the 'F' hotkey to frame all object in viewport. (Focus used to be in lens floatfield.)
Fixed ui bug when viewport would take half the space.
It is non-modal now, allowing you to select object in other modelPanel.
The snap_cam gets its position from the current view making it easier to snap images.

Master/slave reference
Introduced a master/slace reference system. 
You can now reference the master file which is a copy of the latest version allowing for automatic update in scene file where the master file was referenced.
You can easily change the master file to an older version by right-clicking it. Keep in mind that you'll have to re-open a scene for the reference update.

Fixed bug where you needed to re-open main ui to display containers icons after creating a brand new project. 
Fixed Bug where preference menu checkbox state would not update properly when clicking the shelf button if the ui was already open.
Fixed a display bug in wip folders where older wip would appear empty.

Exporting selection to wip folder now preserve reference.
Added a pref to use or not namesapce when importing a wip.

Updated startup shelf code to accommodate change in python version in maya 2014
---------------------
v.0.9.6 release note
---------------------
Fixed a bug where manage file texture wouldn't copy any files if one of them didn't exists.
Fixed a bug where creating a container from selection wouldn't preserve reference.
Fixed a bug where the ui couldn't open anymore when some files were manually deleted off the projects.
Added compatibility for maya 2014 sp2 and extension where Autodesk changed the about command.

------------
what's next
------------


Import and reference options.(ns, name clash, shared node)

Specialties module(material, sequence, animation, sound, image sequence)

Export project, container

Clean sourceimages

snapping:
double node snap(start.end)
multiple snap from multiple selected

main ui:
collapse project gets a name

snap ui:
store a snap camera position.


