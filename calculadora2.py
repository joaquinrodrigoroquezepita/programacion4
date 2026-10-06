import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class DialogoAcerca(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de")
        self.setFixedSize(320, 160)

        layout = QVBoxLayout(self)

        titulo = QLabel("Calculadora 2")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 16, QFont.Bold))

        descripcion = QLabel(
            "Calculadora simple hecha con PyQt5.\n"
            "Usa QApplication, QMainWindow, QDialog,\n"
            "QLabel, QPushButton, QLineEdit, QTextEdit y\n"
            "QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout."
        )
        descripcion.setAlignment(Qt.AlignCenter)

        boton_cerrar = QPushButton("Cerrar")
        boton_cerrar.clicked.connect(self.close)

        layout.addWidget(titulo)
        layout.addWidget(descripcion)
        layout.addWidget(boton_cerrar)


class Calculadora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Simple")
        self.setMinimumSize(520, 520)

        self.operador = None
        self.operando = None
        self.nuevo_numero = True
        self.total_operaciones = 0
        self.ultimo_resultado = ""

        self._crear_menu()
        self._crear_interfaz()

    def _crear_menu(self):
        menu_archivo = self.menuBar().addMenu("&Archivo")
        menu_archivo.addAction("Limpiar todo", self.limpiar_todo)
        menu_archivo.addAction("Salir", self.close)

        menu_ayuda = self.menuBar().addMenu("&Ayuda")
        menu_ayuda.addAction("Acerca de", self.mostrar_dialogo)

    def _crear_interfaz(self):
        central = QWidget()
        self.setCentralWidget(central)

        raiz = QVBoxLayout(central)
        raiz.setContentsMargins(12, 12, 12, 12)
        raiz.setSpacing(10)

        # --- Encabezado (QHBoxLayout) ---
        encabezado = QHBoxLayout()
        titulo = QLabel("Calculadora")
        titulo.setFont(QFont("Segoe UI", 18, QFont.Bold))
        subtitulo = QLabel("Operaciones básicas")
        subtitulo.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        encabezado.addWidget(titulo)
        encabezado.addWidget(subtitulo)
        raiz.addLayout(encabezado)

        # --- Pantalla ---
        self.pantalla = QLineEdit("0")
        self.pantalla.setReadOnly(True)
        self.pantalla.setAlignment(Qt.AlignRight)
        self.pantalla.setFont(QFont("Segoe UI", 24))
        self.pantalla.setMinimumHeight(50)
        raiz.addWidget(self.pantalla)

        # --- Cuerpo: teclado + panel lateral (QHBoxLayout) ---
        cuerpo = QHBoxLayout()
        raiz.addLayout(cuerpo)

        panel_teclado = QWidget()
        teclado_layout = QVBoxLayout(panel_teclado)
        teclado_layout.setContentsMargins(0, 0, 0, 0)
        teclado_layout.setSpacing(8)

        # Teclado numerico (QGridLayout)
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
                    boton.setStyleSheet("background-color:#d9534f; color:white; font-weight:bold;")
                boton.clicked.connect(self._crear_handler(texto))
                grid.addWidget(boton, fila, columna)

        teclado_layout.addLayout(grid)

        # Fila extra (QHBoxLayout)
        fila_extra = QHBoxLayout()
        for texto, handler in (
            ("=", self.calcular),
            ("<--", self.borrar_atras),
            ("±", self.cambiar_signo),
            ("%", self.porcentaje),
        ):
            boton = QPushButton(texto)
            boton.setFixedHeight(44)
            boton.setFont(QFont("Segoe UI", 13))
            if texto == "=":
                boton.setStyleSheet("background-color:#5cb85c; color:white; font-weight:bold;")
                boton.setFixedWidth(120)
            boton.clicked.connect(handler)
            fila_extra.addWidget(boton)
        teclado_layout.addLayout(fila_extra)

        cuerpo.addWidget(panel_teclado, 3)

        # Panel lateral con QFormLayout
        panel_lateral = QWidget()
        form = QFormLayout(panel_lateral)
        form.setContentsMargins(8, 0, 0, 0)
        form.setSpacing(10)

        self.campo_expresion = QLineEdit()
        self.campo_expresion.setReadOnly(True)
        self.campo_expresion.setPlaceholderText("Sin operacion")

        self.campo_resultado = QLineEdit()
        self.campo_resultado.setReadOnly(True)
        self.campo_resultado.setPlaceholderText("0")

        self.campo_operaciones = QLineEdit("0")
        self.campo_operaciones.setReadOnly(True)

        form.addRow(QLabel("Expresion:"), self.campo_expresion)
        form.addRow(QLabel("Ultimo resultado:"), self.campo_resultado)
        form.addRow(QLabel("Operaciones:"), self.campo_operaciones)

        boton_acerca = QPushButton("Acerca de...")
        boton_acerca.clicked.connect(self.mostrar_dialogo)
        form.addRow(boton_acerca)

        cuerpo.addWidget(panel_lateral, 2)

        # --- Historial (QTextEdit) ---
        raiz.addWidget(QLabel("Historial:"))
        self.historial = QTextEdit()
        self.historial.setReadOnly(True)
        self.historial.setPlaceholderText("Aqui se mostraran las operaciones...")
        raiz.addWidget(self.historial, 1)

    def _crear_handler(self, texto):
        def handler():
            if texto == "C":
                self.limpiar_todo()
            else:
                self.ingresar(texto)

        return handler

    def mostrar_dialogo(self):
        DialogoAcerca(self).exec_()

    def _limpiar_error(self):
        if self.pantalla.text() == "Error":
            self.pantalla.setText("0")
            self.nuevo_numero = True
            self.campo_expresion.clear()
            self._reiniciar()

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
        actual = self.pantalla.text()
        if self.operador and not self.nuevo_numero:
            try:
                resultado = self._resolver(float(self.operando), float(actual), self.operador)
            except (TypeError, ValueError) as e:
                self.pantalla.setText("Error")
                self.historial.append(str(e))
                self.campo_expresion.clear()
                self._reiniciar()
                return
            self._mostrar_resultado(resultado)
            self.operando = self._formatear(resultado)
        else:
            self.operando = actual

        self.operador = operador
        self.nuevo_numero = True
        self.campo_expresion.setText(f"{self.operando} {operador}")

    def calcular(self):
        self._limpiar_error()
        if not self.operador:
            return
        actual = self.pantalla.text()
        try:
            resultado = self._resolver(float(self.operando), float(actual), self.operador)
        except (TypeError, ValueError) as e:
            self.pantalla.setText("Error")
            self.historial.append(str(e))
            self.campo_expresion.clear()
            self._reiniciar()
            return

        expresion = f"{self.operando} {self.operador} {actual}"
        self.historial.append(f"{expresion} = {self._formatear(resultado)}")
        self._mostrar_resultado(resultado)
        self.total_operaciones += 1
        self.ultimo_resultado = self._formatear(resultado)
        self.campo_operaciones.setText(str(self.total_operaciones))
        self.campo_resultado.setText(self.ultimo_resultado)
        self.campo_expresion.setText(expresion)
        self._reiniciar()

    def _resolver(self, a, b, operador):
        if operador == "+":
            return a + b
        if operador == "-":
            return a - b
        if operador == "*":
            return a * b
        if b == 0:
            raise ValueError("Error: division por cero")
        return a / b

    def _mostrar_resultado(self, resultado):
        self.pantalla.setText(self._formatear(resultado))
        self.nuevo_numero = True

    @staticmethod
    def _formatear(valor):
        if valor == int(valor):
            return str(int(valor))
        return str(round(valor, 10)).rstrip("0").rstrip(".")

    def _reiniciar(self):
        self.operador = None
        self.operando = None
        self.nuevo_numero = True

    def limpiar_todo(self):
        self.pantalla.setText("0")
        self.campo_expresion.clear()
        self._reiniciar()

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
        try:
            valor = float(self.pantalla.text())
        except ValueError:
            return

        if self.operador in ("+", "-") and self.operando is not None:
            try:
                valor = float(self.operando) * valor / 100
            except (TypeError, ValueError):
                return
        else:
            valor /= 100

        self._mostrar_resultado(valor)


def main():
    app = QApplication(sys.argv)
    ventana = Calculadora()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
