import sys
import multiprocessing
from time import sleep, strftime
from PyQt4 import QtGui, QtCore

class GUIParalela():
    myQueue = multiprocessing.Queue()

    def __init__(self):
        app = QtGui.QApplication(sys.argv)
        p = multiprocessing.Process(target=self.simularLlegadaDatos,args=())
        p.start()
        interfaz = AlarmaGUI(GUIParalela.myQueue)
        sys.exit(app.exec_())
        p.join() 
        
    def simularLlegadaDatos(self):
        for i in range(10):
            valor = (True,str(i),strftime("%Y"+"-"+"%m"+"-"+"%d"+" "+"%H"+":"+"%M"+":"+"%S"))
            print(i,': ',valor)
            GUIParalela.myQueue.put(valor)
            sleep(2)
            valor = (False,'','')
            GUIParalela.myQueue.put(valor)
            print(i,': ',valor)
            sleep(2)  



class AlarmaGUI(QtGui.QWidget):         #QWidget #QMainWindow
    def __init__(self,fila,parent=None):
        super(AlarmaGUI, self).__init__(parent)
        #self.setupUI(self)
        #QtGui.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        # Parámetros constantes:
        self.titulo = 'Estado de alarma'
        self.estado = 'Activado'
        self.thread = ThreadClass(fila)
        self.thread.start()
        self.connect(self.thread,QtCore.SIGNAL('ACTUALIZAR_ESTADO'),self.actualizarValor)
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

    def actualizarValor(self,valor):
        print('Actualizando a:',valor)
        (estado, id, nombre) = valor
        if estado:
            self.desactivarAlarma(id,nombre)
        else:
            self.activarAlarma()

    def desactivarAlarma(self,id,nombre):
        self.imagen.setPixmap(self.pixmapDeact)
        self.labelAutentificacion.setText(id)
        self.labelIdentificado.setText(nombre)

    def activarAlarma(self):
        self.imagen.setPixmap(self.pixmapAct)
        self.labelAutentificacion.setText(self.stringSolicitudAutentificacion)
        self.labelIdentificado.setText('')


class ThreadClass(QtCore.QThread):
    def __init__(self,fila,parent = None):
        super(ThreadClass,self).__init__(parent)
        self.queue = fila

    def run(self):
        while True:
            if not self.queue.empty():
                valor = self.queue.get() # valor = (estado, id, nombre)
                print(valor)
                self.emit(QtCore.SIGNAL('ACTUALIZAR_ESTADO'),valor)
                print('I received')


if __name__ == '__main__':
    a = GUIParalela()