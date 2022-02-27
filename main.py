import sqlite3
import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from ui_file import Ui_MainWindow1
from ui_file1 import Ui_MainWindow2


class Main2(QMainWindow, Ui_MainWindow2):
    def __init__(self, exe):
        super().__init__()
        self.setupUi(self)
        self.exe = exe
        self.connection = sqlite3.connect("data\coffee.db")
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.change)

    def get_col(self):
        return [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(),
                self.lineEdit_5.text(), self.lineEdit_6.text(), self.lineEdit_7.text()]

    def add(self):
        data = self.get_col()
        self.connection.cursor().execute("INSERT INTO coffee(ID, name_of_sort, roasting, ground_or_in_grains, taste_description, price, packing_volume_grams) VALUES(?, ?, ?, ?, ?, ?, ?)", tuple(data))
        self.connection.commit()
        self.hide()
        self.exe.update()
        self.exe.show()

    def change(self):
        data = self.get_col()
        data.append(int(data[0]))
        self.connection.cursor().execute("""UPDATE coffee
        SET name_of_sort = ?
        WHERE ID = ?""", (data[1], data[-1]))
        self.connection.cursor().execute("""UPDATE coffee
        SET roasting = ?
        WHERE ID = ?""", (data[2], data[-1]))
        self.connection.cursor().execute("""UPDATE coffee
        SET ground_or_in_grains = ?
        WHERE ID = ?""", (data[3], data[-1]))
        self.connection.cursor().execute("""UPDATE coffee
        SET taste_description = ?
        WHERE ID = ?""", (data[4], data[-1]))
        self.connection.cursor().execute("""UPDATE coffee
        SET price = ?
        WHERE ID = ?""", (data[5], data[-1]))
        self.connection.cursor().execute("""UPDATE coffee
        SET packing_volume_grams = ?
        WHERE ID = ?""", (data[6], data[-1]))
        self.connection.commit()
        self.hide()
        self.exe.update()
        self.exe.show()


class Main1(QMainWindow, Ui_MainWindow1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.exe = Main2(self)
        self.pushButton.clicked.connect(self.obr)
        self.connection = sqlite3.connect("data\coffee.db")
        res = self.connection.cursor().execute('SELECT * FROM coffee').fetchall()
        self.tableWidget.setColumnCount(7)
        self.columns = ['ID', 'name_of_sort', 'roasting', 'ground_or_in_grains', 'taste_description', 'price',
                        'packing_volume_grams']
        self.tableWidget.setHorizontalHeaderLabels(self.columns)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def obr(self):
        self.hide()
        self.exe.show()

    def update(self):
        res = self.connection.cursor().execute('SELECT * FROM coffee').fetchall()
        self.tableWidget.setColumnCount(7)
        self.columns = ['ID', 'name_of_sort', 'roasting', 'ground_or_in_grains', 'taste_description', 'price',
                        'packing_volume_grams']
        self.tableWidget.setHorizontalHeaderLabels(self.columns)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main1()
    ex.show()
    sys.exit(app.exec())
