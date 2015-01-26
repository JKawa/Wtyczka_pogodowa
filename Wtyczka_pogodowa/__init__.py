# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Wtyczka_pogodowa
                                 A QGIS plugin
 Wtyczka pogodowa dla powiatu tarnogórskiego
                             -------------------
        begin                : 2015-01-24
        copyright            : (C) 2015 by JKawa
        email                : Jolkawa91@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Wtyczka_pogodowa class from file Wtyczka_pogodowa.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Module import Wtyczka_pogodowa
    return Wtyczka_pogodowa(iface)
