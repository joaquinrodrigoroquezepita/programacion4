import sys

from PyQt5.QtCore import QEvent, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import (
    QApplication,
    QAction,
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

TEMA_CLARO = ""

TEMA_OSCURO = """
QMainWindow, QWidget {
    background-color: #2f2f2f;
    color: #eeeeee;
}
QLineEdit {
    background-color: #1f1f1f;
    color: #ffffff;
    border: 1px solid #555555;
    padding: 6px;
}
QTextEdit {
    background-color: #1f1f1f;
    color: #dddddd;
    border: 1px solid #555555;
}
QPushButton {
    background-color: #444444;
    color: #ffffff;
    border: 1px solid #666666;
    border-radius: 4px;
    padding: 6px;
}
QPushButton:hover {
    background-color: #555555;
}
QMenuBar, QMenu, QStatusBar {
    background-color: #252525;
    color: #eeeeee;
}
QMenuBar::item:selected, QMenu::item:selected {
    background-color: #444444;
}
QComboBox {
    background-color: #1f1f1f;
    color: #eeeeee;
    border: 1px solid #555555;
    padding: 4px;
}
QLabel#titulo {
    font-size: 22px;
    font-weight: bold;
    color: #f0ad4e;
}
"""


class DialogoAcerca(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de")
        self.setFixedSize(340, 200)

        layout = QVBoxLayout(self)

        titulo = QLabel("EL CHAPO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 16, QFont.Bold))

        datos = QFormLayout()
        datos.addRow("Versión:", QLabel("1.0"))
        datos.addRow("Interfaz:", QLabel("PyQt5"))
        datos.addRow("Autor:", QLabel("Joaquin"))
        datos.addRow("Señales:", QLabel("pyqtSignal personalizado"))

        boton_cerrar = QPushButton("Cerrar")
        boton_cerrar.clicked.connect(self.accept)

        layout.addWidget(titulo)
        layout.addLayout(datos)
        layout.addWidget(boton_cerrar)


class DialogoConfirmacion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmar salida")
        self.setFixedSize(320, 120)

        layout = QVBoxLayout(self)
        etiqueta = QLabel("Hay operaciones en el historial.\n¿Desea salir de la calculadora?")
        etiqueta.setAlignment(Qt.AlignCenter)

        botones = QHBoxLayout()
        boton_salir = QPushButton("Salir")
        boton_cancelar = QPushButton("Cancelar")
        boton_salir.setDefault(True)
        boton_salir.clicked.connect(self.accept)
        boton_cancelar.clicked.connect(self.reject)
        botones.addWidget(boton_salir)
        botones.addWidget(boton_cancelar)

        layout.addWidget(etiqueta)
        layout.addLayout(botones)


class Calculadora(QMainWindow):

    resultado_calculado = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("EL CHAPO")
        self.setMinimumSize(560, 560)

        self.operador = None
        self.operando = None
        self.nuevo_numero = True
        self.total_operaciones = 0
        self.decimales = 6
        self.segundos = 0

        self._crear_acciones()
        self._crear_menus()
        self._crear_interfaz()
        self._crear_timers()
        self._conectar_senales()

        self.resultado_calculado.connect(self.agregar_al_historial)
        QApplication.instance().installEventFilter(self)
        self.mostrar_mensaje("Listo. Teclado rápido activado (Ctrl para atajos).")

    # ---------------- Acciones y menús (QAction) ----------------

    def _crear_acciones(self):
        self.accion_limpiar = QAction("Limpiar todo", self)
        self.accion_limpiar.setShortcut(QKeySequence("Ctrl+L"))

        self.accion_vaciar = QAction("Vaciar historial", self)
        self.accion_vaciar.setShortcut(QKeySequence("Ctrl+H"))

        self.accion_salir = QAction("Salir", self)
        self.accion_salir.setShortcut(QKeySequence("Ctrl+Q"))

        self.accion_historial = QAction("Mostrar historial", self)
        self.accion_historial.setCheckable(True)
        self.accion_historial.setChecked(True)
        self.accion_historial.setShortcut(QKeySequence("Ctrl+Shift+H"))

        self.accion_tema = QAction("Tema oscuro", self)
        self.accion_tema.setCheckable(True)

        self.accion_crono = QAction("Cronómetro", self)
        self.accion_crono.setCheckable(True)
        self.accion_crono.setShortcut(QKeySequence("Ctrl+T"))

        self.accion_acerca = QAction("Acerca de...", self)
        self.accion_acerca.setShortcut(QKeySequence("F1"))

    def _crear_menus(self):
        menu_archivo = self.menuBar().addMenu("&Archivo")
        menu_archivo.addAction(self.accion_limpiar)
        menu_archivo.addAction(self.accion_vaciar)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accion_salir)

        menu_ver = self.menuBar().addMenu("&Ver")
        menu_ver.addAction(self.accion_historial)
        menu_ver.addAction(self.accion_tema)
        menu_ver.addAction(self.accion_crono)

        menu_ayuda = self.menuBar().addMenu("&Ayuda")
        menu_ayuda.addAction(self.accion_acerca)

    # ---------------- Interfaz ----------------

    def _crear_interfaz(self):
        central = QWidget()
        self.setCentralWidget(central)

        raiz = QVBoxLayout(central)
        raiz.setContentsMargins(12, 12, 12, 12)
        raiz.setSpacing(10)

        encabezado = QHBoxLayout()
        titulo = QLabel("EL CHAPO")
        titulo.setObjectName("titulo")
        titulo.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.label_crono = QLabel("⏱ 00:00")
        self.label_crono.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_crono.setFont(QFont("Consolas", 14))
        encabezado.addWidget(titulo)
        encabezado.addWidget(self.label_crono)
        raiz.addLayout(encabezado)

        self.pantalla = QLineEdit("0")
        self.pantalla.setReadOnly(True)
        self.pantalla.setAlignment(Qt.AlignRight)
        self.pantalla.setFont(QFont("Segoe UI", 24))
        self.pantalla.setMinimumHeight(50)
        raiz.addWidget(self.pantalla)

        cuerpo = QHBoxLayout()
        raiz.addLayout(cuerpo)

        # Teclado (QGridLayout + QHBoxLayout)
        panel_teclado = QWidget()
        teclado = QVBoxLayout(panel_teclado)
        teclado.setContentsMargins(0, 0, 0, 0)
        teclado.setSpacing(8)

        grid = QGridLayout()
        grid.setSpacing(6)
        filas = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "C", "+"],
        ]
        for fila, teclas in enumerate(filas):
            for columna, texto in enumerate(teclas):
                boton = QPushButton(texto)
                boton.setFixedHeight(44)
                boton.setFont(QFont("Segoe UI", 13))
                if texto in "/*-+":
                    boton.setStyleSheet("background-color:#f0ad4e; font-weight:bold;")
                elif texto == "C":
                    boton.setStyleSheet(
                        "background-color:#d9534f; color:white; font-weight:bold;"
                    )
                boton.clicked.connect(self._handler_boton(texto))
                grid.addWidget(boton, fila, columna)
        teclado.addLayout(grid)

        fila_extra = QHBoxLayout()
        for texto, slot in (
            ("=", self.calcular),
            ("<--", self.borrar_atras),
            ("±", self.cambiar_signo),
            ("%", self.porcentaje),
        ):
            boton = QPushButton(texto)
            boton.setFixedHeight(44)
            boton.setFont(QFont("Segoe UI", 13))
            if texto == "=":
                boton.setFixedWidth(110)
                boton.setStyleSheet(
                    "background-color:#5cb85c; color:white; font-weight:bold;"
                )
            boton.clicked.connect(slot)
            fila_extra.addWidget(boton)
        teclado.addLayout(fila_extra)

        cuerpo.addWidget(panel_teclado, 3)

        # Panel de opciones (QFormLayout + QComboBox + QCheckBox + QRadioButton)
        panel_opciones = QWidget()
        form = QFormLayout(panel_opciones)
        form.setContentsMargins(8, 0, 0, 0)
        form.setSpacing(10)

        self.combo_decimales = QComboBox()
        self.combo_decimales.addItems(["0", "2", "4", "6", "8", "10"])
        self.combo_decimales.setCurrentText("6")

        self.chk_historial = QCheckBox("Mostrar historial")
        self.chk_historial.setChecked(True)

        self.chk_teclado = QCheckBox("Teclado rápido")
        self.chk_teclado.setChecked(True)

        self.chk_crono = QCheckBox("Cronómetro")

        contenedor_tema = QWidget()
        tema_layout = QHBoxLayout(contenedor_tema)
        tema_layout.setContentsMargins(0, 0, 0, 0)
        self.radio_claro = QRadioButton("Claro")
        self.radio_oscuro = QRadioButton("Oscuro")
        self.radio_claro.setChecked(True)
        tema_layout.addWidget(self.radio_claro)
        tema_layout.addWidget(self.radio_oscuro)

        self.campo_expresion = QLineEdit()
        self.campo_expresion.setReadOnly(True)
        self.campo_expresion.setPlaceholderText("Sin operación")

        self.campo_resultado = QLineEdit()
        self.campo_resultado.setReadOnly(True)
        self.campo_resultado.setPlaceholderText("0")

        self.campo_operaciones = QLineEdit("0")
        self.campo_operaciones.setReadOnly(True)

        boton_acerca = QPushButton("Acerca de...")

        form.addRow("Decimales:", self.combo_decimales)
        form.addRow("Tema:", contenedor_tema)
        form.addRow("", self.chk_historial)
        form.addRow("", self.chk_teclado)
        form.addRow("", self.chk_crono)
        form.addRow("Expresión:", self.campo_expresion)
        form.addRow("Último:", self.campo_resultado)
        form.addRow("Operaciones:", self.campo_operaciones)
        form.addRow("", boton_acerca)

        cuerpo.addWidget(panel_opciones, 2)

        raiz.addWidget(QLabel("Historial:"))
        self.historial = QTextEdit()
        self.historial.setReadOnly(True)
        self.historial.setPlaceholderText("Las operaciones aparecerán aquí...")
        raiz.addWidget(self.historial, 1)

        boton_acerca.clicked.connect(self.mostrar_acerca)

        self.statusBar().showMessage("Calculadora lista")

    def _crear_timers(self):
        self.timer_crono = QTimer(self)
        self.timer_crono.setInterval(1000)
        self.timer_crono.timeout.connect(self.actualizar_cronometro)

    # ---------------- Señales y slots ----------------

    def _conectar_senales(self):
        self.accion_limpiar.triggered.connect(self.limpiar_todo)
        self.accion_vaciar.triggered.connect(self.vaciar_historial)
        self.accion_salir.triggered.connect(self.close)
        self.accion_acerca.triggered.connect(self.mostrar_acerca)

        self.accion_historial.toggled.connect(self.chk_historial.setChecked)
        self.chk_historial.toggled.connect(self.accion_historial.setChecked)
        self.chk_historial.toggled.connect(self.alternar_historial)

        self.accion_tema.toggled.connect(self.sincronizar_tema_desde_menu)
        self.radio_oscuro.toggled.connect(self.accion_tema.setChecked)
        self.radio_oscuro.toggled.connect(self.alternar_tema)

        self.accion_crono.toggled.connect(self.chk_crono.setChecked)
        self.chk_crono.toggled.connect(self.accion_crono.setChecked)
        self.chk_crono.toggled.connect(self.alternar_cronometro)

        self.combo_decimales.currentTextChanged.connect(self.cambio_decimales)

    def _handler_boton(self, texto):
        def slot():
            if texto == "C":
                self.limpiar_todo()
            else:
                self.ingresar(texto)

        return slot

    def mostrar_acerca(self):
        DialogoAcerca(self).exec_()

    def mostrar_mensaje(self, texto, milisegundos=3000):
        self.statusBar().showMessage(texto)
        QTimer.singleShot(milisegundos, self.statusBar().clearMessage)

    def agregar_al_historial(self, texto):
        self.historial.append(texto)

    def alternar_historial(self, visible):
        self.historial.setVisible(visible)
        self.mostrar_mensaje("Historial visible" if visible else "Historial oculto")

    def alternar_tema(self, oscuro):
        self.setStyleSheet(TEMA_OSCURO if oscuro else TEMA_CLARO)
        self.mostrar_mensaje("Tema oscuro" if oscuro else "Tema claro")

    def sincronizar_tema_desde_menu(self, oscuro):
        if oscuro:
            self.radio_oscuro.setChecked(True)
        else:
            self.radio_claro.setChecked(True)

    def cambio_decimales(self, texto):
        self.decimales = int(texto)
        try:
            valor = float(self.pantalla.text())
        except ValueError:
            pass
        else:
            self.pantalla.setText(self._formatear(valor))
        self.mostrar_mensaje(f"Decimales: {texto}")

    def alternar_cronometro(self, activado):
        if activado:
            self.segundos = 0
            self.label_crono.setText("⏱ 00:00")
            self.timer_crono.start()
            self.mostrar_mensaje("Cronómetro iniciado")
        else:
            self.timer_crono.stop()
            self.mostrar_mensaje("Cronómetro detenido")

    def actualizar_cronometro(self):
        self.segundos += 1
        minutos, segundos = divmod(self.segundos, 60)
        self.label_crono.setText(f"⏱ {minutos:02d}:{segundos:02d}")

    # ---------------- Eventos ----------------

    def eventFilter(self, objeto, evento):
        if (
            evento.type() == QEvent.KeyPress
            and self.chk_teclado.isChecked()
            and QApplication.activeWindow() is self
            and evento.modifiers() in (Qt.NoModifier, Qt.KeypadModifier)
            and self._procesar_tecla(evento)
        ):
            return True
        return super().eventFilter(objeto, evento)

    def keyPressEvent(self, evento):
        if self.chk_teclado.isChecked() and self._procesar_tecla(evento):
            return
        super().keyPressEvent(evento)

    def _procesar_tecla(self, evento):
        tecla = evento.key()
        texto = evento.text()

        if texto.isdigit() or texto == ".":
            self.ingresar(texto)
            return True
        if texto in "+-*/":
            self.definir_operador(texto)
            return True
        if tecla in (Qt.Key_Return, Qt.Key_Enter):
            self.calcular()
            return True
        if tecla == Qt.Key_Backspace:
            self.borrar_atras()
            return True
        if tecla == Qt.Key_Escape:
            self.limpiar_todo()
            return True
        return False

    def closeEvent(self, evento):
        if not self.historial.toPlainText().strip():
            evento.accept()
            return
        dialogo = DialogoConfirmacion(self)
        if dialogo.exec_() == QDialog.Accepted:
            evento.accept()
        else:
            evento.ignore()

    # ---------------- Lógica de la calculadora ----------------

    def ingresar(self, texto):
        self._limpiar_error()
        if texto.isdigit():
            if self.nuevo_numero or self.pantalla.text() == "0":
                self.pantalla.setText(texto)
                self.nuevo_numero = False
            else:
                self.pantalla.setText(self.pantalla.text() + texto)
        elif texto == ".":
            if self.nuevo_numero:
                self.pantalla.setText("0.")
                self.nuevo_numero = False
            elif "." not in self.pantalla.text():
                self.pantalla.setText(self.pantalla.text() + ".")
        else:
            self.definir_operador(texto)

    def definir_operador(self, operador):
        self._limpiar_error()
        actual = self._valor_actual()
        if actual is None:
            return

        if self.operador is not None and not self.nuevo_numero:
            try:
                resultado = self._resolver(self.operando, actual, self.operador)
            except ValueError as error:
                self._mostrar_error(str(error))
                return
            self.pantalla.setText(self._formatear(resultado))
            self.operando = resultado
        else:
            self.operando = actual

        self.operador = operador
        self.nuevo_numero = True
        self.campo_expresion.setText(f"{self._formatear(self.operando)} {operador}")

    def calcular(self):
        self._limpiar_error()
        if self.operador is None or self.operando is None:
            return
        actual = self._valor_actual()
        if actual is None:
            return

        try:
            resultado = self._resolver(self.operando, actual, self.operador)
        except ValueError as error:
            self._mostrar_error(str(error))
            return

        expresion = (
            f"{self._formatear(self.operando)} {self.operador} "
            f"{self._formatear(actual)} = {self._formatear(resultado)}"
        )
        self.resultado_calculado.emit(expresion)

        self.pantalla.setText(self._formatear(resultado))
        self.nuevo_numero = True
        self.total_operaciones += 1
        self.campo_operaciones.setText(str(self.total_operaciones))
        self.campo_resultado.setText(self._formatear(resultado))
        self.campo_expresion.setText(expresion.split(" = ")[0])
        self.operador = None
        self.operando = None
        self.mostrar_mensaje("Operación completada")

    def _resolver(self, a, b, operador):
        if operador == "+":
            return a + b
        if operador == "-":
            return a - b
        if operador == "*":
            return a * b
        if b == 0:
            raise ValueError("Error: división por cero")
        return a / b

    def _valor_actual(self):
        try:
            return float(self.pantalla.text())
        except ValueError:
            return None

    def _formatear(self, valor):
        if valor != valor or valor in (float("inf"), float("-inf")):
            return "Error"
        if self.decimales == 0:
            return str(int(valor))
        texto = f"{valor:.{self.decimales}f}"
        if "." in texto:
            texto = texto.rstrip("0").rstrip(".")
        return texto

    def _mostrar_error(self, mensaje):
        self.pantalla.setText("Error")
        self.resultado_calculado.emit(mensaje)
        self.campo_expresion.clear()
        self._reiniciar()

    def _limpiar_error(self):
        if self.pantalla.text() == "Error":
            self.pantalla.setText("0")
            self.nuevo_numero = True
            self.campo_expresion.clear()
            self._reiniciar()

    def _reiniciar(self):
        self.operador = None
        self.operando = None
        self.nuevo_numero = True

    def limpiar_todo(self):
        self.pantalla.setText("0")
        self.campo_expresion.clear()
        self._reiniciar()
        self.mostrar_mensaje("Pantalla limpiada")

    def vaciar_historial(self):
        self.historial.clear()
        self.total_operaciones = 0
        self.campo_operaciones.setText("0")
        self.campo_resultado.clear()
        self.mostrar_mensaje("Historial vaciado")

    def borrar_atras(self):
        if self.pantalla.text() == "Error":
            self._limpiar_error()
            return
        if self.nuevo_numero:
            return
        texto = self.pantalla.text()[:-1]
        self.pantalla.setText(texto if texto else "0")
        if not texto:
            self.nuevo_numero = True

    def cambiar_signo(self):
        self._limpiar_error()
        texto = self.pantalla.text()
        if texto.startswith("-"):
            self.pantalla.setText(texto[1:])
        elif texto != "0":
            self.pantalla.setText("-" + texto)

    def porcentaje(self):
        self._limpiar_error()
        actual = self._valor_actual()
        if actual is None:
            return
        if self.operador in ("+", "-") and self.operando is not None:
            valor = self.operando * actual / 100
        else:
            valor = actual / 100
        self.pantalla.setText(self._formatear(valor))
        self.nuevo_numero = True


def main():
    app = QApplication(sys.argv)
    ventana = Calculadora()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
