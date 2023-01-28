import math
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

mob = {"weakzom":["Weak Zombie",0,10,2,1,5],"zom":["Zombie",2,25,4,2,15],"strzom":["Strong Zombie",5,50,8,6,40],"mutzom":["Mutant Zombie",10,100,20,10,90],
        "goutcast":["Goblin Outcast",15,200,30,25,180],"gguard":["Goblin Guard",20,450,45,55,300],"gchief":["Goblin Chief",25,750,60,100,550],
        "ancgolem":["Ancient Golem",30,1200,70,175,750],"auggolem":["Augmented Golem",35,1600,75,235,895],
        "ancknight":["Ancient Knight",45,750,115,540,1750],"bfknight":["Bloodflame Knight",55,4400,125,750,3500],
        "anath":["Anath's Spirit",65,9000,165,2563,8000],
        "minion":["Skeleton Minion",100,12000,175,0,0],"overseer":["Skeleton Overseer",100,15000,185,0,0],
        "fireskeleton":["Fire Skeleton",100,17500,200,0,0],"pumpkin":["Corrupted Pumpkin",100,25000,205,0,0]}

#mob -> "name":[name,lvl-req,hp,atk,coin,xp]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eldion Calculator")
        self.setFixedSize(1100, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        scroller=QScrollArea(central_widget)
        scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.container = QWidget()
        scroller.setWidget(self.container)
        scroller.setFixedSize(self.width(),self.height())
        scroller.setWidgetResizable(True)

        # self.setCentralWidget(scroller)
        
        #define widgets
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 10000)
        boxWidth=300
        boxHeight=30
        self.statList={"lvl":None,"hp":None,"def":None,"dmg":None,"rgn":None,"cd":None}

        self.warn=QLabel("please ensure that all field are filled out")
        self.warn.setStyleSheet("color: red;")
        self.warn.setHidden(True)

        editlvl=QLineEdit()
        editlvl.setPlaceholderText("Your LVL")
        editlvl.setValidator(onlyInt)
        editlvl.setFixedSize(boxWidth,boxHeight)
        editlvl.textChanged.connect(lambda value: self.statUpdate("lvl",value)) 

        edithp=QLineEdit()
        edithp.setPlaceholderText("Your HP")
        edithp.setValidator(onlyInt)
        edithp.setFixedSize(boxWidth,boxHeight)
        edithp.textChanged.connect(lambda value: self.statUpdate("hp",value))

        editdef=QLineEdit()
        editdef.setPlaceholderText("Your DEF")
        editdef.setValidator(onlyInt)
        editdef.setFixedSize(boxWidth,boxHeight)
        editdef.textChanged.connect(lambda value: self.statUpdate("def",value))

        editdmg=QLineEdit()
        editdmg.setPlaceholderText("Your *TOTAL* DMG")
        editdmg.setValidator(onlyInt)
        editdmg.setFixedSize(boxWidth,boxHeight)
        editdmg.textChanged.connect(lambda value: self.statUpdate("dmg",value))

        editregen=QLineEdit()
        editregen.setPlaceholderText("Your regen (add 1 base regen)")
        editregen.setValidator(onlyInt)
        editregen.setFixedSize(boxWidth,boxHeight)
        editregen.textChanged.connect(lambda value: self.statUpdate("rgn",value))

        editcd=QComboBox()
        editcd.setEditable(False)
        model = QStandardItemModel() #creates placeholder for combo box
        cdlist=["Fast", "Average", "Slow", "Very Slow"]
        for i in range(4):
            model.appendRow(QStandardItem(cdlist[i]))
        editcd.setModel(ProxyModel(model, '---Select Speed---'))
        editcd.setCurrentIndex(0)
        editcd.currentTextChanged.connect(self.setcd)
        editcd.setFixedSize(boxWidth,boxHeight)

        submitStat=QPushButton("Calculate")
        submitStat.setFixedSize(200,150)
        submitStat.clicked.connect(self.checkField)
        

        column1=QVBoxLayout()
        self.column2=QVBoxLayout()
        row1=QHBoxLayout()
        row2=QHBoxLayout()
        row3=QHBoxLayout()
        row4=QHBoxLayout()
        row5=QHBoxLayout()
        row1.addWidget(editlvl)
        row1.addWidget(edithp)
        row2.addWidget(editdef)
        row2.addWidget(editdmg)
        row3.addWidget(editregen)
        row3.addWidget(editcd)
        column1.addLayout(row1)
        column1.addLayout(row2)
        column1.addLayout(row3)
        row4.addLayout(column1)
        row4.addWidget(submitStat)
        self.column2.addLayout(row4)
        self.column2.addWidget(self.warn)
        
        # self.layout.addLayout(column1,0,0)
        # self.layout.addWidget(self.warn,2,0)
        # self.layout.addWidget(submitStat,0,1)
        # self.layout.addItem(vspacer,1,0,Qt.AlignTop)
        
        self.container.setLayout(self.column2)
    
    def runCalc(self):
        self.column2.addWidget(QLabel(""))
        dps=QLabel("Your DPS: " + str(int(self.statList["dmg"])/self.statList["cd"]))
        dps.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.column2.addWidget(dps)
        
        objs=list()
        for i in mob:
            tempLabel=QLabel()
            tempLabel.setText(self.mobCalc(mob[i]))
            objs.append(tempLabel)
            objs[list(mob.keys()).index(i)].setFixedSize(300,300)
        
        def split(L, n):
            for i in range(0, len(L), n):
                yield L[i:i+n]

        mobSorted = list(split(objs, 3))

        rowList=list()
        for i in mobSorted:
            rowList.append(QHBoxLayout())

        # add to each row, the strings in mobList
        for i in range(len(rowList)): #for i in the number of rows
            for x in mobSorted[i]:
                rowList[i].addWidget(x)
            #rowList[rowList.index(i)].addWidget(z)            
            self.column2.addLayout(rowList[i])

        # self.column2.addWidget(newlabel)
        # x = list(mob.keys()).index(i)
        
        # for i in range(100):
        #     self.column2.addWidget(QPushButton(str(i)))

    #entry field functions
    def setcd(self, cdtype):
        atk_speed = {"Fast":0.2, "Average":0.4, "Slow":0.6, "Very Slow":1} 
        cd=atk_speed[cdtype]
        self.statList["cd"]=cd
    def statUpdate(self,type,value):
        try:self.statList[type]=int(value)
        except:pass
    def checkField(self):
        doPass=True
        for i in self.statList:
            try:
                int(self.statList[i])
            except:
                doPass=False
        if doPass:
            self.fullField()
        else:
            self.emptyField()
    def emptyField(self):
        self.warn.setHidden(False)
    def fullField(self):
        self.warn.setHidden(True)
        self.runCalc()
        
    def mobCalc(self,mobstat):
        mobname=mobstat[0]
        lvlreq=mobstat[1]
        mobhp = mobstat[2]
        coins = mobstat[4]
        xp = mobstat[5]

        hits = math.ceil(mobhp/int(self.statList["dmg"]))
        time = float(self.statList["cd"]*float(hits))
        coinps = coins / time
        xpps = xp / time

        self.mobResult=f"{mobname} [LEVEL {lvlreq}]<br> "
        if int(self.statList["lvl"])<lvlreq:
            self.mobResult+='<font color="red">Your level is too low!</font><br>'
        self.mobResult+=f"{coinps:.2f}"+ " coins per second. <br> " 
        self.mobResult+=f"{xpps:.2f}"+ " xp per second. <br> "
        self.mobResult+=f"Time to kill: {time:.1f} seconds. <br> "
        self.mobResult+=f"Total hits to kill: {hits}<br> "
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(self.mobResult, mode=cb.Clipboard)
        return self.mobResult


        
class ProxyModel(QAbstractProxyModel):
    def __init__(self, model, placeholderText='---', parent=None):
        super().__init__(parent)
        self._placeholderText = placeholderText
        self.setSourceModel(model)
        
    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        return self.createIndex(row, column)

    def parent(self, index: QModelIndex = ...) -> QModelIndex:
        return QModelIndex()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.sourceModel().rowCount()+1 if self.sourceModel() else 0

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self.sourceModel().columnCount() if self.sourceModel() else 0

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> any:
        if index.row() == 0 and role == Qt.DisplayRole:
            return self._placeholderText
        elif index.row() == 0 and role == Qt.EditRole:
            return None
        else:
            return super().data(index, role)

    def mapFromSource(self, sourceIndex: QModelIndex):
        return self.index(sourceIndex.row()+1, sourceIndex.column())

    def mapToSource(self, proxyIndex: QModelIndex):
        return self.sourceModel().index(proxyIndex.row()-1, proxyIndex.column())

    def mapSelectionFromSource(self, sourceSelection: QItemSelection):
        return super().mapSelection(sourceSelection)

    def mapSelectionToSource(self, proxySelection: QItemSelection):
        return super().mapSelectionToSource(proxySelection)
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if not self.sourceModel():
            return None
        if orientation == Qt.Vertical:
            return self.sourceModel().headerData(section-1, orientation, role)
        else:
            return self.sourceModel().headerData(section, orientation, role)

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        return self.sourceModel().removeRows(row, count -1)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

