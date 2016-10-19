#-----------------------------------------------------------------------------------------------maya-
# file: sag_instancerToGeometry.py
# version: 1.4
# date: 2012.05.05
# author: Arkadiy Demchenko (sagroth@sigillarium.com)
#----------------------------------------------------------------------------------------------------
# Converts instancer into keyframed objects:
# Put the file into maya scripts dir and run:
#
# from sag_instancerToGeometry import *
# sag_instancerToGeometry()
#----------------------------------------------------------------------------------------------------
# 2012.05.05 (v1.4) - corrected GUI for older maya versions
# 2012.04.06 (v1.3) - doesn't set visibility to off prior to the starting frame of conversion
#                   - doesn't pay attention to 'start from current frame' if custom range is defined
#
# 2011.06.19 (v1.2) - reworked GUI
#					- uses long names correctly (no problems with objects of the same name anymore)
#					- doesn't freeze source objects' rotations or error if channels have keyframes
#					- keeps input connections for instances also
#					- works with different rotation orders of source objects and instancer itself
#					- each baked object is inside it's own group which actually gets all keyframes
#					- works with any linear units of the scene (switches to cm and back, actually)
#
# 2010.06.11 (v1.1) - duplicates now maintain original input connections 
#					- only translate, rotate, scale and visibility are keyframed now
#
# 2009.11.14 (v1.0) - main release
#----------------------------------------------------------------------------------------------------

from maya.cmds import *

# GUI
def sag_instancerToGeometry():
	if window( 'sag_instancerToGeometry_win', exists = True ): 
		deleteUI( 'sag_instancerToGeometry_win' )

	window( 'sag_instancerToGeometry_win', title = 'Instancer to Geo', sizeable = False )

	columnLayout( adj = True )

	radioButtonGrp( 'sag_instancerToGeometry_win__dupOrInst_RBG', 
					labelArray2 = ['Make Duplicates', 'Make Instances'],
					numberOfRadioButtons = 2,
					select = 2 )

	separator( style = 'in' )

	checkBox( 'sag_instancerToGeometry_win__fromCurFrame_ChB', 
				align = 'left',
				label = 'Start from Current Frame', 
				value = 1 )

	radioButtonGrp( 'sag_instancerToGeometry_win__range_RBG',
					labelArray2 = ['Playback Range', 'Custom Range'], 
					numberOfRadioButtons = 2, 
					select = 1,
					onCommand1 = 'intFieldGrp( "sag_instancerToGeometry_win__range_IFG", edit = True, enable1 = False, enable2 = False )', 
					onCommand2 = 'intFieldGrp( "sag_instancerToGeometry_win__range_IFG", edit = True, enable1 = True, enable2 = True )' )

	intFieldGrp( 'sag_instancerToGeometry_win__range_IFG',
				label = '',
				numberOfFields = 2,
				columnWidth = (1, 24),
				value1 = playbackOptions( q = True, min = True ),
				value2 = playbackOptions( q = True, max = True ),
				enable1 = False,
				enable2 = False )

	sep2 = separator( style = 'in' )

	rowLayout( numberOfColumns = 2, columnWidth2 = [ 172, 40 ], columnAlign2 = [ 'center', 'center' ] )

	button( label = 'Convert',
			width = 172,
			command = 'sag_instancerToGeometry_cmd()' )

	button( label = 'Help',
			width = 48,
			command = 'showHelp( "http://www.sigillarium.com/blog/726/", absolute = True )' )

	showWindow( 'sag_instancerToGeometry_win' )


# RUN MAIN PROCEDURE WITH SETTINGS FROM GUI 
def sag_instancerToGeometry_cmd():
	dupOrInst = radioButtonGrp( 'sag_instancerToGeometry_win__dupOrInst_RBG', q = True, select = True ) - 1
	fromCurFrame = checkBox( 'sag_instancerToGeometry_win__fromCurFrame_ChB', q = True, value = True )
	rangeSpecified = radioButtonGrp( 'sag_instancerToGeometry_win__range_RBG', q = True, select = True ) - 1
	start = intFieldGrp( 'sag_instancerToGeometry_win__range_IFG', q = True, value1 = True )
	end = intFieldGrp( 'sag_instancerToGeometry_win__range_IFG', q = True, value2 = True )

	sag_instancerToGeometry_do( dupOrInst, fromCurFrame, rangeSpecified, start, end )


# MAIN PROCEDURE
def sag_instancerToGeometry_do( dupOrInst, fromCurFrame, rangeSpecified, start, end ):

	# RANGE OPTIONS
	currentFrame = currentTime( q = True )
	startFrame = playbackOptions( q = True, min = True )
	endFrame = playbackOptions( q = True, max = True )

	if rangeSpecified > 0:
		startFrame = start
		endFrame = end
	elif fromCurFrame > 0:
		startFrame = currentFrame

	# MAKE A LIST OF ALL SELECTED INSTANCERS
	instList = []

	selList = ls( selection = True )

	for each in selList:
		if objectType( each ) == 'instancer':
			instList.append( each )

	if instList == []:
		print 'No instancers selected!'
		return

	# FIND GEOMETRY, PARTICLE OBJECTS AND MAPPED ATTRIBUTES FOR INSTANCERS
	geoList = []
	ptList = []
	iamList = []

	blankInsts = []
	for each in instList:
		# MAKE A LIST OF INPUT OBJECTS
		instGeo = listConnections( each + '.inputHierarchy', source = True, destination = False, connections = False, plugs = False )

		if instGeo == None:
			print 'No geometry connected to instancer ' + each + '!'
			blankInsts.append( each )

		else:
			# MAKE A LIST OF PARTICLE OBJECTS AND THEIR INSTANCER MAPPED ATTRIBUTES
			conn = listConnections( each + '.inputPoints', source = True, destination = False, connections = False, plugs = True )

			if conn == None:
				print 'No particles connected to instancer ' + each + '!'
				blankInsts.append( each )
			else:
				geoList.append( instGeo )
				ptList.append( conn[0][:conn[0].find( '.' )] )
				iamList.append( getAttr( conn[0][:conn[0].rfind( '.' )] + '.instanceAttributeMapping' ) )

	# REMOVE INSTANCERS WITH NO GEOMETRY OR PARTICLES ATTACHED FROM THE LIST
	for each in blankInsts:
		instList.remove( each )

	# QUIT IF NO REASONABLE INSTANCERS LEFT
	if instList == []:
		return

	# SET UNITS TO CM (SINCE THAT'S WHAT PARTICLE VALUES USING NO MATTER WHAT)
	origUnits = currentUnit( query = True, linear = True )
	currentUnit( linear = 'cm' )

	# LISTS FOR STORING CONVERTED IDS AND CREATED DUPLICATES
	pids = []
	dups = []
	for inst in instList:
		pids.append( [] )
		dups.append( [] )

	# MAIN CONVERSION LOOP
	for t in xrange( int( startFrame ), int( endFrame ) + 1 ):
		currentTime( t, update = True )

		for inst in instList:
			instInd = instList.index( inst )
			instGeo = geoList[instInd]
			instPt = ptList[instInd]
			instIam = iamList[instInd]

			# GET INSTANCER ROTATION ORDER AND CONVERT IT INTO GEOMETRY ROTATION ORDER
			instRodOrig = getAttr( inst + '.rotationOrder' )
			instRodConv = { 0:0, 1:3, 2:4, 3:1, 4:2, 5:5 }
			instRod = instRodConv[ instRodOrig ]

			deadPids = pids[instList.index(inst)][:] 
			instNum = getAttr( inst + '.instanceCount' )
			for i in xrange( 0, instNum ):
				# GET GENERAL OPTIONS VALUES
				pid = int(particle( instPt, q = True, at = 'particleId', order = i )[0])
				pos = particle( instPt, q = True, at = 'worldPosition', order = i )
				scl = (1,1,1)
				shr = (0,0,0)
				vis = 1.0
				idx = 0.0
				if 'scale' in instIam:
					scl = particle( instPt, q = True, at = instIam[instIam.index( 'scale' )+1], order = i )
				if 'shear' in instIam:
					shr = particle( instPt, q = True, at = instIam[instIam.index( 'shear' )+1], order = i )
				if 'visibility' in instIam:
					vis = particle( instPt, q = True, at = instIam[instIam.index( 'visibility' )+1], order = i )[0]
				if 'objectIndex' in instIam:
					idx = particle( instPt, q = True, at = instIam[instIam.index( 'objectIndex' )+1], order = i )[0]

				# IF OBJECT INDEX IS HIGHER OR LOWER THAN AVAILABLE NUMBER OF INSTANCE OBJECTS - CLAMP TO THE CLOSEST POSSIBLE VALUE
				if idx > (len( instGeo ) - 1):
					idx = (len( instGeo ) - 1)
				elif idx < 0:
					idx = 0

				# IF SCALE ATTRIBUTE IS FLOAT INSTEAD OF VECTOR - FORCE VECTOR
				if len( scl ) < 3:
					scl = [scl[0], scl[0], scl[0]]

				# GET ROTATION OPTIONS VALUES
				rot = (0,0,0)
				if 'rotation' in instIam:
					rot = particle( instPt, q = True, at = instIam[instIam.index( 'rotation' )+1], order = i )

				# IF THE PARTICLE IS NEWBORN MAKE A DUPLICATE
				newBorn = 0

				dupName = inst.replace( '|', '_' ) + '_' + instGeo[int(idx)].replace( '|', '_' ) + '_id_' + str(pid)

				if pid not in pids[instList.index(inst)]:
					pids[instList.index(inst)].append( pid )

					# IF OBJECT WITH THE SAME NAME ALREADY EXISTS, ADD _# SUFFIX
					if objExists( dupName ):
						z = 1
						dupName += '_' + str( z )
						while objExists( dupName ):
							z += 1
							dupName = dupName[:dupName.rfind( '_' )+1] + str( z )

					if dupOrInst > 0:
						dup = instance( instGeo[int(idx)], name = dupName )[0]
						trsConns = listConnections( instGeo[int(idx)], s = True, d = False, c = True, p = True )
						if trsConns != None:
							for y in xrange( 0, len( trsConns ), 2 ):
								if not isConnected( trsConns[y+1], dup + trsConns[y][trsConns[y].rfind( '.' ):] ):
									connectAttr( trsConns[y+1], dup + trsConns[y][trsConns[y].rfind( '.' ):] )
					else:
						dup = duplicate( instGeo[int(idx)], name = dupName, inputConnections = True )[0]

					# CREATE A GROUP FOR A DUPLICATE
					dupGrp = group( em = True, name = dup + '_grp' )
					parent( dupGrp, dup )
					setAttr( dupGrp + '.translate', 0, 0, 0, type = 'double3' )
					parent( dupGrp, world = True )
					parent( dup, dupGrp )

					dup = dupGrp

					dups[instList.index(inst)].append( dup )

					if t != int( startFrame ):
						newBorn = 1
				else:
					# IF OBJECT WITH THE SAME NAME EXISTS FROM PREVIOUS BAKE, FIND THE SUFFIXED NAME FROM THIS BAKE
					if not dupName + '_grp' in dups[instList.index(inst)]:
						z = 1
						dupName += '_' + str( z )
						while not dupName + '_grp' in dups[instList.index(inst)]:
							z += 1
							dupName = dupName[:dupName.rfind( '_' )+1] + str( z )

					dup = dupName + '_grp'
					if pid in deadPids:
						deadPids.remove( pid )

				# TRANSFORM THE DUPLICATE
				setAttr( dup + '.translate', pos[0], pos[1], pos[2], type = 'double3' )
				setAttr( dup + '.scale', scl[0], scl[1], scl[2], type = 'double3' )
				setAttr( dup + '.visibility', vis )

				setAttr( dup + '.rotateOrder', instRod )
				setAttr( dup + '.rotate', rot[0], rot[1], rot[2], type = 'double3' )

				# SET KEYFRAMES
				setKeyframe( dup, inTangentType = 'linear', outTangentType = 'linear', attribute = ( 'translate', 'rotate', 'scale', 'visibility' ) )
				if newBorn > 0:
					setKeyframe( dup + '.visibility', time = currentTime( q = True ) - 1, value = 0 )
			
			# MAKE DEAD INSTANCES INVISIBLE
			for dead in deadPids:
				setKeyframe( dups[instList.index(inst)][pids[instList.index(inst)].index(dead)] + '.visibility', value = 0 )

	# GROUP DUPLICATES, DELETE STATIC CHANNELS AND APPLY EULER FILTER
	for inst in instList:
		group( dups[instList.index(inst)], name = inst + '_geo_grp', world = True )
		for obj in dups[instList.index(inst)]:
			delete( obj, staticChannels = True, unitlessAnimationCurves = False, hierarchy = 'none', controlPoints = False, shape = False )
			animCurves = listConnections( obj, source = True, destination = False, connections = False, plugs = False )
			filterCurve( animCurves )
	
	# RESTORING ORIGINAL UNITS
	currentUnit( linear = origUnits )
