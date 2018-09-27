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

   @pyqtSlot(str)
   def recibir_senal(self, signal):
      print(signal)
      

class MainWindow (QWidget):

   def __init__(self, system):
      super().__init__()
      self.setWindowTitle('PerfectFit')
      self.setGeometry(0, 0, 1200, 600)
      self.system = system
      self.selector_horarios = SelectorHorarios(self)
      self.selector_cursos = SelectorCursos(self)
      self.editor_cursos = EditorCursos(self)
      self.menu_carga = CargarOpciones(self)
      self.menu_guardar = GuardarPreferencias(self)
      self.init_gui()

   def init_gui(self):
      self.fondo = QLabel(self)
      color_fondo = QPixmap(os.path.join("Interfaz", "Gris.png")).scaled(1200, 600, Qt.IgnoreAspectRatio)
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
      self.system.guardar_cursos()

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

      self.boton_back = QPushButton("<", self.main_window)
      self.boton_back.move(95,545)
      self.boton_back.clicked.connect(self.back)

      self.boton_next = QPushButton(">", self.main_window)
      self.boton_next.move(215,545)
      self.boton_next.clicked.connect(self.next)

      self.nombre_curso = QLabel("Nombre curso : ", self.main_window)
      self.nombre_curso.move(440, 175)
      font = QFont()
      font.setPointSize(13)
      self.nombre_curso.setFont(font)
      self.nombre_curso.setFixedWidth(500)

      self.sigla_curso = QLabel("Sigla curso  : ", self.main_window)
      self.sigla_curso.move(440, 205)
      font = QFont()
      font.setPointSize(13)
      self.sigla_curso.setFont(font)
      self.sigla_curso.setFixedWidth(500)

      self.titulo_secciones = QLabel("Secciones:", self.main_window)
      self.titulo_secciones.move(440, 260)
      font = QFont()
      font.setPointSize(12)
      self.titulo_secciones.setFont(font)

      self.cuadro_secciones = QLabel(self.main_window)
      img_cuadro_s = QPixmap(os.path.join("Interfaz", "GrisClaro.png")).scaled(300, 270, Qt.IgnoreAspectRatio)
      self.cuadro_secciones.setPixmap(img_cuadro_s)
      self.cuadro_secciones.move(440, 300)

      self.titulo_profesores = QLabel("Profesores:", self.main_window)
      self.titulo_profesores.move(800, 260)
      font = QFont()
      font.setPointSize(12)
      self.titulo_profesores.setFont(font)

      self.cuadro_profesores = QLabel(self.main_window)
      img_cuadro_p = QPixmap(os.path.join("Interfaz", "GrisClaro.png")).scaled(300, 270, Qt.IgnoreAspectRatio)
      self.cuadro_profesores.setPixmap(img_cuadro_p)
      self.cuadro_profesores.move(800, 300)

      self.listado = ListadoSeleccionCursos(self, 90, 210)
      self.listado_secciones = ListadoSeccionesSeleccion(self, 460, 310)

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

      self.listado.hide()
      self.listado_secciones.hide()

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

      self.listado.show()
      self.listado_secciones.show()

   def back(self):
      self.listado.click_prev()

   def next(self):
      self.listado.click_next()

   def seleccionar_curso(self, curso):
      self.curso_seleccionado = curso
      self.nombre_curso.setText("Nombre curso : " + curso.nombre)
      self.sigla_curso.setText("Sigla curso : " + curso.sigla)
      self.listado_secciones.seleccionar_curso(curso)


class EditorCursos (SubWindow):

   def __init__(self, *args, **kwargs):
      self.curso_seleccionado = None
      super().__init__(*args, **kwargs)

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
      self.boton_agregar_curso.move(1050, 180)
      self.boton_agregar_curso.clicked.connect(self.agregar_curso)

      self.boton_back = QPushButton("<", self.main_window)
      self.boton_back.move(95, 545)
      self.boton_back.clicked.connect(self.back)

      self.boton_next = QPushButton(">", self.main_window)
      self.boton_next.move(215, 545)
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

      self.boton_guardar_cambios = QPushButton("Guardar Cambios", self.main_window)
      self.boton_guardar_cambios.move(770, 175)
      self.boton_guardar_cambios.clicked.connect(self.guardar_cambios)

      self.titulo_secciones = QLabel("Secciones:", self.main_window)
      self.titulo_secciones.move(440, 260)
      font = QFont()
      font.setPointSize(12)
      self.titulo_secciones.setFont(font)
      self.titulo_secciones.setMinimumWidth(500)

      self.cuadro_secciones = QLabel(self.main_window)
      img_sub_cuadro = QPixmap(os.path.join("Interfaz", "GrisClaro.png")).scaled(480, 270, Qt.IgnoreAspectRatio)
      self.cuadro_secciones.setPixmap(img_sub_cuadro)
      self.cuadro_secciones.move(440, 300)

      self.boton_agregar_seccion = QPushButton("Nueva Sección", self.main_window)
      self.boton_agregar_seccion.move(1050, 210)
      self.boton_agregar_seccion.clicked.connect(self.agregar_seccion)

      self.boton_eliminar_curso = QPushButton("Eliminar Curso", self.main_window)
      self.boton_eliminar_curso.move(1050, 265)
      self.boton_eliminar_curso.clicked.connect(self.borrar_curso)

      self.listado = ListadoCursos(self, 90, 210)

      self.listado_secciones = ListadoSeccionesEdicion(self, 480, 320)

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
      self.boton_guardar_cambios.hide()
      self.titulo_secciones.hide()
      self.cuadro_secciones.hide()
      self.boton_agregar_seccion.hide()
      self.boton_eliminar_curso.hide()

      self.listado.hide()
      self.listado_secciones.hide()


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

      self.titulo_secciones.show()
      self.titulo_secciones.raise_()

      self.cuadro_secciones.show()
      self.cuadro_secciones.raise_()      

      self.listado.show()

      if self.curso_seleccionado != None:
         self.seleccionar_curso(self.curso_seleccionado)
      else:
         self.edit_nombre_curso.setText("")
         self.edit_sigla_curso.setText("")
         self.titulo_secciones.setText("Secciones:")


   def agregar_curso(self):
      self.ventana = VentanaNuevoCurso(self.main_window.system)
      self.ventana.show()

   def back(self):
      self.listado.click_prev()

   def next(self):
      self.listado.click_next()

   def seleccionar_curso(self, curso):
      self.curso_seleccionado = curso
      self.edit_nombre_curso.setText(curso.nombre)
      self.edit_sigla_curso.setText(curso.sigla)

      self.edit_nombre_curso.show()
      self.edit_nombre_curso.raise_()
      self.edit_sigla_curso.show()
      self.edit_sigla_curso.raise_()
      self.boton_guardar_cambios.show()
      self.boton_guardar_cambios.raise_()
      self.boton_agregar_seccion.show()
      self.boton_agregar_seccion.raise_()
      self.boton_eliminar_curso.show()
      self.boton_eliminar_curso.raise_()

      if len(self.curso_seleccionado.secciones) != 0:
         self.listado_secciones.show()
         self.mostrar_numero_secciones()
      else:
         self.listado_secciones.hide()


   def agregar_seccion(self):
      self.ventana = VentanaNuevaSeccion(self, self.main_window.system)
      self.ventana.show()

   def guardar_cambios(self):
      if self.curso_seleccionado != None:
         self.curso_seleccionado.nombre = self.edit_nombre_curso.text()
         if self.curso_seleccionado.sigla != self.edit_sigla_curso.text():
            print("cambiar sigla")
            self.main_window.system.cambiar_sigla(self.curso_seleccionado.sigla, self.edit_sigla_curso.text())
         self.listado.show()

   def borrar_curso(self):
      if self.curso_seleccionado != None:
         self.ventana = VentanaBorrarCurso(self)
         self.ventana.show()
      else:
         print("No hay seleccionado")

   def clear(self):
      curso_seleccionado = None
      self.edit_nombre_curso.setText("")
      self.edit_sigla_curso.setText("")
      # vaciar secciones

   def funcion_borrar_curso(self):
      curso = self.curso_seleccionado
      self.clear()
      self.main_window.system.eliminar_curso(curso.sigla)
      self.listado.show()

   def mostrar_numero_secciones(self):
      print("paso por numero secciones")
      numeros = []
      for seccion in self.curso_seleccionado.secciones:
         numeros.append(seccion.numero)
      self.titulo_secciones.setText("Secciones: " + ",".join(numeros))


class VentanaBorrarCurso (QWidget):

   def __init__(self, main_window):
      super().__init__()
      self.setWindowTitle('Eliminar Curso')
      self.setGeometry(100, 100, 250, 100)
      self.main_window = main_window

      self.mensaje = QLabel("¿Seguro que quieres eliminar este curso?", self)
      self.mensaje.move(20, 20)
      self.mensaje.show()

      self.boton = QPushButton("Borrar", self)
      self.boton.move(80, 50)
      self.boton.show()
      self.boton.clicked.connect(self.eliminar)

   def eliminar(self):
      self.main_window.funcion_borrar_curso()
      self.close()


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
      self.titulo = QLabel("Cambios y preferencias guardados.", self.main_window)
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

   def __init__(self, system):
      super().__init__()
      self.setWindowTitle('Agregar Curso')
      self.setGeometry(100, 100, 350, 200)
      self.system = system

      self.titulo = QLabel("Agregar Curso", self)
      self.titulo.move(20, 30)
      font = QFont()
      font.setPointSize(13)
      self.titulo.setFont(font)
      self.titulo.show()

      self.nombre = QLabel("Nombre curso : ", self)
      self.nombre.move(20, 70)
      font = QFont()
      font.setPointSize(12)
      self.nombre.setFont(font)
      self.nombre.show()

      self.edit_nombre = QLineEdit(self)
      self.edit_nombre.move(140, 70)
      self.edit_nombre.setFont(font)
      self.edit_nombre.show()

      self.sigla = QLabel("Sigla curso : ", self)
      self.sigla.move(20, 110)
      self.sigla.setFont(font)
      self.sigla.show()

      self.edit_sigla = QLineEdit(self)
      self.edit_sigla.move(140, 110)
      self.edit_sigla.setFont(font)
      self.edit_sigla.show()

      self.boton = QPushButton("Guardar", self)
      self.boton.move(130, 150)
      self.boton.clicked.connect(self.guardar)
      self.boton.show()

   def guardar(self):
      nombre = self.edit_nombre.text()
      sigla = self.edit_sigla.text()
      if self.system.curso_valido(nombre, sigla):
         self.system.agregar_curso(nombre, sigla)
         self.close()
      else:
         self.edit_nombre.setText("ERROR")
         self.edit_sigla.setText("ERROR")


class VentanaNuevaSeccion (QWidget):

   def __init__(self, subwindow, system):
      super().__init__()
      self.setWindowTitle('Agregar Sección')
      self.setGeometry(100, 100, 400, 300)
      self.system = system
      self.sw = subwindow
      self.curso_seleccionado = self.sw.curso_seleccionado
      self.init_gui()

   def init_gui(self):
      self.starting_x = 20
      self.starting_y = 20

      font = QFont()
      font.setPointSize(12)

      self.numero_seccion = QLabel("Número de sección :", self)
      self.numero_seccion.move(self.starting_x, self.starting_y)
      self.numero_seccion.setFont(font)
      self.numero_seccion.show()

      self.edit_numero_seccion = QLineEdit(self)
      self.edit_numero_seccion.move(self.starting_x + 180, self.starting_y)
      self.edit_numero_seccion.setFont(font)
      self.edit_numero_seccion.show()

      self.docentes = QLabel("Docentes :", self)
      self.docentes.move(self.starting_x, self.starting_y + 40)
      self.docentes.setFont(font)

      self.edit_docentes = QLineEdit(self)
      self.edit_docentes.move(self.starting_x + 180, self.starting_y + 40)
      self.edit_docentes.setFont(font)

      self.horario = QLabel("Horario :", self)
      self.horario.move(self.starting_x, self.starting_y + 80)
      self.horario.setFont(font)

      template = "L:\nM:\nW:\nJ:\nV:\nS:"

      self.edit_horario = QTextEdit(self)
      self.edit_horario.setText(template)
      self.edit_horario.move(self.starting_x + 180, self.starting_y + 80)
      self.edit_horario.setFixedHeight(100)
      self.edit_horario.setFixedWidth(80)

      self.boton_guardar = QPushButton("Guardar Sección", self)
      self.boton_guardar.move(self.starting_x + 130, self.starting_y + 220)
      self.boton_guardar.clicked.connect(self.guardar)
      self.boton_guardar.setFixedWidth(100)


   def guardar(self):
      numero_seccion = self.edit_numero_seccion.text()
      docentes = self.edit_docentes.text()
      horario = self.edit_horario.toPlainText()
      if self.system.seccion_valida(self.curso_seleccionado, numero_seccion, docentes, horario):
         print("seccion creada")
         self.system.agregar_seccion(self.curso_seleccionado, numero_seccion, docentes, horario)
         self.sw.listado_secciones.show()
         self.sw.mostrar_numero_secciones()
         self.close()


class ListadoCursos:

   def __init__(self, subwindow, starting_x, starting_y):
      self.sw = subwindow
      self.main_window = self.sw.main_window
      self.starting_x = starting_x
      self.starting_y = starting_y
      self.init_gui()

   def init_gui(self):
      self.curso1 = QLabel(" ", self.main_window)
      self.curso1.move(self.starting_x + 40, self.starting_y)
      font = QFont()
      font.setPointSize(12)
      self.curso1.setFont(font)
      self.curso1.setFixedWidth(200)

      self.curso2 = QLabel(" ", self.main_window)
      self.curso2.move(self.starting_x + 40 , self.starting_y + 40)
      self.curso2.setFont(font)
      self.curso2.setFixedWidth(200)

      self.curso3 = QLabel(" ", self.main_window)
      self.curso3.move(self.starting_x + 40, self.starting_y + 80)
      self.curso3.setFont(font)
      self.curso3.setFixedWidth(200)

      self.curso4 = QLabel(" ", self.main_window)
      self.curso4.move(self.starting_x + 40, self.starting_y + 120)
      self.curso4.setFont(font)
      self.curso4.setFixedWidth(200)

      self.curso5 = QLabel(" ", self.main_window)
      self.curso5.move(self.starting_x + 40, self.starting_y + 160)
      self.curso5.setFont(font)
      self.curso5.setFixedWidth(200)

      self.curso6 = QLabel(" ", self.main_window)
      self.curso6.move(self.starting_x + 40, self.starting_y + 200)
      self.curso6.setFont(font)
      self.curso6.setFixedWidth(200)

      self.curso7 = QLabel(" ", self.main_window)
      self.curso7.move(self.starting_x + 40, self.starting_y + 240)
      self.curso7.setFont(font)
      self.curso7.setFixedWidth(200)

      self.curso8 = QLabel(" ", self.main_window)
      self.curso8.move(self.starting_x + 40, self.starting_y + 280)
      self.curso8.setFont(font)
      self.curso8.setFixedWidth(200)

      self.boton_curso1 = QPushButton(self.main_window)
      self.boton_curso1.setMinimumWidth(10)
      self.boton_curso1.move(self.starting_x, self.starting_y)
      self.boton_curso1.clicked.connect(self.click_curso1)

      self.boton_curso2 = QPushButton(self.main_window)
      self.boton_curso2.setMinimumWidth(10)
      self.boton_curso2.move(self.starting_x, self.starting_y + 40)
      self.boton_curso2.clicked.connect(self.click_curso2)

      self.boton_curso3 = QPushButton(self.main_window)
      self.boton_curso3.setMinimumWidth(10)
      self.boton_curso3.move(self.starting_x, self.starting_y + 80)
      self.boton_curso3.clicked.connect(self.click_curso3)

      self.boton_curso4 = QPushButton(self.main_window)
      self.boton_curso4.setMinimumWidth(10)
      self.boton_curso4.move(self.starting_x, self.starting_y + 120)
      self.boton_curso4.clicked.connect(self.click_curso4)

      self.boton_curso5 = QPushButton(self.main_window)
      self.boton_curso5.setMinimumWidth(10)
      self.boton_curso5.move(self.starting_x, self.starting_y + 160)
      self.boton_curso5.clicked.connect(self.click_curso5)

      self.boton_curso6 = QPushButton(self.main_window)
      self.boton_curso6.setMinimumWidth(10)
      self.boton_curso6.move(self.starting_x, self.starting_y + 200)
      self.boton_curso6.clicked.connect(self.click_curso6)

      self.boton_curso7 = QPushButton(self.main_window)
      self.boton_curso7.setMinimumWidth(10)
      self.boton_curso7.move(self.starting_x, self.starting_y + 240)
      self.boton_curso7.clicked.connect(self.click_curso7)

      self.boton_curso8 = QPushButton(self.main_window)
      self.boton_curso8.setMinimumWidth(10)
      self.boton_curso8.move(self.starting_x, self.starting_y + 280)
      self.boton_curso8.clicked.connect(self.click_curso8)

      self.cursos_labels = []
      self.cursos_labels.append(self.curso1)
      self.cursos_labels.append(self.curso2)
      self.cursos_labels.append(self.curso3)
      self.cursos_labels.append(self.curso4)
      self.cursos_labels.append(self.curso5)
      self.cursos_labels.append(self.curso6)
      self.cursos_labels.append(self.curso7)
      self.cursos_labels.append(self.curso8)

      self.botones_cursos = []
      self.botones_cursos.append(self.boton_curso1)
      self.botones_cursos.append(self.boton_curso2)
      self.botones_cursos.append(self.boton_curso3)
      self.botones_cursos.append(self.boton_curso4)
      self.botones_cursos.append(self.boton_curso5)
      self.botones_cursos.append(self.boton_curso6)
      self.botones_cursos.append(self.boton_curso7)
      self.botones_cursos.append(self.boton_curso8)

      self.obj_cursos = []

      self.state = 0

   def show(self):
      self.llenar_labels()
      for boton in self.botones_cursos:
         index = self.botones_cursos.index(boton)
         if self.cursos_labels[index].text() != " ":
            boton.show()
            boton.raise_()
         else:
            boton.hide()

   def hide(self):
      for curso in self.cursos_labels:
         curso.hide()
      for boton in self.botones_cursos:
         boton.hide()

   def llenar_labels(self):
      print("llenar labels")
      cursos = list(self.main_window.system.cursos.values())
      if len(cursos) <= 8:
         self.state = 0
      elif self.state < 0:
         self.state = 0
      elif self.state > 0 and len(cursos) < self.state * 8:
         self.state = len(cursos) // 8

      if len(cursos) > 0:
         for i in range(0, len(cursos[self.state * 8: self.state * 8 + 8])):
            index = i + self.state * 8
            self.cursos_labels[i].setText(cursos[index].nombre)
            self.cursos_labels[i].show()
            self.cursos_labels[i].raise_()
         index_ultimo =  len(cursos[self.state * 8: self.state * 8 + 8]) - 1
         for i in range(index_ultimo + 1, 8):
            self.cursos_labels[i].setText(" ")


   def click_curso1(self):
      self.click_button(1)

   def click_curso2(self):
      self.click_button(2)

   def click_curso3(self):
      self.click_button(3)

   def click_curso4(self):
      self.click_button(4)

   def click_curso5(self):
      self.click_button(5)

   def click_curso6(self):
      self.click_button(6)

   def click_curso7(self):
      self.click_button(7)

   def click_curso8(self):
      self.click_button(8)

   def click_button(self, button):
      print(self.curso_indicado(button).nombre)
      self.sw.seleccionar_curso(self.curso_indicado(button))

   def click_next(self):
      self.state += 1
      self.show()

   def click_prev(self):
      self.state -= 1
      self.show()

   def curso_indicado(self, numero):
      index = self.state * 8 + numero - 1
      cursos = list(self.main_window.system.cursos.values())
      return cursos[index]


class ListadoSeleccionCursos (ListadoCursos):

   def __init__(self, subwindow, starting_x, starting_y):
      super().__init__(subwindow, starting_x, starting_y)
      self.init_gui2()

   def init_gui2(self):
      self.seleccionado_img = QPixmap(os.path.join("Interfaz", "Check.png"))
      self.seleccionado_img = self.seleccionado_img.scaled(25, 25, Qt.KeepAspectRatio)
      self.seleccionado_icon = QIcon()
      self.seleccionado_icon.addPixmap(self.seleccionado_img)

      self.no_seleccionado_img = QPixmap(os.path.join("Interfaz", "Uncheck.png"))
      self.no_seleccionado_img = self.no_seleccionado_img.scaled(25, 25, Qt.KeepAspectRatio)
      self.no_seleccionado_icon = QIcon()
      self.no_seleccionado_icon.addPixmap(self.no_seleccionado_img)
      
      self.selector1 = QPushButton(self.main_window)
      self.selector1.move(self.starting_x - 30, self.starting_y)
      self.selector1.clicked.connect(self.select1)
      self.selector1.setIcon(self.no_seleccionado_icon)
      self.selector1.setFixedHeight(23)

      self.selector2 = QPushButton(self.main_window)
      self.selector2.move(self.starting_x - 30, self.starting_y + 40)
      self.selector2.clicked.connect(self.select2)
      self.selector2.setIcon(self.no_seleccionado_icon)
      self.selector2.setFixedHeight(23)

      self.selector3 = QPushButton(self.main_window)
      self.selector3.move(self.starting_x - 30, self.starting_y + 80)
      self.selector3.clicked.connect(self.select3)
      self.selector3.setIcon(self.no_seleccionado_icon)
      self.selector3.setFixedHeight(23)

      self.selector4 = QPushButton(self.main_window)
      self.selector4.move(self.starting_x - 30, self.starting_y + 120)
      self.selector4.clicked.connect(self.select4)
      self.selector4.setIcon(self.no_seleccionado_icon)
      self.selector4.setFixedHeight(23)

      self.selector5 = QPushButton(self.main_window)
      self.selector5.move(self.starting_x - 30, self.starting_y + 160)
      self.selector5.clicked.connect(self.select5)
      self.selector5.setIcon(self.no_seleccionado_icon)
      self.selector5.setFixedHeight(23)

      self.selector6 = QPushButton(self.main_window)
      self.selector6.move(self.starting_x - 30, self.starting_y + 200)
      self.selector6.clicked.connect(self.select6)
      self.selector6.setIcon(self.no_seleccionado_icon)
      self.selector6.setFixedHeight(23)

      self.selector7 = QPushButton(self.main_window)
      self.selector7.move(self.starting_x - 30, self.starting_y + 240)
      self.selector7.clicked.connect(self.select7)
      self.selector7.setIcon(self.no_seleccionado_icon)
      self.selector7.setFixedHeight(23)

      self.selector8 = QPushButton(self.main_window)
      self.selector8.move(self.starting_x - 30, self.starting_y + 280)
      self.selector8.clicked.connect(self.select8)
      self.selector8.setIcon(self.no_seleccionado_icon)
      self.selector8.setFixedHeight(23)

      self.selectores = []
      self.selectores.append(self.selector1)
      self.selectores.append(self.selector2)
      self.selectores.append(self.selector3)
      self.selectores.append(self.selector4)
      self.selectores.append(self.selector5)
      self.selectores.append(self.selector6)
      self.selectores.append(self.selector7)
      self.selectores.append(self.selector8)

   def select1(self):
      self.seleccionar_curso(1)

   def select2(self):
      self.seleccionar_curso(2)

   def select3(self):
      self.seleccionar_curso(3)

   def select4(self):
      self.seleccionar_curso(4)

   def select5(self):
      self.seleccionar_curso(5)

   def select6(self):
      self.seleccionar_curso(6)

   def select7(self):
      self.seleccionar_curso(7)

   def select8(self):
      self.seleccionar_curso(8)

   def seleccionar_curso(self, numero):
      curso = self.curso_indicado(numero)
      curso.seleccionado = not curso.seleccionado   

      print(self.curso_indicado(numero).nombre)
      print(curso.seleccionado)

      index = numero - 1
      if curso.seleccionado:
         self.selectores[index].setIcon(self.seleccionado_icon)
      else:
         self.selectores[index].setIcon(self.no_seleccionado_icon)

   def show(self):
      super().show()
      
      cursos = list(self.main_window.system.cursos.values())
      for selector in self.selectores:
         index = self.selectores.index(selector)
         if self.cursos_labels[index].text() != " ":
            if cursos[self.state * 8 + index].seleccionado:
               selector.setIcon(self.seleccionado_icon)
            else:
               selector.setIcon(self.no_seleccionado_icon)
            selector.show()
            selector.raise_()
         else:
            selector.hide()
      

   def hide(self):
      super().hide()
      for selector in self.selectores:
         selector.hide()


class ListadoSeccionesEdicion:

   def __init__(self, subwindow, starting_x, starting_y):
      self.sw = subwindow
      self.main_window = self.sw.main_window
      self.starting_x = starting_x
      self.starting_y = starting_y
      self.curso_seleccionado = subwindow.curso_seleccionado
      self.seccion_seleccionada = None
      self.state = 0
      self.init_gui()

   def init_gui(self):
      font = QFont()
      font.setPointSize(12)

      self.numero_seccion = QLabel("Número de sección :", self.main_window)
      self.numero_seccion.move(self.starting_x, self.starting_y)
      self.numero_seccion.setFont(font)

      self.edit_numero_seccion = QLineEdit(self.main_window)
      self.edit_numero_seccion.move(self.starting_x + 180, self.starting_y)
      self.edit_numero_seccion.setFont(font)

      self.docentes = QLabel("Docentes :", self.main_window)
      self.docentes.move(self.starting_x, self.starting_y + 40)
      self.docentes.setFont(font)

      self.edit_docentes = QLineEdit(self.main_window)
      self.edit_docentes.move(self.starting_x + 180, self.starting_y + 40)
      self.edit_docentes.setFont(font)

      self.horario = QLabel("Horario :", self.main_window)
      self.horario.move(self.starting_x, self.starting_y + 80)
      self.horario.setFont(font)

      self.edit_horario = QTextEdit(self.main_window)
      self.edit_horario.move(self.starting_x + 180, self.starting_y + 80)
      self.edit_horario.setFixedHeight(100)
      self.edit_horario.setFixedWidth(80)

      self.boton_guardar = QPushButton("Guardar Sección", self.main_window)
      self.boton_guardar.move(self.starting_x, self.starting_y + 200)
      self.boton_guardar.clicked.connect(self.guardar)
      self.boton_guardar.setFixedWidth(100)

      self.boton_next = QPushButton(">", self.main_window)
      self.boton_next.move(self.starting_x + 260, self.starting_y + 200)
      self.boton_next.clicked.connect(self.click_next)

      self.boton_prev = QPushButton("<", self.main_window)
      self.boton_prev.move(self.starting_x + 160, self.starting_y + 200)
      self.boton_prev.clicked.connect(self.click_prev)


   def show(self):
      print("paso por show secciones")

      self.numero_seccion.show()
      self.numero_seccion.raise_()

      self.edit_numero_seccion.show()
      self.edit_numero_seccion.raise_()

      self.docentes.show()
      self.docentes.raise_()

      self.edit_docentes.show()
      self.edit_docentes.raise_()

      self.horario.show()
      self.horario.raise_()

      self.edit_horario.show()
      self.edit_horario.raise_()

      self.boton_guardar.show()
      self.boton_guardar.raise_()

      self.boton_next.show()
      self.boton_next.raise_()

      self.boton_prev.show()
      self.boton_prev.raise_()

      self.llenar_informacion()

   def hide(self):
      self.numero_seccion.hide()
      self.edit_numero_seccion.hide()
      self.docentes.hide()
      self.edit_docentes.hide()
      self.horario.hide()
      self.edit_horario.hide()
      self.boton_guardar.hide()
      self.boton_next.hide()
      self.boton_prev.hide()
      self.edit_numero_seccion.setText("")
      self.edit_docentes.setText("")
      self.edit_horario.setText("")

   def llenar_informacion(self):
      self.curso_seleccionado = self.sw.curso_seleccionado
      if self.state < 0:
         self.state = 0
      elif self.state >= len(self.curso_seleccionado.secciones):
         self.state = len(self.curso_seleccionado.secciones) - 1

      self.seccion_seleccionada = self.curso_seleccionado.secciones[self.state]

      self.edit_numero_seccion.setText(self.seccion_seleccionada.numero)
      self.edit_docentes.setText(", ".join(self.seccion_seleccionada.docentes))
      self.edit_horario.setText(self.seccion_seleccionada.horario.texto())

   def guardar(self):
      numero = self.edit_numero_seccion.text()
      docentes = self.edit_docentes.text()
      horario = self.edit_horario.toPlainText()
      if self.sw.main_window.system.cambio_seccion_valido(self.curso_seleccionado, self.seccion_seleccionada, numero, docentes, horario):
         print("valido")
         self.seccion_seleccionada.editar(numero, docentes, horario)
         self.sw.mostrar_numero_secciones()

   def click_next(self):
      self.state += 1
      self.llenar_informacion()

   def click_prev(self):
      self.state -= 1
      self.llenar_informacion()


class ListadoSeccionesSeleccion:

   def __init__(self, subwindow, starting_x, starting_y):
      self.sw = subwindow
      self.main_window = self.sw.main_window
      self.starting_x = starting_x
      self.starting_y = starting_y
      self.curso_seleccionado = None
      self.init_gui()

   def init_gui(self):
      self.state = 0
      font = QFont()
      font.setPointSize(12)

      self.seccion1 = QLabel(" ", self.main_window)
      self.seccion1.move(self.starting_x + 30, self.starting_y)
      self.seccion1.setFont(font)

      self.seccion2 = QLabel(" ", self.main_window)
      self.seccion2.move(self.starting_x + 30, self.starting_y + 70)
      self.seccion2.setFont(font)

      self.seccion3 = QLabel(" ", self.main_window)
      self.seccion3.move(self.starting_x + 30, self.starting_y + 140)
      self.seccion3.setFont(font)

      self.secciones_labels = []
      self.secciones_labels.append(self.seccion1)
      self.secciones_labels.append(self.seccion2)
      self.secciones_labels.append(self.seccion3)

      self.seleccionado_img = QPixmap(os.path.join("Interfaz", "Check.png"))
      self.seleccionado_img = self.seleccionado_img.scaled(25, 25, Qt.KeepAspectRatio)
      self.seleccionado_icon = QIcon()
      self.seleccionado_icon.addPixmap(self.seleccionado_img)

      self.no_seleccionado_img = QPixmap(os.path.join("Interfaz", "Uncheck.png"))
      self.no_seleccionado_img = self.no_seleccionado_img.scaled(25, 25, Qt.KeepAspectRatio)
      self.no_seleccionado_icon = QIcon()
      self.no_seleccionado_icon.addPixmap(self.no_seleccionado_img)

      self.selector1 = QPushButton(self.main_window)
      self.selector1.move(self.starting_x - 5, self.starting_y)
      self.selector1.setFixedWidth(25)
      self.selector1.clicked.connect(self.select1)

      self.selector2 = QPushButton(self.main_window)
      self.selector2.move(self.starting_x - 5, self.starting_y + 70)
      self.selector2.setFixedWidth(25)
      self.selector2.clicked.connect(self.select2)

      self.selector3 = QPushButton(self.main_window)
      self.selector3.move(self.starting_x - 5, self.starting_y + 140)
      self.selector3.setFixedWidth(25)
      self.selector3.clicked.connect(self.select3)

      self.secciones_selectores = []
      self.secciones_selectores.append(self.selector1)
      self.secciones_selectores.append(self.selector2)
      self.secciones_selectores.append(self.selector3)

      self.boton_next = QPushButton(">", self.main_window)
      self.boton_next.move(self.starting_x + 150, self.starting_y + 220)
      self.boton_next.clicked.connect(self.next)

      self.boton_prev = QPushButton("<", self.main_window)
      self.boton_prev.move(self.starting_x + 30, self.starting_y + 220)
      self.boton_prev.clicked.connect(self.prev)

   def show(self):
      self.llenar_labels()
      if len(self.curso_seleccionado.secciones) > 0:
         for selector in self.secciones_selectores:
            index = self.secciones_selectores.index(selector)
            if self.secciones_labels[index].text() != " ":
               secciones = self.curso_seleccionado.secciones
               if secciones[self.state * 3 + index].seleccionado:
                  selector.setIcon(self.seleccionado_icon)
               else:
                  selector.setIcon(self.no_seleccionado_icon)
               selector.show()
               selector.raise_()
            else:
               selector.hide()
         self.boton_prev.show()
         self.boton_prev.raise_()
         self.boton_next.show()
         self.boton_next.raise_()
      else:
         self.hide()


   def hide(self):
      for label in self.secciones_labels:
         label.hide()
      for boton in self.secciones_selectores:
         boton.hide()
      self.boton_prev.hide()
      self.boton_next.hide()

   def next(self):
      self.state += 1
      self.show()

   def prev(self):
      self.state -= 1
      self.show()

   def llenar_labels(self):
      if self.curso_seleccionado != None:
         print("llenar labels secciones")
         secciones = self.curso_seleccionado.secciones

         if len(secciones) <= 3:
            self.state = 0
         elif self.state < 0:
            self.state = 0
         elif self.state > 0 and len(secciones) < self.state * 3:
            self.state = len(secciones) // 3

         if len(secciones) > 0:
            for i in range(0, len(secciones[self.state * 3: self.state * 3 + 3])):
               index = i + self.state * 3
               self.secciones_labels[i].setText(secciones[index].texto())
               self.secciones_labels[i].show()
               self.secciones_labels[i].raise_()
            index_ultimo =  len(secciones[self.state * 3: self.state * 3 + 3]) - 1
            for i in range(index_ultimo + 1, 3):
               self.secciones_labels[i].setText(" ")

   def seleccionar_curso(self, curso):
      self.curso_seleccionado = curso
      print("curso seleccionado " + curso.nombre)
      self.show()

   def seleccionar_seccion(self, numero):
      seccion = self.seccion_indicada(numero)
      seccion.seleccionado = not seccion.seleccionado  
      print(seccion.seleccionado)
      index = numero - 1
      if seccion.seleccionado:
         self.secciones_selectores[index].setIcon(self.seleccionado_icon)
      else:
         self.secciones_selectores[index].setIcon(self.no_seleccionado_icon)

   def select1(self):
      self.seleccionar_seccion(1)

   def select2(self):
      self.seleccionar_seccion(2)

   def select3(self):
      self.seleccionar_seccion(3)

   def seccion_indicada(self, numero):
      index = self.state * 3 + numero - 1
      secciones = self.curso_seleccionado.secciones
      return secciones[index]



if __name__ == '__main__':
   def hook(type, value, traceback):
      print(type)
      print(traceback)
   sys.__excepthook__ = hook

   app = QApplication(sys.argv)
   perfectfit = PerfectFit()
   sys.exit(app.exec_())