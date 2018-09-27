import os
import json
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt


class System (QObject):

   def __init__(self):
      super().__init__()
      self.cursos = {}
      self.cargar_cursos()

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

   def agregar_curso(self, nombre, sigla):
      curso = Curso(nombre, sigla)
      self.cursos[sigla] = curso

   def curso_valido(self, nombre, sigla):
      if sigla in list(self.cursos.keys()):
         return False
      if len(nombre) == 0:
         return False
      if nombre == "ERROR":
         return False
      for char in sigla:
         if not char.isalnum():
            return False
      return True

   def eliminar_curso(self, sigla):
      del self.cursos[sigla]
      os.remove(os.path.join("Data", "Cursos", sigla + ".json"))

   def cambiar_sigla(self, sigla_vieja, sigla_nueva):
      curso = self.cursos[sigla_vieja]
      curso.sigla = sigla_nueva
      curso.guardar_curso()
      self.cursos[sigla_nueva] = curso
      self.cursos[sigla_vieja] = None
      del self.cursos[sigla_vieja]
      os.remove(os.path.join("Data", "Cursos", sigla_vieja + ".json"))

   def seccion_valida(self, curso, numero_seccion, docentes, horario):
      if numero_seccion == "0":
         print("no hay seccion 0")
         return False
      for seccion in curso.secciones:
         if seccion.numero == numero_seccion:
            print("Ya existe esa sección")
            return False
      if not HorarioCurso.es_horario(horario):
         print("Formato horario incorrecto")
         return False
      if not Docente.es_docente(docentes):
         print("Docente invalido")
         return False
      print("seccion_valida")
      return True

   def cambio_seccion_valido(self, curso_seleccionado, seccion_seleccionada, nuevo_numero, nuevo_docente, nuevo_horario):
      if nuevo_numero == "0":
         print("no hay seccion 0")
         return False
      for seccion in curso_seleccionado.secciones:
         if seccion.numero == nuevo_numero:
            if seccion_seleccionada.numero == nuevo_numero:
               break
            else:
               print("numero ya existe")
               return False
      if not HorarioCurso.es_horario(nuevo_horario):
         print("Formato horario incorrecto")
         return False
      if not Docente.es_docente(nuevo_docente):
         print("Docente invalido")
         return False
      return True

   def agregar_seccion(self, curso, numero_seccion, docentes, horario):
      curso.agregar_seccion(numero_seccion, docentes, horario)


class Curso:

   def __init__(self, nombre, sigla):
      self.nombre = nombre
      self.sigla = sigla
      self.secciones = []
      self.profes = {}
      self.seleccionado = False
 
   def secciones_disponibles(self):
      if len(self.secciones) == 0:
         return "0"
      n_secciones = []
      for seccion in self.secciones:
         n_secciones.append(seccion.numero)
      return ",".join(n_secciones)

   def guardar_curso(self):
      diccionario = {}
      diccionario["Sigla"] = self.sigla
      diccionario["Nombre"] = self.nombre
      diccionario["Secciones"] = self.secciones_disponibles()
      for seccion in self.secciones:
         diccionario["Profe" + seccion.numero] = ",".join(seccion.docentes)
         diccionario["Horario" + seccion.numero] = seccion.horario.texto()
      with open(os.path.join("Data", "Cursos", self.sigla + ".json"), "w") as file:
         json.dump(diccionario, file)

   def cargar_curso(archivo):
      with open(os.path.join("Data", "Cursos", archivo)) as file:
         contenido = json.load(file)
      nuevo_curso = Curso(contenido["Nombre"], contenido["Sigla"])
      secciones_disp = contenido["Secciones"].split(",")
      if secciones_disp[0] == "0":
         return nuevo_curso
      print(archivo)
      print(contenido["Secciones"])
      print(secciones_disp)
      for seccion_n in secciones_disp:
         profe = contenido["Profe" + seccion_n]
         horario = contenido["Horario" + seccion_n]
         nuevo_curso.secciones.append(Seccion(seccion_n, profe, horario, nuevo_curso))
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

   def agregar_seccion(self, numero_seccion, docentes, horario):
      nueva_seccion = Seccion(numero_seccion, docentes, horario, self)
      self.secciones.append(nueva_seccion)


class Seccion:

   def __init__(self, numero, docentes, horario, curso):
      self.curso = curso
      self.numero = str(numero)
      self.docentes = self.set_profesores(docentes)
      self.horario = HorarioCurso(horario)
      self.seleccionado = True

   def set_profesores(self, texto):
      lista = texto.split(",")
      return lista

   def editar(self, numero, docentes, horario):
      self.numero = numero
      self.docentes = self.set_profesores(docentes)
      self.horario = HorarioCurso(horario)

   def texto(self):
      texto = "Seccion: " + self.numero + "\n"
      texto = texto + "Docente(s): " + ", ".join(self.docentes) + "\n"
      texto = texto + "Horario: " + self.horario.texto_lineal()
      return texto


class Docente:

   def __init__(self, nombre):
      self.nombre = nombre
      self.seleccionado = True

   def es_docente(text):
      if len(text) == 0:
         return False
      return True


class HorarioCurso:

   
   def __init__(self, text):
      self.semana = []
      lista_dias = text.split("\n")
      for dia in lista_dias:
         modulos_dia = dia[2::].split(",")
         self.semana.append(modulos_dia)

   def es_horario(text):
      if len(text) == 0:
         return False
      dias = text.split("\n")
      if len(dias) != 6:
         return False
      if dias[0][0:2] != "L:":
         return False
      if dias[1][0:2] != "M:":
         return False
      if dias[2][0:2] != "W:":
         return False
      if dias[3][0:2] != "J:":
         return False
      if dias[4][0:2] != "V:":
         return False
      if dias[5][0:2] != "S:":
         return False
      l = dias[0][2::].split(",")
      m = dias[1][2::].split(",")
      w = dias[2][2::].split(",")
      j = dias[3][2::].split(",")
      v = dias[4][2::].split(",")
      s = dias[5][2::].split(",")
      semana = [l, m, w, j, v, s]
      print(semana)
      for dia in semana:
         for modulo in dia:
            if not modulo.isnumeric():
               return False
      return True

   def texto(self):
      texto = "L:" + ",".join(self.semana[0]) + "\n"
      texto = texto + "M:" + ",".join(self.semana[1]) + "\n"
      texto = texto + "W:" + ",".join(self.semana[2]) + "\n"
      texto = texto + "J:" + ",".join(self.semana[3]) + "\n"
      texto = texto + "V:" + ",".join(self.semana[4]) + "\n"
      texto = texto + "S:" + ",".join(self.semana[5])
      return texto

   def texto_lineal(self):
      semana_texto = []
      for dia in self.semana:
         semana_texto.append(",".join(dia))
      return "-".join(semana_texto)








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