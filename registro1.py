import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class PanelRegistro(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.marca_agua = QLabel("EL CHAPO", self)
        self.marca_agua.setAlignment(Qt.AlignCenter)
        self.marca_agua.setStyleSheet(
            "color: rgba(0, 0, 0, 28);"
            "background: transparent;"
            "font-size: 90px;"
            "font-weight: bold;"
        )
        self.marca_agua.lower()

    def resizeEvent(self, evento):
        self.marca_agua.setGeometry(self.rect())
        super().resizeEvent(evento)


class DialogoRegistro(QDialog):
    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EL CHAPO")
        self.setFixedSize(380, 240)

        layout = QVBoxLayout(self)

        titulo = QLabel("EL CHAPO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 20, QFont.Bold))

        mensaje = QLabel("Registro realizado con éxito")
        mensaje.setAlignment(Qt.AlignCenter)

        resumen = QLabel(
            f"Nombre: {datos['nombre']}\n"
            f"Correo: {datos['correo']}\n"
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


class Registro1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EL CHAPO")
        self.setFixedSize(480, 540)

        self.panel = PanelRegistro()
        self.setCentralWidget(self.panel)

        raiz = QVBoxLayout(self.panel)
        raiz.setContentsMargins(20, 20, 20, 20)
        raiz.setSpacing(12)

        titulo = QLabel("EL CHAPO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 26, QFont.Bold))
        raiz.addWidget(titulo)

        subtitulo = QLabel("Formulario de registro")
        subtitulo.setAlignment(Qt.AlignCenter)
        raiz.addWidget(subtitulo)

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

        if not nombre or not correo or not clave:
            self._error("Todos los campos son obligatorios.")
            return
        if "@" not in correo or "." not in correo.split("@")[-1]:
            self._error("El correo no es válido.")
            return
        if len(clave) < 6:
            self._error("La contraseña debe tener al menos 6 caracteres.")
            return

        self.etiqueta_mensaje.setStyleSheet("color: #5cb85c; font-weight: bold;")
        self.etiqueta_mensaje.setText("Registro guardado correctamente.")
        self.statusBar().showMessage("Registro guardado")

        datos = {
            "nombre": nombre,
            "correo": correo,
            "observaciones": self.campo_observaciones.toPlainText().strip(),
        }
        QTimer.singleShot(200, lambda: self._mostrar_dialogo(datos))

    def _mostrar_dialogo(self, datos):
        DialogoRegistro(datos, self).exec_()

    def _error(self, mensaje):
        self.etiqueta_mensaje.setStyleSheet("color: #d9534f; font-weight: bold;")
        self.etiqueta_mensaje.setText(mensaje)
        self.statusBar().showMessage("Error en el formulario")

    def limpiar(self):
        self.campo_nombre.clear()
        self.campo_correo.clear()
        self.campo_clave.clear()
        self.campo_observaciones.clear()
        self.etiqueta_mensaje.setText("")
        self.statusBar().showMessage("Formulario limpiado")


def main():
    app = QApplication(sys.argv)
    ventana = Registro1()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
