import os
import json
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt


class System (QObject):

   interface_response = pyqtSignal(str)

   def __init__(self):
      super().__init__()
      self.cursos = {}

   def connect_signal(self, function):
      self.interface_response.connect(function)

   def cargar_cursos(self):
      for archivo in os.listdir(os.path.join("Data", "Cursos")):
         curso_cargado = Curso.cargar_curso(archivo)
         self.cursos[curso_cargado.sigla] = curso_cargado

   def cargar_preferencias(self):
      if os.path.exists(os.path.join("Data", "Preferencias", "ListaCursos.json")):
         # cursos seleccionados
         with open(os.path.join("Data", "Preferencias", "ListaCursos.json")) as archivo:
            preferencias = json.load(archivo)
         lista = preferencias["Lista"].split(",")
         for sigla in lista:
            self.cursos[sigla].seleccionado = True
      for archivo in os.listdir(os.path.join("Data", "Preferencias")):
         if archivo != "ListaCursos.json":
            # secciones y profes descartados
            sigla_curso = archivo[0:len(archivo)-5]
            curso = self.cursos[sigla_curso]
            curso.cargar_preferencias()

   def guardar_cursos(self):
      for curso in self.cursos.values():
         curso.guardar_curso()

   def guardar_preferencias(self):
      lista_cursos = []
      for curso in self.cursos.values():
         if curso.seleccionado:
            lista_cursos.append(curso.sigla)
      diccionario = {}
      diccionario["Lista"] = ",".join(lista_cursos)
      with open(os.path.join("Data", "Preferencias", self.sigla + ".json"), "w") as archivo:
         json.dump(diccionario, archivo)
      for curso in self.cursos.values():
         curso.guardar_preferencias()


class Curso:

   def __init__(self, nombre, sigla):
      self.nombre = nombre
      self.sigla = sigla
      self.secciones = {}
      self.profes = {}
      self.seleccionado = False

   def secciones_disponibles(self):
      n_secciones = []
      for seccion in self.secciones.values():
         n_secciones.append(seccion.numero)
      return ",".join(n_secciones)

   def guardar_curso(self):
      diccionario = {}
      diccionario["Sigla"] = self.sigla
      diccionario["Nombre"] = self.nombre
      diccionario["Secciones"] = self.secciones_disponibles()
      for seccion in self.secciones.values():
         diccionario["Profe" + seccion.numero] = ",".join(seccion.docentes)
         diccionario["Horario" + seccion.numero] = str(seccion.horario)
      json.dump(diccionario, os.path.join("Data", "Cursos", self.sigla + ".json"))

   def cargar_curso(archivo):
      contenido = json.load(os.path.join("Data", "Cursos", archivo))
      nuevo_curso = Curso(contenido["Nombre"], contenido["Sigla"])
      secciones_disp = contenido["Secciones"].split(",")
      for seccion_n in secciones_disp:
         profe = contenido["Profe" + seccion_n]
         horario = contenido["Horario" + seccion_n]
         nuevo_curso.secciones[seccion_n] = Seccion(seccion_n, profe, horario, self)
      return nuevo_curso

   def cargar_preferencias(self):
      with open(os.path.join("Data", "Preferencias", self.sigla + ".json")) as archivo:
         contenido = json.load(archivo)
      lista_profes = contenido["Profes"].split(",")
      lista_secciones = contenido["Secciones"].spit(",")
      if len(lista_profes) == 1 and lista_profes[0] == "-":
         pass
      else:
         for profe in lista_profes:
            self.profes[profe].seleccionado = False
      if len(lista_secciones) == 1 and lista_secciones[0] == "-":
         pass
      else:
         for seccion in lista_secciones:
            self.secciones[seccion].seleccionado = False

   def guardar_preferencias(self):
      lista_profes_no = []
      lista_secciones_no = []
      for profe in self.profes.values():
         if profe.seleccionado == False:
            lista_profes_no.append(profe.nombre)
      if len(lista_profes_no) == 0:
         lista_profes_no.append("-")
      for seccion in self.secciones.values():
         if seccion.seleccionado == False:
            lista_secciones_no.append(seccion.numero)
      if len(lista_secciones_no) == 0:
         lista_secciones_no.append("-")
      diccionario = {}
      diccionario["Profes"] = ",".join(lista_profes_no)
      diccionario["Secciones"] = ",".join(lista_secciones_no)
      with open(os.path.join("Data", "Preferencias", self.sigla + ".json"), "w") as archivo:
         json.dump(diccionario, archivo)


class Seccion:

   def __init__(self, numero, docentes, horario, curso):
      self.curso = curso
      self.numero = str(numero)
      self.docentes = self.set_profesores(docentes)
      self.horario = HorarioCurso(horario)
      self.seleccionado = True

   def set_profesores(self, texto):
      lista = texto.split(",")
      # solo crear los docentes repetidos


class Docente:

   def __init__(self, nombre):
      self.nombre = nombre
      self.seleccionado = True


class HorarioCurso:

   def __init__(self, text):
      self.semana = []
      lista_dias = text.split(";")
      for dia in lista_dias:
         modulos_dia = dia.split(",")
         self.semana.append(modulos_dia)

class Horario:

   def __init__(self):
      self.semana = [[], [], [], [], [], []]

   def inscribir_curso(self, horario_curso):
      for i in range(0,6):
         for modulo in horario_curso.semana[i]:
            if self.semana[i] == 0:
               self.semana[i] = [modulo]
            else:
               self.semana[i].append(modulo)

   def hay_tope(self, horario_curso):
      for i in range(0,6):
         for modulo in horario_curso.semana[i]:
            if modulo in self.semana[i]:
               return True
      return False


class Alternativa:

   def __init__(self):
      self.horario = Horario()
      self.cursos = []

   def hay_tope(self, horario_curso):
      return self.horario.hay_tope(horario_curso)

   def agregar_seccion(self, curso, seccion):
      self.cursos.append((curso, seccion.numero))
      self.horario.inscribir_curso(seccion.horario)