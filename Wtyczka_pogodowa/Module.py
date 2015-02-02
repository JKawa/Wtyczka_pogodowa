# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Wtyczka_pogodowa
                                 A QGIS plugin
 Wtyczka pogodowa dla powiatu tarnogórskiego
                              -------------------
        begin                : 2015-01-24
        git sha              : $Format:%H$
        copyright            : (C) 2015 by JKawa
        email                : Jolkawa91@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from Module_dialog import Wtyczka_pogodowaDialog
import os.path
import qgis.core
import qgis.utils
import qgis.gui
import urllib
from qgis.utils import iface
import json 
import time
from pprint import pprint 
from datetime import  datetime
from datetime import timedelta
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import *
from PyQt4.QtGui import QTextDocument
from PyQt4 import QtGui
from PyQt4 import QtCore
import os
from qgis.core import *
from qgis.gui import *
import qgis.gui
import urllib
import json 
import time
from pprint import pprint 
from datetime import  datetime
from datetime import timedelta
from PyQt4.QtCore import QVariant
import os



class Wtyczka_pogodowa:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Wtyczka_pogodowa_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = Wtyczka_pogodowaDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Wtyczka_pogodowa')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Wtyczka_pogodowa')
        self.toolbar.setObjectName(u'Wtyczka_pogodowa')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Wtyczka_pogodowa', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Wtyczka_pogodowa/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'  '),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Wtyczka_pogodowa'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            czasutw=os.stat("C:\Users\Jolanta\.qgis2\python\plugins\Wtyczka_pogodowa\dane.json").st_mtime
            czas_otw=time.time()
            delta_czas= timedelta(seconds=czas_otw)-timedelta(seconds=czas_otw)
            try:
                plik=open(os.path.join("C:\Users\Jolanta\.qgis2\python\plugins\Wtyczka_pogodowa\dane.json"),'r')
            except IOError:
                plik=open(os.path.join("C:\Users\Jolanta\.qgis2\python\plugins\Wtyczka_pogodowa\dane.json"),'w+')
            plikdane=plik.read()
            plik.close()
            try:
                dane=json.loads(plikdane)
                if 'data' in dane:
                    t_dane=dane['data']
                else:
                    t_dane=0
            except ValueError:
                t_dane=0
        if delta_czas >=timedelta(seconds=600):
            plikk=open(os.path.join("C:\Users\Jolanta\.qgis2\python\plugins\Wtyczka_pogodowa\dane.json"),'w+')
            odp=urllib.urlopen( "http://api.openweathermap.org/data/2.5/group?id=3096472%2C3100946%2C3099230%2C3083440%2C3092906%2C3103402%2C3082914%2C3086586&units=metric%20%3E%3E%20%22%29")
            danee=json.loads(odp.read())
            odp.close()
            plikk.write(json.dumps(danee,plikk))
            plikk.close()
        else:
            danee=dane
        pogoda=danee['list']
        wojew=qgis.core.QgsVectorLayer("C:\Users\Jolanta\.qgis2\python\plugins\Wtyczka_pogodowa\Export_Output.shp","wojew","ogr")   
        warstwa=QgsVectorLayer("Point", "Pogoda", "memory")
        warstwa.setCrs( QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId) )
        warstwa.startEditing()
        warstwa.LayerData=warstwa.dataProvider()
        warstwa.LayerData.addAttributes([QgsField('Miasto', QVariant.String),QgsField("temperatura",QVariant.Double),QgsField("temperaturaMax",QVariant.Double),QgsField("tempeaturaMin",QVariant.Double),QgsField("ciśnienie",QVariant.Double),QgsField("wilgotność",QVariant.Double),QgsField("prędkość_wiatru",QVariant.Double),QgsField("kierune_wiatru",QVariant.Double),QgsField("zachmurzenie",QVariant.Double)])
        warstwa.updateFields()
        warstwa.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(wojew)
        QgsMapLayerRegistry.instance().addMapLayer(warstwa)
        TarG=danee["list"]
        Katowice=TarG[0]
        Katowice_coord=Katowice["coord"]
        Katowice_main=Katowice["main"]
        Katowice_wind=Katowice["wind"]
        Katowice_clouds=Katowice["clouds"]
        Katowice_weather=Katowice["weather"]
        Katowice_weather1=Katowice_weather[0]
        Katowice_descr=Katowice_weather1["description"]
        Katowice_name=Katowice["name"]
        Katowice_temp=Katowice_main["temp"]
        Katowice_temp_min=Katowice_main["temp_min"]
        Katowice_temp_max=Katowice_main["temp_max"]
        Katowice_pressure=Katowice_main['pressure']
        Katowice_humidity=Katowice_main["humidity"]
        Katowice_wind_speed=Katowice_wind["speed"]
        Katowice_wind_dir=Katowice_wind["deg"]
        Katowice_clouds=Katowice_clouds["all"]
        war_Katowice=[Katowice_name,Katowice_temp,Katowice_temp_max,Katowice_temp_min,Katowice_pressure,Katowice_humidity,Katowice_wind_speed,Katowice_wind_dir,Katowice_clouds]
        Katowice_lat=Katowice_coord["lat"]
        Katowice_lon=Katowice_coord["lon"]
        Czestochowa=TarG[1]
        Czestochowa_coord=Czestochowa["coord"]
        Czestochowa_main=Czestochowa["main"]
        Czestochowa_wind=Czestochowa["wind"]
        Czestochowa_clouds=Czestochowa["clouds"]
        Czestochowa_weather=Czestochowa["weather"]
        Czestochowa_weather1=Czestochowa_weather[0]
        Czestochowa_descr=Czestochowa_weather1["description"]
        Czestochowa_name=Czestochowa["name"]
        Czestochowa_temp=Czestochowa_main["temp"]
        Czestochowa_temp_min=Czestochowa_main["temp_min"]
        Czestochowa_temp_max=Czestochowa_main["temp_max"]
        Czestochowa_pressure=Czestochowa_main['pressure']
        Czestochowa_humidity=Czestochowa_main["humidity"]
        Czestochowa_wind_speed=Czestochowa_wind["speed"]
        Czestochowa_wind_dir=Czestochowa_wind["deg"]
        Czestochowa_clouds=Czestochowa_clouds["all"]
        war_Czestochowa=[Czestochowa_name,Czestochowa_temp,Czestochowa_temp_max,Czestochowa_temp_min,Czestochowa_pressure,Czestochowa_humidity,Czestochowa_wind_speed,Czestochowa_wind_dir,Czestochowa_clouds]
        Czestochowa_lat=Czestochowa_coord["lat"]
        Czestochowa_lon=Czestochowa_coord["lon"]
        Bielsko_Biala=TarG[5]
        Bielsko_Biala_coord=Bielsko_Biala["coord"]
        Bielsko_Biala_main=Bielsko_Biala["main"]
        Bielsko_Biala_wind=Bielsko_Biala["wind"]
        Bielsko_Biala_clouds=Bielsko_Biala["clouds"]
        Bielsko_Biala_weather=Bielsko_Biala["weather"]
        Bielsko_Biala_weather1=Bielsko_Biala_weather[0]
        Bielsko_Biala_descr=Bielsko_Biala_weather1["description"]
        Bielsko_Biala_name=Bielsko_Biala["name"]
        Bielsko_Biala_temp=Bielsko_Biala_main["temp"]
        Bielsko_Biala_temp_min=Bielsko_Biala_main["temp_min"]
        Bielsko_Biala_temp_max=Bielsko_Biala_main["temp_max"]
        Bielsko_Biala_pressure=Bielsko_Biala_main['pressure']
        Bielsko_Biala_humidity=Bielsko_Biala_main["humidity"]
        Bielsko_Biala_wind_speed=Bielsko_Biala_wind["speed"]
        Bielsko_Biala_wind_dir=Bielsko_Biala_wind["deg"]
        Bielsko_Biala_clouds=Bielsko_Biala_clouds["all"]
        war_Bielsko_Biala=[Bielsko_Biala_name,Bielsko_Biala_temp,Bielsko_Biala_temp_max,Bielsko_Biala_temp_min,Bielsko_Biala_pressure,Bielsko_Biala_humidity,Bielsko_Biala_wind_speed,Bielsko_Biala_wind_dir,Bielsko_Biala_clouds]
        Bielsko_Biala_lat=Bielsko_Biala_coord["lat"]
        Bielsko_Biala_lon=Bielsko_Biala_coord["lon"]
        Gliwice=TarG[2]
        Gliwice_coord=Gliwice["coord"]
        Gliwice_main=Gliwice["main"]
        Gliwice_wind=Gliwice["wind"]
        Gliwice_clouds=Gliwice["clouds"]
        Gliwice_weather=Gliwice["weather"]
        Gliwice_weather1=Gliwice_weather[0]
        Gliwice_descr=Gliwice_weather1["description"]
        Gliwice_name=Gliwice["name"]
        Gliwice_temp=Gliwice_main["temp"]
        Gliwice_temp_min=Gliwice_main["temp_min"]
        Gliwice_temp_max=Gliwice_main["temp_max"]
        Gliwice_pressure=Gliwice_main['pressure']
        Gliwice_humidity=Gliwice_main["humidity"]
        Gliwice_wind_speed=Gliwice_wind["speed"]
        Gliwice_wind_dir=Gliwice_wind["deg"]
        Gliwice_clouds=Gliwice_clouds["all"]
        war_Gliwice=[Gliwice_name,Gliwice_temp,Gliwice_temp_max,Gliwice_temp_min,Gliwice_pressure,Gliwice_humidity,Gliwice_wind_speed,Gliwice_wind_dir,Gliwice_clouds]
        Gliwice_lat=Gliwice_coord["lat"]
        Gliwice_lon=Gliwice_coord["lon"]
        Lubliniec=TarG[4]
        Lubliniec_coord=Lubliniec["coord"]
        Lubliniec_main=Lubliniec["main"]
        Lubliniec_wind=Lubliniec["wind"]
        Lubliniec_clouds=Lubliniec["clouds"]
        Lubliniec_weather=Lubliniec["weather"]
        Lubliniec_weather1=Lubliniec_weather[0]
        Lubliniec_descr=Lubliniec_weather1["description"]
        Lubliniec_name=Lubliniec["name"]
        Lubliniec_temp=Lubliniec_main["temp"]
        Lubliniec_temp_min=Lubliniec_main["temp_min"]
        Lubliniec_temp_max=Lubliniec_main["temp_max"]
        Lubliniec_pressure=Lubliniec_main['pressure']
        Lubliniec_humidity=Lubliniec_main["humidity"]
        Lubliniec_wind_speed=Lubliniec_wind["speed"]
        Lubliniec_wind_dir=Lubliniec_wind["deg"]
        Lubliniec_clouds=Lubliniec_clouds["all"]
        war_Lubliniec=[Lubliniec_name,Lubliniec_temp,Lubliniec_temp_max,Lubliniec_temp_min,Lubliniec_pressure,Lubliniec_humidity,Lubliniec_wind_speed,Lubliniec_wind_dir,Lubliniec_clouds]
        Lubliniec_lat=Lubliniec_coord["lat"]
        Lubliniec_lon=Lubliniec_coord["lon"]
        Tarnowskie_Gory=TarG[3]
        Tarnowskie_Gory_coord=Tarnowskie_Gory["coord"]
        Tarnowskie_Gory_main=Tarnowskie_Gory["main"]
        Tarnowskie_Gory_wind=Tarnowskie_Gory["wind"]
        Tarnowskie_Gory_clouds=Tarnowskie_Gory["clouds"]
        Tarnowskie_Gory_weather=Tarnowskie_Gory["weather"]
        Tarnowskie_Gory_weather1=Tarnowskie_Gory_weather[0]
        Tarnowskie_Gory_descr=Tarnowskie_Gory_weather1["description"]
        Tarnowskie_Gory_name=Tarnowskie_Gory["name"]
        Tarnowskie_Gory_temp=Tarnowskie_Gory_main["temp"]
        Tarnowskie_Gory_temp_min=Tarnowskie_Gory_main["temp_min"]
        Tarnowskie_Gory_temp_max=Tarnowskie_Gory_main["temp_max"]
        Tarnowskie_Gory_pressure=Tarnowskie_Gory_main['pressure']
        Tarnowskie_Gory_humidity=Tarnowskie_Gory_main["humidity"]
        Tarnowskie_Gory_wind_speed=Tarnowskie_Gory_wind["speed"]
        Tarnowskie_Gory_wind_dir=Tarnowskie_Gory_wind["deg"]
        Tarnowskie_Gory_clouds=Tarnowskie_Gory_clouds["all"]
        war_Tarnowskie_Gory=[Tarnowskie_Gory_name,Tarnowskie_Gory_temp,Tarnowskie_Gory_temp_max,Tarnowskie_Gory_temp_min,Tarnowskie_Gory_pressure,Tarnowskie_Gory_humidity,Tarnowskie_Gory_wind_speed,Tarnowskie_Gory_wind_dir,Tarnowskie_Gory_clouds]
        Tarnowskie_Gory_lat=Tarnowskie_Gory_coord["lat"]
        Tarnowskie_Gory_lon=Tarnowskie_Gory_coord["lon"]
        Tychy=TarG[6]
        Tychy_coord=Tychy["coord"]
        Tychy_main=Tychy["main"]
        Tychy_wind=Tychy["wind"]
        Tychy_clouds=Tychy["clouds"]
        Tychy_weather=Tychy["weather"]
        Tychy_weather1=Tychy_weather[0]
        Tychy_descr=Tychy_weather1["description"]
        Tychy_name=Tychy["name"]
        Tychy_temp=Tychy_main["temp"]
        Tychy_temp_min=Tychy_main["temp_min"]
        Tychy_temp_max=Tychy_main["temp_max"]
        Tychy_pressure=Tychy_main['pressure']
        Tychy_humidity=Tychy_main["humidity"]
        Tychy_wind_speed=Tychy_wind["speed"]
        Tychy_wind_dir=Tychy_wind["deg"]
        Tychy_clouds=Tychy_clouds["all"]
        war_Tychy=[Tychy_name,Tychy_temp,Tychy_temp_max,Tychy_temp_min,Tychy_pressure,Tychy_humidity,Tychy_wind_speed,Tychy_wind_dir,Tychy_clouds]
        Tychy_lat=Tychy_coord["lat"]
        Tychy_lon=Tychy_coord["lon"]
        Rybnik=TarG[7]
        Rybnik_coord=Rybnik["coord"]
        Rybnik_main=Rybnik["main"]
        Rybnik_wind=Rybnik["wind"]
        Rybnik_clouds=Rybnik["clouds"]
        Rybnik_weather=Rybnik["weather"]
        Rybnik_weather1=Rybnik_weather[0]
        Rybnik_descr=Rybnik_weather1["description"]
        Rybnik_name=Rybnik["name"]
        Rybnik_temp=Rybnik_main["temp"]
        Rybnik_temp_min=Rybnik_main["temp_min"]
        Rybnik_temp_max=Rybnik_main["temp_max"]
        Rybnik_pressure=Rybnik_main['pressure']
        Rybnik_humidity=Rybnik_main["humidity"]
        Rybnik_wind_speed=Rybnik_wind["speed"]
        Rybnik_wind_dir=Rybnik_wind["deg"]
        Rybnik_clouds=Rybnik_clouds["all"]
        war_Rybnik=[Rybnik_name,Rybnik_temp,Rybnik_temp_max,Rybnik_temp_min,Rybnik_pressure,Rybnik_humidity,Rybnik_wind_speed,Rybnik_wind_dir,Rybnik_clouds]
        Rybnik_lat=Rybnik_coord["lat"]
        Rybnik_lon=Rybnik_coord["lon"]
        print Katowice
        Bielsko_Biala=QgsFeature()
        Bielsko_Biala.setGeometry(QgsGeometry.fromPoint(QgsPoint(Bielsko_Biala_lon,Bielsko_Biala_lat)))
        Bielsko_Biala.setAttributes(war_Bielsko_Biala)
        Katowice=QgsFeature()
        Katowice.setGeometry(QgsGeometry.fromPoint(QgsPoint(Katowice_lon,Katowice_lat)))
        Katowice.setAttributes(war_Katowice)
        Rybnik=QgsFeature()
        Rybnik.setGeometry(QgsGeometry.fromPoint(QgsPoint(Rybnik_lon,Rybnik_lat)))
        Rybnik.setAttributes(war_Rybnik)
        Tarnowskie_Gory=QgsFeature()
        Tarnowskie_Gory.setGeometry(QgsGeometry.fromPoint(QgsPoint(Tarnowskie_Gory_lon,Tarnowskie_Gory_lat)))
        Tarnowskie_Gory.setAttributes(war_Tarnowskie_Gory)
        Czestochowa=QgsFeature()
        Czestochowa.setGeometry(QgsGeometry.fromPoint(QgsPoint(Czestochowa_lon,Czestochowa_lat)))
        Czestochowa.setAttributes(war_Czestochowa)
        Gliwice=QgsFeature()
        Gliwice.setGeometry(QgsGeometry.fromPoint(QgsPoint(Gliwice_lon,Gliwice_lat)))
        Gliwice.setAttributes(war_Gliwice)
        Lubliniec=QgsFeature()
        Lubliniec.setGeometry(QgsGeometry.fromPoint(QgsPoint(Lubliniec_lon,Lubliniec_lat)))
        Lubliniec.setAttributes(war_Lubliniec)
        Tychy=QgsFeature()
        Tychy.setGeometry(QgsGeometry.fromPoint(QgsPoint(Tychy_lon,Tychy_lat)))
        Tychy.setAttributes(war_Tychy)

        warstwa.startEditing()
        warstwa.addFeature(Katowice,True)
        warstwa.addFeature(Czestochowa,True)
        warstwa.addFeature(Tarnowskie_Gory,True)
        warstwa.addFeature(Tychy,True)
        warstwa.addFeature(Lubliniec,True)
        warstwa.addFeature(Gliwice,True)
        warstwa.addFeature(Rybnik,True)
        warstwa.addFeature(Bielsko_Biala,True)

        warstwa.commitChanges()
        warstwa.updateExtents()
        a=qgis.gui.QgsTextAnnotationItem(iface.mapCanvas())
        a.setDocument(QtGui.QTextDocument( "Tychy:      temp: "+str(war_Tychy[1])+"    press:"+str(war_Tychy[4])))
        a.setMapPosition(QgsPoint(Tychy_lon,Tychy_lat))
        a.setFrameSize(QtCore.QSizeF(80,50))
        a.setFrameBackgroundColor(QtGui.QColor("white"))
        a.setFrameColor(QtGui.QColor("black"))
        a.setFrameBorderWidth(1.0)
        iface.mapCanvas().refresh()
        a1=qgis.gui.QgsTextAnnotationItem(iface.mapCanvas())
        a1.setDocument(QtGui.QTextDocument( " Katowice: temp: "+str(war_Katowice[1])+"    press:"+str(war_Katowice[4])))
        a1.setMapPosition(QgsPoint(Katowice_lon,Katowice_lat))
        a1.setFrameSize(QtCore.QSizeF(80,50))
        a1.setFrameBackgroundColor(QtGui.QColor("white"))
        a1.setFrameColor(QtGui.QColor("black"))
        a1.setFrameBorderWidth(1.0)
        iface.mapCanvas().refresh()
        a2=qgis.gui.QgsTextAnnotationItem(iface.mapCanvas())
        a2.setDocument(QtGui.QTextDocument( "Gliwice:   temp: "+str(war_Gliwice[1])+"    press:"+str(war_Gliwice[4])))
        a2.setMapPosition(QgsPoint(Gliwice_lon,Gliwice_lat))
        a2.setFrameSize(QtCore.QSizeF(80,50))
        a2.setFrameBackgroundColor(QtGui.QColor("white"))
        a2.setFrameColor(QtGui.QColor("black"))
        a2.setFrameBorderWidth(1.0)
        iface.mapCanvas().refresh()
        a3=qgis.gui.QgsTextAnnotationItem(iface.mapCanvas())
        a3.setDocument(QtGui.QTextDocument( " Tarnowskie_Gory: temp: "+str(war_Tarnowskie_Gory[1])+"    press:"+str(war_Tarnowskie_Gory[4])))
        a3.setMapPosition(QgsPoint(Tarnowskie_Gory_lon,Tarnowskie_Gory_lat))
        a3.setFrameSize(QtCore.QSizeF(100,50))
        a3.setFrameBackgroundColor(QtGui.QColor("white"))
        a3.setFrameColor(QtGui.QColor("black"))
        a3.setFrameBorderWidth(1.0)
        iface.mapCanvas().refresh()
        a4=qgis.gui.QgsTextAnnotationItem(iface.mapCanvas())
        a4.setDocument(QtGui.QTextDocument( " Lubliniec: temp: "+str(war_Lubliniec[1])+"    press:"+str(war_Lubliniec[4])))
        a4.setMapPosition(QgsPoint(Lubliniec_lon,Lubliniec_lat))
        a4.setFrameSize(QtCore.QSizeF(80,50))
        a4.setFrameBackgroundColor(QtGui.QColor("white"))
        a4.setFrameColor(QtGui.QColor("black"))
        a4.setFrameBorderWidth(1.0)
        iface.mapCanvas().refresh()
        a5=qgis.gui.QgsTextAnnotationItem(iface.mapCanvas())
        a5.setDocument(QtGui.QTextDocument( "Rybnik:   temp: "+str(war_Rybnik[1])+"    press:"+str(war_Rybnik[4])))
        a5.setMapPosition(QgsPoint(Rybnik_lon,Rybnik_lat))
        a5.setFrameSize(QtCore.QSizeF(80,50))
        a5.setFrameBackgroundColor(QtGui.QColor("white"))
        a5.setFrameColor(QtGui.QColor("black"))
        a5.setFrameBorderWidth(1.0)
        iface.mapCanvas().refresh()
        a6=qgis.gui.QgsTextAnnotationItem(iface.mapCanvas())
        a6.setDocument(QtGui.QTextDocument( " Czestochowa: temp: "+str(war_Czestochowa[1])+"    press:"+str(war_Czestochowa[4])))
        a6.setMapPosition(QgsPoint(Czestochowa_lon,Czestochowa_lat))
        a6.setFrameSize(QtCore.QSizeF(80,50))
        a6.setFrameBackgroundColor(QtGui.QColor("white"))
        a6.setFrameColor(QtGui.QColor("black"))
        a6.setFrameBorderWidth(1.0)
        iface.mapCanvas().refresh()
        a7=qgis.gui.QgsTextAnnotationItem(iface.mapCanvas())
        a7.setDocument(QtGui.QTextDocument( " Bielsko Biala: temp: "+str(war_Bielsko_Biala[1])+"    press:"+str(war_Bielsko_Biala[4])))
        a7.setMapPosition(QgsPoint(Bielsko_Biala_lon,Bielsko_Biala_lat))
        a7.setFrameSize(QtCore.QSizeF(90,50))
        a7.setFrameBackgroundColor(QtGui.QColor("white"))
        a7.setFrameColor(QtGui.QColor("black"))
        a7.setFrameBorderWidth(1.0)
        iface.mapCanvas().refresh()
        pass