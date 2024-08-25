from blackjack import blackjackUI
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import * 
from PyQt5 import uic, QtCore
import database
import sys

userdata = {}
def updateuserdata() -> dict:
	"""Updates the userdata info"""
	global userdata
	userdata.clear()
	data = database.get_user_login()
	for a in data:
		userdata[a[0]] = a[1]
	return userdata



# class for main window
class mainui(QMainWindow):
	def __init__(self) -> None:
		super(mainui,self).__init__()
		self.Loginui = LoginUi()
		self.Signupui = SignupUi()
		self.stackedui = QStackedWidget()
		self.stackedui.addWidget(self.Loginui)
		self.stackedui.addWidget(self.Signupui)
		self.stackedui.setCurrentIndex(0)
		self.stackedui.show()

	def loadgame(self,username: str):
		self.stackedui.addWidget(blackjackUI(username))
		self.stackedui.setCurrentIndex(2)


		




# class for login window 
class LoginUi(QWidget):
	def __init__(self):
		super(LoginUi, self).__init__()
		updateuserdata()
		
	
		# Loading ui file
		uic.loadUi('UI/login.ui', self)
		
		# Declaring childs
		self.loginButton = self.findChild(QPushButton, "loginb")
		self.signupButton = self.findChild(QPushButton, "signupb")
		self.usernameField = self.findChild(QLineEdit, "username")
		self.passwordField = self.findChild(QLineEdit, "password")
		self.passwordField.setEchoMode(QLineEdit.Password)

		# assiging login Button function
		self.loginButton.clicked.connect(self.checklogin)
		self.signupButton.clicked.connect(self.signup)
		# self.show()


	def signup(self):
		widgets.stackedui.setCurrentIndex(1)


	def checklogin(self):
		username = self.usernameField.text()
		password = self.passwordField.text()
		if username != "":
			if username in userdata:
				if password != "":
					if password == userdata[username]:
						# QMessageBox.about(self,"Passed","Login Succesfull")
						widgets.loadgame(username=username)
					else:
						QMessageBox.about(self,"Error",f"Password doesn't match")
				else:
					QMessageBox.about(self,"Enter details","Enter Password")
			else:
				QMessageBox.about(self,"Error","username not exists")
		else:
			QMessageBox.about(self,"Enter details","Enter username")


class SignupUi(QWidget):
	def __init__(self):
		super(SignupUi,self).__init__()

		# loading signup ui file
		uic.loadUi('UI/signup.ui',self)
		self.setFixedSize(1000,700)
		# declaring childs of ui
		self.loginButton = self.findChild(QPushButton, "loginb")
		self.signupButton = self.findChild(QPushButton, "signupb")
		self.usernameField = self.findChild(QLineEdit, "username")
		self.confirmpass = self.findChild(QLineEdit, "confirmPass")
		self.confirmpass.setEchoMode(QLineEdit.Password)
		self.passwordField = self.findChild(QLineEdit, "password")
		self.passwordField.setEchoMode(QLineEdit.Password)

		# applying functions to buttons
		self.signupButton.clicked.connect(self.singup)
		self.loginButton.clicked.connect(self.login)

	def singup(self):
		username = self.usernameField.text()
		password = self.passwordField.text()
		conpass = self.confirmpass.text()
		if username != "":
			if username in userdata:
				QMessageBox.about(self,"Error","Username already exisit")
			else:
				if password == '':
					QMessageBox.about(self,"Error","Please fill all details")
				elif conpass == '':
					QMessageBox.about(self,"Error","Please fill all details")
				elif password == conpass:
					database.insert_new_user(username,password)
					updateuserdata()
					QMessageBox.about(self,"Registered","User registred!!! Now you can login")
					widgets.stackedui.setCurrentIndex(0)
				elif password != conpass:
					QMessageBox.about(self,"Error","Passsword doesn't matched")
				else:
					QMessageBox.about(self,"Error","Unknow Error occured")
		else:
			QMessageBox.about(self,"Error","Please fill all details")
					

	def login(self):
		widgets.stackedui.setCurrentIndex(0)




# class stackui(QStackedWidget):
# 	def __init__(self) -> None:
# 		super(stackui,self).__init__()

# 		self.addWidget(LoginUi())
# 		self.addWidget(SignupUi())
# 		self.addWidget(blackjackUI())
# 		self.setFixedSize(1000,700)
# 		self.show()


# Initialization 

app = QApplication(sys.argv)
# mainapp = QMainWindow()
# widgets = stackui()
widgets=  mainui()
app.exec_()