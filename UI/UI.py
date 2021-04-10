import csv
import sys
from os import path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon, QPixmap, QColor
from PyQt5.QtWidgets import *
import os

from PyQt5.uic.properties import QtGui

from Algos import Apriori as ap


class Start(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        # Window Properties
        self.setWindowTitle('The Smart Supermarket')
        self.setWindowIcon(QIcon('Images\market.png'))
        self.setMinimumWidth(800)
        self.setMaximumWidth(800)
        self.setMinimumHeight(500)
        self.setMaximumHeight(500)
        # Background
        sImage = QImage("Images\Supermarke.jpg").scaled(QSize(800, 500))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        # Layout Props
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(300, 330, 300, 40)

        # Content
        self.start = QPushButton('Start')
        self.exit = QPushButton('Exit')
        self.start.clicked.connect(self.lauch)
        self.exit.clicked.connect(self.close)
        self.client_name = QLineEdit()
        self.client_name.setAlignment(QtCore.Qt.AlignCenter)
        self.client_name.setPlaceholderText("Enter your name")
        # self.client_name.setText('Rima')
        self.start.setAutoDefault(True)

        # PARAMETRE
        self.prods = None

        # Adding Content to window
        layout.addWidget(self.start)
        layout.addWidget(self.client_name)
        layout.addWidget(self.exit)
        self.setLayout(layout)

    def lauch(self):
        self.switch_window.emit(self.client_name.text())


class MainWindow(QtWidgets.QWidget):
    def __init__(self, client_name):

        # Window Props
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('The Smart Supermarket')
        self.setWindowIcon(QIcon('Images\market.png'))
        self.setMinimumWidth(800)
        self.setMaximumWidth(800)
        self.setMinimumHeight(500)
        self.setMaximumHeight(500)

        # setting background color
        p = self.palette()
        from PyQt5.QtGui import QColor
        p.setColor(self.backgroundRole(), QColor(58, 58, 58))
        self.setPalette(p)

        # Layout Props
        self.newL = QHBoxLayout()
        BigL = QVBoxLayout()
        HL = QHBoxLayout()
        TranL = QVBoxLayout()
        GameL = QVBoxLayout()

        # List
        self.listWidget = QListWidget()
        self.listWidget.setMaximumWidth(200)
        self.listWidget.setMinimumWidth(200)
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)

        self.game = QListWidget()
        self.game.setMinimumHeight(300)
        self.game.setMaximumHeight(300)
        self.game.setMaximumWidth(550)
        self.game.setMinimumWidth(550)
        self.game.setSelectionMode(QAbstractItemView.SingleSelection)
        self.disable = True  # no signal
        # Butons
        self.buy = QPushButton("Buy")
        self.buy.clicked.connect(self.addTrans)
        self.play = QPushButton("Play a guessing game")
        self.play.clicked.connect(self.play_game)
        self.achats = QPushButton("Previous purchases")
        self.achats.clicked.connect(self.view)
        self.reset = QPushButton("Reset game")
        self.reset.clicked.connect(self.resetV)

        # Label
        self.client = QLabel(client_name)
        self.client.setAlignment(QtCore.Qt.AlignCenter)
        self.score = 0
        self.scoreLabel = QLabel(str(self.score))
        self.scoreLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.desc = QLabel(
            "You can click on 'Play Game' to have a fun guessing game or on 'Buy' to make new purchases!")
        self.desc.setWordWrap(True)
        self.desc.setAlignment(QtCore.Qt.AlignCenter)
        self.desc.setMinimumWidth(400)
        self.desc.setMaximumWidth(400)

        # Logic
        files = os.listdir("Images/Products")
        # POPULATING MY LIST
        for x in files:
            item = QListWidgetItem(os.path.splitext(x)[0])
            item.setText(os.path.splitext(x)[0])
            item.setIcon(QIcon("Images/Products/" + x))
            self.listWidget.addItem(item)

        # Adding Content
        BigL.addWidget(self.client)
        BigL.addLayout(HL)

        HL.addLayout(TranL)
        HL.addLayout(GameL)

        ScoreLayout = QHBoxLayout()
        ScoreLayout.addWidget(self.desc)
        ScoreLayout.addWidget(self.scoreLabel)

        TranL.addWidget(self.listWidget)
        TranL.addWidget(self.buy)

        GameL.addLayout(ScoreLayout)
        GameL.addWidget(self.game)
        self.newL.addWidget(self.play)
        GameL.addLayout(self.newL)
        GameL.addWidget(self.achats)

        self.setLayout(BigL)

    def addTrans(self):
        # print([item.text() for item in self.listWidget.selectedItems()])
        items = []
        for item in self.listWidget.selectedItems():
            items.append(item.text())
        ap.Ajouter_transaction(items, self.client.text())
        self.listWidget.clearSelection()
        self.view()

    def resetV(self):
        self.disable = True
        self.game.clear()
        self.listWidget.clearSelection()
        self.score = 0
        self.scoreLabel.setText(str(self.score))
        self.desc.setText("All cleared!")
        self.reset.setParent(None)

    def view(self):
        self.resetV()
        self.game.clear()
        if path.exists('../DataBase/Clients/' + self.client.text() + '.csv'):
            with open('../DataBase/Clients/' + self.client.text() + '.csv', 'r') as read_obj:
                Transactions = csv.reader(read_obj)
                Transactions = list(Transactions)
                for t in Transactions:
                    s = ""
                    for p in t:
                        s = s + p + ", "
                    item = QListWidgetItem(s)
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsSelectable)
                    self.game.addItem(item)
        else:
            self.desc.setText("You have to buy things first.")

    def play_game(self):

        if path.exists('../DataBase/Clients/' + self.client.text() + '.csv'):
            with open('../DataBase/Clients/' + self.client.text() + '.csv', 'r') as read_obj:
                n = sum(1 for row in read_obj)
                if n >= 10:
                    if self.listWidget.selectedItems().__len__() >= 1:
                        self.desc.setText("You can play now!")
                        minsup = 0.4 if n <= 50 else 0.2 if n <= 500 else 0.1
                        minconf = 0.6
                        minlift = 1 if n < 20 else 1.5 if n < 500 else 1
                        guesses = ap.game(self.client.text(), 0, minsup, minconf, minlift)
                        if guesses is not None:
                            list_items = []
                            self.game.clear()

                            # add non selected items to the game for an eventuel guess
                            for i in range(0, self.listWidget.count()):
                                if not self.listWidget.item(i).isSelected():
                                    self.game.addItem(self.listWidget.item(i).text())
                                else:
                                    list_items.append(self.listWidget.item(i).text())

                            prods_guessed = []
                            # je vais trouver des regles pour les produits selctionnes
                            # je parcoure les itemsets de taille 2----->K
                            for i in guesses:
                                # Si l'itemset contient mes items selected mais taille != je prends les regles (contre-ex: (A,B) : A->B , B->A j'ai deja A et B :3)
                                for itemset in guesses[i]:
                                    rule = itemset.split(',')
                                    # if mes items selected existent dans mes itemsets
                                    if all(item in rule for item in list_items) and rule != list_items:
                                        for rules in guesses[i][itemset]:
                                            if set(list_items) == set(list(rules)):
                                                print(rules, "--->", guesses[i][itemset][rules])
                                                prods_guessed.append(list(guesses[i][itemset][rules].tuple))

                            # If i have guesses
                            if prods_guessed.__len__() != 0:
                                # DONT FORGET TO UPDATE SCORE
                                self.desc.setText("I think i can guess the rest of your purchase!")
                                self.prods = []
                                for l in prods_guessed:
                                    for i in l:
                                        self.prods.append(i) if i not in self.prods else self.prods
                                self.score = 0
                                self.scoreLabel.setText(str(self.score))
                                self.newL.addWidget(self.reset)
                                # we wait for the user to select something
                                self.disable = False
                                self.game.itemClicked.connect(self.gameClicked)
                            else:
                                self.desc.setText("I could'nt find anything :( try different products!")
                                self.game.clear()
                        else:
                            self.desc.setText("I could'nt find anything :( try different products!")
                            self.game.clear()
                    else:
                        self.desc.setText("Select some products from the list on the left, and i'll guess the "
                                          "rest of your purchase.")
                else:
                    self.desc.setText("You have to make at least 10 transactions.")
        else:
            self.desc.setText("You have to make at least 10 transactions.")

    def gameClicked(self, item):
        if not self.disable:
            if item.background().color().name() != '#ff0000' and item.background().color().name() != '#7fc97f':
                if self.prods is not None:
                    if item.text() in self.prods:
                        self.score = self.score + 10
                        self.scoreLabel.setText(str(self.score))
                        item.setBackground(QColor('#7fc97f'))
                    else:
                        self.score = self.score - 15
                        self.scoreLabel.setText(str(self.score))
                        item.setBackground(QColor('#ff0000'))

        # for i in range(0, self.game.count()):
        #     if list(self.game.item(i).text().split(" ")) in self.prods:
        #         if self.game.item(i) in self.game.selectedItems():
        #             self.game.item(i).setBackground(QColor('#7fc97f'))
        #         else:
        #             self.game.item(i).setBackground(QColor('#ff0000'))


class Controller:

    def __init__(self):
        pass

    def show_main(self):
        self.main = Start()
        self.main.switch_window.connect(self.show_game)
        self.main.show()

    def show_game(self, name):
        self.game = MainWindow(name)
        self.main.close()
        self.game.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open('style.css').read())
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())
