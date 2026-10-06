import sys

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
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


class DialogoExito(QDialog):
    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EL CHAPO")
        self.setFixedSize(400, 280)

        layout = QVBoxLayout(self)

        titulo = QLabel("EL CHAPO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 20, QFont.Bold))

        mensaje = QLabel("Registro realizado con éxito")
        mensaje.setAlignment(Qt.AlignCenter)

        resumen = QLabel(
            f"Nombre: {datos['nombre']}\n"
            f"Correo: {datos['correo']}\n"
            f"País: {datos['pais']}\n"
            f"Género: {datos['genero']}\n"
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


class DialogoConfirmacion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EL CHAPO")
        self.setFixedSize(340, 130)

        layout = QVBoxLayout(self)
        etiqueta = QLabel("Hay datos sin guardar.\n¿Desea salir sin registrarse?")
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


class DialogoAcerca(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EL CHAPO")
        self.setFixedSize(340, 180)

        layout = QVBoxLayout(self)
        titulo = QLabel("EL CHAPO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 20, QFont.Bold))

        datos = QLabel("Formulario de registro\nVersión 1.0 - PyQt5")
        datos.setAlignment(Qt.AlignCenter)

        boton = QPushButton("Cerrar")
        boton.clicked.connect(self.accept)

        layout.addWidget(titulo)
        layout.addWidget(datos)
        layout.addWidget(boton)


class Registro5(QMainWindow):

    bitacora_evento = pyqtSignal(str)
    dato_invalido = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("EL CHAPO")
        self.setMinimumSize(560, 760)
        self.segundos = 0

        self.panel = PanelRegistro()
        self.setCentralWidget(self.panel)

        self._crear_acciones()
        self._crear_menus()
        self._crear_timers()
        self._crear_interfaz()
        self._conectar_senales()

        self.timer_reloj.start()
        self.statusBar().showMessage("Formulario listo (Enter registra, Esc limpia)")

    # ---------------- Menús y QAction ----------------

    def _crear_acciones(self):
        self.accion_limpiar = QAction("Limpiar formulario", self)
        self.accion_limpiar.setShortcut(QKeySequence("Ctrl+L"))

        self.accion_vaciar = QAction("Vaciar bitácora", self)
        self.accion_vaciar.setShortcut(QKeySequence("Ctrl+B"))

        self.accion_salir = QAction("Salir", self)
        self.accion_salir.setShortcut(QKeySequence("Ctrl+Q"))

        self.accion_bitacora = QAction("Mostrar bitácora", self)
        self.accion_bitacora.setCheckable(True)
        self.accion_bitacora.setChecked(True)
        self.accion_bitacora.setShortcut(QKeySequence("Ctrl+Shift+B"))

        self.accion_reloj = QAction("Reloj de sesión", self)
        self.accion_reloj.setCheckable(True)
        self.accion_reloj.setChecked(True)
        self.accion_reloj.setShortcut(QKeySequence("Ctrl+R"))

        self.accion_validar = QAction("Validar ahora", self)
        self.accion_validar.setShortcut(QKeySequence("Ctrl+V"))

        self.accion_reiniciar_reloj = QAction("Reiniciar reloj", self)

        self.accion_acerca = QAction("Acerca de...", self)
        self.accion_acerca.setShortcut(QKeySequence("F1"))

    def _crear_menus(self):
        menu_archivo = self.menuBar().addMenu("&Archivo")
        menu_archivo.addAction(self.accion_limpiar)
        menu_archivo.addAction(self.accion_vaciar)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accion_salir)

        menu_ver = self.menuBar().addMenu("&Ver")
        menu_ver.addAction(self.accion_bitacora)
        menu_ver.addAction(self.accion_reloj)

        menu_herramientas = self.menuBar().addMenu("&Herramientas")
        menu_herramientas.addAction(self.accion_validar)
        menu_herramientas.addAction(self.accion_reiniciar_reloj)

        menu_ayuda = self.menuBar().addMenu("&Ayuda")
        menu_ayuda.addAction(self.accion_acerca)

    # ---------------- Timers ----------------

    def _crear_timers(self):
        self.timer_reloj = QTimer(self)
        self.timer_reloj.setInterval(1000)
        self.timer_reloj.timeout.connect(self.actualizar_reloj)

        self.timer_mensaje = QTimer(self)
        self.timer_mensaje.setSingleShot(True)
        self.timer_mensaje.setInterval(3000)
        self.timer_mensaje.timeout.connect(self.statusBar().clearMessage)

        self.timer_fuerza = QTimer(self)
        self.timer_fuerza.setSingleShot(True)
        self.timer_fuerza.setInterval(400)
        self.timer_fuerza.timeout.connect(self.evaluar_fuerza)

    # ---------------- Interfaz ----------------

    def _crear_interfaz(self):
        raiz = QVBoxLayout(self.panel)
        raiz.setContentsMargins(20, 20, 20, 20)
        raiz.setSpacing(10)

        # Encabezado (QHBoxLayout)
        encabezado = QHBoxLayout()
        titulo = QLabel("EL CHAPO")
        titulo.setFont(QFont("Segoe UI", 26, QFont.Bold))
        self.label_reloj = QLabel("⏱ 00:00")
        self.label_reloj.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_reloj.setFont(QFont("Consolas", 12))
        encabezado.addWidget(titulo)
        encabezado.addWidget(self.label_reloj)
        raiz.addLayout(encabezado)

        # Datos principales (QFormLayout)
        form = QFormLayout()
        form.setSpacing(8)

        self.campo_nombre = QLineEdit()
        self.campo_nombre.setPlaceholderText("Nombre y apellido")

        self.campo_correo = QLineEdit()
        self.campo_correo.setPlaceholderText("ejemplo@correo.com")

        self.campo_clave = QLineEdit()
        self.campo_clave.setEchoMode(QLineEdit.Password)
        self.campo_clave.setPlaceholderText("Mínimo 6 caracteres")

        self.label_fuerza = QLabel(" ")
        self.label_fuerza.setAlignment(Qt.AlignRight)

        form.addRow("Nombre:", self.campo_nombre)
        form.addRow("Correo:", self.campo_correo)
        form.addRow("Contraseña:", self.campo_clave)
        form.addRow("", self.label_fuerza)
        raiz.addLayout(form)

        # Datos adicionales (QGridLayout con QComboBox y QRadioButton)
        cuadricula = QGridLayout()
        cuadricula.setSpacing(8)

        self.campo_edad = QLineEdit()
        self.campo_edad.setPlaceholderText("Ej: 25")

        self.campo_telefono = QLineEdit()
        self.campo_telefono.setPlaceholderText("Ej: 5555-1234")

        self.combo_pais = QComboBox()
        self.combo_pais.addItems(["Argentina", "Chile", "México", "España", "Otro"])

        contenedor_genero = QWidget()
        genero_layout = QHBoxLayout(contenedor_genero)
        genero_layout.setContentsMargins(0, 0, 0, 0)
        self.radio_masculino = QRadioButton("Masculino")
        self.radio_femenino = QRadioButton("Femenino")
        self.radio_masculino.setChecked(True)
        genero_layout.addWidget(self.radio_masculino)
        genero_layout.addWidget(self.radio_femenino)

        self.chk_terminos = QCheckBox("Acepto los términos y condiciones")
        self.chk_novedades = QCheckBox("Quiero recibir novedades")

        cuadricula.addWidget(QLabel("Edad:"), 0, 0)
        cuadricula.addWidget(self.campo_edad, 0, 1)
        cuadricula.addWidget(QLabel("Teléfono:"), 0, 2)
        cuadricula.addWidget(self.campo_telefono, 0, 3)
        cuadricula.addWidget(QLabel("País:"), 1, 0)
        cuadricula.addWidget(self.combo_pais, 1, 1)
        cuadricula.addWidget(QLabel("Género:"), 1, 2)
        cuadricula.addWidget(contenedor_genero, 1, 3)
        cuadricula.addWidget(self.chk_terminos, 2, 0, 1, 2)
        cuadricula.addWidget(self.chk_novedades, 2, 2, 1, 2)
        raiz.addLayout(cuadricula)

        # Observaciones (QTextEdit)
        raiz.addWidget(QLabel("Observaciones:"))
        self.campo_observaciones = QTextEdit()
        self.campo_observaciones.setPlaceholderText("Escribe aquí (opcional)...")
        self.campo_observaciones.setFixedHeight(70)
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
        boton_limpiar = QPushButton("Limpiar")
        boton_salir = QPushButton("Salir")
        botones.addWidget(boton_registrar)
        botones.addWidget(boton_limpiar)
        botones.addWidget(boton_salir)
        raiz.addLayout(botones)

        # Bitácora (QTextEdit)
        raiz.addWidget(QLabel("Bitácora:"))
        self.bitacora = QTextEdit()
        self.bitacora.setReadOnly(True)
        self.bitacora.setPlaceholderText("Eventos de la sesión...")
        self.bitacora.setFixedHeight(60)
        raiz.addWidget(self.bitacora)

        raiz.addStretch()

        self._boton_registrar = boton_registrar
        self._boton_limpiar = boton_limpiar
        self._boton_salir = boton_salir

    def _conectar_senales(self):
        self.bitacora_evento.connect(self.escribir_bitacora)
        self.dato_invalido.connect(self.mostrar_error)

        self._boton_registrar.clicked.connect(self.registrar)
        self._boton_limpiar.clicked.connect(self.limpiar)
        self._boton_salir.clicked.connect(self.close)

        for campo in (self.campo_nombre, self.campo_correo, self.campo_clave):
            campo.returnPressed.connect(self.registrar)

        self.campo_clave.textChanged.connect(lambda _t: self.timer_fuerza.start())
        self.combo_pais.currentTextChanged.connect(
            lambda pais: self.mostrar_mensaje(f"País seleccionado: {pais}")
        )

        self.accion_limpiar.triggered.connect(self.limpiar)
        self.accion_vaciar.triggered.connect(self.vaciar_bitacora)
        self.accion_salir.triggered.connect(self.close)
        self.accion_validar.triggered.connect(self.registrar)
        self.accion_reiniciar_reloj.triggered.connect(self.reiniciar_reloj)
        self.accion_acerca.triggered.connect(self.mostrar_acerca)

        self.accion_bitacora.toggled.connect(self.alternar_bitacora)
        self.accion_reloj.toggled.connect(self.alternar_reloj)

    # ---------------- Eventos ----------------

    def keyPressEvent(self, evento):
        if evento.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.registrar()
        elif evento.key() == Qt.Key_Escape:
            self.limpiar()
        else:
            super().keyPressEvent(evento)

    def closeEvent(self, evento):
        if not self.hay_datos():
            evento.accept()
            return
        dialogo = DialogoConfirmacion(self)
        if dialogo.exec_() == QDialog.Accepted:
            evento.accept()
        else:
            evento.ignore()

    def hay_datos(self):
        return bool(
            self.campo_nombre.text().strip()
            or self.campo_correo.text().strip()
            or self.campo_clave.text()
            or self.campo_observaciones.toPlainText().strip()
        )

    # ---------------- Señales y slots ----------------

    def registrar(self):
        nombre = self.campo_nombre.text().strip()
        correo = self.campo_correo.text().strip()
        clave = self.campo_clave.text()
        edad = self.campo_edad.text().strip()

        if not nombre or not correo or not clave:
            self.dato_invalido.emit("Nombre, correo y contraseña son obligatorios.")
            return
        if "@" not in correo or "." not in correo.split("@")[-1]:
            self.dato_invalido.emit("El correo no es válido.")
            return
        if len(clave) < 6:
            self.dato_invalido.emit("La contraseña debe tener al menos 6 caracteres.")
            return
        if edad and not edad.isdigit():
            self.dato_invalido.emit("La edad debe ser un número.")
            return
        if not self.chk_terminos.isChecked():
            self.dato_invalido.emit("Debe aceptar los términos y condiciones.")
            return

        genero = "Masculino" if self.radio_masculino.isChecked() else "Femenino"
        datos = {
            "nombre": nombre,
            "correo": correo,
            "pais": self.combo_pais.currentText(),
            "genero": genero,
            "observaciones": self.campo_observaciones.toPlainText().strip(),
        }

        self.etiqueta_mensaje.setStyleSheet("color: #5cb85c; font-weight: bold;")
        self.etiqueta_mensaje.setText("Registro guardado correctamente.")
        self.bitacora_evento.emit(f"Registro exitoso: {nombre} ({correo})")
        self.mostrar_mensaje("Registro guardado")

        QTimer.singleShot(200, lambda: self._mostrar_dialogo(datos))

    def _mostrar_dialogo(self, datos):
        DialogoExito(datos, self).exec_()

    def mostrar_error(self, mensaje):
        self.etiqueta_mensaje.setStyleSheet("color: #d9534f; font-weight: bold;")
        self.etiqueta_mensaje.setText(mensaje)
        self.bitacora_evento.emit(f"Error de validación: {mensaje}")
        self.mostrar_mensaje("Error en el formulario")

    def escribir_bitacora(self, texto):
        self.bitacora.append(texto)

    def vaciar_bitacora(self):
        self.bitacora.clear()
        self.mostrar_mensaje("Bitácora vaciada")

    def mostrar_mensaje(self, texto):
        self.statusBar().showMessage(texto)
        self.timer_mensaje.start()

    def mostrar_acerca(self):
        DialogoAcerca(self).exec_()

    # ---------------- Slots de menú ----------------

    def alternar_bitacora(self, visible):
        self.bitacora.setVisible(visible)
        self.mostrar_mensaje("Bitácora visible" if visible else "Bitácora oculta")

    def alternar_reloj(self, activo):
        if activo:
            self.timer_reloj.start()
            self.label_reloj.setVisible(True)
            self.mostrar_mensaje("Reloj activado")
        else:
            self.timer_reloj.stop()
            self.label_reloj.setVisible(False)
            self.mostrar_mensaje("Reloj desactivado")

    def reiniciar_reloj(self):
        self.segundos = 0
        self.label_reloj.setText("⏱ 00:00")
        self.mostrar_mensaje("Reloj reiniciado")

    # ---------------- QTimer ----------------

    def actualizar_reloj(self):
        self.segundos += 1
        minutos, segundos = divmod(self.segundos, 60)
        self.label_reloj.setText(f"⏱ {minutos:02d}:{segundos:02d}")

    def evaluar_fuerza(self):
        clave = self.campo_clave.text()
        if len(clave) < 6:
            self.label_fuerza.setText("Fuerza: débil")
            self.label_fuerza.setStyleSheet("color: #d9534f; font-weight: bold;")
        elif len(clave) < 10:
            self.label_fuerza.setText("Fuerza: media")
            self.label_fuerza.setStyleSheet("color: #f0ad4e; font-weight: bold;")
        else:
            self.label_fuerza.setText("Fuerza: fuerte")
            self.label_fuerza.setStyleSheet("color: #5cb85c; font-weight: bold;")

    # ---------------- Utilidades ----------------

    def limpiar(self):
        for campo in (
            self.campo_nombre,
            self.campo_correo,
            self.campo_clave,
            self.campo_edad,
            self.campo_telefono,
        ):
            campo.clear()
        self.combo_pais.setCurrentIndex(0)
        self.radio_masculino.setChecked(True)
        self.chk_terminos.setChecked(False)
        self.chk_novedades.setChecked(False)
        self.campo_observaciones.clear()
        self.etiqueta_mensaje.setText("")
        self.label_fuerza.setText(" ")
        self.bitacora_evento.emit("Formulario limpiado")
        self.mostrar_mensaje("Formulario limpiado")


def main():
    app = QApplication(sys.argv)
    ventana = Registro5()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
