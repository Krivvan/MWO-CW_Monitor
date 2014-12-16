INTERVAL = 15 * 60 * 1000 #check every 15 minutes
URL = "https://static.mwomercs.com/data/cw/mapdata.json"

import sys

# QT
from PySide.QtCore import *
from PySide.QtGui import *

# JSON
import json
import urllib

# in order to update at 15 minute marks
import sched, time, datetime

class CWmonitor(QWidget):
    def __init__(self):
      super(CWmonitor, self).__init__()
      self.setup()
      self.update()
        
    def setup(self):
      self.setFixedSize(834, 300)
      self.setWindowTitle('CW Monitor')     
  
      self.factionSelectBox = QComboBox()
      self.factionSelectBox.addItem("Davion"            , "5" )
      self.factionSelectBox.addItem("Liao"              , "7" )
      self.factionSelectBox.addItem("Steiner"           , "10")
      self.factionSelectBox.addItem("Rasalhague"        , "9" )
      self.factionSelectBox.addItem("Kurita"            , "6" )
      self.factionSelectBox.addItem("Clan Jade Falcon"  , "12")
      self.factionSelectBox.addItem("Clan Wolf"         , "13")
      self.factionSelectBox.addItem("Clan Ghost Bear"   , "14")
      self.factionSelectBox.addItem("Clan Smoke Jaguar" , "11")
      self.factionSelectBox.currentIndexChanged.connect(self.update)

      self.messageBox = self.createMessageBox()
      self.messageBox.setFixedHeight(50)
  
      self.defendTable = QTableWidget()
      self.defendTable.setColumnCount(4)
      self.defendTable.setRowCount(0)
      self.defendTable.verticalHeader().setVisible(False)
      self.defendTable.setHorizontalHeaderLabels("Planet Defender Contested Attacker".split())
      
      self.attackTable = QTableWidget()
      self.attackTable.setColumnCount(4)
      self.attackTable.setRowCount(0)
      self.attackTable.verticalHeader().setVisible(False)
      self.attackTable.setHorizontalHeaderLabels("Planet Attacker Contested Defender".split())      
      
      layout = QVBoxLayout()
      self.setLayout(layout)
      layout.addWidget(self.factionSelectBox)
      
      hlayout = QHBoxLayout()
      hlayout.addWidget(self.defendTable)
      hlayout.addWidget(self.attackTable)
      layout.addLayout(hlayout)
      
      layout.addWidget(self.messageBox)
      
      self.timer = QTimer(self)
      self.connect(self.timer, SIGNAL("timeout()"), self.update)
      
      self.show()

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
      
      self.defendTable.setRowCount(0)
      for id in range (1,2241):
        if (data[str(id)]["invading"]["id"] != "0") and (data[str(id)]["owner"]["id"] == factionID):
          self.addToDefendTable(data[str(id)])
          
      self.attackTable.setRowCount(0)
      for id in range (1,2241):
        if (data[str(id)]["invading"]["id"] == factionID):
          self.addToAttackTable(data[str(id)])          
        
      self.timer.stop()
      t = datetime.datetime.time(datetime.datetime.now())
      timeTillFifteeen = 15 - (t.minute % 15) # number of minutes until the next 15 minute period
      self.timer.start(timeTillFifteeen * 60 * 1000)
      self.message("Updated on " + time.asctime(time.localtime(time.time())))
      
    def addToDefendTable(self, planetInfo):
      count = self.defendTable.rowCount()
      self.defendTable.insertRow(count)
      self.defendTable.setItem(count, 0, QTableWidgetItem(planetInfo["name"]))
      self.defendTable.setItem(count, 1, QTableWidgetItem(planetInfo["owner"]["name"]))
      contestedItem = QTableWidgetItem(planetInfo["contested"])
      contestedItem.setTextAlignment(Qt.AlignCenter)
      self.defendTable.setItem(count, 2, contestedItem)
      self.defendTable.setItem(count, 3, QTableWidgetItem(planetInfo["invading"]["name"]))
      
    def addToAttackTable(self, planetInfo):
      count = self.attackTable.rowCount()
      self.attackTable.insertRow(count)
      self.attackTable.setItem(count, 0, QTableWidgetItem(planetInfo["name"]))
      self.attackTable.setItem(count, 1, QTableWidgetItem(planetInfo["invading"]["name"]))
      contestedItem = QTableWidgetItem(planetInfo["contested"])
      contestedItem.setTextAlignment(Qt.AlignCenter)
      self.attackTable.setItem(count, 2, contestedItem)
      self.attackTable.setItem(count, 3, QTableWidgetItem(planetInfo["owner"]["name"]))      

def main():
    app = QApplication(sys.argv)
    mon = CWmonitor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()