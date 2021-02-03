from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from data_connection.h1pos import db1



class CL_printCoupon(QtWidgets.QDialog):

    def __init__(self):
        super(CL_printCoupon, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/coupon_ui'
        self.conn = db1.connect()


    def FN_LOADUI(self):
        filename = self.dirname + '/printCoupon.ui'
        loadUi(filename, self)
        self.FN_getData()

    def FN_getData(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COP_DESC,COP_ID FROM COUPON")
        records = mycursor.fetchall()
        for row,val in records:
            self.CMB_CouponDes.addItem(row,val)
        mycursor.close()








