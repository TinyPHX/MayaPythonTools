import maya.cmds as cmds
from functools import partial

widgets = {}

def spaceMatchUI():
	if (cmds.window('window', exists = True)):
		cmds.deleteUI('window', window = True)
			
	#create window
	widgets['win'] = cmds.window('window', title = 'pose space matcher', w = 300, h = 400)
	
	#create top frame
	widgets['topFrame'] = cmds.frameLayout(l = 'object selection', w = 300 )
	widgets['topColumn'] = cmds.columnLayout(adjustableColumn = True)
	
	#create some test
	widgets['winText'] = cmds.text(label = 'by: Wesley Wilson')
	
	#create animation button
	widgets['animCheck'] = cmds.radioButtonGrp( label='set keyframes?', labelArray2 = ['Yes', 'No'], nrb = 2, sl = 2 )
	
	#create object selection area
	widgets['objTFG'] = cmds.textFieldGrp(l = 'select object', w = 300)
	widgets['objButton'] = cmds.button(l = 'select obj', w = 300, c = getObj)
	
	#go back to window
	cmds.setParent(widgets['win'])
	
	#create bottom frame
	widgets['bottomFrame'] = cmds.frameLayout(l = 'space selection', w = 300 )
	widgets['bottomColumn'] = cmds.columnLayout()
	
	#show window
	cmds.showWindow(widgets['win'])
	
	
	
	
def getObj(*args):
	#clear list
	clearList()
	
	#getselected object and put it in field
	sel = cmds.ls(sl = True)[0]
	cmds.textFieldGrp(widgets['objTFG'], e = True, text = sel)

	#for that attr grab all of the values
	values = cmds.attributeQuery('parentTo', node = sel, listEnum = True)[0].split(':')
	print values
	
	for i in range(len(values)):
		widgets['button_%02i'%i] = cmds.button(l = values[i], w = 300, h = 50, c = partial(spaceMatch, i))
		
		
def clearList(*args):
	cmds.deleteUI(widgets['bottomColumn'])
	widgets['bottomColumn'] = cmds.columnLayout( p = widgets['bottomFrame'] )


def spaceMatch(value, *args):
	obj = cmds.textFieldGrp(widgets['objTFG'], q = True, text = True)
	obj_grp = '%s_grp'%obj
	animCheck =  cmds.radioButtonGrp(widgets['animCheck'], q = True, sl = True)

	#get ws trans and ws rots of object n obj_grp
	wsTrans_obj = cmds.xform(obj, q = True, ws = True, t = True)
	wsRots_obj = cmds.xform(obj, q = True, ws = True, ro = True)

	if animCheck == 1:
		#set keyframes @ frame before for the obj's attrs
		for each in ['o_tx','o_ty','o_tz','o_rx','o_ry','o_rz','parentTo','translate','rotate']:
			cmds.setKeyframe(obj, at = each, t = (cmds.currentTime(q = True) - 1))
	
	#set switch
	cmds.setAttr('%s.parentTo'%obj, value)
	
	#set ws trans  and ws rots of object
	cmds.xform(obj, ws = True, t = wsTrans_obj)
	cmds.xform(obj, ws = True, ro = wsRots_obj)

	if animCheck == 1:
		#set NEW keyframes @ current frame for the obj's attrs
		for each in ['o_tx','o_ty','o_tz','o_rx','o_ry','o_rz','parentTo','translate','rotate']:
			cmds.setKeyframe(obj, at = each, t = cmds.currentTime(q = True))