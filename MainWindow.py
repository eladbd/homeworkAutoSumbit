import os
import threading
import seleniumScript
import CredReader
from CredReader import read
import CreateCred
from CreateCred import Credentials
from auto_submit import Ui_Form
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

cred_filename = 'CredFile.ini'
key_file = 'key.key'
key = ''


class SubmitWindow(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cred = Credentials()
        # self.cred.create_cred()
        if (os.path.exists('CredFile.ini')):
            username, password = read(cred_filename, key_file, key)
            self.ui.username_input.setText(username)
            self.ui.password_input.setText(password)
            os.remove(cred_filename)
        self.ui.courses_comboBox.addItem('10008 אלגוריתמיקה 2, ד"ר לוריא צור,  יום שלישי, 12:00-14:45,   , סמסטר : ב')
        self.ui.courses_comboBox.addItem('10015 הסתברות וסטטיסטיקה 1, ד"ר שטיינבוך ביאנה,  יום שלישי, 10:00-11:45,   , סמסטר : ב')
        self.ui.courses_comboBox.addItem('10036 מסדי נתונים, מר תבור שי,  יום חמישי, 10:00-10:45,   , סמסטר : ב')
        self.ui.courses_comboBox.addItem('10040 מערכות הפעלה, ד"ר שפנייר אסף,  יום ראשון, 09:00-11:45,   , סמסטר : ב')
        self.ui.courses_comboBox.addItem("10040 מערכות הפעלה, גב' באש תמר,  יום חמישי, 12:00-14:45,   , סמסטר : ב")
        self.ui.courses_comboBox.addItem('10072 פיסיקה 2 - חשמל ומגנטיות, ד"ר כהנא אביב,  יום שני, 09:00-11:45,   , סמסטר : ב')
        self.ui.courses_comboBox.addItem('10077 מבוא לתכנות מדעי, ד"ר חסין יהודה,  יום רביעי, 09:00-09:45,   , סמסטר : ב')
        self.ui.submit_button.clicked.connect(self.checkLogin)
        self.ui.browse_file_button.clicked.connect(self.browseFile)
        self.ui.submit_button.clicked.connect(self.launch_selenium_thread)

    def checkLogin(self):
        self.username = self.ui.username_input.text()
        self.password = self.ui.password_input.text()
        check = self.ui.save_login_checkBox.isChecked()
        if check:
            CreateCred.main(self.username, self.password)

        # CredReader.read(cred_filename, key_file, key)
        # if self.username == 'user' and self.password == 'pass':
        #     qtw.QMessageBox.information(self, "Success", "Login done")
        # else:
        #     qtw.QMessageBox.critical(self, "failed", 'failed to login')

    def browseFile(self):
        self.fname = QFileDialog.getOpenFileName()[0]
        self.ui.file_path_text.setText(self.fname)

    def launch_selenium_thread(self):
        t = threading.Thread(target=self.submitForm)
        t.start()

    def submitForm(self):
        # q = queue.Queue()
        seleniumScript.go(self.username, self.password, self.fname,
                          self.ui.courses_comboBox.currentText(), self.ui.assignment_number_input.text())
        # result = q.get()
        # if result == -1: # need to fix
        #     password_error = QMessageBox()
        #     password_error.setText('Username or password is invalid')
        #     password_error.setIcon(QMessageBox.Critical)
        #     password_error.exec_()
        # elif result == -2:
        #     course_error = QMessageBox()
        #     course_error.setText('No such assignment')
        #     course_error.setIcon(QMessageBox.Critical)
        #     course_error.exec_()


if __name__ == '__main__':
    app = qtw.QApplication([])

    widget = SubmitWindow()
    widget.show()
    app.exec_()
