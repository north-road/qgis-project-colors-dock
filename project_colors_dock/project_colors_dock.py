# -*- coding: utf-8 -*-
"""QGIS Project Colors Dock

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""

__author__ = '(C) 2019 by Nyall Dawson'
__date__ = '18/01/2019'
__copyright__ = 'Copyright 2019, North Road'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import os
from qgis.PyQt.QtCore import (Qt,
                              QTranslator,
                              QCoreApplication)
from qgis.core import QgsApplication
from qgis.gui import QgisInterface
from project_colors_dock.gui.colors_dock import ColorsDock

VERSION = '1.0.0'


class ProjectColorsDockPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface: QgisInterface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        super().__init__()
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QgsApplication.locale()
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.colors_dock = None

    @staticmethod
    def tr(message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ProjectColorsDock', message)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.colors_dock = ColorsDock(self.iface)
        self.iface.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.colors_dock)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.iface.removeDockWidget(self.colors_dock)
