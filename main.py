# data.db file from Delver Lens N extracted apk.
import os
import sys

from PySide2 import QtWidgets, QtGui

import ijson
import sqlite3
from datetime import datetime
from functools import lru_cache
from PySide2.QtCore import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setFixedWidth(800)
        MainWindow.setFixedHeight(431)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionQuit.triggered.connect(lambda: sys.exit())
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 20, 121, 31))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 60, 141, 31))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 100, 141, 31))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(160, 20, 511, 34))
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(160, 60, 511, 34))
        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(160, 100, 511, 34))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(680, 20, 94, 34))
        self.pushButton.clicked.connect(lambda: self.openFileNameDialog("apk"))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(680, 60, 94, 34))
        self.pushButton_2.clicked.connect(lambda: self.openFileNameDialog("scryfall"))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(680, 100, 94, 34))
        self.pushButton_3.clicked.connect(lambda: self.openFileNameDialog("dlens"))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(22, 169, 71, 31))
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(110, 170, 481, 31))
        self.progressBar.setValue(0)
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(600, 170, 81, 31))
        self.pushButton_4.clicked.connect(self.startexport)
        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(693, 170, 81, 31))
        self.pushButton_5.clicked.connect(lambda: self.setRunning(False))
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(20, 230, 761, 131))
        self.textEdit.setReadOnly(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 32))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.errorFormat = '<span style="color:red;">{}</span>'
        self.warningFormat = '<span style="color:orange;">{}</span>'
        self.validFormat = '<span style="color:green;">{}</span>'

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menuMenu.addAction(self.actionAbout)
        self.menuMenu.addAction(self.actionQuit)

        self.scryfall_errors = 0
        self.delver_errors = 0
        self.scryfall_fd = None
        self.scryfall_database = {}

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

        for file in os.listdir(os.getcwd()):
            if file.endswith(".db"):
                self.lineEdit.setText(os.path.join(os.getcwd(), file))
            elif file.endswith(".json"):
                self.lineEdit_2.setText(os.path.join(os.getcwd(), file))
            elif file.endswith(".dlens"):
                self.lineEdit_3.setText(os.path.join(os.getcwd(), file))

    def log(self, string, format_type=None):
        print(string)
        if format_type and type(format_type) == str:
            string = format_type.format(string)
        self.textEdit.append(string)
        return

    def setRunning(self, is_running):
        global running
        running = is_running
        if is_running == False:
            self.getcarddatabyid.cache_clear()


    def getRunning(self):
        global running
        return running


    def showAbout(self):
        self.textEdit.append(f"dlensExporter Version 1.0. \nWritten by jertzukka@github under MIT License.")


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"dlensExporter", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"APK Database .db", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Offline Scryfall .json", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"D Lens File .dlens", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Select file", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Select file", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Select file", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Progress:", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.menuMenu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))


    def openFileNameDialog(self, type):
        fname = QFileDialog.getOpenFileName(None, "Select a file...",
                                            './', filter="All files (*)")
        if fname[0] == "":
            return
        elif type == "apk":
            self.log(f"APK file set to: {fname[0]}")
            self.lineEdit.setText(fname[0])
        elif type == "scryfall":
            self.log(f"Scryfall file set to: {fname[0]}")
            self.lineEdit_2.setText(fname[0])
        elif type == "dlens":
            self.log(f"Dlens file set to: {fname[0]}")
            self.lineEdit_3.setText(fname[0])


    def connectapkdatabase(self):
        global apkdatabase
        apkconn = sqlite3.connect(apkdatabase)
        global apkc
        apkc = apkconn.cursor()


    def connectdlensdatabase(self):
        dlensconn = sqlite3.connect(dlens)
        global dlensc
        dlensc = dlensconn.cursor()

    def init_scryfall_database(self):
        self.scryfall_database = {}
        relevant_fields = ["name", "set", "set_name", "collector_number"]
        for record in ijson.items(self.scryfall_fd, "item"):
            self.scryfall_database[record["id"]] = {key:record[key] for key in relevant_fields}

    @lru_cache(maxsize=128)
    def ScryfallIDFromDelver(self, delver_id):
        t = (delver_id,)
        apkc.execute('SELECT scryfall_id FROM cards WHERE _id=?', t)
        apkc_result = apkc.fetchone()
        if not apkc_result:
            return None
        return apkc_result[0]

    @lru_cache(maxsize=128)
    def getcarddatabyid(self, scryfall_id):
        try:
            return self.scryfall_database[scryfall_id]
        except TypeError:
            return None


    def startexport(self):
        global apkdatabase, offlinescryfall, dlens
        self.setRunning(True)
        apkdatabase = self.lineEdit.text()
        offlinescryfall = self.lineEdit_2.text()
        dlens = self.lineEdit_3.text()

        # Open both SQLite files
        self.connectapkdatabase()
        self.connectdlensdatabase()

        # Get all cards from .dlens file
        dlensc.execute('SELECT * from cards')
        cardstoimport = dlensc.fetchall()

        # Set new .csv file name
        now = datetime.now()
        newcsvname = now.strftime("%d_%m_%Y-%H_%M_%S") + ".csv"

        # For each card, match the id to the apk database and with scryfall_id search further data from Scryfall database.
        with open(newcsvname, "a", encoding="utf-8") as file:
            total = len(cardstoimport)
            self.scryfall_errors = 0
            self.delver_errors = 0
            file.write(f'Count,Tradelist Count,Name,Edition,Card Number,Condition,Language,Foil,Signed,Artist Proof,Altered Art,Misprint,Promo,Textless,My Price\n')
            for iteration, each in enumerate(cardstoimport):
                if iteration == 0:
                    self.log(f"Preparing files, this might take a bit...")
                    QtWidgets.QApplication.processEvents()
                    if self.scryfall_fd and not self.scryfall_fd.closed:
                        self.scryfall_fd.close()
                    self.scryfall_fd = open(offlinescryfall, 'rb')
                    self.init_scryfall_database()
                    self.log(f"Loaded {len(self.scryfall_database.keys())} cards from {offlinescryfall}.")
                if not self.getRunning():
                    break
                delver_id = each[1]
                foil = each[2]
                quantity = each[4]
                self.progressBar.setValue((iteration + 1)/total*100)
                self.textEdit.append(f"[ {iteration + 1} / {total} ] Getting data for ID: {delver_id}")
                QtWidgets.QApplication.processEvents()

                scryfall_id = self.ScryfallIDFromDelver(delver_id)
                if scryfall_id is None:
                    self.log(f"[ {iteration + 1} / {total} ] Couldn't find id Delver id {delver_id}; is your Delver DB out-of-date?")
                    QtWidgets.QApplication.processEvents()
                    self.delver_errors = self.delver_errors + 1
                    continue

                carddata = self.getcarddatabyid(scryfall_id)
                if carddata is None:
                    self.log(f"[ {iteration + 1} / {total} ] Card could not be found from the Scryfall .json with Delver ID: {delver_id}")
                    QtWidgets.QApplication.processEvents()
                    self.scryfall_errors = self.scryfall_errors + 1
                    continue

                number = carddata['collector_number']
                language = each[10]

                # Fix names from Scryfall to Deckbox
                name = carddata['name']
                if name == "Solitary Hunter // One of the Pack":
                    name = "Solitary Hunter"

                # Fix condition names from Scryfall to Deckbox
                condition = each[9]
                if condition == "Moderately Played":
                    condition = "Played"
                elif condition == "Slighty Played":
                    condition = "Good (Lightly Played)"

                # Fix set names from Scryfall to Deckbox
                set_name = carddata['set_name']
                if set_name == "Magic 2015":
                    set_name = "Magic 2015 Core Set"
                elif set_name == "Magic 2014":
                    set_name = "Magic 2014 Core Set"
                elif set_name == "Modern Masters 2015":
                    set_name = "Modern Masters 2015 Edition"
                elif set_name == "Modern Masters 2017":
                    set_name = "Modern Masters 2017 Edition"
                elif set_name == "Time Spiral Timeshifted":
                    set_name = 'Time Spiral ""Timeshifted""'
                elif set_name == "Commander 2011":
                    set_name = "Commander"
                elif set_name == "Friday Night Magic 2009":
                    set_name = "Friday Night Magic"
                elif set_name == "DCI Promos":
                    set_name = "WPN/Gateway"

                file.write(
                    f'''"{quantity}","{quantity}","{name}","{set_name}","{number}","{condition}","{language}","{foil}","","","","","","",""\n''')

                self.textEdit.append(f"[ {iteration + 1} / {total} ] Imported {name} - {set_name} #{number}")

            self.scryfall_fd.close()
            self.scryfall_fd = None

        errors = self.scryfall_errors + self.delver_errors
        if self.getRunning():
            if errors > 0:
                self.log(f"Successfully imported {total - errors} entries into {newcsvname}")
                if self.scryfall_errors >= 1:
                    self.log(f"There {'was' if errors > 1 else 'were'}  {self.scryfall_errors} error{'s' if errors > 1 else ''} finding card data from the Scryfall .json. " 
                            "To fix this, please use a larger Scryfall bulk data file such as 'All Cards' instead of 'Default Cards'.", 
                            format_type=self.warningFormat)
                if self.delver_errors >= 1:
                    self.log(f"There {'was' if errors > 1 else 'were'}  {self.delver_errors} error{'s' if errors > 1 else ''} finding correct Scryfall IDs from the Delver Database. " 
                            "To fix this, please make sure your local Delver DB file is up-to-date with the instance that created the list.", 
                            format_type=self.warningFormat)
            else:
                self.log(f"Successfully imported {total} entries into {newcsvname}", format_type=self.validFormat)
        else:
            self.log(f"Stopping early, imported {iteration - errors} out of {total} cards in {newcsvname}")



        QtWidgets.QApplication.processEvents()

        self.setRunning(False)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)
    w.show()
    sys.exit(app.exec_())
