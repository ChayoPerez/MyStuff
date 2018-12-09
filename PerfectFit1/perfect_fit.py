def separar(text):
	array = []
	for i in range(0,len(text)):
		array.append(text[i])
	return array

def equals(array):
	new_array = []
	for i in range(0,len(array)):
		new_array.append([])
		for j in range(0,len(array[i])):
			new_array[i].append(array[i][j])
	return new_array

def small_equals(array):
	new_array = []
	for number in array:
		new_array.append(number)
	return new_array

def equals_h(array):
	new_array = []
	for i in range(0,len(array)):
		new_array.append(array[i])
	return new_array


class Curso:
	biblioteca = []
	def __init__(self,nombre):
		self.nombre = nombre
		self.secciones = []

	def cargar_curso(nombre_curso):
		archivo = open(nombre_curso+".txt")
		lines = archivo.readlines()
		for i in range(0,len(lines)):
			lines[i] = lines[i].strip("\n")

		nuevo_curso = Curso(nombre_curso)
		Curso.biblioteca.append(nuevo_curso)

		marker = 0
		for i in range(0,len(lines)):
			if i >= marker and not(len(lines[i]) == 0) and lines[i][0] == "s":
				numero_seccion = lines[i][1:]
				profe = lines[i+1]
				l = separar(lines[i+2])
				m = separar(lines[i+3])
				w = separar(lines[i+4])
				j = separar(lines[i+5])
				v = separar(lines[i+6])
				s = separar(lines[i+7])

				horario_sec = [l,m,w,j,v,s]

				new_sec = Seccion(numero_seccion,profe,horario_sec, nombre_curso)

				marker = i+8

				nuevo_curso.add_seccion(new_sec)

		archivo.close()
		print("Curso agregado.")


	def borrar_seccion(self, numero_seccion):

		for seccion in self.secciones:
			if seccion.numero == numero_seccion:
				self.secciones.remove(seccion)

	def borrar_profe(self,nombre_profe):
		secciones_a_borrar = []
		for seccion in self.secciones:
			if seccion.profesor == nombre_profe:
				secciones_a_borrar.append(seccion)
		for seccion in secciones_a_borrar:
			self.secciones.remove(seccion)
		if len(secciones_a_borrar)==0:
			print("No se encontró un profesor con ese nombre en ese ramo.")


	def borrar_horario(self,horario_a_borrar):
		secciones_a_borrar = []
		for seccion in self.secciones:
			if seccion.tope_horario(horario_a_borrar):
				secciones_a_borrar.append(seccion)
		for seccion in secciones_a_borrar:
			self.secciones.remove(seccion)


	def add_seccion(self, seccion):
		new_sec = Seccion(seccion.numero,seccion.profesor,equals(seccion.horario),seccion.curso)
		self.secciones.append(new_sec)

	def imprimir_curso(self, horario):
		print("Lista de secciones para "+self.nombre + ":\n")
		for seccion in self.secciones:
			print("Sección: "+seccion.numero)
			print("Profesor/a: "+seccion.profesor)
			if horario:
				if not(seccion.horario[0] == 0):
					print("L: " + ",".join(seccion.horario[0]))
				if not(seccion.horario[1] == 0):
					print("M: " + ",".join(seccion.horario[1]))
				if not(seccion.horario[2] == 0):
					print("W: " + ",".join(seccion.horario[2]))
				if not(seccion.horario[3] == 0):
					print("J: " + ",".join(seccion.horario[3]))
				if not(seccion.horario[4] == 0):
					print("V: " + ",".join(seccion.horario[4]))
				if not(seccion.horario[5] == 0):
					print("S: " + ",".join(seccion.horario[5]))
				
			print("\n")

	def armar_horario(ip=[], total=[]):
		#in-process
		n = len(ip)
		if len(Curso.biblioteca) == n:
			total.append(ip)
			return total
		else:
			for seccion in Curso.biblioteca[n].secciones:
				if not(seccion.tope_seccion_vs_horario(ip)):
					total = Curso.armar_horario(equals_h(ip+[seccion]),total)
			return total



class Seccion:
	def __init__(self,numero,profesor,horario, curso):
		self.numero = numero
		self.profesor = profesor
		self.horario = equals(horario)
		self.curso = curso

	def tope_horario(self, horario_tope):
		for i in range(0,6):
			for j in range(0,len(self.horario[i])):
				if (self.horario[i][j] in horario_tope[i]) and not(self.horario[i][j]=="0"):
					return True
		return False

	def tope_seccion_vs_horario(self, horario_actual):
		for seccion in horario_actual:
			if self.tope_horario(seccion.horario):
				return True
		return False


def imprimir_horario(horario):
	week = []
	week.append("".join(horario[0]))
	week.append("".join(horario[1]))
	week.append("".join(horario[2]))
	week.append("".join(horario[3]))
	week.append("".join(horario[4]))
	week.append("".join(horario[5]))
	imp = "-".join(week)
	print(imp)

def pegar_horario(secciones):
	horario_final = []
	for i in range(0,6):
		horario_final.append([])
		addition = []
		for seccion in secciones:
			for number in seccion.horario[i]:
				addition.append(number)
		horario_final[i] = small_equals(addition)

	horario_final_ordenado =[]
	for i in range(0,6):
		horario_final_ordenado.append([])
		horario_final_ordenado[i] = ordenar_lista_str(horario_final[i])
		if horario_final_ordenado[i].count("0") > 0:
			horario_final_ordenado[i].remove("0")
		if len(horario_final_ordenado[i]) == 0:
			horario_final_ordenado[i].append("0")

	return horario_final_ordenado


def ordenar_lista_str(lista):
	numeros = []
	for numero in lista:
		numeros.append(int(numero))
	numeros.sort()
	new = []
	for numero in numeros:
		new.append(str(numero))
	return new







print("Hola, bienvenido al organizador de Ramos")

while(True):
	print("Opción:")
	print("(0) Cargar ramo")
	print("(1) Desplegar lista de ramos y secciones")
	print("(2) Eliminar profesor")
	print("(3) Eliminar módulos")
	print("(4) Borrar una sección")
	print("(5) Generar horarios")
	print("(6) *")


	while (True):
		respuesta = input("Ingresa un número: ")
		if respuesta == "0":
			respuesta = input("Ingresa el nombre del ramo que quieres cargar:")
			Curso.cargar_curso(respuesta)
			break
		elif respuesta == "1":
			respuesta1 = input("Ingresa el ramo que quieres imprimir: ('0' si quiere imprimir todos)")
			respuesta2 = input("(1) Con horarios (2) Sin horarios\n")
			horarios = False
			if respuesta2 == "1":
				horarios = True
			if respuesta1 == "0":
				for curso in Curso.biblioteca:
					curso.imprimir_curso(horarios)

			else:
				for curso in Curso.biblioteca:
					if curso.nombre == respuesta1:
						curso.imprimir_curso(horarios)

			break
		elif respuesta == "2":
			nombre_curso = input("Ingresa el nombre del curso:")
			profe = input("Ingresa el nombre del profesor: ")
			curso_encontrado = False
			for curso in Curso.biblioteca:
				if curso.nombre == nombre_curso:
					curso_encontrado = True
					curso.borrar_profe(profe)
			if curso_encontrado == False:
				print("No hay un curso con ese nombre en la lista.")
			else:
				print("Las secciones con ese profesor se han borrado de la lista.")
			break
		elif respuesta == "3":
			print("Escribe los módulos cada día, con los números juntos y '0' en los días que no anulas nada. Ejemplo L: 0 M: 34")
			l = input("L: ")
			m = input("M: ")
			w = input("W: ")
			j = input("J: ")
			v = input("V: ")
			s = input("S: ")
			modulos_a_borrar = [separar(l),separar(m),separar(w),separar(j),separar(v),separar(s)]

			for curso in Curso.biblioteca:
				curso.borrar_horario(modulos_a_borrar)
			print("Módulos borrados")
			break
		elif respuesta == "5":
			print("Horarios posibles:")
			n = 1
			horarios_posibles = Curso.armar_horario()
			for opcion in horarios_posibles:
				print("Opción "+str(n) + ":")
				for curso in opcion:
					print(curso.curso + " (s" + curso.numero + "): " + curso.profesor)
					imprimir_horario(curso.horario)
				print("\nHorario final:")
				imprimir_horario(pegar_horario(opcion))
				print()
				n += 1
			break

		elif respuesta == "4":
			nombre_curso = input("Ingresa el nombre del curso:")
			n_seccion = input("Ingresa el número de la sección que quieres borrar: ")
			curso_encontrado = False
			for curso in Curso.biblioteca:
				if curso.nombre == nombre_curso:
					curso_encontrado = True
					curso.borrar_seccion(n_seccion)
			if curso_encontrado == False:
				print("No hay un curso con ese nombre en la lista.")
			else:
				print("La sección que ingresaste ya no está disponible.")
			break


		elif respuesta == "6":

			Curso.cargar_curso("Cálculo 2")
			Curso.cargar_curso("Química")
			Curso.cargar_curso("Estática")
			Curso.cargar_curso("Laboratorio Estática")
			Curso.cargar_curso("Coro")
			Curso.cargar_curso("Electivos")

			Curso.biblioteca[0].borrar_profe("Héctor Pasten")
			Curso.biblioteca[0].borrar_profe("Christian Sadel")
			Curso.biblioteca[0].borrar_profe("Rodrigo Vargas")
			Curso.biblioteca[0].borrar_profe("Luís Disset")
			#Curso.biblioteca[0].borrar_profe("Vania Ramirez")

			Curso.biblioteca[2].borrar_profe("Ignacio Espinoza")
			Curso.biblioteca[2].borrar_profe("Esteban Ramos")
			Curso.biblioteca[2].borrar_profe("Andrés Meza")
			Curso.biblioteca[2].borrar_profe("Benjamin Koch")
			#Curso.biblioteca[2].borrar_profe("Rodrigo Soto")
			

			"""
                        Ejemplos
			Curso.biblioteca[0].borrar_profe("yo-ying")
			Curso.biblioteca[0].borrar_seccion("1")

			"""
			
			print("Preferencias cargadas\n")
		else:
			print("Input inválido.")
	print("\n")
