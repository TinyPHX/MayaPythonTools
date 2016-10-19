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


import sys
import logging

from PyQt4.uic import compileUi, loadUi


class Driver(object):
    """ This encapsulates access to the pyuic functionality so that it can be
    called by code that is Python v2/v3 specific.
    """

    LOGGER_NAME = 'PyQt4.uic'

    def __init__(self, opts, ui_file):
        """ Initialise the object.  opts is the parsed options.  ui_file is the
        name of the .ui file.
        """

        if opts.debug:
            logger = logging.getLogger(self.LOGGER_NAME)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(name)s: %(message)s"))
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

        self._opts = opts
        self._ui_file = ui_file

    def invoke(self):
        """ Invoke the action as specified by the parsed options.  Returns 0 if
        there was no error.
        """

        if self._opts.preview:
            return self._preview()

        self._generate()

        return 0

    def _preview(self):
        """ Preview the .ui file.  Return the exit status to be passed back to
        the parent process.
        """

        from PyQt4 import QtGui

        app = QtGui.QApplication([self._ui_file])
        widget = loadUi(self._ui_file)
        widget.show()

        return app.exec_()

    def _generate(self):
        """ Generate the Python code. """

        if sys.hexversion >= 0x03000000:
            if self._opts.output == '-':
                from io import TextIOWrapper

                pyfile = TextIOWrapper(sys.stdout.buffer, encoding='utf8')
            else:
                pyfile = open(self._opts.output, 'wt', encoding='utf8')
        else:
            if self._opts.output == '-':
                pyfile = sys.stdout
            else:
                pyfile = open(self._opts.output, 'wt')

        compileUi(self._ui_file, pyfile, self._opts.execute, self._opts.indent,
                self._opts.pyqt3_wrapper, self._opts.from_imports)

    def on_IOError(self, e):
        """ Handle an IOError exception. """

        sys.stderr.write("Error: %s: \"%s\"\n" % (e.strerror, e.filename))

    def on_SyntaxError(self, e):
        """ Handle a SyntaxError exception. """

        sys.stderr.write("Error in input file: %s\n" % e)

    def on_NoSuchWidgetError(self, e):
        """ Handle a NoSuchWidgetError exception. """

        if e.args[0].startswith("Q3"):
            sys.stderr.write("Error: Q3Support widgets are not supported by PyQt4.\n")
        else:
            sys.stderr.write(str(e) + "\n")

    def on_Exception(self, e):
        """ Handle a generic exception. """

        if logging.getLogger(self.LOGGER_NAME).level == logging.DEBUG:
            import traceback

            traceback.print_exception(*sys.exc_info())
        else:
            from PyQt4 import QtCore

            sys.stderr.write("""An unexpected error occurred.
Check that you are using the latest version of PyQt and send an error report to
support@riverbankcomputing.com, including the following information:

  * your version of PyQt (%s)
  * the UI file that caused this error
  * the debug output of pyuic4 (use the -d flag when calling pyuic4)
""" % QtCore.PYQT_VERSION_STR)
