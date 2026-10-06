import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DialogoExito(QDialog):
    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EL CHAPO")
        self.setFixedSize(360, 220)

        layout = QVBoxLayout(self)

        titulo = QLabel("¡Registro exitoso!")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 16, QFont.Bold))

        resumen = QLabel(
            f"Usuario: {datos['usuario']}\n"
            f"Nombre: {datos['nombre']}\n"
            f"Correo: {datos['correo']}"
        )
        resumen.setAlignment(Qt.AlignCenter)

        boton_aceptar = QPushButton("Aceptar")
        boton_aceptar.setDefault(True)
        boton_aceptar.clicked.connect(self.accept)

        layout.addWidget(titulo)
        layout.addWidget(resumen)
        layout.addWidget(boton_aceptar)


class VentanaRegistro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EL CHAPO")
        self.setFixedSize(460, 480)

        self._crear_menu()
        self._crear_interfaz()

    def _crear_menu(self):
        menu = self.menuBar().addMenu("&Archivo")
        menu.addAction("Limpiar formulario", self.limpiar)
        menu.addSeparator()
        menu.addAction("Salir", self.close)

    def _crear_interfaz(self):
        central = QWidget()
        self.setCentralWidget(central)

        raiz = QVBoxLayout(central)
        raiz.setContentsMargins(16, 16, 16, 16)
        raiz.setSpacing(12)

        titulo = QLabel("EL CHAPO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 26, QFont.Bold))
        raiz.addWidget(titulo)

        subtitulo = QLabel("Formulario de registro")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setFont(QFont("Segoe UI", 11))
        raiz.addWidget(subtitulo)

        form = QFormLayout()
        form.setSpacing(10)

        self.campo_nombre = QLineEdit()
        self.campo_nombre.setPlaceholderText("Nombre y apellido")

        self.campo_usuario = QLineEdit()
        self.campo_usuario.setPlaceholderText("Nombre de usuario")

        self.campo_correo = QLineEdit()
        self.campo_correo.setPlaceholderText("ejemplo@correo.com")

        self.campo_clave = QLineEdit()
        self.campo_clave.setEchoMode(QLineEdit.Password)
        self.campo_clave.setPlaceholderText("Mínimo 6 caracteres")

        self.campo_clave2 = QLineEdit()
        self.campo_clave2.setEchoMode(QLineEdit.Password)
        self.campo_clave2.setPlaceholderText("Repite la contraseña")

        form.addRow("Nombre:", self.campo_nombre)
        form.addRow("Usuario:", self.campo_usuario)
        form.addRow("Correo:", self.campo_correo)
        form.addRow("Contraseña:", self.campo_clave)
        form.addRow("Confirmar:", self.campo_clave2)

        raiz.addLayout(form)

        self.chk_terminos = QCheckBox("Acepto los términos y condiciones")
        raiz.addWidget(self.chk_terminos)

        self.etiqueta_mensaje = QLabel("")
        self.etiqueta_mensaje.setWordWrap(True)
        self.etiqueta_mensaje.setAlignment(Qt.AlignCenter)
        self.etiqueta_mensaje.setStyleSheet("color: #d9534f; font-weight: bold;")
        raiz.addWidget(self.etiqueta_mensaje)

        botones = QHBoxLayout()

        boton_registrar = QPushButton("Registrarse")
        boton_registrar.setFont(QFont("Segoe UI", 11, QFont.Bold))
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

        self.statusBar().showMessage("Complete todos los campos para registrarse")

    def registrar(self):
        nombre = self.campo_nombre.text().strip()
        usuario = self.campo_usuario.text().strip()
        correo = self.campo_correo.text().strip()
        clave = self.campo_clave.text()
        clave2 = self.campo_clave2.text()

        if not nombre or not usuario or not correo or not clave:
            self._error("Todos los campos son obligatorios.")
            return
        if "@" not in correo or "." not in correo.split("@")[-1]:
            self._error("El correo no es válido.")
            return
        if len(clave) < 6:
            self._error("La contraseña debe tener al menos 6 caracteres.")
            return
        if clave != clave2:
            self._error("Las contraseñas no coinciden.")
            return
        if not self.chk_terminos.isChecked():
            self._error("Debe aceptar los términos y condiciones.")
            return

        self.etiqueta_mensaje.setStyleSheet("color: #5cb85c; font-weight: bold;")
        self.etiqueta_mensaje.setText("Registro completado correctamente.")
        self.statusBar().showMessage("Registro guardado")

        datos = {"nombre": nombre, "usuario": usuario, "correo": correo}
        QTimer.singleShot(200, lambda: self._mostrar_exito(datos))

    def _mostrar_exito(self, datos):
        DialogoExito(datos, self).exec_()

    def _error(self, mensaje):
        self.etiqueta_mensaje.setStyleSheet("color: #d9534f; font-weight: bold;")
        self.etiqueta_mensaje.setText(mensaje)
        self.statusBar().showMessage("Error en el formulario")

    def limpiar(self):
        for campo in (
            self.campo_nombre,
            self.campo_usuario,
            self.campo_correo,
            self.campo_clave,
            self.campo_clave2,
        ):
            campo.clear()
        self.chk_terminos.setChecked(False)
        self.etiqueta_mensaje.setText("")
        self.statusBar().showMessage("Formulario limpiado")


def main():
    app = QApplication(sys.argv)
    ventana = VentanaRegistro()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
