from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl, QVariant
from PyQt5.QtPositioning import QGeoCoordinate
import csv
from collections import defaultdict

######  PROGRAM MEMANGGIL WINDOWS PYQT5 ##########################

####### memanggil library PyQt5 ##################################
#----------------------------------------------------------------#
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtQml import * 
from PyQt5.QtWidgets import *
from PyQt5.QtQuick import *  
import sys
#----------------------------------------------------------------#

import pandas as pd

csv_file = "sea_current_now.csv"

df = pd.read_csv(csv_file)

lat_current = df["latitude"].tolist()

long_current = df["longitude"].tolist()

dir_current = df["direction"].tolist()

print(lat_current)
print(long_current)
print(dir_current)

current_data = []

for i in range(len(lat_current)):

    current_data.append({

        "lat": lat_current[i],
        "lon": long_current[i],
        "dir": dir_current[i]

    })

print(current_data)


########## mengisi class table dengan instruksi pyqt5#############
#----------------------------------------------------------------#
class table(QObject):    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.app = QApplication(sys.argv)
        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty("backend", self)    
        self.engine.load(QUrl("main.qml"))
        sys.exit(self.app.exec_())
    
    @pyqtSlot(result='QVariantList')
    def getCurrentArray(self):

        current_data = []

        for i in range(len(lat_current)):

            current_data.append({

                "lat": lat_current[i],
                "lon": long_current[i],
                "dir": dir_current[i]

            })

        return current_data
    
    
    
    
#----------------------------------------------------------------#

########## memanggil class table di mainloop######################
#----------------------------------------------------------------#    
if __name__ == "__main__":
    main = table()
    
    
#----------------------------------------------------------------#
