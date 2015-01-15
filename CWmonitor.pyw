URL = "https://static.mwomercs.com/data/cw/mapdata.json"
TOTAL_TERRITORIES = 15.0
VERSION = 0.30

import sys

# QT
from PySide.QtCore import *
from PySide.QtGui import *

# JSON
import json
import urllib

# System/OS
import sys
import os

# in order to update at 15 minute marks
import sched, time, datetime

# No enums in 2.7 :(
class Factions():
  Comstar_ID         =  "1"
  Davion_ID          =  "5"
  Liao_ID            =  "7"
  Marik_ID           =  "8"
  Steiner_ID         = "10"
  Rasalhague_ID      =  "9"
  Kurita_ID          =  "6"
  ClanJadeFalcon_ID  = "12"
  ClanWolf_ID        = "13"
  ClanGhostBear_ID   = "14"
  ClanSmokeJaguar_ID = "11"
  IncludedFactions   = [Comstar_ID, Davion_ID, Liao_ID, Marik_ID, Steiner_ID, Rasalhague_ID, Kurita_ID, ClanJadeFalcon_ID, ClanWolf_ID, ClanGhostBear_ID, ClanSmokeJaguar_ID]
  IS_Factions        = [Davion_ID, Liao_ID, Marik_ID, Steiner_ID, Rasalhague_ID, Kurita_ID]
  Clan_Factions      = [ClanJadeFalcon_ID, ClanWolf_ID, ClanGhostBear_ID, ClanSmokeJaguar_ID]
  
class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.initUI()
    self.setCentralWidget(self.tablesWidget)
    self.checkForUpdates()
      
  def initUI(self):               
    menubar = self.menuBar()
    
    # File
    fileMenu = menubar.addMenu('&File')
    
    exitAction = QAction('&Exit', self)        
    exitAction.setShortcut('Ctrl+Q')
    exitAction.triggered.connect(qApp.quit)

    # Updates are automatically checked for now
    #checkUpdateAction = QAction('&Check for updates', self)
    #checkUpdateAction.triggered.connect(self.checkForUpdates)
    
    fileMenu.addAction(exitAction)
    #fileMenu.addAction(checkUpdateAction)
    
    # Options
    optionsMenu = menubar.addMenu('&Options') 
    skinsMenu = optionsMenu.addMenu('&Skins')
    
    defaultSkin = QAction("&Default", self)
    defaultSkin.setCheckable(True)
    defaultSkin.setObjectName("DefaultSkin")
    innerSphereSkin = QAction("&Inner Sphere HUD", self)
    innerSphereSkin.setCheckable(True)
    innerSphereSkin.setObjectName("InnerSphereSkin")
    clanSkin = QAction("&Clan HUD", self)
    clanSkin.setCheckable(True)
    clanSkin.setObjectName("ClanSkin")
    skinsGroup = QActionGroup(self)
    skinsGroup.addAction(defaultSkin)
    skinsGroup.addAction(innerSphereSkin)
    skinsGroup.addAction(clanSkin)
    defaultSkin.setChecked(True)
    skinsGroup.triggered.connect(self.skinChanged)    
    
    skinsMenu.addAction(defaultSkin)
    skinsMenu.addAction(innerSphereSkin)
    skinsMenu.addAction(clanSkin)
    
    # Tools
    toolsMenu = menubar.addMenu('&Tools')
    
    timelineAction = QAction("&Generate Timeline Reports", self)
    self.connect(timelineAction, SIGNAL("triggered()"), self.timeline)
    toolsMenu.addAction(timelineAction)
    
    unitListAction = QAction("&Unit Holdings", self)
    self.connect(unitListAction, SIGNAL("triggered()"), self.unitList)
    #toolsMenu.addAction(unitListAction)
    
    # Help
    helpMenu = menubar.addMenu('&Help')
    
    aboutAction = QAction("&About", self)
    aboutAction.setShortcut("Ctrl+A")
    self.connect(aboutAction, SIGNAL("triggered()"), self.about)
    helpMenu.addAction(aboutAction)      
    
    self.resize(840, 300)
    self.setFixedWidth(840)
    self.setMinimumHeight(350)
    #self.setMaximumHeight(350)
    self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
    
    self.setWindowTitle('Comstar Reports')
    self.tablesWidget = CWmonitor()
    self.show()
      
  def about(self):
    about = "Version %s\n" % (VERSION)
    box = QMessageBox()
    box.setTextFormat(Qt.RichText)
    box.setInformativeText(about)
    box.setText("Made by Krivvan<br> <a href='mailto:krivvan@gmail.com?Subject=CW Monitor Feedback'>krivvan@gmail.com</a><br>\
                 <a href='https://github.com/Krivvan/MWO-CW_Monitor/issues'>Bugs and upcoming features</a><br><br>\
                 Tips are absolutely not necessary, but if you insist:<br>\
                 Bitcoin Address: 1AEhKmoYjKdNeoV2RViPZ39zgWkq1vWRKi<br> \
                 <img src='assets/1AEhKmoYjKdNeoV2RViPZ39zgWkq1vWRKi.png' /> ")
    box.setWindowTitle("About")
    box.exec_()
  
  def timeline(self):
    self.timelineWindow = TimelineWindow(self)
    self.timelineWindow.setWindowFlags(Qt.Window)
    self.timelineWindow.show()
    
  def unitList(self):
    self.tablesWidget.openUnitList()
 
  def checkForUpdates(self):  
    import re
    import urllib
    import urllib2
    
    try:
      filesPage = urllib2.urlopen("http://sourceforge.net/projects/mwocwmonitor/files/")
    except Exception, err:
      print "Failure to open page", err, err.message
      return None
    filesPageData = filesPage.read();
    
    regex = re.compile("Download CWMonitor-(.*)\.zip")
    
    try:
      sourceforgeVersion = float(regex.search(filesPageData).group(1))
      
      if (sourceforgeVersion > VERSION):
        box = QMessageBox()
        box.setTextFormat(Qt.RichText)
        box.setWindowTitle("Update")      
        box.setText("New update available:<br> <a href='http://sourceforge.net/projects/mwocwmonitor/files/latest/download'>Download</a>")
        box.exec_()
      elif (sourceforgeVersion == VERSION):
        print "Version currently up to date"
      else:
        print "Either something went wrong with version numbers or you have a neutral build"
    except Exception, err:
      print "Couldn't find version number", err, err.message
    
  def skinChanged(self, action):
    if action.objectName() == "DefaultSkin":
      qApp.setStyleSheet("")
    elif action.objectName() == "InnerSphereSkin":
      styleSheet =  "QWidget {color: IS_color;\
                      background-color: IS_farBackground;\
                      font-family: Microsoft Sans Serif;\
                      font-weight: Bold;}\
                    QMenuBar::item {color: IS_color;\
                      background-color: IS_farBackground;}\
                    QMenuBar::item:selected {background-color: IS_selected;\
                      selection-background-color: IS_selected;}\
                    QMenu::item {color: IS_color;\
                      background-color: IS_farBackground;}\
                    QMenu::item:selected {background-color: IS_selected;\
                      selection-background-color: IS_selected;}\
                    QTableWidget {background-color: IS_middleBackground;\
                      selection-background-color: IS_selected;\
                      selection-color: IS_color;\
                      border-color: IS_border;\
                      border-width: 1px;\
                      border-style: inset;}\
                    QHeaderView::section {background-color: IS_middleBackground;}\
                    QTableWidget::item:focus { border: 0px;\
                      selection-background-color: IS_selected;}\
                    QComboBox {background-color: IS_middleBackground;\
                      selection-background-color: IS_middleBackground;\
                      border-color: ;\
                      border-width: 1px;}\
                    QListView {background-color: IS_middleBackground;\
                      selection-background-color: IS_selected;}\
                    QTextEdit {background-color: IS_middleBackground;\
                      border-color: IS_border;\
                      border-width: 1px;\
                      border-style: inset;}\
                    QPushButton {background-color: IS_middleBackground;}"
                    
      styleSheet = styleSheet.replace("IS_color",            "rgb(146, 160, 65)")
      styleSheet = styleSheet.replace("IS_farBackground",    "rgb(26, 17, 2)")
      styleSheet = styleSheet.replace("IS_selected",         "rgb(121, 104, 52)")
      styleSheet = styleSheet.replace("IS_middleBackground", "rgb(78, 63, 30)")
      styleSheet = styleSheet.replace("IS_border",           "rgb(104 ,84 ,49)")
      
      qApp.setStyleSheet(styleSheet)
    elif action.objectName() == "ClanSkin":
      styleSheet =  "QWidget {color: Clan_color;\
                      background-color: Clan_farBackground;\
                      font-family: Microsoft Sans Serif;\
                      font-weight: Bold;}\
                    QMenuBar::item {color: Clan_color;\
                      background-color: Clan_farBackground;}\
                    QMenuBar::item:selected {background-color: Clan_selected;\
                      selection-background-color: Clan_selected;}\
                    QMenu::item {color: Clan_color;\
                      background-color: Clan_farBackground;}\
                    QMenu::item:selected {background-color: Clan_selected;\
                      selection-background-color: Clan_selected;}\
                    QTableWidget {background-color: Clan_middleBackground;\
                      selection-background-color: Clan_selected;\
                      selection-color: Clan_color;\
                      border-color: Clan_border;\
                      border-width: 1px;\
                      border-style: inset;}\
                    QHeaderView::section {background-color: Clan_middleBackground;}\
                    QTableWidget::item:focus { border: 0px;\
                      selection-background-color: Clan_selected;}\
                    QComboBox {background-color: Clan_middleBackground;\
                      selection-background-color: Clan_middleBackground;\
                      border-color: ;\
                      border-width: 1px;}\
                    QListView {background-color: Clan_middleBackground;\
                      selection-background-color: Clan_selected;}\
                    QTextEdit {background-color: Clan_middleBackground;\
                      border-color: Clan_border;\
                      border-width: 1px;\
                      border-style: inset;}\
                    QPushButton {background-color: Clan_middleBackground;}"
                    
      styleSheet = styleSheet.replace("Clan_color",            "rgb(195, 233, 236)")
      styleSheet = styleSheet.replace("Clan_farBackground",    "rgb(33, 76, 92)")
      styleSheet = styleSheet.replace("Clan_selected",         "rgb(21, 157, 197)")
      styleSheet = styleSheet.replace("Clan_middleBackground", "rgb(22, 96, 123)")
      styleSheet = styleSheet.replace("Clan_border",           "rgb(90 ,180 ,206)")
      
      qApp.setStyleSheet(styleSheet)
 
 
class CWmonitor(QWidget):
  upArrowIcon   = u'\u25b2' # unicode for arrows
  downArrowIcon = u'\u25bc'
  
  def __init__(self):
    super(CWmonitor, self).__init__()
    self.updateMap = False
    self.factionID = Factions.IncludedFactions
    self.setup()
    self.message("Client will automatically update on 15 minute clock intervals (10:00, 10:15, 10:30, 10:45, etc.)")
    self.onScheduledUpdate()
      
  def setup(self):
    self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
    
    ## Update timer
    self.timer = QTimer(self)
    self.connect(self.timer, SIGNAL("timeout()"), self.onScheduledUpdate)    
    
    ## Tables and attacker wins
    self.factionSelectBox = QComboBox()
    self.factionSelectBox.addItem("ALL FACTIONS"      , Factions.IncludedFactions  )
    self.factionSelectBox.addItem("INNER SPHERE"      , Factions.IS_Factions       )
    self.factionSelectBox.addItem("THE CLANS"         , Factions.Clan_Factions     )
    self.factionSelectBox.addItem("DAVION"            , Factions.Davion_ID         )
    self.factionSelectBox.addItem("LIAO"              , Factions.Liao_ID           )
    self.factionSelectBox.addItem("MARIK"             , Factions.Marik_ID          )
    self.factionSelectBox.addItem("STEINER"           , Factions.Steiner_ID        )
    self.factionSelectBox.addItem("RASALHAGUE"        , Factions.Rasalhague_ID     )
    self.factionSelectBox.addItem("KURITA"            , Factions.Kurita_ID         )
    self.factionSelectBox.addItem("CLAN JADE FALCON"  , Factions.ClanJadeFalcon_ID )
    self.factionSelectBox.addItem("CLAN WOLF"         , Factions.ClanWolf_ID       )
    self.factionSelectBox.addItem("CLAN GHOST BEAR"   , Factions.ClanGhostBear_ID  )
    self.factionSelectBox.addItem("CLAN SMOKE JAGUAR" , Factions.ClanSmokeJaguar_ID)
    self.factionSelectBox.currentIndexChanged.connect(self.onChangeFaction)

    self.defendTable = QTableWidget()
    self.defendTable.setColumnCount(4)
    self.defendTable.setRowCount(0)
    self.defendTable.verticalHeader().setVisible(False)
    self.defendTable.setHorizontalHeaderLabels("PLANET,DEFENDER,WINS,ATTACKER".split(","))
    self.defendTable.horizontalHeader().setStretchLastSection(True)
    self.defendTable.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.defendTable.setMaximumWidth(415) # TODO: lay it out better and resort less on fixed sizes, just wanted it working for now
    self.defendTable.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding))
    self.defendTable.setFocusPolicy(Qt.NoFocus)
    self.defendTable.setSortingEnabled(True)
    self.defendTable.itemSelectionChanged.connect(self.onHighlightPlanets)
    
    self.attackTable = QTableWidget()
    self.attackTable.setColumnCount(4)
    self.attackTable.setRowCount(0)
    self.attackTable.verticalHeader().setVisible(False)
    self.attackTable.setHorizontalHeaderLabels("PLANET,ATTACKER,WINS,DEFENDER".split(","))
    self.attackTable.horizontalHeader().setStretchLastSection(True)    
    self.attackTable.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.attackTable.setMaximumWidth(415)
    self.attackTable.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding))
    self.attackTable.setFocusPolicy(Qt.NoFocus)
    self.attackTable.setSortingEnabled(True)
    self.attackTable.itemSelectionChanged.connect(self.onHighlightPlanets)
    
    layout = QVBoxLayout()
    self.setLayout(layout)
    layout.addWidget(self.factionSelectBox)
    
    topTablesLayout = QVBoxLayout()
    
    tablesLayout = QHBoxLayout()
    tablesLayout.addWidget(self.defendTable)
    tablesLayout.addWidget(self.attackTable)
    topTablesLayout.addLayout(tablesLayout)
    
    self.messageBox = createMessageBox()
    self.messageBox.setFixedHeight(50)
    
    topTablesLayout.addWidget(self.messageBox)
    
    updateButton = QPushButton("MANUAL UPDATE")
    updateButton.clicked.connect(self.onUpdateButton)    
    topTablesLayout.addWidget(updateButton)
    
    ## Inner sphere map
    self.showMapButton = QPushButton(self.downArrowIcon + " SHOW INNER SPHERE MAP " + self.downArrowIcon)
    self.showMapButton.clicked.connect(self.onShowMapButtonClicked)
    topTablesLayout.addWidget(self.showMapButton)
    
    tablesWidget = QWidget()
    tablesWidget.setLayout(topTablesLayout)
    
    self.innerSphereMap = InnerSphereMapView()    
    self.innerSphereMapScene = InnerSphereMap()  
    self.innerSphereMap.setScene(self.innerSphereMapScene)
    self.innerSphereMap.hide()
   
    splitter = QSplitter()
    splitter.setOrientation(Qt.Vertical)
    splitter.setHandleWidth(2)
    splitter.addWidget(tablesWidget)
    splitter.addWidget(self.innerSphereMap)
    
    layout.addWidget(splitter)
    
  def onChangeFaction(self):
    self.factionID = self.factionSelectBox.itemData(self.factionSelectBox.currentIndex())
    if (self.factionID in Factions.Clan_Factions):
      self.window().setWindowTitle("Operation Revival Status")
    else:
      self.window().setWindowTitle("Comstar Reports")
    self.update()
      
  def message(self, txt):
    self.messageBox.moveCursor(QTextCursor.End)
    self.messageBox.append(txt)
    self.messageBox.moveCursor(QTextCursor.End)
    self.messageBox.ensureCursorVisible()
  
  def loadJSON(self):
    jsonurl = urllib.urlopen(URL)
    self.data = json.loads(jsonurl.read())
    t = datetime.datetime.time(datetime.datetime.now())
    timeTillFifteeen = 15 - (t.minute % 15) # number of minutes until the next 15 minute period 
    self.timer.start((timeTillFifteeen * 60 * 1000) + 30000) # plus 30 seconds, to make up for potential time differences
    
  def onScheduledUpdate(self):
    self.loadJSON()
    self.update()
    self.message("Scheduled update on " + time.asctime(time.localtime(time.time())))
    
  def onUpdateButton(self):
    self.loadJSON()
    self.update()
    self.message("Manual update on " + time.asctime(time.localtime(time.time())))
  
  def update(self):
    # Update Tables
    self.defendTable.setSortingEnabled(False)
    self.defendTable.setRowCount(0)
    for id in range (1,2241):
      if ((self.data[str(id)]["invading"]["id"] != "0") and ((self.data[str(id)]["owner"]["id"] == self.factionID) or (self.data[str(id)]["owner"]["id"] in self.factionID))):
        self.addToDefendTable(self.data[str(id)], id)
    self.defendTable.setSortingEnabled(True)
    
    self.attackTable.setSortingEnabled(False)
    self.attackTable.setRowCount(0)
    for id in range (1,2241):
      if ((self.data[str(id)]["invading"]["id"] == self.factionID) or (self.data[str(id)]["invading"]["id"] in self.factionID)):
        self.addToAttackTable(self.data[str(id)], id)
    self.attackTable.setSortingEnabled(True)
    
    # Update Map
    if (self.updateMap):
      if len(self.innerSphereMapScene.planetDict) < 2240:
        self.innerSphereMapScene.populateWithPlanets(self.data)
        self.innerSphereMapScene.addDate( "Current: " + ((self.data["generated"])[:-9]) )
      else:
        self.innerSphereMapScene.updatePlanetFactions(self.data)
    
  def addToDefendTable(self, planetInfo, id):
    count = self.defendTable.rowCount()
    self.defendTable.insertRow(count)
    
    nameItem = QTableWidgetItem(planetInfo["name"])
    nameItem.setData(Qt.UserRole, id)
    nameItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    self.defendTable.setItem(count, 0, nameItem)
    
    ownerItem = QTableWidgetItem(planetInfo["owner"]["name"])
    ownerItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    self.defendTable.setItem(count, 1, ownerItem)
    
    attackerWins = sum( [bin(int(item)).count("1") for item in planetInfo["territories"]] )
    attackerPercent = int(attackerWins / TOTAL_TERRITORIES * 100)
    attackerWinsString = str(attackerWins) + " (" + str(attackerPercent) + "%)"
    contestedItem = QTableWinsWidgetItem(attackerWinsString, attackerWins)
    contestedItem.setTextAlignment(Qt.AlignCenter)
    contestedItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    self.defendTable.setItem(count, 2, contestedItem)
    
    invaderItem = QTableWidgetItem(planetInfo["invading"]["name"])
    invaderItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    self.defendTable.setItem(count, 3, invaderItem)
    
  def addToAttackTable(self, planetInfo, id):
    count = self.attackTable.rowCount()
    self.attackTable.insertRow(count)
    
    nameItem = QTableWidgetItem(planetInfo["name"])
    nameItem.setData(Qt.UserRole, id)
    nameItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    self.attackTable.setItem(count, 0, nameItem)
    
    invaderItem = QTableWidgetItem(planetInfo["invading"]["name"])
    invaderItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    self.attackTable.setItem(count, 1, invaderItem)
    
    attackerWins = sum( [bin(int(item)).count("1") for item in planetInfo["territories"]] )
    
    attackerPercent = int(attackerWins / TOTAL_TERRITORIES * 100)
    attackerWinsString = str(attackerWins) + " (" + str(attackerPercent) + "%)"
    contestedItem = QTableWinsWidgetItem(attackerWinsString, attackerWins)
    contestedItem.setTextAlignment(Qt.AlignCenter)
    contestedItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    self.attackTable.setItem(count, 2, contestedItem)
    
    ownerItem = QTableWidgetItem(planetInfo["owner"]["name"])
    ownerItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    self.attackTable.setItem(count, 3, ownerItem)
    
  def onShowMapButtonClicked(self):
    if self.updateMap:
      self.innerSphereMap.hide()
      self.updateMap = False
      self.showMapButton.setText(self.downArrowIcon + " SHOW INNER SPHERE MAP " + self.downArrowIcon)
    else:
      self.innerSphereMap.show()
      self.showMapButton.setText(self.upArrowIcon   + " HIDE INNER SPHERE MAP " + self.upArrowIcon)
      self.updateMap = True
      self.update()
  
  def onHighlightPlanets(self):
    if self.updateMap:
      for row in range(0,self.defendTable.rowCount()):
        planet = (self.innerSphereMapScene.planetDict[int(self.defendTable.item(row, 0).data(Qt.UserRole))])
        if self.defendTable.item(row,0).isSelected():
          planet.setSelected(True)
        else:
          planet.setSelected(False)
          
      for row in range(0,self.attackTable.rowCount()):
        planet = (self.innerSphereMapScene.planetDict[int(self.attackTable.item(row, 0).data(Qt.UserRole))])
        if self.attackTable.item(row,0).isSelected():
          planet.setSelected(True)
        else:
          planet.setSelected(False)
          
  def openUnitList(self):
    unitListWindow = UnitListWindow(self.data, self)
    unitListWindow.show()
 
class QTableWinsWidgetItem(QTableWidgetItem):
  def __init__(self, text, sortKey):
    QTableWidgetItem.__init__(self, text, QTableWidgetItem.UserType)
    self.sortKey = sortKey

  # So we can sort attacker wins properly
  def __lt__(self, other):
    #return int(self.sortKey.split(' ',1)[0]) < int(other.sortKey.split(' ',1)[0])
    return self.sortKey < other.sortKey

class InnerSphereMapView(QGraphicsView):
  def __init__(self, parent=None):
    super(InnerSphereMapView, self).__init__(parent)
    self.setDragMode(QGraphicsView.ScrollHandDrag)
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.setMouseTracking(True)
    self.minScale = 1.15
    self.maxScale = 5.00
    self.currentScale = 1.00

  def wheelEvent(self, event):
    self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
    scaleFactor = 1.15
    if ((self.currentScale < self.maxScale) & (event.delta() > 0)):
      self.scale(scaleFactor, scaleFactor)
      self.currentScale = self.currentScale * scaleFactor
    elif ((self.currentScale > self.minScale) & (event.delta() < 0)):
      self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)
      self.currentScale = self.currentScale / scaleFactor
    
class InnerSphereMap(QGraphicsScene):
  MapWidth = 811
  MapHeight = 604
  def __init__(self, parent=None):
    super(InnerSphereMap, self).__init__(parent)
    self.addPixmap(QPixmap('assets/map.png'))
    self.setBackgroundBrush(Qt.black)
    self.planetDict = {}
    
  def populateWithPlanets(self, data):
    # clear the list, in the possible situation that the list is not fully populated for some reason
    for key, planet in self.planetDict.viewitems():
      self.removeItem(planet)
    self.planetDict.clear()
    
    for id in range (2240,0,-1):
      ownerID = data[str(id)]["owner"]["id"]
      if ownerID in Factions.IncludedFactions:
        x = int( data[str(id)]["position"]["x"] ) # min -469; max 633;
        y = int( data[str(id)]["position"]["y"] ) # min -412; max 522;
        x = (x + 485) * (self.MapWidth / 1140.0)
        y = self.MapHeight - ((y + 430) * (self.MapHeight / 980.0)) # originally flipped
        planet = Planet(id, x, y, ownerID)
        self.planetDict[id] = planet
        self.addItem(planet)
        
  def updatePlanetFactions(self, data):   
    for id, planet in self.planetDict:
      ownerID = data[str(planet.id)]["owner"]["id"]
      if ownerID in Factions.IncludedFactions:
        planet.setFaction(ownerID)
        
  def addDate(self, dateString):
    dateItem = QGraphicsTextItem()
    dateItem.setPlainText(dateString)
    dateItem.setDefaultTextColor(QColor(255,255,255))
    font = QFont("Sans Serif", 13, QFont.Bold)
    dateItem.setFont(font)
    dateItem.setPos(self.MapWidth - QFontMetrics(font).width(dateString) - 20, 20)    
    self.addItem(dateItem)
        
class Planet(QGraphicsEllipseItem):
  def __init__(self, id, x, y, faction):
    QGraphicsEllipseItem.__init__(self, x, y, 3.5, 3.5)
    self.id = id
    self.faction = faction
    self.setFaction(faction)
    self.blankPen = (QPen(QColor(0,0,0,0)))
    self.highlightPen = (QPen(QColor(255,255,10,80)))
    self.highlightPen.setWidth(6)
    self.setPen(self.blankPen)
    self.setFlags(QGraphicsItem.ItemIsSelectable)
    #self.setMouseTracking(True)
    self.setAcceptHoverEvents(True)
  
  def setFaction(self, newFaction):
    self.faction = newFaction
    self.setFactionColour()
  
  def setFactionColour(self):
    if self.faction == Factions.Davion_ID:
      color = QColor(116,  3,  0)
    elif self.faction == Factions.Liao_ID:
      color = QColor( 47,147,23 )
    elif self.faction == Factions.Marik_ID:
      color = QColor(163, 49,184)
    elif self.faction == Factions.Steiner_ID:
      color = QColor( 15, 69,172)
    elif self.faction == Factions.Rasalhague_ID:
      color = QColor( 15,197,197)
    elif self.faction == Factions.Kurita_ID:
      color = QColor(197,  0, 20)
    elif self.faction == Factions.ClanJadeFalcon_ID:
      color = QColor( 98,125, 92)
    elif self.faction == Factions.ClanWolf_ID:
      color = QColor(146, 90, 91)
    elif self.faction == Factions.ClanGhostBear_ID:
      color = QColor( 19, 88,163)
    elif self.faction == Factions.ClanSmokeJaguar_ID:
      color = QColor(166,183,199)
    elif self.faction == Factions.Comstar_ID:
      color = QColor(255,255,255)
    brush = QBrush(color)
    self.setBrush(brush)
    self.update()
    
  def setOutline(self, selected):
    if selected:
      self.setPen(self.highlightPen)
      self.update()
    else:
      self.setPen(self.blankPen)
      self.update()
  
  def itemChange(self, change, value):
    if (change == QGraphicsItem.ItemSelectedChange):
      if (value == True):
        self.setOutline(True)
      else:
        self.setOutline(False)
    return QGraphicsItem.itemChange(self, change, value)
  
  def hoverEnterEvent(self, event):
    self.setCursor(Qt.PointingHandCursor);

class TimelineWindow(QWidget):
  def __init__(self, parent=None):
    super(TimelineWindow, self).__init__(parent)
    self.setWindowTitle("Invasion Timeline")
    self.mapScenes = []
    self.mapDates = []
    self.mapReports = []
    self.setup()
    
  def setup(self):
    self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
  
    self.dateTime = datetime.datetime.utcnow() # Game time is in UTC + 1035 directly to year

    self.calendarFrom = QDateTimeEdit()
    self.calendarFrom.setCalendarPopup(True)
    self.calendarFrom.setDisplayFormat("MMMM dd, yyyy")
    self.calendarFrom.setDateRange(QDate(2014, 12, 16), QDate(self.dateTime.year, self.dateTime.month, self.dateTime.day))    
    self.calendarFrom.setDate(QDate(2014, 12, 16))
    self.calendarFrom.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

    self.calendarTo = QDateTimeEdit()
    self.calendarTo.setCalendarPopup(True)
    self.calendarTo.setDisplayFormat("MMMM dd, yyyy")
    self.calendarTo.setDateRange(QDate(2014, 12, 16), QDate(self.dateTime.year, self.dateTime.month, self.dateTime.day))    
    self.calendarTo.setDate(QDate(self.dateTime.year, self.dateTime.month, self.dateTime.day))
    self.calendarTo.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

    generateButton = QPushButton("Generate Maps and Reports")
    generateButton.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
    generateButton.clicked.connect(self.onGenerateMaps)
    
    toLabel = QLabel(" to ")
    toLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
    
    dateBoxLayout = QHBoxLayout()
    dateBoxLayout.addWidget(self.calendarFrom)
    dateBoxLayout.addWidget(toLabel)
    dateBoxLayout.addWidget(self.calendarTo)
    dateBoxLayout.addWidget(generateButton) 

    self.slider = QSlider(Qt.Horizontal)
    self.slider.setMinimum(0)
    self.slider.setMaximum(0)
    self.slider.setSingleStep(1)
    self.slider.setPageStep(1)
    self.slider.setTickPosition(QSlider.TicksBothSides)
    self.slider.setMinimumHeight(15)
    self.slider.valueChanged.connect(self.onSliderValueChanged)
    
    self.sliderButtonLeft = QPushButton("<")
    self.sliderButtonLeft.setFixedWidth(50)
    self.sliderButtonLeft.clicked.connect(self.onSliderButtonLeft)
    self.sliderButtonRight = QPushButton(">")
    self.sliderButtonRight.setFixedWidth(50)
    self.sliderButtonRight.clicked.connect(self.onSliderButtonRight)
    
    sliderLayout = QHBoxLayout()
    sliderLayout.addWidget(self.slider)
    sliderLayout.addWidget(self.sliderButtonLeft)
    sliderLayout.addWidget(self.sliderButtonRight)
    
    self.innerSphereMap = InnerSphereMapView()
    self.innerSphereMap.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    placeholderScene = QGraphicsScene(self)
    placeholderScene.setBackgroundBrush(Qt.black)
    self.innerSphereMap.setScene(placeholderScene)
    #self.innerSphereMap.setMaximumSize(1000,InnerSphereMap.MapHeight)
    
    self.reportBox = createMessageBox()
    self.reportBox.setMinimumWidth(200)
    self.reportBox.setMaximumWidth(400)
    
    reportLayout = QHBoxLayout()
    reportLayout.addWidget(self.innerSphereMap)
    reportLayout.addWidget(self.reportBox)

    layout = QVBoxLayout()
    self.setLayout(layout)
    layout.addLayout(dateBoxLayout)
    layout.addLayout(sliderLayout)
    layout.addLayout(reportLayout)
    
    self.slider.hide()
    self.sliderButtonRight.hide()
    self.sliderButtonLeft.hide()
    self.innerSphereMap.hide()
    self.reportBox.hide()
    
  def message(self, txt):
    self.reportBox.moveCursor(QTextCursor.End)
    self.reportBox.append(txt)
    self.reportBox.moveCursor(QTextCursor.End)
    self.reportBox.ensureCursorVisible()
    
  def onGenerateMaps(self):
    self.mapDates = []
    self.mapScenes = []

    startDate = self.calendarFrom.date()
    endDate = self.calendarTo.date()
    
    nDate = startDate
    while nDate <= endDate:
      self.mapDates.append(nDate)
      nDate = nDate.addDays(1)
    
    progressBarDialog = QProgressDialog("Starting map generation...", "Cancel", 0, len(self.mapDates))
    progressBarDialog.setWindowModality(Qt.WindowModal)
    progressBarDialog.setWindowTitle("Creating Timeline")
    progressBarDialog.show()
    qApp.processEvents()
    
    progress = 0
    oldData = None
      
    for date in self.mapDates:
      year = str(date.year() + 1035)
      month = str(date.month()).zfill(2)
      day = str(date.day()).zfill(2)
      
      nextDayDate = date.addDays(1)
      nextDayYear = str(nextDayDate.year() + 1035)
      nextDayMonth = str(nextDayDate.month()).zfill(2)
      nextDayDay = str(nextDayDate.day()).zfill(2)      
      
      progressBarDialog.setValue(progress)
      if (progressBarDialog.wasCanceled()):
        break
      qApp.processEvents()      
      
      progressBarDialog.setLabelText("Accessing data archives for ("+year+"-"+month+"-"+day+")...")
      qApp.processEvents()
      
      if (date == QDate(self.dateTime.year, self.dateTime.month, self.dateTime.day)):
        dataURL = "https://static.mwomercs.com/data/cw/mapdata-" + year + "-" + month + "-" + day + "T05-00" + ".json"
      else:
        dataURL = "https://static.mwomercs.com/data/cw/mapdata-" + nextDayYear + "-" + nextDayMonth + "-" + nextDayDay + "T04-45" + ".json"
      # TODO: catch exception when urlopen fails
      jsonurl = urllib.urlopen(dataURL)
      data = json.loads(jsonurl.read())
      
      progressBarDialog.setLabelText("Generating map for ("+year+"-"+month+"-"+day+")...")
      qApp.processEvents()
      
      newMapScene = InnerSphereMap(self)
      newMapScene.populateWithPlanets(data)
      newMapScene.addDate((data["generated"])[:-9])
      
      self.mapScenes.append(newMapScene)
      
      progressBarDialog.setLabelText("Writing reports for ("+year+"-"+month+"-"+day+")...")
      qApp.processEvents()      

      report = "No report available"
      #defenseReport = "\n \n\nSuccessful defence actions:\n"
      defenseReportList = []
      #attackReport = "Successful attacks:\n"
      attackReportList = []
      
      if (oldData != None):
        for id in range (1,2241):
          if (oldData[str(id)]["contested"] == "1"):
            if (oldData[str(id)]["owner"]["id"] == data[str(id)]["owner"]["id"]):
              planetName = oldData[str(id)]["name"]
              defender = oldData[str(id)]["owner"]["name"]
              attacker = oldData[str(id)]["invading"]["name"]
              attackerWins = sum( [bin(int(item)).count("1") for item in oldData[str(id)]["territories"]] )
              if (attackerWins > 0):
                defenseReportLine = defender + " holds " + attacker + " to " + str(attackerWins) + " on " + planetName + ".\n"
                defenseReportList.append(defenseReportLine)
            elif (oldData[str(id)]["owner"]["id"] != data[str(id)]["owner"]["id"]):
              planetName = oldData[str(id)]["name"]
              defender = oldData[str(id)]["owner"]["name"]
              attacker = oldData[str(id)]["invading"]["name"]
              attackReportLine = attacker + " takes " + planetName + " from " + defender + "!\n"
              attackReportList.append(attackReportLine)
        attackReport = ''.join(sorted(attackReportList, key=lambda x:x[:2]))
        defenseReport = ''.join(sorted(defenseReportList, key=lambda x:x[:2]))
        report = attackReport + "\n" + defenseReport
      
      self.mapReports.append(report)
      
      progress += 1
      oldData = data
      
    progressBarDialog.setValue(len(self.mapDates))    
    
    self.slider.setMaximum(len(self.mapScenes) - 1)
    self.slider.setValue(len(self.mapScenes))
    
    self.slider.show()
    self.sliderButtonRight.show()
    self.sliderButtonLeft.show()
    self.innerSphereMap.show()
    self.reportBox.show()
    
    self.adjustSize()
    self.showMaximized()
    
  def onSliderValueChanged(self, newValue):
    self.innerSphereMap.setScene(self.mapScenes[newValue])
    self.reportBox.clear()
    self.message(self.mapReports[newValue])
    
  def onSliderButtonLeft(self):
    self.slider.triggerAction(QAbstractSlider.SliderSingleStepSub)
    
  def onSliderButtonRight(self):
    self.slider.triggerAction(QAbstractSlider.SliderSingleStepAdd)

class UnitListWindow(QWidget):
  def __init__(self, data, parent=None):
    super(TimelineWindow, self).__init__(parent)
    self.setWindowTitle("Unit Holdings")
    self.data = data
    self.setup()
    
  def setup(self):
    pass
    
    
def createMessageBox():
  messageBox = QTextEdit()
  messageBox.setReadOnly(True)

  messageBox.setStyleSheet("font: 9pt \"Courier\";")
  messageBox.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

  return messageBox    
  
def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/CWmonitorico.png"))
    mon = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()