'''
main test module
'''
import maya.cmds as cmds
import maya.mel as mel
import test_lib

varA = test_lib.FindVar("pickles")

test_lib.Thingy01(varA)

test_lib.MelStringFunction()