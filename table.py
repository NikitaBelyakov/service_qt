#from tbl import Ui_MainWindow
from database import Client, Car, ClientCar, global_init, create_session
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QTableWidgetItem, QFileDialog, \
    QInputDialog, QColorDialog, QDialog, QLabel
from PyQt5.QtCore import Qt, QModelIndex
from updt_cl import Ui_Dialog
from updt_car import Ui_Dialog_1
from crt_clcar import Ui_Dialog_2
from tbl1 import Ui_MainWindow
from tbl2 import Ui_MainWindow1

class TableViewer(QMainWindow, Ui_MainWindow1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.table_is_changeable = True
        self.count = 0

    def initUI(self):
        global_init("C:/Users/79223/PycharmProjects/service/database/serv.db")
        self.session = create_session()
        self.pushButtonLoadCl.clicked.connect(self.load_table)
        self.pushButtonLoadCar.clicked.connect(self.load_table_1)
        self.pushButtonLoadClCar.clicked.connect(self.load_table_2)
        self.tableWidget.doubleClicked.connect(self.update_client)
        self.pushButtonAddCl.clicked.connect(self.create_client)
        self.pushButtonDelClient.clicked.connect(self.delete_client)
        self.pushButtonDelCar.clicked.connect(self.delete_car)
        self.tableWidget_2.doubleClicked.connect(self.update_car)
        self.pushButtonAddCar.clicked.connect(self.create_car)
        self.pushButtonAddClCar.clicked.connect(self.create_client_car)
        self.pushButtonDelClCar.clicked.connect(self.delete_client_car)

    def load_table(self):
        self.currentPageLabel = QLabel()
        self.table_is_changeable = False
        clients = self.session.query(Client).all()
        self.tableWidget.setRowCount(0)
        for client in clients:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            tmp = QTableWidgetItem(str(client.client_id))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(row_position, 0, tmp)
            tmp = QTableWidgetItem(str(client.full_name))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(row_position, 1, tmp)
            tmp = QTableWidgetItem(str(client.phone))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(row_position, 2, tmp)
        self.table_is_changeable = True
    def load_table_1(self):
        self.currentPageLabel = QLabel()
        self.table_is_changeable = False
        cars = self.session.query(Car).all()
        self.tableWidget_2.setRowCount(0)
        for car in cars:
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)
            tmp = QTableWidgetItem(str(car.car_id))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget_2.setItem(row_position, 0, tmp)
            tmp = QTableWidgetItem(str(car.brand))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget_2.setItem(row_position, 1, tmp)
            tmp = QTableWidgetItem(str(car.color))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget_2.setItem(row_position, 2, tmp)
            tmp = QTableWidgetItem(str(car.vin_number))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget_2.setItem(row_position, 3, tmp)
            cl = self.session.query(Client).filter(Client.client_id==car.main_owner_id).first()
            tmp = QTableWidgetItem(str(cl.full_name))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget_2.setItem(row_position, 4, tmp)

        self.table_is_changeable = True

    def load_table_2(self):
        self.currentPageLabel = QLabel()
        self.table_is_changeable = False
        clients_cars = self.session.query(ClientCar).all()
        self.tableWidget_3.setRowCount(0)
        for clients_car in clients_cars:
            row_position = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_position)
            tmp = QTableWidgetItem(str(clients_car.client_id))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget_3.setItem(row_position, 0, tmp)
            tmp = QTableWidgetItem(str(clients_car.car_id))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget_3.setItem(row_position, 1, tmp)
            cl = self.session.query(Client).filter(Client.client_id==clients_car.client_id).first()
            tmp = QTableWidgetItem(str(cl.full_name))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget_3.setItem(row_position, 2, tmp)
            cr = self.session.query(Car).filter(Car.car_id==clients_car.car_id).first()
            tmp = QTableWidgetItem(str(cr.brand))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget_3.setItem(row_position, 3, tmp)
        self.table_is_changeable = True

    def update_client(self, index: QModelIndex):
        current_row = index.row()
        id_ = int(self.tableWidget.item(current_row, 0).text())
        self.client_updater = ClintUpdater(id_)
        self.client_updater.exec_()
        self.load_table()

    def create_client(self, index: QModelIndex):
        self.client_updater = ClientCreator()
        self.client_updater.exec_()
        self.load_table()

    def delete_client(self, index: QModelIndex):
        current_row = self.tableWidget.currentRow()
        id_ = int(self.tableWidget.item(current_row, 0).text())
        cl = self.session.query(Client).get(id_)
        clcars = self.session.query(ClientCar).filter(ClientCar.client_id == cl.client_id)
        for clcar in clcars:
            self.session.delete(clcar)
            self.session.commit()
        cars = self.session.query(Car).filter(Car.main_owner_id==cl.client_id)
        for car in cars:
            self.session.delete(car)
            self.session.commit()
        self.session.delete(cl)
        self.session.commit()
        self.load_table()

    def update_car(self, index: QModelIndex):
        current_row = index.row()
        id_ = int(self.tableWidget_2.item(current_row, 0).text())
        self.car_updater = CarUpdater(id_)
        self.car_updater.exec_()
        self.load_table_1()

    def create_car(self, index: QModelIndex):
        self.car_updater = CarCreator()
        self.car_updater.exec_()
        self.load_table_1()

    def delete_car(self, index: QModelIndex):
        current_row = self.tableWidget_2.currentRow()
        id_ = int(self.tableWidget_2.item(current_row, 0).text())
        cr = self.session.query(Car).get(id_)
        clcars = self.session.query(ClientCar).filter(ClientCar.car_id == cr.car_id)
        for clcar in clcars:
            self.session.delete(clcar)
            self.session.commit()
        self.session.delete(cr)
        self.session.commit()
        self.load_table_1()

    def create_client_car(self, index: QModelIndex):
        self.client_car_creator = ClientCarCreator()
        self.client_car_creator.exec_()
        self.load_table_2()

    def delete_client_car(self, index: QModelIndex):
        current_row = self.tableWidget_3.currentRow()
        id_ = int(self.tableWidget_3.item(current_row, 0).text())
        id1_ = int(self.tableWidget_3.item(current_row, 1).text())
        cl = self.session.query(ClientCar).get((id_, id1_))
        self.session.delete(cl)
        self.session.commit()
        self.load_table_2()
class ClintUpdater(QDialog, Ui_Dialog):
    def __init__(self, client_id):
        super().__init__()
        self.setupUi(self)
        self.session = create_session()
        self.client = self.session.query(Client).get(client_id)
        self.label_id.setText(str(self.client.client_id))
        self.lineEdit_name.setText(str(self.client.full_name))
        self.lineEdit_phone.setText(str(self.client.phone))
        self.pushButtonSaveCl.clicked.connect(self.save_data)
    def save_data(self):
        self.client.full_name = self.lineEdit_name.text()
        self.client.phone = self.lineEdit_phone.text()
        self.session.commit()
        self.close()


class ClientCreator(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.session = create_session()
        self.new = Client(full_name="...",phone="...")
        self.label_id.setText(str(self.new.client_id))
        self.lineEdit_name.setText(str(self.new.full_name))
        self.lineEdit_phone.setText(str(self.new.phone))
        self.pushButtonSaveCl.clicked.connect(self.save_data)

    def save_data(self):
        self.new.full_name = self.lineEdit_name.text()
        self.new.phone = self.lineEdit_phone.text()
        self.session.add(self.new)
        self.session.commit()
        self.close()

class CarUpdater(QDialog, Ui_Dialog_1):
    def __init__(self, car_id):
        super().__init__()
        self.setupUi(self)
        self.session = create_session()
        self.car = self.session.query(Car).get(car_id)
        self.lineEditModel.setText(str(self.car.brand))
        self.lineEditColor.setText(str(self.car.color))
        self.lineEditVin.setText(str(self.car.vin_number))
        cli = self.session.query(Client).filter(Client.client_id == self.car.main_owner_id).first()
        self.lineEditOwn.setText(str(cli.full_name))
        self.pushButtonSaveCar.clicked.connect(self.save_data)
    def save_data(self):
        self.car.brand = self.lineEditModel.text()
        self.car.color = self.lineEditColor.text()
        self.car.vin_number = self.lineEditVin.text()
        cli = self.session.query(Client).filter(Client.full_name == self.lineEditOwn.text()).first()
        self.car.main_owner_id = cli.client_id
        self.session.commit()
        self.close()
class CarCreator(QDialog, Ui_Dialog_1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.session = create_session()
        self.new = Car(brand="...",color="...",vin_number="...",main_owner_id=0)
        self.lineEditModel.setText(str(self.new.brand))
        self.lineEditColor.setText(str(self.new.color))
        self.lineEditVin.setText(str(self.new.vin_number))
        self.lineEditOwn.setText(str(self.new.main_owner_id))
        self.pushButtonSaveCar.clicked.connect(self.save_data)

    def save_data(self):
        self.new.brand = self.lineEditModel.text()
        self.new.color = self.lineEditColor.text()
        self.new.vin_number = self.lineEditVin.text()
        self.new.main_owner_id = int(self.lineEditOwn.text())
        cl_ = self.session.query(Client).filter(Client.client_id == self.new.main_owner_id).first()
        self.lineEditOwn = cl_.full_name
        self.session.add(self.new)
        self.session.commit()
        self.close()
class ClientCarCreator(QDialog, Ui_Dialog_2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.session = create_session()
        self.new = ClientCar(client_id=0,car_id=0)
        self.lineEdit1.setText(str(self.new.car_id))
        self.lineEdit_2.setText(str(self.new.client_id))
        self.pushButton.clicked.connect(self.save_data)

    def save_data(self):
        self.new.car_id = self.lineEdit1.text()
        self.new.client_id = self.lineEdit_2.text()
        self.session.add(self.new)
        self.session.commit()
        self.close()
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TableViewer()
    ex.show()
    sys.exit(app.exec())