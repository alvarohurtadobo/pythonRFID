from PyQt4 import QtGui

class AlarmaGUI(QtGui.QWidget):    
    def __init__(self):
        super(AlarmaGUI, self).__init__()
        self.titulo = 'Estado de alarma'
        self.estado = 'Activado'
        self.initUI()

    def initUI(self):