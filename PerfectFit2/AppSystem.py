import os
import json


class System:

   def __init__(self):
      self.cursos = {}
      self.cargar_cursos()

   def cargar_cursos(self):
      for archivo in os.listdir(os.path.join("Data", "Cursos")):
         curso_cargado = Curso.cargar_curso(archivo)
         self.cursos[curso_cargado.sigla] = curso_cargado

   def guardar_cursos(self):
      for curso in self.cursos.values():
         curso.guardar_curso()

   def agregar_curso(self, nombre, sigla):
      curso = Curso(nombre, sigla)
      self.cursos[sigla] = curso

   def curso_valido(self, nombre, sigla):
      if sigla in list(self.cursos.keys()):
         return "La sigla ya existe."
      if len(nombre) == 0:
         return "No hay nombre."
      if len(sigla) == 0:
         return "No hay sigla."
      if nombre == "ERROR":
         return "Nombre no válido."
      for char in sigla:
         if not char.isalnum():
            return "Sigla no válida"
      return "valido"

   def cambio_valido(self, curso, nombre, sigla):
      if sigla in list(self.cursos.keys()) and curso.sigla != sigla:
         return "La sigla ya existe."
      if len(nombre) == 0:
         return "No hay nombre."
      if len(sigla) == 0:
         return "No hay sigla."
      for char in sigla:
         if not char.isalnum():
            return "Sigla no válida"
      return "valido"

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
         return "No hay sección 0."
      for seccion in curso.secciones:
         if seccion.numero == numero_seccion:
            return "Ya existe esa sección."
      if not HorarioCurso.es_horario(horario):
         return "Formato de horario incorrecto."
      if not Docente.es_docente(docentes):
         return "Docente inválido"
      return "valido"

   def cambio_seccion_valido(self, curso_seleccionado, seccion_seleccionada, nuevo_numero, nuevo_docente, nuevo_horario):
      if nuevo_numero == "0":
         return "No hay sección 0."
      for seccion in curso_seleccionado.secciones:
         if seccion.numero == nuevo_numero:
            if seccion_seleccionada.numero == nuevo_numero:
               break
            else:
               return "El número ya existe."
      if not HorarioCurso.es_horario(nuevo_horario):
         return "Formato de horario incorrecto."
      if not Docente.es_docente(nuevo_docente):
         return "Docente inválido"
      return "valido"

   def agregar_seccion(self, curso, numero_seccion, docentes, horario):
      curso.agregar_seccion(numero_seccion, docentes, horario)

   def generar_horarios(self):
      horarios = []
      return horarios


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
      if self.seleccionado:
         diccionario["Seleccionado"] = "Sí"
      else:
         diccionario["Seleccionado"] = "No"
      secciones_no_seleccionadas = []
      for seccion in self.secciones:
         diccionario["Profe" + seccion.numero] = ",".join(seccion.docentes)
         diccionario["Horario" + seccion.numero] = seccion.horario.texto()
         if seccion.seleccionado == False:
            secciones_no_seleccionadas.append(seccion.numero)
      if len(secciones_no_seleccionadas) == 0:
         diccionario["Secciones No Seleccionadas"] = "-"
      else:
         diccionario["Secciones No Seleccionadas"] = ",".join(secciones_no_seleccionadas)

      with open(os.path.join("Data", "Cursos", self.sigla + ".json"), "w") as file:
         json.dump(diccionario, file)

   def cargar_curso(archivo):
      with open(os.path.join("Data", "Cursos", archivo)) as file:
         contenido = json.load(file)
      nuevo_curso = Curso(contenido["Nombre"], contenido["Sigla"])
      if contenido["Seleccionado"] == "Sí":
         nuevo_curso.seleccionado = True
      else:
         nuevo_curso.seleccionado = False
      secciones_disp = contenido["Secciones"].split(",")
      if secciones_disp[0] == "0":
         return nuevo_curso
      for seccion_n in secciones_disp:
         profe = contenido["Profe" + seccion_n]
         horario = contenido["Horario" + seccion_n]
         nuevo_curso.secciones.append(Seccion(seccion_n, profe, horario, nuevo_curso))
      lista_secciones_no = contenido["Secciones No Seleccionadas"]
      nuevo_curso.cargar_preferencias_secciones(lista_secciones_no.split(","))
      return nuevo_curso

   def cargar_preferencias_secciones(self, lista):
      print(lista)
      for seccion in self.secciones:
         if seccion.numero in lista:
            seccion.seleccionado = False

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
            self.semana[i].append(modulo)

   def hay_tope(self, horario_curso):
      for i in range(0,6):
         for modulo in horario_curso.semana[i]:
            if modulo in self.semana[i]:
               return True
      return False

   def texto(self):
      semana_texto = []
      for dia in self.semana:
         semana_texto.append(",".join(dia))
         dia.sort()
      return "-".join(semana_texto)


class Alternativa:

   def __init__(self, numero):
      self.numero = str(numero)
      self.horario = Horario()
      self.cursos = []

   def hay_tope(self, horario_curso):
      return self.horario.hay_tope(horario_curso)

   def agregar_seccion(self, curso, seccion):
      self.cursos.append((curso, seccion.numero))
      self.horario.inscribir_curso(seccion.horario)

   def texto_corto(self):
      texto = "Alternativa " + self.numero + "\n"
      texto = texto + "Horario: " + self.horario.texto()
      return texto

   def texto_largo(self):
      texto = "Alternativa " + self.numero + "\n"
      texto = texto + "Cursos:\n" + self.texto_cursos()
      texto = texto + "Horario: " + self.horario.texto()
      return texto

   def texto_cursos(self):
      texto = ""
      for curso in self.cursos:
         texto = texto + curso[0].nombre + " - Sección " + curso[1] + "\n"
      return texto 
