from datetime import datetime
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

from data_connection.h1pos import db1


class CL_form(QtWidgets.QDialog):
    dirname=''
    def __init__(self):
        super(CL_form, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/authorization_ui'
        self.conn = db1.connect()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createForm.ui'
        loadUi( filename, self )
        self.BTN_createForm.clicked.connect(self.FN_CREATE_FORM)
        self.CMB_formStatus.addItems(["Active", "Inactive"])
        self.CMB_formType.addItems( ["Frontend", "Backend"] )
    def FN_LOAD_MODIFY(self):
        filename = self.dirname + '/modifyForm.ui'
        loadUi( filename, self )
        CL_form.FN_GET_FORMS(self)
        self.FN_GET_FORMID()
        self.FN_GET_FORM()
        self.CMB_formName.currentIndexChanged.connect( self.FN_GET_FORM )
        self.BTN_modifyForm.clicked.connect(self.FN_MODIFY_FORM)
        self.CMB_formStatus.addItems(["Active", "Inactive"])
        self.CMB_formType.addItems( ["Frontend", "Backend"] )
    @staticmethod
    def FN_GET_FORMS(self):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT FORM_DESC FROM SYS_FORM  where FORM_STATUS  = 1 order by FORM_ID  asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_formName.addItems([row[0]])
        mycursor.close()
        return records

    def FN_GET_FORMID(self):

        self.form = self.CMB_formName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT FORM_ID FROM SYS_FORM WHERE FORM_DESC = %s  "
        x = (self.form,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        self.LB_formID.setText(myresult[0])
        mycursor.close()

    def FN_GET_FORM(self):

        self.FN_GET_FORMID()
        self.id = self.LB_formID.text()
        mycursor = self.conn.cursor()
        sql_select_query = "select * from SYS_FORM where FORM_ID = %s"
        x = (self.id,)
        mycursor.execute(sql_select_query, x)
        record = mycursor.fetchone()
        #print(record)
        self.LE_desc.setText(record[1])
        self.CMB_formType.setCurrentText(record[2])
        self.LE_help.setText(record[4])
        if record[3]== '1':

            self.CMB_formStatus.setCurrentText('Active')
        else:
            self.CMB_formStatus.setCurrentText( 'Inactive' )
        mycursor.close()


        print(mycursor.rowcount, "record retrieved.")

    def FN_MODIFY_FORM(self):
        self.id = self.LB_formID.text()
        self.desc = self.LE_desc.text().strip()
        self.type = self.CMB_formType.currentText()
        self.status = self.CMB_formStatus.currentText()
        if self.status == 'Active':
            self.status = '1'
        else:
            self.status = '0'
        self.help = self.LE_help.text()

        if self.desc == '' or self.type == '':
            QtWidgets.QMessageBox.warning( self, "Error", "Please all required field" )
        #connection = mysql.connector.connect(host='localhost',database='test',user='shelal',password='2ybQvkZbNijIyq2J',port='3306')
        else:
            mycursor = self.conn.cursor()

            changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

            sql = "UPDATE SYS_FORM  set FORM_DESC= %s ,FORM_TYPE= %s  , FORM_STATUS = %s, FORM_HELP = %s where FORM_id= %s "

            val = (self.desc  , self.type, self.status, self.help, self.id)

            mycursor.execute(sql, val)
            # mycursor.execute(sql)

            db1.connectionCommit( self.conn )
            mycursor.close()
            db1.connectionClose(self.conn)

            print(mycursor.rowcount, "record Modified.")

            self.close()
            QtWidgets.QMessageBox.information( self, "Success", "Form is modified successfully" )

    def FN_CREATE_FORM(self):
        self.desc = self.LE_desc.text().strip()

        self.type = self.CMB_formStatus.currentText()
        self.help= self.LE_help.text()

        self.status = self.CMB_formStatus.currentText()
        if self.status == 'Active':
            self.status = '1'
        else:
            self.status = '0'
        if self.desc == '' or self.type ==''  :
            QtWidgets.QMessageBox.warning( self, "Error", "Please all required field" )

        else:
            mycursor = self.conn.cursor()
            # get max userid
            mycursor.execute("SELECT max(cast(FORM_ID  AS UNSIGNED)) FROM SYS_FORM")
            myresult = mycursor.fetchone()

            if myresult[0] == None:
                self.id = "1"
            else:
                self.id = int(myresult[0]) + 1

            sql = "INSERT INTO SYS_FORM (FORM_ID, FORM_DESC, FORM_TYPE,FORM_STATUS,FORM_HELP)  VALUES ( %s, %s, %s, %s,%s)"

            # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
            val = (self.id, self.desc, self.type, self.status, self.help)
            mycursor.execute(sql, val)
            # mycursor.execute(sql)
            db1.connectionCommit(self.conn)
            mycursor.close()
            db1.connectionClose(self.conn)


            print(mycursor.rowcount, "record inserted.")

            self.close()
            QtWidgets.QMessageBox.information( self, "Success", "Form is created successfully" )