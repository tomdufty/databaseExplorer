from PyQt5 import QtGui,QtCore, QtWidgets # Import the PyQt4 module we'll need
import sys # We need sys so that we can pass argv to QApplication
from numpy import genfromtxt #required to import csv

import mainWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
import importWindow_ui
import dbmanager

TABLESIZE = 21


class Application(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    #
    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined
        self.actionFrom_CSV.triggered.connect(self.run_import_from_csv)

    def run_search_query(self):
        searchquery = dbmanager.run_search_query(self.searchField.toPlainText())
        self.update_table(searchquery)


    def run_import_from_csv(self):
        importgui = ImportWin(self)
        importgui.show()

    def update_table(self, entrys):
        print("updating table")
        self.MainList.setRowCount(0)
        for entry in entrys:
            self.MainList.insertRow(0)
            self.MainList.setItem(0,1,QtWidgets.QTableWidgetItem(entry[1]))
            chkBoxItem = QtWidgets.QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.MainList.setItem(0,0,chkBoxItem)# access table and


class ImportWin(QtWidgets.QMainWindow, importWindow_ui.Ui_Form):
    def __init__(self, parent=None):
        super(ImportWin, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        print("importing data")
        data = self.file_open()
        self.populate_table(data)

    def populate_table(self,tabledata):
        print("populating table")
        self.importTable.insertColumn(0)  # add first column for checkboxes
        self.importTable.insertRow(0)   # add first row for comboboxes
        headeroptions = ['','Description','Category','Sub-Category','Quality','Group','Model','Reference','Parameter',
                         'Comments', 'Approved', 'dba', '31.5hz', '63hz', '125hz', '250hz', '500hz', '1khz',
                         '2khz', '4khz', '8khz']
        for entry in tabledata:
            i = 1
            self.importTable.insertRow(self.importTable.rowCount())

            for item in entry:
                if i >= self.importTable.columnCount(): #check to see if tehre are adequate columns
                    self.importTable.insertColumn(i)                    #insert if not enough
                    hdrcombobox = QtWidgets.QComboBox()
                    for t in headeroptions:
                        hdrcombobox.addItem(t)
                    self.importTable.setCellWidget(0,i,hdrcombobox)
                self.importTable.setItem(self.importTable.rowCount() - 1, i, QtWidgets.QTableWidgetItem(str(item,'utf-8')))
                chkBoxItem = QtWidgets.QTableWidgetItem()
                chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                self.importTable.setItem(self.importTable.rowCount() - 1, 0, chkBoxItem)# access table and
                i += 1

    def file_open(self):
        name,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File Menu","","Comma Delimited (*.csv)")
        print('file to open is ',name)
        data = genfromtxt(name,delimiter=',',dtype = None).tolist()
        print('data imported successfully')
        return data

    def runImport(self):
        print("running import")
        importList = []             #initialise import list
        for row in range(1, self.importTable.rowCount()):
            listItem = [None]*TABLESIZE                     #initialise list item
            if self.importTable.item(row,0).checkState() == QtCore.Qt.Checked:
                for column in range(1,self.importTable.columnCount()):
                    if self.importTable.cellWidget(0,column).currentIndex() != 0:
                        listItem[self.importTable.cellWidget(0,column).currentIndex() - 1] = \
                            self.importTable.item(row,column).text()
                importList.append(listItem)
        print(importList)
        for entry in importList:
            dbmanager.add_entry(entry)


    def adjustStartRow(self):
        print("adjusting start row")

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