import sys
from time import sleep, strftime
from PyQt4 import QtGui, QtCore

class AlarmaGUI(QtGui.QWidget):         #QWidget
    def __init__(self):
        #super(AlarmaGUI, self).__init__()
        QtGui.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        # Parámetros constantes:
        self.titulo = 'Estado de alarma'
        self.estado = 'Activado'
        # Clases auxiliares:
        self.initUI()
        # Al inicializarse la clase se muestra:
        #self.showFullScreen()
        self.show()


    def initUI(self):
        # Definición de campos:
        self.stringSolicitudAutentificacion = 'AUTENTIFIQUESE POR FAVOR'
        self.imagen = QtGui.QLabel(self)
        self.imagen.setGeometry(150, 150, 250, 250)
        self.labelAutentificacion = QtGui.QLabel(self.stringSolicitudAutentificacion)
        self.labelAutentificacion.setFont(QtGui.QFont('SansSerif', 36))
        self.labelIdentificado = QtGui.QLabel('')
        self.labelIdentificado.setFont(QtGui.QFont('SansSerif', 24))

        self.imagenLogo = QtGui.QLabel(self)
        self.fechaYHora = QtGui.QLabel('Fecha')
        self.estadoAlarma = QtGui.QLabel('Alarma Activada')
        self.fechaYHora.setGeometry(25, 25, 250, 250)
        self.pixmapAct = QtGui.QPixmap('./imagenes/alarmaActivada.png')
        self.pixmapDeact = QtGui.QPixmap('./imagenes/alarmaDesactivada.png')
        self.pixmapLogo = QtGui.QPixmap('./imagenes/logoWeb.png')
        self.imagen.setPixmap(self.pixmapAct)
        self.imagenLogo.setPixmap(self.pixmapLogo)
        self.lcd = QtGui.QLCDNumber(self)
        self.lcd.setDigitCount(19)
        self.lcd.setMaximumHeight(60)
        self.lcd.display(strftime("%Y"+"-"+"%m"+"-"+"%d"+" "+"%H"+":"+"%M"+":"+"%S"))
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)

        # Layouts:
        layoutVertical = QtGui.QVBoxLayout()
        layoutHorizontalSuperior = QtGui.QHBoxLayout()

        # Agregar Widgets
        layoutHorizontalSuperior.addWidget(self.imagenLogo)
        #layoutHorizontalSuperior.addWidget(self.timer)
        layoutHorizontalSuperior.addWidget(self.lcd)
        layoutVertical.addLayout(layoutHorizontalSuperior)
        layoutVertical.addWidget(self.imagen)
        layoutVertical.addWidget(self.labelAutentificacion)
        layoutVertical.addWidget(self.labelIdentificado)
        layoutVertical.setAlignment(self.imagen, QtCore.Qt.AlignHCenter)
        layoutVertical.setAlignment(self.labelAutentificacion, QtCore.Qt.AlignHCenter)
        layoutVertical.setAlignment(self.labelIdentificado, QtCore.Qt.AlignHCenter)

        self.setMinimumHeight(450)
        self.setLayout(layoutVertical)
        self.setGeometry(300, 300, 300, 150)
        # Algunas visualizaciones:
        self.setWindowIcon(QtGui.QIcon('./imagenes/logo.png')) 
        self.setWindowTitle(self.titulo)
        
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
            #self.desactivarAlarma(strftime("%Y"+"-"+"%m"+"-"+"%d"),strftime("%H"+":"+"%M"+":"+"%S"))

    def Time(self):
        self.lcd.display(strftime("%Y"+"-"+"%m"+"-"+"%d"+" "+"%H"+":"+"%M"+":"+"%S"))

    def desactivarAlarma(self,id,nombre):
        self.imagen.setPixmap(self.pixmapDeact)
        self.labelIdentificado.setText(nombre)
        self.labelAutentificacion.setText(id)

    def activarAlarma(self):
        self.imagen.setPixmap(self.pixmapAct)
        self.labelAutentificacion.setText(self.stringSolicitudAutentificacion)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = AlarmaGUI()
    print('Sali inicializacion')
    sys.exit(app.exec_())
    print('Sali exec')
    for i in range(10):
        print(i)
        ex.desactivarAlarma(str(i),strftime("%Y"+"-"+"%m"+"-"+"%d"+" "+"%H"+":"+"%M"+":"+"%S"))
        sleep(2)
        ex.activarAlarma()
        sleep(2)
    
    

if __name__ == '__main__':
    main()