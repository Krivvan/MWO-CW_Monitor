URL = "https://static.mwomercs.com/data/cw/mapdata.json"
TOTAL_TERRITORIES = 15.0

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
      
  def initUI(self):               
    exitAction = QAction('&Exit', self)        
    exitAction.setShortcut('Ctrl+Q')
    exitAction.triggered.connect(qApp.quit)

    #self.statusBar()
    menubar = self.menuBar()
    
    # File
    fileMenu = menubar.addMenu('&File')
    fileMenu.addAction(exitAction)
    
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
    
    # Help
    helpMenu = menubar.addMenu('&Help')
    
    aboutAction = QAction("&About", self)
    aboutAction.setShortcut("Ctrl+A")
    self.connect(aboutAction, SIGNAL("triggered()"), self.about)            
    helpMenu.addAction(aboutAction)
    
    self.resize(840, 300)
    self.setFixedWidth(840)
    self.setMinimumHeight(350)
    self.setMaximumHeight(350)
    self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
    
    self.setWindowTitle('Comstar Reports')
    self.tablesWidget = CWmonitor()
    self.show()
      
  def about(self):
    about = "Version %s\n" % (0.2) 
    box = QMessageBox()
    box.setTextFormat(Qt.RichText)
    box.setInformativeText(about)
    box.setText("Made by Krivvan<br>More significant updates and additions to come!<br><br>\
                 Tips are absolutely not necessary, but if you insist:<br>\
                 Bitcoin Address: 1AEhKmoYjKdNeoV2RViPZ39zgWkq1vWRKi<br> \
                 <img src='assets/1AEhKmoYjKdNeoV2RViPZ39zgWkq1vWRKi.png' /> ")
    box.setWindowTitle("About")
    box.exec_()
  
  
  # def check_sourceforge_version(html):

    # import re
    # regex=re.compile("Download MWOMonitor_(.*?)\.zip", re.DOTALL | re.MULTILINE)
    # try:
    # match = regex.search(html)
    # if len(match.groups())>0:
      # return match.group(1)
    # except Exception, err:
    # print "Couldn't match :(", err, err.message
    # return None     
    
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
    self.factionID = Factions.Davion_ID
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
    self.defendTable.setFixedHeight(150)
    self.defendTable.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
    self.defendTable.setFocusPolicy(Qt.NoFocus)
    self.defendTable.itemSelectionChanged.connect(self.onHighlightPlanets)
    
    self.attackTable = QTableWidget()
    self.attackTable.setColumnCount(4)
    self.attackTable.setRowCount(0)
    self.attackTable.verticalHeader().setVisible(False)
    self.attackTable.setHorizontalHeaderLabels("PLANET,ATTACKER,WINS,DEFENDER".split(","))
    self.attackTable.horizontalHeader().setStretchLastSection(True)    
    self.attackTable.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.attackTable.setMaximumWidth(415)
    self.attackTable.setFixedHeight(150)
    self.attackTable.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
    self.attackTable.setFocusPolicy(Qt.NoFocus)
    self.attackTable.itemSelectionChanged.connect(self.onHighlightPlanets)
    
    layout = QVBoxLayout()
    self.setLayout(layout)
    layout.addWidget(self.factionSelectBox)
    
    hlayout = QHBoxLayout()
    hlayout.addWidget(self.defendTable)
    hlayout.addWidget(self.attackTable)
    layout.addLayout(hlayout)
    
    self.messageBox = self.createMessageBox()
    self.messageBox.setFixedHeight(50)    
    layout.addWidget(self.messageBox)
    
    updateButton = QPushButton("MANUAL UPDATE")
    updateButton.clicked.connect(self.onUpdateButton)    
    
    layout.addWidget(updateButton)
    
    ## Inner sphere map
    self.showMapButton = QPushButton(self.downArrowIcon + " SHOW INNER SPHERE MAP " + self.downArrowIcon)
    self.showMapButton.clicked.connect(self.onShowMapButtonClicked)
    layout.addWidget(self.showMapButton)
    
    self.innerSphereMap = InnerSphereMap()    
    layout.addWidget(self.innerSphereMap)
    self.innerSphereMap.hide()
    
    layout.addStretch(1)
  
  def onChangeFaction(self):
    self.factionID = self.factionSelectBox.itemData(self.factionSelectBox.currentIndex())
    if (self.factionID in Factions.IS_Factions):
      self.window().setWindowTitle("Comstar Reports")
    else:
      self.window().setWindowTitle("Operation Revival Status")
    self.update()
  
  def createMessageBox(self):
    self.messageBox = QTextEdit()
    self.messageBox.setReadOnly(True)

    self.messageBox.setStyleSheet("font: 9pt \"Courier\";")

    return self.messageBox
      
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
    self.defendTable.setRowCount(0)
    for id in range (1,2241):
      if (self.data[str(id)]["invading"]["id"] != "0") and (self.data[str(id)]["owner"]["id"] == self.factionID):
        self.addToDefendTable(self.data[str(id)], id)
        
    self.attackTable.setRowCount(0)
    for id in range (1,2241):
      if (self.data[str(id)]["invading"]["id"] == self.factionID):
        self.addToAttackTable(self.data[str(id)], id)
    
    # Update Map
    if (self.updateMap):
      if len(self.innerSphereMap.planetDict) < 2240:
        self.innerSphereMap.populateWithPlanets(self.data)
      else:
        self.innerSphereMap.updatePlanetFactions(self.data)
    
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
    contestedItem = QTableWidgetItem(attackerWinsString)
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
    contestedItem = QTableWidgetItem(attackerWinsString)
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
      self.window().setFixedHeight(350)
      self.adjustSize()
      self.window().adjustSize()
      self.showMapButton.setText(self.downArrowIcon + " SHOW INNER SPHERE MAP " + self.downArrowIcon)
    else:
      self.innerSphereMap.show()
      self.showMapButton.setText(self.upArrowIcon +   " HIDE INNER SPHERE MAP " + self.upArrowIcon)
      self.updateMap = True
      
      self.window().setMinimumHeight(430) #sort of a temporary workaround due to a few issues with inner sphere map sizing and layouts
      self.window().setMaximumHeight(970)
      self.window().resize(self.width(), 970)
      self.update()
  
  def onHighlightPlanets(self):
    if self.updateMap:
      for row in range(0,self.defendTable.rowCount()):
        planet = (self.innerSphereMap.planetDict[int(self.defendTable.item(row, 0).data(Qt.UserRole))])
        if self.defendTable.item(row,0).isSelected():
          planet.setOutline(True)
        else:
          planet.setOutline(False)
          
      for row in range(0,self.attackTable.rowCount()):
        planet = (self.innerSphereMap.planetDict[int(self.attackTable.item(row, 0).data(Qt.UserRole))])
        if self.attackTable.item(row,0).isSelected():
          planet.setOutline(True)
        else:
          planet.setOutline(False)

class InnerSphereMap(QGraphicsView):
  MapWidth = 811
  MapHeight = 604
  def __init__(self):
    QGraphicsView.__init__(self)
    self.scene = QGraphicsScene(self)
    self.scene.setSceneRect(QRectF(0,0,self.MapWidth,self.MapHeight))
    self.setScene(self.scene)
    self.scene.addPixmap(QPixmap('assets/map.png'))
    self.planetDict = {}
    self.setDragMode(QGraphicsView.ScrollHandDrag)
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    
  def populateWithPlanets(self, data):
    # clear the list, in the possible situation that the list is not fully populated for some reason
    for key, planet in self.planetDict.viewitems():
      self.scene.removeItem(planet)
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
        self.scene.addItem(planet)
        
  def updatePlanetFactions(self, data):   
    for id, planet in self.planetDict:
      ownerID = data[str(planet.id)]["owner"]["id"]
      if ownerID in Factions.IncludedFactions:
        planet.setFaction(ownerID)
        
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
    
def main():
    app = QApplication(sys.argv)
    mon = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()