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

from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsProjectColorScheme
)
from qgis.gui import (
    QgsDockWidget,
    QgsPanelWidgetStack,
    QgsPanelWidget,
    QgsColorSchemeList)
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.PyQt.QtCore import QTimer


class ColorsDock(QgsDockWidget):
    """
    Custom dock widget for modfication of project colors
    """

    def __init__(self, iface):
        super().__init__()
        self.iface = iface

        stack = QgsPanelWidgetStack()

        self.main_panel = QgsPanelWidget()
        self.main_panel.setDockMode(True)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setMargin(0)  # pylint: disable=no-value-for-parameter
        self.main_panel.setLayout(layout)
        self.setWindowTitle(self.tr('Project Colors'))
        self.setObjectName('project_colors_dock')

        scheme = [s for s in QgsApplication.colorSchemeRegistry().schemes() if isinstance(s, QgsProjectColorScheme)]
        self.color_list = QgsColorSchemeList(None, scheme[0])
        layout.addWidget(self.color_list)

        # defer updates for a short timeout -- prevents flooding with signals
        # when doing lots of color changes, improving app responsiveness
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(100)

        self.block_updates = False

        def apply_colors():
            """
            Applies color changes to canvas and project
            """
            self.block_updates = True
            self.color_list.saveColorsToScheme()
            self.block_updates = False
            self.iface.mapCanvas().refreshAllLayers()

        self.timer.timeout.connect(apply_colors)

        def colors_changed():
            """
            Triggers a deferred update of the project colors
            """
            if self.timer.isActive():
                return
            self.timer.start()

        self.color_list.model().dataChanged.connect(colors_changed)
        stack.setMainPanel(self.main_panel)
        self.setWidget(stack)

        QgsProject.instance().projectColorsChanged.connect(self.repopulate_list)

    def repopulate_list(self):
        """
        Rebuild the colors list when project colors are changed
        """
        if self.block_updates:
            return
        scheme = [s for s in QgsApplication.colorSchemeRegistry().schemes() if isinstance(s, QgsProjectColorScheme)][0]
        self.color_list.setScheme(scheme)
