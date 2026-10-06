import sys

from PyQt5.QtCore import Qt, QTimer
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


class DialogoExito(QDialog):
    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EL CHAPO")
        self.setFixedSize(400, 260)

        layout = QVBoxLayout(self)

        titulo = QLabel("EL CHAPO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 20, QFont.Bold))

        mensaje = QLabel("Registro realizado con éxito")
        mensaje.setAlignment(Qt.AlignCenter)

        resumen = QLabel(
            f"Nombre: {datos['nombre']}\n"
            f"Correo: {datos['correo']}\n"
            f"Edad: {datos['edad']}\n"
            f"Ciudad: {datos['ciudad'] or '(sin dato)'}\n"
            f"Observaciones: {datos['observaciones'] or '(ninguna)'}"
        )
        resumen.setAlignment(Qt.AlignCenter)

        boton = QPushButton("Aceptar")
        boton.setDefault(True)
        boton.clicked.connect(self.accept)

        layout.addWidget(titulo)
        layout.addWidget(mensaje)
        layout.addWidget(resumen)
        layout.addWidget(boton)


class Registro2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EL CHAPO")
        self.setFixedSize(520, 640)

        self._crear_interfaz()

    def _crear_interfaz(self):
        central = QWidget()
        self.setCentralWidget(central)

        raiz = QVBoxLayout(central)
        raiz.setContentsMargins(16, 16, 16, 16)
        raiz.setSpacing(12)

        # Encabezado (QHBoxLayout)
        encabezado = QHBoxLayout()
        titulo = QLabel("EL CHAPO")
        titulo.setFont(QFont("Segoe UI", 26, QFont.Bold))
        subtitulo = QLabel("Registro 2")
        subtitulo.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        subtitulo.setFont(QFont("Segoe UI", 12))
        encabezado.addWidget(titulo)
        encabezado.addWidget(subtitulo)
        raiz.addLayout(encabezado)

        # Datos principales (QFormLayout)
        form = QFormLayout()
        form.setSpacing(10)

        self.campo_nombre = QLineEdit()
        self.campo_nombre.setPlaceholderText("Nombre y apellido")

        self.campo_correo = QLineEdit()
        self.campo_correo.setPlaceholderText("ejemplo@correo.com")

        self.campo_clave = QLineEdit()
        self.campo_clave.setEchoMode(QLineEdit.Password)
        self.campo_clave.setPlaceholderText("Mínimo 6 caracteres")

        form.addRow("Nombre:", self.campo_nombre)
        form.addRow("Correo:", self.campo_correo)
        form.addRow("Contraseña:", self.campo_clave)
        raiz.addLayout(form)

        # Datos adicionales (QGridLayout)
        cuadricula = QGridLayout()
        cuadricula.setSpacing(8)

        self.campo_edad = QLineEdit()
        self.campo_edad.setPlaceholderText("Ej: 25")
        self.campo_telefono = QLineEdit()
        self.campo_telefono.setPlaceholderText("Ej: 5555-1234")
        self.campo_ciudad = QLineEdit()
        self.campo_ciudad.setPlaceholderText("Ej: Buenos Aires")
        self.campo_pais = QLineEdit()
        self.campo_pais.setPlaceholderText("Ej: Argentina")

        cuadricula.addWidget(QLabel("Edad:"), 0, 0)
        cuadricula.addWidget(self.campo_edad, 0, 1)
        cuadricula.addWidget(QLabel("Teléfono:"), 0, 2)
        cuadricula.addWidget(self.campo_telefono, 0, 3)
        cuadricula.addWidget(QLabel("Ciudad:"), 1, 0)
        cuadricula.addWidget(self.campo_ciudad, 1, 1)
        cuadricula.addWidget(QLabel("País:"), 1, 2)
        cuadricula.addWidget(self.campo_pais, 1, 3)
        raiz.addLayout(cuadricula)

        # Observaciones (QTextEdit)
        raiz.addWidget(QLabel("Observaciones:"))
        self.campo_observaciones = QTextEdit()
        self.campo_observaciones.setPlaceholderText("Escribe aquí (opcional)...")
        self.campo_observaciones.setFixedHeight(90)
        raiz.addWidget(self.campo_observaciones)

        self.etiqueta_mensaje = QLabel("")
        self.etiqueta_mensaje.setWordWrap(True)
        self.etiqueta_mensaje.setAlignment(Qt.AlignCenter)
        self.etiqueta_mensaje.setStyleSheet("color: #d9534f; font-weight: bold;")
        raiz.addWidget(self.etiqueta_mensaje)

        # Botones (QHBoxLayout)
        botones = QHBoxLayout()

        boton_registrar = QPushButton("Registrarse")
        boton_registrar.setStyleSheet(
            "background-color:#5cb85c; color:white; font-weight:bold; padding:8px;"
        )
        boton_registrar.clicked.connect(self.registrar)

        boton_limpiar = QPushButton("Limpiar")
        boton_limpiar.clicked.connect(self.limpiar)

        boton_salir = QPushButton("Salir")
        boton_salir.clicked.connect(self.close)

        botones.addWidget(boton_registrar)
        botones.addWidget(boton_limpiar)
        botones.addWidget(boton_salir)
        raiz.addLayout(botones)

        raiz.addStretch()
        self.statusBar().showMessage("Complete el formulario para registrarse")

    def registrar(self):
        nombre = self.campo_nombre.text().strip()
        correo = self.campo_correo.text().strip()
        clave = self.campo_clave.text()
        edad = self.campo_edad.text().strip()

        if not nombre or not correo or not clave:
            self._error("Nombre, correo y contraseña son obligatorios.")
            return
        if "@" not in correo or "." not in correo.split("@")[-1]:
            self._error("El correo no es válido.")
            return
        if len(clave) < 6:
            self._error("La contraseña debe tener al menos 6 caracteres.")
            return
        if edad and not edad.isdigit():
            self._error("La edad debe ser un número.")
            return

        self.etiqueta_mensaje.setStyleSheet("color: #5cb85c; font-weight: bold;")
        self.etiqueta_mensaje.setText("Registro guardado correctamente.")
        self.statusBar().showMessage("Registro guardado")

        datos = {
            "nombre": nombre,
            "correo": correo,
            "edad": edad or "(sin dato)",
            "ciudad": self.campo_ciudad.text().strip(),
            "observaciones": self.campo_observaciones.toPlainText().strip(),
        }
        QTimer.singleShot(200, lambda: self._mostrar_dialogo(datos))

    def _mostrar_dialogo(self, datos):
        DialogoExito(datos, self).exec_()

    def _error(self, mensaje):
        self.etiqueta_mensaje.setStyleSheet("color: #d9534f; font-weight: bold;")
        self.etiqueta_mensaje.setText(mensaje)
        self.statusBar().showMessage("Error en el formulario")

    def limpiar(self):
        for campo in (
            self.campo_nombre,
            self.campo_correo,
            self.campo_clave,
            self.campo_edad,
            self.campo_telefono,
            self.campo_ciudad,
            self.campo_pais,
        ):
            campo.clear()
        self.campo_observaciones.clear()
        self.etiqueta_mensaje.setText("")
        self.statusBar().showMessage("Formulario limpiado")


def main():
    app = QApplication(sys.argv)
    ventana = Registro2()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
