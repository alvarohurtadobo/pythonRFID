import sys
from PyQt4 import QtGui, QtCore

class AlarmaGUI(QtGui.QWidget):    
    def __init__(self):
        #super(AlarmaGUI, self).__init__()
        QtGui.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        # Parámetros constantes:
        self.titulo = 'Estado de alarma'
        self.estado = 'Activado'
        # Clases auxiliares:
        self.initUI()
        # Al inicializarse la clase se muestra:
        self.showFullScreen()
        #self.show()


    def initUI(self):
        # Definición de campos:
        self.imagen = QtGui.QLabel(self)
        self.imagen.setGeometry(150, 150, 250, 250)
        self.fechaYHora = QtGui.QLineEdit('Fecha')
        self.estadoAlarma = QtGui.QLineEdit('Alarma Activada')
        self.fechaYHora.setGeometry(25, 25, 250, 250)
        self.pixmap = QtGui.QPixmap('./imagenes/alarmaActivada.png')
        self.imagen.setPixmap(self.pixmap)

        # Layouts:
        layoutVertical = QtGui.QVBoxLayout()
        layoutHorizontalSuperior = QtGui.QHBoxLayout()

        # Agregar Widgets
        layoutHorizontalSuperior.addWidget(self.estadoAlarma)
        layoutHorizontalSuperior.addWidget(self.fechaYHora)
        layoutVertical.addLayout(layoutHorizontalSuperior)
        layoutVertical.addWidget(self.imagen)

        self.setMinimumHeight(450)
        self.setLayout(layoutVertical)
        self.setGeometry(300, 300, 300, 150)
        # Algunas visualizaciones:
        self.setWindowIcon(QtGui.QIcon('./imagenes/logo.png')) 
        self.setWindowTitle(self.titulo)
        

def main():
    app = QtGui.QApplication(sys.argv)
    ex = AlarmaGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()