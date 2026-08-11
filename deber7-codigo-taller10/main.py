"""
Taller 10 - Sistema de Gestión Académica
Desarrollado por: [Nombre del Estudiante]
Fecha: [Fecha actual]
"""

from estudiantes import GestionEstudiantes
from notas import GestionNotas
from utils import mostrar_menu, validar_opcion, limpiar_pantalla

class Taller10:
    def __init__(self):
        """Constructor de la clase principal"""
        self.gestion_estudiantes = GestionEstudiantes()
        self.gestion_notas = GestionNotas()
        self.ejecutar = True
    
    def ejecutar_programa(self):
        """Método principal que ejecuta el programa"""
        while self.ejecutar:
            limpiar_pantalla()
            print("=" * 50)
            print("   SISTEMA DE GESTIÓN ACADÉMICA - TALLER 10")
            print("=" * 50)
            mostrar_menu()
            
            opcion = validar_opcion(input("Seleccione una opción: "))
            
            if opcion == 1:
                self.registrar_estudiante()
            elif opcion == 2:
                self.consultar_estudiante()
            elif opcion == 3:
                self.listar_estudiantes()
            elif opcion == 4:
                self.registrar_notas()
            elif opcion == 5:
                self.consultar_notas()
            elif opcion == 6:
                self.calcular_promedios()
            elif opcion == 7:
                self.generar_reporte()
            elif opcion == 8:
                self.ejecutar = False
                print("\n¡Gracias por usar el sistema!")
            else:
                print("\nOpción inválida. Intente de nuevo.")
            
            if self.ejecutar:
                input("\nPresione Enter para continuar...")
    
    def registrar_estudiante(self):
        """Registra un nuevo estudiante en el sistema"""
        print("\n" + "=" * 40)
        print("   REGISTRO DE NUEVO ESTUDIANTE")
        print("=" * 40)
        
        cedula = input("Ingrese la cédula del estudiante: ")
        
        if self.gestion_estudiantes.verificar_existencia(cedula):
            print("¡Error! Ya existe un estudiante con esa cédula.")
            return
        
        nombre = input("Ingrese el nombre completo: ")
        edad = input("Ingrese la edad: ")
        carrera = input("Ingrese la carrera: ")
        
        estudiante = {
            'cedula': cedula,
            'nombre': nombre,
            'edad': edad,
            'carrera': carrera
        }
        
        if self.gestion_estudiantes.agregar_estudiante(estudiante):
            print("\n✅ Estudiante registrado exitosamente!")
        else:
            print("\n❌ Error al registrar el estudiante.")
    
    def consultar_estudiante(self):
        """Consulta y muestra la información de un estudiante"""
        print("\n" + "=" * 40)
        print("   CONSULTA DE ESTUDIANTE")
        print("=" * 40)
        
        cedula = input("Ingrese la cédula del estudiante: ")
        
        estudiante = self.gestion_estudiantes.buscar_estudiante(cedula)
        
        if estudiante:
            print("\n📋 INFORMACIÓN DEL ESTUDIANTE:")
            print(f"Cédula: {estudiante['cedula']}")
            print(f"Nombre: {estudiante['nombre']}")
            print(f"Edad: {estudiante['edad']}")
            print(f"Carrera: {estudiante['carrera']}")
        else:
            print("\n❌ Estudiante no encontrado.")
    
    def listar_estudiantes(self):
        """Lista todos los estudiantes registrados"""
        print("\n" + "=" * 40)
        print("   LISTADO DE ESTUDIANTES")
        print("=" * 40)
        
        estudiantes = self.gestion_estudiantes.listar_estudiantes()
        
        if not estudiantes:
            print("\nNo hay estudiantes registrados.")
            return
        
        print("\nCédula     | Nombre                | Edad | Carrera")
        print("-" * 60)
        for est in estudiantes:
            print(f"{est['cedula']:10} | {est['nombre']:20} | {est['edad']:4} | {est['carrera']}")
    
    def registrar_notas(self):
        """Registra notas para un estudiante"""
        print("\n" + "=" * 40)
        print("   REGISTRO DE NOTAS")
        print("=" * 40)
        
        cedula = input("Ingrese la cédula del estudiante: ")
        
        if not self.gestion_estudiantes.verificar_existencia(cedula):
            print("❌ Estudiante no encontrado.")
            return
        
        asignatura = input("Ingrese el nombre de la asignatura: ")
        
        try:
            nota1 = float(input("Ingrese la nota del primer parcial: "))
            nota2 = float(input("Ingrese la nota del segundo parcial: "))
            nota3 = float(input("Ingrese la nota del examen final: "))
            
            if all(0 <= nota <= 20 for nota in [nota1, nota2, nota3]):
                notas = {
                    'cedula': cedula,
                    'asignatura': asignatura,
                    'parcial1': nota1,
                    'parcial2': nota2,
                    'examen': nota3
                }
                
                if self.gestion_notas.agregar_notas(notas):
                    print("\n✅ Notas registradas exitosamente!")
                else:
                    print("\n❌ Error al registrar las notas.")
            else:
                print("\n❌ Las notas deben estar entre 0 y 20.")
        except ValueError:
            print("\n❌ Error: Ingrese valores numéricos válidos.")
    
    def consultar_notas(self):
        """Consulta las notas de un estudiante"""
        print("\n" + "=" * 40)
        print("   CONSULTA DE NOTAS")
        print("=" * 40)
        
        cedula = input("Ingrese la cédula del estudiante: ")
        
        if not self.gestion_estudiantes.verificar_existencia(cedula):
            print("❌ Estudiante no encontrado.")
            return
        
        notas = self.gestion_notas.consultar_notas(cedula)
        
        if not notas:
            print("\nNo hay notas registradas para este estudiante.")
            return
        
        estudiante = self.gestion_estudiantes.buscar_estudiante(cedula)
        print(f"\n📊 NOTAS DE {estudiante['nombre']}:")
        print("-" * 50)
        
        for nota in notas:
            print(f"\nAsignatura: {nota['asignatura']}")
            print(f"Primer Parcial: {nota['parcial1']:.1f}")
            print(f"Segundo Parcial: {nota['parcial2']:.1f}")
            print(f"Examen Final: {nota['examen']:.1f}")
            
            promedio = self.calcular_promedio_nota(nota)
            print(f"Promedio: {promedio:.1f}")
            print(f"Estado: {self.determinar_estado(promedio)}")
    
    def calcular_promedios(self):
        """Calcula y muestra los promedios de todos los estudiantes"""
        print("\n" + "=" * 40)
        print("   CÁLCULO DE PROMEDIOS")
        print("=" * 40)
        
        estudiantes = self.gestion_estudiantes.listar_estudiantes()
        
        if not estudiantes:
            print("\nNo hay estudiantes registrados.")
            return
        
        print("\nCédula     | Estudiante           | Promedio | Estado")
        print("-" * 60)
        
        for est in estudiantes:
            notas = self.gestion_notas.consultar_notas(est['cedula'])
            if notas:
                total_promedios = 0
                for nota in notas:
                    total_promedios += self.calcular_promedio_nota(nota)
                promedio = total_promedios / len(notas)
            else:
                promedio = 0
            
            estado = self.determinar_estado(promedio)
            print(f"{est['cedula']:10} | {est['nombre']:20} | {promedio:8.1f} | {estado}")
    
    def calcular_promedio_nota(self, notas):
        """Calcula el promedio ponderado de las notas"""
        # 30% primer parcial, 30% segundo parcial, 40% examen final
        return (notas['parcial1'] * 0.3 + notas['parcial2'] * 0.3 + notas['examen'] * 0.4)
    
    def determinar_estado(self, promedio):
        """Determina el estado del estudiante según su promedio"""
        if promedio >= 14:
            return "Aprobado"
        elif promedio >= 10:
            return "Suspenso"
        else:
            return "Reprobado"
    
    def generar_reporte(self):
        """Genera un reporte completo del sistema"""
        print("\n" + "=" * 40)
        print("   REPORTE GENERAL")
        print("=" * 40)
        
        estudiantes = self.gestion_estudiantes.listar_estudiantes()
        
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"Total de estudiantes: {len(estudiantes)}")
        
        if estudiantes:
            aprobados = 0
            suspensos = 0
            reprobados = 0
            
            for est in estudiantes:
                notas = self.gestion_notas.consultar_notas(est['cedula'])
                if notas:
                    total_promedios = 0
                    for nota in notas:
                        total_promedios += self.calcular_promedio_nota(nota)
                    promedio = total_promedios / len(notas)
                    
                    estado = self.determinar_estado(promedio)
                    if estado == "Aprobado":
                        aprobados += 1
                    elif estado == "Suspenso":
                        suspensos += 1
                    else:
                        reprobados += 1
            
            print(f"Estudiantes aprobados: {aprobados}")
            print(f"Estudiantes en suspenso: {suspensos}")
            print(f"Estudiantes reprobados: {reprobados}")

if __name__ == "__main__":
    programa = Taller10()
    programa.ejecutar_programa()