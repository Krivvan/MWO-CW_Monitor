URL = "https://static.mwomercs.com/data/cw/mapdata.json"

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

class MainWindow(QMainWindow):
  def __init__(self):
      super(MainWindow, self).__init__()
      self.initUI()
      self.setCentralWidget(self.tablesWidget)
      
  def initUI(self):               
      exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
      exitAction.setShortcut('Ctrl+Q')
      exitAction.setStatusTip('Exit application')
      exitAction.triggered.connect(qApp.quit)

      self.statusBar()

      # File
      menubar = self.menuBar()
      fileMenu = menubar.addMenu('&File')
      fileMenu.addAction(exitAction)
      
      # Tools
      toolsMenu = menubar.addMenu('&Tools')
      
      nothingAction = QAction("&Coming \"Soon\"", self)    
      toolsMenu.addAction(nothingAction)
      
      # Help
      helpMenu = menubar.addMenu('&Help')
      
      aboutAction = QAction("&About", self)
      aboutAction.setShortcut("Ctrl+A")
      self.connect(aboutAction, SIGNAL("triggered()"), self.about)            
      helpMenu.addAction(aboutAction)
      

      
      self.resize(832, 300)
      self.setFixedWidth(832)
      self.setMinimumHeight(350)
      self.setMaximumHeight(350)
      self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
      
      self.setWindowTitle('CW Monitor')

      self.tablesWidget = CWmonitor()
      
      self.show()
      
  def about(self):
    about = "Version %s\n" % (0.2) 
    box = QMessageBox()
    box.setTextFormat(Qt.RichText)
    box.setInformativeText(about)
    box.setText("Made by Krivvan<br>More significant updates and additions to come!<br><br>\
                 Tips are absolutely not necessary, but if you insist:<br>\
                 Bitcoin Address: 1C3EQMqu3FDMFvHucFskByFPxQnNVSENdt<br> \
                 <img src='1AEhKmoYjKdNeoV2RViPZ39zgWkq1vWRKi.png' /> ")
    box.setWindowTitle("About")
    box.exec_()

class CWmonitor(QWidget):
  upArrowIcon   = u'\u25b2' # unicode for arrows
  downArrowIcon = u'\u25bc'
  
  def __init__(self):
    super(CWmonitor, self).__init__()
    self.setup()
    self.updateMap = False
    self.update()
      
  def setup(self):
    self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
    
    ## Tables and attacker wins
    self.factionSelectBox = QComboBox()
    self.factionSelectBox.addItem("Davion"            , Factions.Davion_ID         )
    self.factionSelectBox.addItem("Liao"              , Factions.Liao_ID           )
    self.factionSelectBox.addItem("Marik"             , Factions.Marik_ID          )
    self.factionSelectBox.addItem("Steiner"           , Factions.Steiner_ID        )
    self.factionSelectBox.addItem("Rasalhague"        , Factions.Rasalhague_ID     )
    self.factionSelectBox.addItem("Kurita"            , Factions.Kurita_ID         )
    self.factionSelectBox.addItem("Clan Jade Falcon"  , Factions.ClanJadeFalcon_ID )
    self.factionSelectBox.addItem("Clan Wolf"         , Factions.ClanWolf_ID       )
    self.factionSelectBox.addItem("Clan Ghost Bear"   , Factions.ClanGhostBear_ID  )
    self.factionSelectBox.addItem("Clan Smoke Jaguar" , Factions.ClanSmokeJaguar_ID)
    self.factionSelectBox.currentIndexChanged.connect(self.update)

    self.defendTable = QTableWidget()
    self.defendTable.setColumnCount(4)
    self.defendTable.setRowCount(0)
    self.defendTable.verticalHeader().setVisible(False)
    self.defendTable.setHorizontalHeaderLabels("Planet,Defender,Attacker Wins,Attacker".split(","))
    self.defendTable.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.defendTable.setMaximumWidth(402) # TODO: lay it out better and resort less on fixed sizes, just wanted it working for now
    self.defendTable.setFixedHeight(150)
    self.defendTable.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
    self.defendTable.itemSelectionChanged.connect(self.onHighlightPlanets)
    
    self.attackTable = QTableWidget()
    self.attackTable.setColumnCount(4)
    self.attackTable.setRowCount(0)
    self.attackTable.verticalHeader().setVisible(False)
    self.attackTable.setHorizontalHeaderLabels("Planet,Attacker,Attacker Wins,Defender".split(","))
    self.attackTable.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.attackTable.setMaximumWidth(402)
    self.attackTable.setFixedHeight(150)
    self.attackTable.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
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
    
    updateButton = QPushButton("Update")
    updateButton.clicked.connect(self.update)    
    layout.addWidget(updateButton)
    
    ## Inner sphere map
    self.showMapButton = QPushButton(self.downArrowIcon + " Show Inner Sphere Map " + self.downArrowIcon)
    self.showMapButton.clicked.connect(self.onShowMapButtonClicked)
    layout.addWidget(self.showMapButton)
    
    self.innerSphereMap = InnerSphereMap()    
    layout.addWidget(self.innerSphereMap)
    self.innerSphereMap.hide()
    
    layout.addStretch(1)
    
    ## QTimer
    self.timer = QTimer(self)
    self.connect(self.timer, SIGNAL("timeout()"), self.update)

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
  
  def update(self):
    jsonurl = urllib.urlopen(URL)
    data = json.loads(jsonurl.read())
    
    factionID = self.factionSelectBox.itemData(self.factionSelectBox.currentIndex())
    
    # Update Tables
    self.defendTable.setRowCount(0)
    for id in range (1,2241):
      if (data[str(id)]["invading"]["id"] != "0") and (data[str(id)]["owner"]["id"] == factionID):
        self.addToDefendTable(data[str(id)], id)
        
    self.attackTable.setRowCount(0)
    for id in range (1,2241):
      if (data[str(id)]["invading"]["id"] == factionID):
        self.addToAttackTable(data[str(id)], id)
    
    # Update Map
    if (self.updateMap):
      if len(self.innerSphereMap.planetDict) < 2240:
        self.innerSphereMap.populateWithPlanets(data)
      else:
        self.innerSphereMap.updatePlanetFactions(data)
      
    self.timer.stop()
    t = datetime.datetime.time(datetime.datetime.now())
    timeTillFifteeen = 15 - (t.minute % 15) # number of minutes until the next 15 minute period
    self.timer.start(timeTillFifteeen * 60 * 1000)
    self.message("Updated on " + time.asctime(time.localtime(time.time())))
    
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
    contestedItem = QTableWidgetItem(str(attackerWins))
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
    contestedItem = QTableWidgetItem(str(attackerWins))
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
      self.showMapButton.setText(self.downArrowIcon + " Show Inner Sphere Map " + self.downArrowIcon)
    else:
      self.innerSphereMap.show()
      self.showMapButton.setText(self.upArrowIcon +   " Hide Inner Sphere Map " + self.upArrowIcon)
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
    self.scene.addPixmap(QPixmap('map.png'))
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
    QGraphicsEllipseItem.__init__(self, x, y, 3, 3)
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