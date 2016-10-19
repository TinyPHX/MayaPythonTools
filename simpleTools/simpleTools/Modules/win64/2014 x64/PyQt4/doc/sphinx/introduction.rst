Introduction
============

This is the reference guide for PyQt4 4.10.  PyQt4 is a set of
`Python <http://www.python.org>`__ bindings for v4 and v5 of the Qt application
framework from `Nokia <http://qt.nokia.com>`__.

There is a separate `PyQt4 Class Reference <classes.html>`__.

Qt is a set of C++ libraries and development tools that includes platform
independent abstractions for graphical user interfaces, networking, threads,
Unicode, regular expressions, SQL databases, SVG, OpenGL, XML, and user and
application settings.  PyQt4 implements 440 of these classes as a set of
Python modules.

PyQt4 supports the Windows, Linux, UNIX and MacOS/X platforms.

PyQt4 does not include Qt itself - you must obtain it separately.

The homepage for PyQt4 is http://www.riverbankcomputing.com/software/pyqt/.
Here you will always find the latest stable version, current development
snapshots, and the latest version of this documentation.

PyQt4 is built using the `SIP bindings generator
<http://www.riverbankcomputing.com/software/sip/>`__.  SIP must be installed in
order to build and use PyQt4.

Earlier versions of Qt are supported by PyQt v3.


License
-------

PyQt4 is licensed on all platforms under a commercial license, the GPL v2 and
the GPL v3.  Your PyQt4 license must be compatible with your Qt license.  If
you use the GPL versions then your own code must also use a compatible
license.

PyQt4, unlike Qt, is not available under the LGPL.

You can purchase a commercial PyQt4 license `here
<http://www.riverbankcomputing.com/commercial/buy>`__.


PyQt4 Components
----------------

PyQt4 comprises a number of different components.  First of all there are a
number of Python extension modules.  These are all installed in the
:mod:`PyQt4` Python package.

- The :mod:`~PyQt4.QtCore` module.  This contains the core non-GUI classes,
  including the event loop and Qt's signal and slot mechanism.  It also
  includes platform independent abstractions for Unicode, threads, mapped
  files, shared memory, regular expressions, and user and application settings.

- The :mod:`~PyQt4.QtGui` module.  This contains the majority of the GUI
  classes.

- The :mod:`~PyQt4.QtHelp` module.  This contains classes for creating and
  viewing searchable documentation.

- The :mod:`~PyQt4.QtNetwork` module.  This module contains classes for writing
  UDP and TCP clients and servers.  It includes classes that implement FTP and
  HTTP clients and support DNS lookups.

- The :mod:`~PyQt4.QtOpenGL` module.  This module contains classes that enable
  the use of OpenGL in rendering 3D graphics in PyQt4 applications.

- The :mod:`~PyQt4.QtScript` module.  This module contains classes that enable
  PyQt4 applications to be scripted using Qt's JavaScript interpreter.

- The :mod:`~PyQt4.QtScriptTools` module.  This module contains classes that
  contain additional components (e.g. a debugger) that are used with Qt's
  JavaScript interpreter.

- The :mod:`~PyQt4.QtSql` module.  This module contains classes that integrate
  with SQL databases.  It includes editable data models for database tables
  that can be used with GUI classes.  It also includes an implementation of
  `SQLite <http://www.sqlite.org>`__.

- The :mod:`~PyQt4.QtSvg` module.  This module contains classes for displaying
  the contents of SVG files.

- The :mod:`~PyQt4.QtTest` module.  This module contains functions that enable
  unit testing of PyQt4 applications.  (PyQt4 does not implement the complete
  Qt unit test framework.  Instead it assumes that the standard Python unit
  test framework will be used and implements those functions that simulate a
  user interacting with a GUI.)

- The :mod:`~PyQt4.QtWebKit` module.  This module implements a web browser
  engine based on the WebKit open source browser engine.

- The :mod:`~PyQt4.QtXml` module.  This module contains classes that implement
  SAX and DOM interfaces to Qt's XML parser.

- The :mod:`~PyQt4.QtXmlPatterns` module.  This module contains classes that
  implement XQuery and XPath support for XML and custom data models.

- The :mod:`~PyQt4.phonon` module.  This module contains classes that implement
  a cross-platform multimedia framework that enables the use of audio and video
  content in PyQt4 applications.

- The :mod:`~PyQt4.QtDBus` module.  This Unix-only module provides classes that
  support Inter-Process Communication using the D-Bus protocol.

- The :mod:`~PyQt4.QtDeclarative` module.  This module provides a declarative
  framework for building highly dynamic, custom user interfaces using QML.

- The :mod:`~PyQt4.QtMultimedia` module.  This module provides low-level
  multimedia functionality.  Application developers would normally use the
  :mod:`~PyQt4.phonon` module.

- The :mod:`~PyQt4.QtAssistant` module.  This module contains classes that
  allow Qt Assistant to be integrated with a PyQt4 application to provide
  online help.  This module is not available with Qt v4.7 and later - use the
  :mod:`~PyQt4.QtHelp` module instead.

- The :mod:`~PyQt4.QtDesigner` module.  This module contains classes that allow
  Qt Designer to be extended using PyQt4.  See :ref:`ref-designer-plugins` for
  a full description of how to do this.

- The :mod:`~PyQt4.QAxContainer` module.  This Windows-only module contains
  classes that allow access to ActiveX controls and COM objects.

- The :mod:`~PyQt4.Qt` module.  This module consolidates the classes contained
  in all of the modules described above into a single module.  This has the
  advantage that you don't have to worry about which underlying module contains
  a particular class.  It has the disadvantage that it loads the whole of the
  Qt framework, thereby increasing the memory footprint of an application.
  Whether you use this consolidated module, or the individual component modules
  is down to personal taste.

- The `DBus <http://www.freedesktop.org/wiki/Software/DBusBindings>`__ support
  module is installed as :mod:`dbus.mainloop.qt`.  This module provides support
  for the Qt event loop in the same way that the :mod:`dbus.mainloop.glib`
  included with the standard ``dbus-python`` bindings package provides support
  for the GLib event loop.  The API is described in :ref:`ref-dbus`.  It is
  only available if the ``dbus-python`` v0.80 (or later) bindings package is
  installed.  The :mod:`~PyQt4.QtDBus` module provides a more Qt-like interface
  to DBus.

- The :mod:`~PyQt4.uic` module.  This module contains classes for handling the
  ``.ui`` files created by Qt Designer that describe the whole or part of a
  graphical user interface.  It includes classes that load a ``.ui`` file and
  render it directly, and classes that generate Python code from a ``.ui`` file
  for later execution.

- The :mod:`~PyQt4.pyqtconfig` module is an extention of the SIP build system
  and is created when PyQt4 is configured.  It encapsulates all the necessary
  information about your Qt installation and makes it easier to write
  installation scripts for bindings built on top of PyQt4.  It is covered in
  detail in :ref:`ref-build-system`.

PyQt4 also contains a number of utility programs.

- :program:`pyuic4` corresponds to the Qt :program:`uic` utility.  It converts
  GUIs created using Qt Designer to Python code.

- :program:`pyrcc4` corresponds to the Qt :program:`rcc` utility.  It embeds
  arbitrary resources (eg. icons, images, translation files) described by a
  resource collection file in a Python module.

  .. note::
    It will only be included if your copy of Qt includes the XML module.

- :program:`pylupdate4` corresponds to the Qt :program:`lupdate` utility.  It
  extracts all of the translatable strings from Python code and creates or
  updates ``.ts`` translation files.  These are then used by Qt Linguist to
  manage the translation of those strings.

  .. note::
    It will only be included if your copy of Qt includes the XML module.

When PyQt4 is configured a file called :file:`PyQt4.api` is generated.  This
can be used by the QScintilla editor component (at
http://www.riverbankcomputing.com/software/qscintilla/) to enable the use of
auto-completion and call tips when editing PyQt4 code.  The API file is
installed automatically if QScintilla is already installed.

PyQt4 includes a large number of examples.  These are ports to Python of many
of the C++ examples provided with Qt.  They can be found in the
:file:`examples` directory.

Finally, PyQt4 contains the ``.sip`` files used by SIP to generate PyQt4
itself.  These can be used by developers of bindings of other Qt based class
libraries - for example `PyQwt and PyQwt3D <http://pyqwt.sourceforge.net/>`__.
