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


from PyQt4.uic.exceptions import NoSuchWidgetError


def invoke(driver):
    """ Invoke the given command line driver.  Return the exit status to be
    passed back to the parent process.
    """

    exit_status = 1

    try:
        exit_status = driver.invoke()

    except IOError as e:
        driver.on_IOError(e)

    except SyntaxError as e:
        driver.on_SyntaxError(e)

    except NoSuchWidgetError as e:
        driver.on_NoSuchWidgetError(e)

    except Exception as e:
        driver.on_Exception(e)

    return exit_status
