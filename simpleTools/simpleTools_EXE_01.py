def env_check():
	"""
	Check for env setting. Shelf button func.
	"""
	import os, sys
	import maya.cmds as mc
	env = 'SIMPLE_TOOLS_ROOT'
	modules = 'Modules'
	title = 'Simple Tools Setup'
	os_ = mc.about(os = True)
	maya = mc.about(v = True)
	if len(maya) == 4:
		maya = maya + ' x64'
	smp_tools_root = False
	proceed = True
	if not os.getenv(env):
		message = env + ' environment variable is not correctly configured.\nDo you want to set it now? You can still run the asset manager without setting it.'
		confirm = mc.confirmDialog(t = title, m = message, b = ['Yes', 'No', 'Cancel'], db = 'Yes', cb = 'Cancel')
		if confirm != 'Cancel':
			smpTools = mc.fileDialog2(ds = 2, cap = "Select Simple Tools folder", okc = "Select", fm = 3)
			if smpTools != None:
				smp_tools_root = smpTools[0]
				if confirm == 'Yes':
					if mc.about(win = True):
						command = 'SETX ' + env + ' ' + smpTools[0]
						try:
							os.popen(command)
						except:
							message = env + ' was NOT succesfully set to: ' + smpTools[0] + '\nError: ' + command
						else:
							message = env + ' was succesfully set to: ' + smpTools[0]
							os.environ[env] = smpTools[0]
						mc.confirmDialog(t = title, m = message, b = ['OK'], db = 'OK', cb = 'OK')
					else:
						pass
			
		else:
			proceed = False
	
	if proceed:
		if not smp_tools_root:
			smp_tools_root = os.getenv(env)
		error = []
		folders = [smp_tools_root + '/st_assets/' + maya, smp_tools_root + '/' +  modules, smp_tools_root + '/' +  modules + '/' + os_, smp_tools_root + '/' +  modules + '/' + os_ + '/' + maya]
		exists = []
		appended = []
		for f in folders:
			if not os.path.isdir(f):
				error.append(f)
		if not error:
			for f in folders:
				if f not in sys.path:
					sys.path.append(f)
					appended.append(f)
				else:
					exists.append(f)
		else:
			message  = 'The folder structure for Simple Tools ran into problems.\nThese folders were not found.\n'
			for e in error:
				message = message + e + '\n'
			message = message + ''
			mc.confirmDialog(t = title, m = message, b = ['OK'], db = 'OK', cb = 'OK')
			return False
		if len(folders) != len(exists) + len(appended):
			message = 'Problem occured during sys.path.append.\nError: ' + str(len(folder)) + ':' + str(len(exists)) + ':' + str(len(appended))
			mc.confirmDialog(t = title, m = message, b = ['OK'], db = 'OK', cb = 'OK')
			return False
		else:
			return maya
	else:
		return False

proceed = env_check()
if proceed:
	import st_assets
	reload(st_assets)
	st_assets.main()
