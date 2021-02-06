from pathlib import Path

from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import QRegExp

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1

from datetime import datetime


class CL_customerTP(QtWidgets.QDialog):
    dirname = ''

    def __init__(self):
        super(CL_customerTP, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()
        self.conn1 = db1.connect()
        #mycursor = self.conn.cursor()

    def FN_LOAD_DISPlAY(self):
        filename = self.dirname + '/createModifyCustTp.ui'
        loadUi(filename, self)

        self.FN_GET_CUSTTPS()
        records=self.FN_GET_NEXTlEVEL()
        for row in records:
            self.CMB_nextLevel.addItems([row[0]])
        try:
            self.CMB_custType.addItems(["Active", "Inactive"])
            self.BTN_createCustTp.clicked.connect(self.FN_CREATE_CUSTTP)
            self.BTN_modifyCustTp.clicked.connect(self.FN_MODIFY_CUSTTP)
        except Exception as err:
            print(err)

    def FN_GET_NEXTlEVEL(self):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT LOYCT_DESC FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  order by LOYCT_TYPE_ID   asc")
        records = mycursor.fetchall()
        #mycursor.close()
        return records

    def FN_GET_NEXTlEVEL_ID(self,desc):
        try:
            mycursor3 = self.conn1.cursor()
            mycursor3.execute("SELECT LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  where LOYCT_DESC= '"+desc+"'")
            records = mycursor3.fetchone()
            mycursor3.close()
            return records[0]
        except Exception as err:
            print(err)

    def FN_GET_NEXTlEVEL_DESC(self,id):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT  LOYCT_DESC FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  where LOYCT_TYPE_ID= '"+id+"'")
        records = mycursor.fetchone()
        #mycursor3.close()
        return records[0]

    def FN_GET_STATUS_DESC(self, id):
        if id == '1':
            return "Active"
        else:
            return "Inactive"

    def FN_GET_CUSTTPS(self):
        for i in reversed(range(self.Qtable_custTP.rowCount())):
            self.Qtable_custTP.removeRow(i)
        mycursor = self.conn1.cursor(buffered=True)
        mycursor.execute("SELECT  LOYCT_TYPE_ID, LOYCT_DESC, LOYCT_POINTS_TO_PROMOTE, LOYCT_TYPE_NEXT, LOYCT_STATUS FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  order by LOYCT_TYPE_ID   asc")
        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.Qtable_custTP.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 3 and row_number >0 :
                    #data= self.FN_GET_NEXTlEVEL_DESC(str(data))
                    # comboBox = QtWidgets.QComboBox()
                    # records = self.FN_GET_NEXTlEVEL()
                    # for row in records:
                    #    comboBox.addItems([row[0]])
                    # comboBox.setCurrentText(data)
                    # self.Qtable_custTP.setCellWidget(row_number, column_number, comboBox)
                    item = QTableWidgetItem(str(data))
                else:
                    if column_number == 4:
                        data = self.FN_GET_STATUS_DESC(str(data))
                    item = QTableWidgetItem(str(data))
                    if column_number == 0:
                        item.setFlags(QtCore.Qt.NoItemFlags)
                self.Qtable_custTP.setItem(row_number, column_number, item)
        mycursor.close()

    def FN_CHECK_STATUS(self, status):
        if status == 'Active' or status == 'Inactive' :
            return True
        else :
            return False

    def FN_CHECK_DUP_NAME(self, name):
        mycursor1 = self.conn.cursor()
        # get max userid
        sql = "SELECT LOYCT_DESC  FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_DESC ='"+name+"'"
        #val = (name,)
        mycursor1.execute(sql)
        len = mycursor1.rowcount
        if len > 0:
            return True
        else:
            return False

    def FN_CHECK_DUP_NEXTLEVEL(self, name):
        try:
            mycursor2 = self.conn.cursor()
            print(name)
            sql = "SELECT LOYCT_DESC  FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '" + name + "'"
            mycursor2.execute(sql)
            len = mycursor2.rowcount
            if len > 0:
                return True
            else:
                return False
        except Exception as err:
            #mycursor2.close()
            print(err)

    def FN_CREATE_CUSTTP(self):
        try:
            name = self.LE_desc.text().strip()
            print(name)
            points = self.LE_points.text().strip()

            custType = self.CMB_custType.currentText()
            nextLevel = self.CMB_nextLevel.currentText()
            if custType == 'Active':
                status = 1
            else:
               status = 0

            mycursor = self.conn1.cursor()
            # get max userid
            mycursor.execute("SELECT max(cast(LOYCT_TYPE_ID   AS UNSIGNED))   FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE ")
            myresult = mycursor.fetchone()

            if myresult[0] == None:
                self.id = "1"
            else:
                self.id = int(myresult[0]) + 1
            ret = self.FN_CHECK_DUP_NAME(name)
            if name == '':
                QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")
            else:
                if ret != True :

                    nextLevel1 = self.FN_GET_NEXTlEVEL_ID(nextLevel)
                    sql = "INSERT INTO Hyper1_Retail.LOYALITY_CUSTOMER_TYPE" \
                          "         VALUES ( %s, %s, %s,  %s,%s)"

                    # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                    val = (self.id, name,points,nextLevel1 ,  status
                           )
                    mycursor.execute(sql, val)
                    mycursor.close()

                    print(mycursor.rowcount, "Cust Tp inserted.")
                    QtWidgets.QMessageBox.information(self, "Success", "Cust Tp inserted.")
                    db1.connectionCommit(self.conn1)
                    self.FN_GET_CUSTTPS()
                    # rowNo= self.Qtable_custTP.rowCount()
                    # self.Qtable_custTP.insertRow(rowNo)
                    # item = QTableWidgetItem(str(self.id))
                    # self.Qtable_custTP.setItem(rowNo, 0, item)
                    # item = QTableWidgetItem(str(name))
                    # self.Qtable_custTP.setItem(rowNo, 1, item)
                    # item = QTableWidgetItem(str(points))
                    # self.Qtable_custTP.setItem(rowNo, 2, item)
                    #
                    #
                    # item = QTableWidgetItem(nextLevel)
                    # self.Qtable_custTP.setItem(rowNo, 3, item)
                    #
                    # item = QTableWidgetItem(custType)
                    # self.Qtable_custTP.setItem(rowNo, 4, item)
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Name duplicated' ")
                    #mycursor.close()
        except Exception as err:
            #mycursor.close()
            print(err)

    def FN_MODIFY_CUSTTP(self):
        try:
            mycursor = self.conn1.cursor()
            if len(self.Qtable_custTP.selectedIndexes()) > 0:
                rowNo = self.Qtable_custTP.selectedItems()[0].row()
                id = self.Qtable_custTP.item(rowNo, 0).text()
                desc = self.Qtable_custTP.item(rowNo, 1).text()
                points = self.Qtable_custTP.item(rowNo, 2).text()
                nextLevel = self.Qtable_custTP.item(rowNo, 3).text()
                # nextLevel = CMB_nextLevel.currentText()
                status = self.Qtable_custTP.item(rowNo, 4).text()
                ret1 = self.FN_CHECK_DUP_NEXTLEVEL(nextLevel)
                nextLevel = self.FN_GET_NEXTlEVEL_ID(nextLevel)
                ret1 = True
                ret = self.FN_CHECK_STATUS(status)

                if ret != False and ret1 != False:
                #if FN_CHECK_DUP_NEXTLEVEL
                    if status == 'Active':
                        status = 1
                    else:
                        status = 0                   #

                    sql = "update  Hyper1_Retail.LOYALITY_CUSTOMER_TYPE set LOYCT_STATUS= %s ,LOYCT_DESC= %s,LOYCT_POINTS_TO_PROMOTE=%s ,LOYCT_TYPE_NEXT= %s where LOYCT_TYPE_ID = %s"
                    val = (status,desc,points,nextLevel ,id,)
                    mycursor.execute(sql, val)
                    mycursor.close()                #
                    print(mycursor.rowcount, "record updated.")
                    QtWidgets.QMessageBox.information(self, "Success", "Cust Tp updated")
                    db1.connectionCommit(self.conn1)
                elif ret !=True:

                    QtWidgets.QMessageBox.warning(self, "Error", "Status should be 'Active' or 'Inactive' ")

                # elif ret1 != True:
                #     #mycursor = self.conn.cursor()
                #     QtWidgets.QMessageBox.warning(self, "Error", "NextLevel is invalid' ")
            else:
                #mycursor.close()
                QtWidgets.QMessageBox.warning(self, "Error", "Please select the row you want to modify ")


        except Exception as err:
            mycursor.close()
            print(err)
        #db1.connectionClose(self.conn)
        #self.close()





