import gui.editvar_ui 
from PyQt5.QtWidgets import QDialog
from model.cyvariable import CyVariable
from model.cycontroller import CyController

class EditVarDialog(QDialog, gui.editvar_ui.Ui_Dialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		self.var = None

	    # get current date and time from the dialog
	def readVar(self):
		if self.var is None:
			return
		self.desc.insertPlainText(self.var.getDesc())
		self.name.insert(self.var.getName())

	def setVarId(self, varid):
		self.var=CyController().getVar(varid)
	
	def setVar(self, var):
		self.var = var

	def createVar(self):
		if self.var is None:
			self.var = CyController().createVar()

	#write content of dialog into var, create var if needed
	def writeVar(self):
		if self.var is None:
			self.createVar()
		self.var.setName(self.name.text())
		self.var.setDesc(self.desc.toPlainText())
		return self.var

	#initializes the dialog and save edits, returns the var itself
	#if no var is given, new one is created
	def edit(self):
		self.readVar()
		result = self.exec_()
		retval = None
		if result == QDialog.Accepted:
			retval = self.writeVar()
		return (retval, result == QDialog.Accepted)

	#calls the editdialog with varable itself at input
	@staticmethod
	def editVar(var, parent = None):
		dialog = EditVarDialog(parent)
		dialog.setVar(var)
		return dialog.edit()
	
	#calls the editdialog with varid at input
	@staticmethod
	def editVarId(varid, parent = None):
		dialog = EditVarDialog(parent)
		dialog.setVarId(varid)
		return dialog.edit()

