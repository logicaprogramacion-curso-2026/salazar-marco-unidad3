"""
Módulo de utilidades para el taller
"""

import os
import platform

def limpiar_pantalla():
    """
    Limpia la pantalla de la consola según el sistema operativo
    """
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def mostrar_menu():
    """
    Muestra el menú principal del sistema
    """
    print("\n" + "-" * 50)
    print("   MENÚ PRINCIPAL")
    print("-" * 50)
    print("1. Registrar estudiante")
    print("2. Consultar estudiante")
    print("3. Listar estudiantes")
    print("4. Registrar notas")
    print("5. Consultar notas")
    print("6. Calcular promedios")
    print("7. Generar reporte")
    print("8. Salir")
    print("-" * 50)

def validar_opcion(opcion):
    """
    Valida que la opción ingresada sea un número válido
    Args:
        opcion (str): Opción ingresada por el usuario
    Returns:
        int: Número de opción válido, 0 si es inválido
    """
    try:
        return int(opcion)
    except ValueError:
        return 0

def validar_cedula(cedula):
    """
    Valida que la cédula tenga el formato correcto
    Args:
        cedula (str): Cédula a validar
    Returns:
        bool: True si es válida, False en caso contrario
    """
    # Eliminar espacios y guiones
    cedula = cedula.replace(' ', '').replace('-', '')
    
    # Verificar que tenga 10 dígitos y sean numéricos
    if len(cedula) != 10 or not cedula.isdigit():
        return False
    
    # Implementar algoritmo de validación de cédula ecuatoriana
    # (Este es un ejemplo básico)
    return True

def validar_nota(nota):
    """
    Valida que la nota esté en el rango 0-20
    Args:
        nota (float): Nota a validar
    Returns:
        bool: True si es válida, False en caso contrario
    """
    return 0 <= nota <= 20