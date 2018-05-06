from PyQt5 import QtGui, QtWidgets # Import the PyQt4 module we'll need
import sys # We need sys so that we can pass argv to QApplication

import mainWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
import dbmanager

class ExampleApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined


def main():
    entrys = dbmanager.get_all_descriptions()        #initial test of connection - requires more error handling
    print(entrys)
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
          # and execute the app
    for entry in entrys:
        form.MainList.insertRow(0)
        form.MainList.setItem(0,1,QtWidgets.QTableWidgetItem(entry[1])) # access table and
    form.show()                         # Show the form
    app.exec_()

if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function