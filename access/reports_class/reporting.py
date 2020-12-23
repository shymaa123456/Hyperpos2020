#!/usr/bin/env python3
# -*     - coding: utf-8 -*-
"""
Created on Mon Jun 29 19:52:06 2020

@author: hossam
"""

#####

import pandas as pd
from PyQt5.QtGui import QStandardItemModel

from access.promotion_class.Promotion_Add import CheckableComboBox
from access.reports_class.ReportPDF import body, Text
from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from data_connection.h1pos import db1
import sys
class CL_report(QtWidgets.QDialog):
    #self.Qtime_from.dateTime().toString('hh:mm:ss')
    model = QStandardItemModel()

    switch_window = QtCore.pyqtSignal()
    cond=0
    status=0
    query=""
    customer_group_list=[]
    sponsor_list=[]
    magazine_list=[]
    company_list=[]
    branch_list=[]
    conn=db1.connect()

    prom_status=""
    prom_CG= ""
    sponsor_prom=""
    magazine_prom=""
    bmc=""
    list_num = []

    def FN_close(self):
        self.close()

    def FN_loadData(self, PROM_ID):
        self.customer_group_list.clear()
        self.sponsor_list.clear()
        self.magazine_list.clear()
        self.company_list.clear()
        self.branch_list.clear()

        if len(self.Qcombo_company.currentData()) > 0:
            for i in self.Qcombo_company.currentData():
                self.company_list.append("'" + i + "'")
        if len(self.Qcombo_branchEdition.currentData()) > 0:
            for i in self.Qcombo_branchEdition.currentData():
                self.branch_list.append("'" + i + "'")

        if self.QcheckBox_customer_group.isChecked():
            if len(self.Qcombo_cust_group.currentData())>0:
                for i in self.Qcombo_cust_group.currentData():
                    self.customer_group_list.append("'" + i + "'")
                self.prom_CG = "JOIN `promotion_group` ON `PROMOTION_GROUP`.`CG_GROUP_ID` IN (" +','.join(self.customer_group_list) + ")"
        if self.QcheckBox_sponsor_prom.isChecked():
            if len(self.Qcombo_sponsor.currentData()) > 0:
                for i in self.Qcombo_sponsor.currentData():
                    self.sponsor_list.append("'" + i + "'")
                self.sponsor_prom="JOIN `PROMOTION_SPONSER` ON `PROMOTION_SPONSER`.`SPONSER_ID`IN(" +','.join(self.sponsor_list) + ")"
        if self.QcheckBox_magazine.isChecked():
            if len(self.Qcombo_magazine.currentData()) > 0:
                for i in self.Qcombo_magazine.currentData():
                    self.magazine_list.append("'" + i + "'")
                self.magazine_prom="AND `PROMOTION_HEADER`.`MAGAZINE_ID` IN ("+','.join(self.magazine_list)+")"
        if self.QcheckBox_department.isChecked():
            self.bmc = "AND `PROMOTION_DETAIL`.`BMC_ID` IN (" + self.Qcombo_classification.currentData() + ")"
        self.Qtable_promotion.setRowCount(0)
        self.conn = db1.connect()


        mycursor = self.conn.cursor()
        query=""
        if self.cond==1:
            self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID`and `PROMOTION_HEADER`.`PROM_ID`= '"+self.Qline_promotion.text()+"'")
        elif self.cond==2:
            self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID`"+self.bmc+" " + self.prom_status + " " + self.prom_CG + " " + self.sponsor_prom + " "+self.magazine_prom+"and `PROMOTION_HEADER`.`PROM_TYPE_ID`= '" + self.Qcombo_promotion.currentData() +"'"+self.prom_status+"and `PROMOTION_DETAIL`.`PROM_START_DATE`<='" + self.Qdate_from.dateTime().toString('yyyy-MM-dd') +" " + "00:00:00" +"' and `PROMOTION_DETAIL`.`PROM_END_DATE`>='" + self.Qdate_to.dateTime().toString('yyyy-MM-dd') +" " + "23:59:00" +"' JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`IN (" + ','.join(self.branch_list )+ ") and `PROM_BRANCH`.`COMPANY_ID` IN ("+ ','.join(self.company_list)+ ")")
        elif self.cond==3:
            self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID`and `PROMOTION_DETAIL`.`POS_GTIN`= '" + self.Qline_promotion_2.text() +"'" + self.prom_status +" "+self.bmc+"" + self.prom_CG + " "+self.sponsor_prom+" "+self.magazine_prom+"and `PROMOTION_DETAIL`.`PROM_START_DATE`>='" + self.Qdate_from.dateTime().toString('yyyy-MM-dd') + " " +"00:00:00" + "' and `PROMOTION_DETAIL`.`PROM_END_DATE`<='" + self.Qdate_to.dateTime().toString('yyyy-MM-dd') + " " + "23:59:00" + "' JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`IN (" + ','.join(self.branch_list )+ ") and `PROM_BRANCH`.`COMPANY_ID` IN ("+ ','.join(self.company_list )+ ")")

               # elif self.cond==6:
        #     self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID` JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`=(SELECT `BRANCH`.`BRANCH_NO` FROM `BRANCH` WHERE `BRANCH`.`BRANCH_DESC_A`='" + self.Qcombo_branchEdition.currentText() + "')")
        # elif self.cond==7:
        #     self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID` JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`=(SELECT `BRANCH`.`BRANCH_NO` FROM `BRANCH` WHERE `BRANCH`.`BRANCH_DESC_A`='" + self.Qcombo_branchEdition.currentText() + "') AND `PROMOTION_HEADER`.`MAGAZINE_ID`=(SELECT `MAGAZINE`.`MAGAZINE_ID` FROM `MAGAZINE` WHERE `MAGAZINE`.`MAGAZINE_DESC`='" + self.Qcombo_magazine.currentText() + "')")
             # elif self.cond==11 :
        #     self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID` JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`=(SELECT `BRANCH`.`BRANCH_NO` FROM `BRANCH` WHERE `BRANCH`.`BRANCH_DESC_A`='" + self.Qcombo_branchEdition.currentText() + "')")

        print(self.query)

        mycursor.execute(self.query)
        records = mycursor.fetchall()
        print(records)
        for row_number, row_data in enumerate( records ):

          self.Qtable_promotion.insertRow( row_number )
          for column_number, data in enumerate( row_data ):
               self.Qtable_promotion.setItem( row_number, column_number, QTableWidgetItem( str( data ) ) )
        mycursor.close()
        self.disable()


    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY" )
        records = mycursor.fetchall()
        print(records)
        for row , val in records:
            self.Qcombo_company.addItem(row,val)
        mycursor.close()


    def FN_GET_Branch(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT BRANCH_DESC_A ,BRANCH_NO FROM BRANCH" )
        records = mycursor.fetchall()
        for row,val in records:
            self.Qcombo_branchEdition.addItem( row,val )
        mycursor.close()
    def FN_GET_CustomerGroup(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT CG_DESC,CG_GROUP_ID FROM CUSTOMER_GROUP" )
        records = mycursor.fetchall()
        for row ,val in records:
            self.Qcombo_cust_group.addItem(row,val)
        mycursor.close()
    def FN_GET_MAGAZINE(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT MAGAZINE_DESC , MAGAZINE_ID FROM MAGAZINE" )
        records = mycursor.fetchall()
        for row, val in records:
            self.Qcombo_magazine.addItem( row,val )
        mycursor.close()
    def FN_GET_department(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT DEPARTMENT_DESC ,DEPARTMENT_ID FROM DEPARTMENT" )
        records = mycursor.fetchall()
        for row, val in records:
            self.Qcombo_department.addItem( row,val )
        mycursor.close()
    def FN_GET_promotion_sponser(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT SPONSER_NAME ,SPONSER_ID FROM SPONSER" )
        records = mycursor.fetchall()
        for row ,val in records:
            self.Qcombo_sponsor.addItem( row,val )
        mycursor.close()

    def FN_GET_section(self, id):
        self.Qcombo_section.clear()
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT SECTION_DESC ,SECTION_ID FROM SECTION where DEPARTMENT_ID = '"+id+"'")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_section.addItem(row, val)
        mycursor.close()


    def FN_GET_classification(self, id):
        self.Qcombo_classification.clear()
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT BMC_LEVEL4_DESC , BMC_LEVEL4 FROM BMC_LEVEL4 where SECTION_ID ="+id+"")
        records = mycursor.fetchall()
        print(records)
        for row , val in records:
             self.Qcombo_classification.addItem(row , val)
        mycursor.close()

    def FN_GET_promotion_type(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT PROMT_NAME_AR , PROMOTION_TYPE_ID FROM PROMOTION_TYPE order by PROMOTION_TYPE_ID*1 " )
        records = mycursor.fetchall()
        for row,val in records:
            self.Qcombo_promotion.addItem( row,val )
        mycursor.close()



    def FN_Checked_Selected(self):
       self.radioBtnPromNum_2.setChecked(False)
       self.radioBtnPromNum.setChecked(False)
       self.radioButton_2.setChecked(True)
       self.Qline_promotion.setEnabled(False)
       self.Qline_promotion.clear()
       self.groupBox_2.setEnabled(True)
       self.Qcombo_promotion.setEnabled(True)
       self.Qline_promotion_2.setEnabled(False)
       self.Qline_promotion_2.clear()
       self.cond=2
       self.Qtable_promotion.setRowCount(0)
       self.disable()


    def FN_Checked_Selected2(self):
       self.radioBtnPromNum_2.setChecked(False)
       self.radioButton_2.setChecked(False)
       self.radioBtnPromNum.setChecked(True)

       self.Qcombo_promotion.setEnabled(False)
       self.Qline_promotion.setEnabled(True)
       self.groupBox_2.setEnabled(False)
       self.Qline_promotion_2.setEnabled(False)
       self.Qline_promotion_2.clear()
       self.cond=1
       self.Qtable_promotion.setRowCount(0)
       self.disable()

    def FN_Checked_Selected3(self):
       self.radioBtnPromNum.setChecked(False)
       self.radioButton_2.setChecked(False)
       self.radioBtnPromNum_2.setChecked(True)
       self.Qline_promotion.clear()
       self.Qline_promotion_2.setEnabled(True)
       self.groupBox_2.setEnabled(False)
       self.groupBox_2.setEnabled(True)
       self.Qcombo_promotion.setEnabled(False)
       self.cond = 3
       self.Qtable_promotion.setRowCount(0)
       self.disable()

    def FN_Check_Group(self):
        if self.QcheckBox_customer_group.isChecked():
            self.Qcombo_cust_group.setEnabled(True)
            self.Qtable_promotion.setRowCount(0)
            self.disable()
        else:
            self.customer_group_list.clear()
            self.Qcombo_cust_group.setEnabled(False)
            self.prom_CG = ""



    def FN_Check_Sponsor(self):
        if self.QcheckBox_sponsor_prom.isChecked():
            self.Qcombo_sponsor.setEnabled(True)
            self.Qtable_promotion.setRowCount(0)
            self.disable()
        else:
            self.Qcombo_sponsor.setEnabled(False)
            self.sponsor_prom=""

    def FN_Check_department(self):
        if self.QcheckBox_department.isChecked():
            self.Qcombo_department.setEnabled(True)
            self.Qtable_promotion.setRowCount(0)
            self.disable()

        else:
            self.Qcombo_department.setEnabled(False)

    def FN_Check_Magazine(self):
        if self.QcheckBox_magazine.isChecked():
            self.Qcombo_magazine.setEnabled(True)
            self.Qtable_promotion.setRowCount(0)
            self.disable()


        else:
            self.Qcombo_magazine.setEnabled(False)
            self.magazine_prom=""



    def FN_Check_Active(self):
        self.status=1
        self.Qtable_promotion.setRowCount(0)
        self.disable()
        self.prom_status="and `PROMOTION_DETAIL`.`PROM_STATUS`='1'"



    def FN_Check_Stopped(self):
        self.status=0
        self.Qtable_promotion.setRowCount(0)
        self.disable()
        self.prom_status="and `PROMOTION_DETAIL`.`PROM_STATUS`='0'"



    def FN_Check_Expired(self):
        self.status=2
        self.Qtable_promotion.setRowCount(0)
        self.disable()
        self.prom_status="and `PROMOTION_DETAIL`.`PROM_STATUS`='2'"



    def FN_Check_All(self):
        self.Qtable_promotion.setRowCount(0)
        self.disable()
        self.prom_status=""



    def handleSave(self):


        frame = pd.read_sql(str(self.query),self.conn)
        df = pd.DataFrame(frame,columns=['PROM_ID', 'PROM_TYPE_ID', 'PROM_CREATED_BY', 'PROM_CREATED_BY', 'PROM_CREATED_ON','PROM_LINE_NO'])

        # Dump Pandas DataFrame to Excel sheet
        writer = pd.ExcelWriter('myreport.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', startrow=2)
        writer.save()
        import os
        os.system('myreport.xlsx')
        ####################################
    def saveFile(self):
        df = pd.DataFrame()
        savePath = QtGui.QFileDialog.getSaveFileName(None, "Blood Hound","Testing.csv", "CSV files (*.csv)")
        rows = self.Qtable_promotion.rowCount()
        columns = self.Qtable_promotion.columnCount()

        for i in range(rows):
            for j in range(columns):
                df.loc[i, j] = str(self.Qtable_promotion.item(i, j).text())
        df.to_csv((savePath), header=None, index=0)

    def printpreviewDialog(self):

        title = Text()
        title.setName("Invoice")
        title.setFooter(
            " Ø³ Øª 36108 Ù…Ù„Ù  Ø¶Ø±ÙŠØ¨ÙŠ 212/306/5 Ù…Ø£Ù…ÙˆØ±ÙŠÙ‡  Ø¶Ø±Ø§Ø¦Ø¨ Ø§Ù„Ø´Ø±ÙƒØ§Øª Ø§Ù„Ù…Ø³Ø§Ù‡Ù…Ø© Ø±Ù‚Ù… Ø§Ù„ØªØ³Ø¬ÙŠÙ„ Ø¨Ø¶Ø±Ø§Ø¦Ø¨ Ø§Ù„Ù…Ø¨ÙŠØ¹Ø§Øª 153/846/310 ")
        title.setFont('Scheherazade-Regular.ttf')
        title.setFontsize(10)
        title.setcodeText("15235")
        title.setwaterText("hyperone company")
        title.settelText("1266533")
        title.setbrachText("Entrance 1,EL Sheikh Zayed City")
        title.setCursor(self.Qline_promotion.text)
        title.setQuery(self.query)

        body()
        QtWidgets.QMessageBox.information(self, "Success", "Report is printed successfully")
        ######################################################
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
        #                                           " Files (*.pdf)", options=options)
        import os
        os.system('my_file.pdf')
        #print(f.read())
        # dialog = QtPrintSupport.QP
        # rintPreviewDialog()
        # dialog.paintRequested.connect(self.handlePaintRequest)
        # dialog.exec_()

    def handlePaintRequest(self, printer):
        title = Text()

        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        table = cursor.insertTable(self.Qtable_promotion.rowCount(), self.Qtable_promotion.columnCount())
        for row in range(table.rows()):
            for col in range(table.columns()):
                cursor.insertText(self.Qtable_promotion.item(row, col).text())
                cursor.movePosition(QtGui.QTextCursor.NextCell)

        document.print_(printer)

    def disable(self):
        if self.Qtable_promotion.rowCount() == 0:
            self.Qbtn_exprot.setEnabled(False)
            self.Qbtn_print.setEnabled(False)
        else:
            self.Qbtn_exprot.setEnabled(True)
            self.Qbtn_print.setEnabled(True)

    def updatestatecombo(self):
        indx = self.Qcombo_department.currentData()
        self.FN_GET_section(indx)
        indx = self.Qcombo_section.currentData()
        self.Qcombo_classification.clear()
        self.FN_GET_classification(indx)
        self.Qcombo_section.activated[str].connect(self.updateBMCcombo)



    def updateBMCcombo(self):
        indx = self.Qcombo_section.currentData()
        self.FN_GET_classification(indx)



    def __init__(self):
        super(CL_report, self).__init__()

        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        dirname = mod_path.__str__() + '/presentation/reports_ui'
        filename = dirname + '/Promotion_display.ui'
        loadUi(filename, self)
        self.setWindowTitle('HyperPOS Reporting')

        self.Qcombo_company = CheckableComboBox(self)
        self.Qcombo_company.setGeometry(242, 20, 179, 18)
        self.Qcombo_company.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.Qcombo_branchEdition = CheckableComboBox(self)
        self.Qcombo_branchEdition.setGeometry(242, 45, 179, 18)
        self.Qcombo_branchEdition.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_branchEdition.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.Qcombo_cust_group = CheckableComboBox(self)
        self.Qcombo_cust_group.setGeometry(242, 75, 179, 18)
        self.Qcombo_cust_group.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_cust_group.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.Qcombo_sponsor = CheckableComboBox(self)
        self.Qcombo_sponsor.setGeometry(242, 98, 179, 18)
        self.Qcombo_sponsor.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_sponsor.setStyleSheet("background-color: rgb(198, 207, 199)")


        self.Qcombo_magazine = CheckableComboBox(self)
        self.Qcombo_magazine.setGeometry(242, 145, 179, 18)
        self.Qcombo_magazine.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_magazine.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.Qbtn_exit.clicked.connect(self.FN_close)
        self.Qbtn_search.clicked.connect(self.FN_loadData)
        self.FN_GET_Company()
        self.FN_GET_Branch()
        self.FN_GET_CustomerGroup()
        self.FN_GET_MAGAZINE()
        self.FN_GET_department()
        self.FN_GET_promotion_sponser()
        self.FN_GET_promotion_type()
        self.Qtable_promotion.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.radioBtnPromNum.clicked.connect(self.FN_Checked_Selected2)
        self.radioButton_2.clicked.connect(self.FN_Checked_Selected)
        self.radioBtnPromNum_2.clicked.connect(self.FN_Checked_Selected3)
        self.radioBtnPromExpired.clicked.connect(self.FN_Check_Expired)
        self.radioBtnPromStop.clicked.connect(self.FN_Check_Stopped)
        self.radioBtnPromActive.clicked.connect(self.FN_Check_Active)
        self.radioBtnPromAll.clicked.connect(self.FN_Check_All)

        self.Qline_promotion.setEnabled(False)
        self.Qcombo_cust_group.setEnabled(False)
        self.Qcombo_sponsor.setEnabled(False)
        self.Qcombo_department.setEnabled(False)
        self.Qcombo_magazine.setEnabled(False)
        self.QcheckBox_customer_group.toggled.connect(self.FN_Check_Group)
        self.QcheckBox_sponsor_prom.toggled.connect(self.FN_Check_Sponsor)
        self.QcheckBox_department.toggled.connect(self.FN_Check_department)
        self.QcheckBox_magazine.toggled.connect(self.FN_Check_Magazine)
        self.Qbtn_exprot.clicked.connect(self.handleSave)
        self.groupBox_2.setEnabled(False)
        self.Qcombo_promotion.setEnabled(False)
        self.Qline_promotion_2.setEnabled(False)
        self.Qbtn_print.clicked.connect(self.printpreviewDialog)

        self.Qcombo_department.activated[str].connect(self.updatestatecombo)
        self.Qcombo_department.setCurrentIndex(0)

        #self.Qcombo_section.currentIndexChanged.connect(self.updateBMCcombo)



        self.disable()

class CL_controller():
    def __init__(self):
        pass

    def FN_show_login(self):
        self.report = CL_report()
        self.report.show()


    def FN_show_main(self):
        self.window = CL_report()

        self.report.close()

        self.window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = CL_controller()
    controller.FN_show_login()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()


