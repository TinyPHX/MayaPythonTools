#############################################################################
##
## Copyright (c) 2011 Riverbank Computing Limited <info@riverbankcomputing.com>
## 
## This file is part of PyQt.
## 
## This file may be used under the terms of the GNU General Public
## License versions 2.0 or 3.0 as published by the Free Software
## Foundation and appearing in the files LICENSE.GPL2 and LICENSE.GPL3
## included in the packaging of this file.  Alternatively you may (at
## your option) use any later version of the GNU General Public
## License if such license has been publicly approved by Riverbank
## Computing Limited (or its successors, if any) and the KDE Free Qt
## Foundation. In addition, as a special exception, Riverbank gives you
## certain additional rights. These rights are described in the Riverbank
## GPL Exception version 1.1, which can be found in the file
## GPL_EXCEPTION.txt in this package.
## 
## Please review the following information to ensure GNU General
## Public Licensing requirements will be met:
## http://trolltech.com/products/qt/licenses/licensing/opensource/. If
## you are unsure which license is appropriate for your use, please
## review the following information:
## http://trolltech.com/products/qt/licenses/licensing/licensingoverview
## or contact the sales department at sales@riverbankcomputing.com.
## 
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################


from PyQt4.uic.exceptions import WidgetPluginError


def load_plugin(plugin, plugin_globals, plugin_locals):
    """ Load the given plugin (which is an open file).  Return True if the
    plugin was loaded, or False if it wanted to be ignored.  Raise an exception
    if there was an error.
    """

    try:
        exec(plugin.read(), plugin_globals, plugin_locals)
    except ImportError:
        return False
    except Exception as e:
        raise WidgetPluginError("%s: %s" % (e.__class__, str(e)))

    return True
