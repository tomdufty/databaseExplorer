from PyQt5 import QtGui,QtCore, QtWidgets # Import the PyQt4 module we'll need
import sys # We need sys so that we can pass argv to QApplication
from numpy import genfromtxt #required to import csv

import mainWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
import importWindow_ui
import dbmanager

class Application(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    #
    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined
        self.actionFrom_CSV.triggered.connect(self.run_import_from_csv)

    def run_search_query(self):
        searchquery = dbmanager.run_search_query(self.textEdit.toPlainText())

    def run_import_from_csv(self):
        importgui = importWin(self)
        importgui.show()


class importWin(QtWidgets.QMainWindow, importWindow_ui.Ui_Form):
    def __init__(self, parent=None):
        super(importWin, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        print("importing data")
        data = self.file_open()
        self.populate_table(data)

    def populate_table(self,tabledata):
        print("populating table")
        for entry in tabledata:
            self.importTable.insertRow(0)
            self.importTable.setItem(0,1,QtWidgets.QTableWidgetItem(entry[1]))
            chkBoxItem = QtWidgets.QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.importTable.setItem(0,0,chkBoxItem)# access table and

    def file_open(self):
        name,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File Menu","","Comma Delimited (*.csv)")
        print('file to open is ',name)
        data = genfromtxt(name,delimiter=',')
        print('data imported successfully')
        return data

# main body of program initialised on startup
def main():
    entrys = dbmanager.get_all_descriptions()        #initial test of connection - requires more error handling
    print(entrys)
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = Application()                 # We set the form to be our ExampleApp (design)
          # and execute the app
    for entry in entrys:
        form.MainList.insertRow(0)
        form.MainList.setItem(0,1,QtWidgets.QTableWidgetItem(entry[1]))
        chkBoxItem = QtWidgets.QTableWidgetItem()
        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
        form.MainList.setItem(0,0,chkBoxItem)# access table and
    form.show()                         # Show the form
    app.exec_()

if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function