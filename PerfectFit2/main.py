import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import QCoreApplication, Qt, QSize, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QPixmap, QFont, QIcon
import AppSystem
import os


class PerfectFit:

   def __init__(self):
      self.system = AppSystem.System()
      self.window = MainWindow(self.system)
      self.system.connect_signal(self.recibir_senal)

   @pyqtSlot(str)
   def recibir_senal(self, signal):
      print(signal)
      
class MainWindow (QWidget):

   def __init__(self, system):
      super().__init__()
      self.setWindowTitle('PerfectFit')
      self.setGeometry(0, 0, 1400, 900)
      self.system = system
      self.selector_horarios = SelectorHorarios(self)
      self.selector_cursos = SelectorCursos(self)
      self.editor_cursos = EditorCursos(self)
      self.menu_carga = CargarOpciones(self)
      self.menu_guardar = GuardarPreferencias(self)
      self.init_gui()

   def init_gui(self):
      self.fondo = QLabel(self)
      color_fondo = QPixmap(os.path.join("Interfaz", "Gris.png")).scaled(1400, 900, Qt.IgnoreAspectRatio)
      self.fondo.setPixmap(color_fondo)
      self.fondo.show()

      self.titulo = QLabel(self)
      imagen_titulo = QPixmap(os.path.join("Interfaz", "Titulo.png"))
      self.titulo.setPixmap(imagen_titulo)
      self.titulo.move(10,10)
      self.titulo.show()

      self.boton_ver_opciones = QPushButton("Ver Opciones", self)
      self.boton_ver_opciones.setMinimumWidth(170)
      self.boton_ver_opciones.move(30, 115)
      self.boton_ver_opciones.clicked.connect(self.ver_opciones)
      self.boton_ver_opciones.show()

      self.boton_editar_preferencias = QPushButton("Editar Preferencias", self)
      self.boton_editar_preferencias.setMinimumWidth(170)
      self.boton_editar_preferencias.move(220, 115)
      self.boton_editar_preferencias.clicked.connect(self.editar_preferencias)
      self.boton_editar_preferencias.show()

      self.boton_editar_datos = QPushButton("Editar Datos", self)
      self.boton_editar_datos.setMinimumWidth(170)
      self.boton_editar_datos.move(410, 115)
      self.boton_editar_datos.clicked.connect(self.editar_datos)
      self.boton_editar_datos.show()

      self.boton_guardar_cambios = QPushButton("Guardar Cambios", self)
      self.boton_guardar_cambios.setMinimumWidth(170)
      self.boton_guardar_cambios.move(600, 115)
      self.boton_guardar_cambios.clicked.connect(self.guardar_cambios)
      self.boton_guardar_cambios.show()

      self.boton_cargar_opciones = QPushButton("Cargar Opciones", self)
      self.boton_cargar_opciones.setMinimumWidth(170)
      self.boton_cargar_opciones.move(790, 115)
      self.boton_cargar_opciones.clicked.connect(self.cargar_opciones)
      self.boton_cargar_opciones.show()

      self.boton_salir = QPushButton("Salir", self)
      self.boton_salir.setMinimumWidth(170)
      self.boton_salir.move(980, 115)
      self.boton_salir.clicked.connect(self.salir)
      self.boton_salir.show()

      self.fondo_contenido = QLabel(self)
      color_fondo_interno = QPixmap(os.path.join("Interfaz", "Blanco.png")).scaled(1330, 700, Qt.IgnoreAspectRatio)
      self.fondo_contenido.setPixmap(color_fondo_interno)
      self.fondo_contenido.move(30, 160)
      self.fondo_contenido.show()

      self.show()

   def cerrar_todo(self):
      self.selector_horarios.cerrar()
      self.selector_cursos.cerrar()
      self.editor_cursos.cerrar()
      self.menu_guardar.cerrar()
      self.menu_carga.cerrar()

   def ver_opciones(self):
      print("ver opciones")
      self.cerrar_todo()
      self.selector_horarios.abrir()

   def editar_preferencias(self):
      print("editar preferencias")
      self.cerrar_todo()
      self.selector_cursos.abrir()

   def editar_datos(self):
      print("editar datos")
      self.cerrar_todo()
      self.editor_cursos.abrir()

   def guardar_cambios(self):
      print("guardar cambios")
      self.cerrar_todo()
      self.menu_guardar.abrir()

   def cargar_opciones(self):
      print("cargar opciones")
      self.cerrar_todo()
      self.menu_carga.abrir()

   def salir(self):
      exit()

class SubWindow:

   def __init__(self, main_window):
      self.main_window = main_window
      self.init_gui()

   def init_gui(self):
      pass

   def cerrar(self):
      pass

   def abrir(self):
      pass

class SelectorHorarios (SubWindow):

   def init_gui(self):
      pass

   def cerrar(self):
      pass

   def abrir(self):
      pass

class SelectorCursos (SubWindow):

   def init_gui(self):
      self.barra = QLabel(self.main_window)
      img_barra = QPixmap(os.path.join("Interfaz", "Negro.png")).scaled(1, 700, Qt.IgnoreAspectRatio)
      self.barra.setPixmap(img_barra)
      self.barra.move(400, 160)

      self.titulo = QLabel("Cursos disponibles", self.main_window)
      self.titulo.move(90, 170)
      font = QFont()
      font.setPointSize(15)
      self.titulo.setFont(font)

      self.boton_back = QPushButton("<", self.main_window)
      self.boton_back.move(95,780)
      self.boton_back.clicked.connect(self.back)

      self.boton_next = QPushButton(">", self.main_window)
      self.boton_next.move(215,780)
      self.boton_next.clicked.connect(self.next)

      self.nombre_curso = QLabel("Nombre curso : ", self.main_window)
      self.nombre_curso.move(440, 175)
      font = QFont()
      font.setPointSize(13)
      self.nombre_curso.setFont(font)

      self.sigla_curso = QLabel("Sigla curso  : ", self.main_window)
      self.sigla_curso.move(440, 205)
      font = QFont()
      font.setPointSize(13)
      self.sigla_curso.setFont(font)

      self.titulo_secciones = QLabel("Secciones:", self.main_window)
      self.titulo_secciones.move(440, 260)
      font = QFont()
      font.setPointSize(12)
      self.titulo_secciones.setFont(font)

      self.cuadro_secciones = QLabel(self.main_window)
      img_cuadro_s = QPixmap(os.path.join("Interfaz", "GrisClaro.png")).scaled(400, 460, Qt.IgnoreAspectRatio)
      self.cuadro_secciones.setPixmap(img_cuadro_s)
      self.cuadro_secciones.move(440, 300)

      self.titulo_profesores = QLabel("Profesores:", self.main_window)
      self.titulo_profesores.move(900, 260)
      font = QFont()
      font.setPointSize(12)
      self.titulo_profesores.setFont(font)

      self.cuadro_profesores = QLabel(self.main_window)
      img_cuadro_p = QPixmap(os.path.join("Interfaz", "GrisClaro.png")).scaled(400, 460, Qt.IgnoreAspectRatio)
      self.cuadro_profesores.setPixmap(img_cuadro_p)
      self.cuadro_profesores.move(900, 300)

   def cerrar(self):
      self.barra.hide()
      self.titulo.hide()
      self.boton_back.hide()
      self.boton_next.hide()
      self.nombre_curso.hide()
      self.sigla_curso.hide()
      self.titulo_secciones.hide()
      self.titulo_profesores.hide()
      self.cuadro_secciones.hide()
      self.cuadro_profesores.hide()

   def abrir(self):
      print("paso por abrir")
      self.barra.show()
      self.barra.raise_()

      self.titulo.show()
      self.titulo.raise_()

      self.boton_back.show()
      self.boton_back.raise_()

      self.boton_next.show()
      self.boton_next.raise_()

      self.nombre_curso.show()
      self.nombre_curso.raise_()

      self.sigla_curso.show()
      self.sigla_curso.raise_()

      self.titulo_secciones.show()
      self.titulo_secciones.raise_()

      self.titulo_profesores.show()
      self.titulo_profesores.raise_()

      self.cuadro_secciones.show()
      self.cuadro_secciones.raise_()

      self.cuadro_profesores.show()
      self.cuadro_profesores.raise_()

   def back(self):
      pass

   def next(self):
      pass

class EditorCursos (SubWindow):

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.curso_seleccionado = None

   def init_gui(self):
      self.barra = QLabel(self.main_window)
      img_barra = QPixmap(os.path.join("Interfaz", "Negro.png")).scaled(1, 700, Qt.IgnoreAspectRatio)
      self.barra.setPixmap(img_barra)
      self.barra.move(400, 160)

      self.titulo = QLabel("Cursos disponibles", self.main_window)
      self.titulo.move(90, 170)
      font = QFont()
      font.setPointSize(15)
      self.titulo.setFont(font)

      self.boton_agregar_curso = QPushButton("Agregar Curso", self.main_window)
      self.boton_agregar_curso.move(155, 740)
      self.boton_agregar_curso.clicked.connect(self.agregar_curso)

      self.boton_back = QPushButton("<", self.main_window)
      self.boton_back.move(95, 780)
      self.boton_back.clicked.connect(self.back)

      self.boton_next = QPushButton(">", self.main_window)
      self.boton_next.move(215, 780)
      self.boton_next.clicked.connect(self.next)

      self.nombre_curso = QLabel("Nombre curso : ", self.main_window)
      self.nombre_curso.move(440, 175)
      font = QFont()
      font.setPointSize(13)
      self.nombre_curso.setFont(font)

      self.edit_nombre_curso = QLineEdit("x", self.main_window)
      self.edit_nombre_curso.move(610, 175)
      font = QFont()
      font.setPointSize(10)
      self.edit_nombre_curso.setFont(font)

      self.sigla_curso = QLabel("Sigla curso  : ", self.main_window)
      self.sigla_curso.move(440, 205)
      font = QFont()
      font.setPointSize(13)
      self.sigla_curso.setFont(font)

      self.edit_sigla_curso = QLineEdit("x", self.main_window)
      self.edit_sigla_curso.move(610, 205)
      font = QFont()
      font.setPointSize(10)
      self.edit_sigla_curso.setFont(font)

      self.titulo_secciones = QLabel("Secciones:", self.main_window)
      self.titulo_secciones.move(440, 260)
      font = QFont()
      font.setPointSize(12)
      self.titulo_secciones.setFont(font)

      self.cuadro_secciones = QLabel(self.main_window)
      img_sub_cuadro = QPixmap(os.path.join("Interfaz", "GrisClaro.png")).scaled(880, 460, Qt.IgnoreAspectRatio)
      self.cuadro_secciones.setPixmap(img_sub_cuadro)
      self.cuadro_secciones.move(440, 300)

      self.boton_agregar_seccion = QPushButton("Nueva Sección", self.main_window)
      self.boton_agregar_seccion.move(1205, 200)
      self.boton_agregar_seccion.clicked.connect(self.agregar_seccion)


   def cerrar(self):
      self.barra.hide()
      self.titulo.hide()
      self.boton_agregar_curso.hide()
      self.boton_back.hide()
      self.boton_next.hide()

      self.nombre_curso.hide()
      self.sigla_curso.hide()
      self.edit_nombre_curso.hide()
      self.edit_sigla_curso.hide()
      self.titulo_secciones.hide()
      self.cuadro_secciones.hide()
      self.boton_agregar_seccion.hide()

   def abrir(self):
      self.barra.show()
      self.barra.raise_()

      self.titulo.show()
      self.titulo.raise_()

      self.boton_agregar_curso.show()
      self.boton_agregar_curso.raise_()

      self.boton_back.show()
      self.boton_back.raise_()

      self.boton_next.show()
      self.boton_next.raise_()

      # Esto no va aqui

      self.nombre_curso.show()
      self.nombre_curso.raise_()

      self.sigla_curso.show()
      self.sigla_curso.raise_()

      self.edit_nombre_curso.show()
      self.edit_nombre_curso.raise_()

      self.edit_sigla_curso.show()
      self.edit_sigla_curso.raise_()

      self.titulo_secciones.show()
      self.titulo_secciones.raise_()

      self.cuadro_secciones.show()
      self.cuadro_secciones.raise_()

      self.boton_agregar_seccion.show()
      self.boton_agregar_seccion.raise_()

   def agregar_curso(self):
      pass

   def back(self):
      pass

   def next(self):
      pass

   def seleccionar_curso(self):
      pass

   def agregar_seccion(self):
      pass

class CargarOpciones (SubWindow):

   def init_gui(self):
      self.titulo = QLabel("Opciones Guardadas", self.main_window)
      self.titulo.move(90, 165)
      font = QFont()
      font.setPointSize(15)
      self.titulo.setFont(font)

   def cerrar(self):
      self.titulo.hide()

   def abrir(self):
      self.titulo.show()
      self.titulo.raise_()

class GuardarPreferencias (SubWindow):

   def init_gui(self):
      self.titulo = QLabel("Preferencias guardadas.", self.main_window)
      self.titulo.move(90, 165)
      font = QFont()
      font.setPointSize(15)
      self.titulo.setFont(font)

   def cerrar(self):
      self.titulo.hide()

   def abrir(self):
      self.titulo.show()
      self.titulo.raise_()

class VentanaNuevoCurso (QWidget):

   pass

class VentanaNuevaSeccion (QWidget):

   pass


if __name__ == '__main__':
   def hook(type, value, traceback):
      print(type)
      print(traceback)
   sys.__excepthook__ = hook

   app = QApplication(sys.argv)
   perfectfit = PerfectFit()
   sys.exit(app.exec_())