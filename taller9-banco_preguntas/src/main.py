"""
Módulo principal del sistema de banco de preguntas
"""

import os
import sys
from gestor import GestorPreguntas
from simulador import Simulador


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu():
    """Muestra el menú principal del sistema"""
    print("\n" + "="*60)
    print("   📚 SISTEMA DE BANCO DE PREGUNTAS")
    print("="*60)
    print("1. Cargar preguntas desde archivo")
    print("2. Ver todas las preguntas")
    print("3. Ver estadísticas de preguntas")
    print("4. Iniciar simulación de evaluación")
    print("5. Exportar datos a archivos")
    print("6. Ver reportes generados")
    print("7. Salir")
    print("="*60)


def menu_cargar_archivos(gestor):
    """
    Menú para cargar preguntas desde archivos
    
    Args:
        gestor (GestorPreguntas): Instancia del gestor
    """
    print("\n" + "="*60)
    print("   📂 CARGAR PREGUNTAS DESDE ARCHIVO")
    print("="*60)
    print("1. Cargar desde TXT (preguntas.txt)")
    print("2. Cargar desde CSV (preguntas.csv)")
    print("3. Cargar desde JSON (preguntas.json)")
    print("4. Volver al menú principal")
    print("="*60)
    
    opcion = input("Seleccione una opción: ").strip()
    
    preguntas = []
    
    if opcion == '1':
        preguntas = gestor.cargar_desde_txt('preguntas.txt')
    elif opcion == '2':
        preguntas = gestor.cargar_desde_csv('preguntas.csv')
    elif opcion == '3':
        preguntas = gestor.cargar_desde_json('preguntas.json')
    elif opcion == '4':
        return
    else:
        print("❌ Opción inválida.")
        return
    
    if preguntas:
        # Guardar en base de datos
        guardadas = gestor.guardar_en_base_datos(preguntas)
        print(f"\n✅ {guardadas} preguntas guardadas en la base de datos.")


def ver_todas_preguntas(gestor):
    """
    Muestra todas las preguntas de la base de datos
    
    Args:
        gestor (GestorPreguntas): Instancia del gestor
    """
    preguntas = gestor.obtener_todas()
    
    if not preguntas:
        print("\n❌ No hay preguntas en la base de datos.")
        print("Por favor, cargue preguntas primero.")
        return
    
    print("\n" + "="*60)
    print(f"   📋 LISTADO DE PREGUNTAS ({len(preguntas)})")
    print("="*60)
    
    for p in preguntas:
        print(f"\nID: {p.id}")
        print(f"Pregunta: {p.pregunta}")
        print(f"Opciones: A) {p.opcion_a}  B) {p.opcion_b}  C) {p.opcion_c}  D) {p.opcion_d}")
        print(f"Respuesta: {p.respuesta_correcta} | Dificultad: {p.dificultad} | Tema: {p.tema}")
        print("-"*60)


def ver_estadisticas(gestor):
    """
    Muestra estadísticas de las preguntas
    
    Args:
        gestor (GestorPreguntas): Instancia del gestor
    """
    total = gestor.contar_preguntas()
    
    if total == 0:
        print("\n❌ No hay preguntas en la base de datos.")
        print("Por favor, cargue preguntas primero.")
        return
    
    estadisticas = gestor.estadisticas_por_tema()
    
    print("\n" + "="*60)
    print(f"   📊 ESTADÍSTICAS DE PREGUNTAS (Total: {total})")
    print("="*60)
    
    print("\n📊 Por Tema:")
    print("-"*60)
    print(f"{'Tema':<25} {'Total':<8} {'Fácil':<8} {'Media':<8} {'Difícil':<8}")
    print("-"*60)
    
    for tema, stats in estadisticas.items():
        print(f"{tema:<25} {stats['total']:<8} {stats['facil']:<8} {stats['media']:<8} {stats['dificil']:<8}")
    
    # Estadísticas por dificultad
    print("\n📊 Por Dificultad:")
    print("-"*60)
    
    facil = sum(stats['facil'] for stats in estadisticas.values())
    media = sum(stats['media'] for stats in estadisticas.values())
    dificil = sum(stats['dificil'] for stats in estadisticas.values())
    
    print(f"Fácil: {facil} ({(facil/total*100):.1f}%)")
    print(f"Media: {media} ({(media/total*100):.1f}%)")
    print(f"Difícil: {dificil} ({(dificil/total*100):.1f}%)")


def menu_exportar(gestor):
    """
    Menú para exportar datos
    
    Args:
        gestor (GestorPreguntas): Instancia del gestor
    """
    print("\n" + "="*60)
    print("   💾 EXPORTAR DATOS")
    print("="*60)
    print("1. Exportar a TXT")
    print("2. Exportar a CSV")
    print("3. Exportar a JSON")
    print("4. Volver al menú principal")
    print("="*60)
    
    opcion = input("Seleccione una opción: ").strip()
    
    if opcion == '1':
        gestor.exportar_a_txt('resultados/preguntas_exportadas.txt')
    elif opcion == '2':
        gestor.exportar_a_csv('resultados/preguntas_exportadas.csv')
    elif opcion == '3':
        gestor.exportar_a_json('resultados/preguntas_exportadas.json')
    elif opcion == '4':
        return
    else:
        print("❌ Opción inválida.")


def ver_reportes():
    """Muestra los reportes generados en la carpeta resultados"""
    import glob
    
    reportes = glob.glob('resultados/*.*')
    
    if not reportes:
        print("\n❌ No hay reportes generados.")
        print("Realice una simulación primero.")
        return
    
    print("\n" + "="*60)
    print("   📄 REPORTES GENERADOS")
    print("="*60)
    
    for reporte in reportes:
        nombre = os.path.basename(reporte)
        tamaño = os.path.getsize(reporte)
        print(f"📄 {nombre} ({tamaño} bytes)")
    
    # Mostrar el último reporte
    try:
        ultimo = max(reportes, key=os.path.getctime)
        print(f"\n📋 Último reporte: {os.path.basename(ultimo)}")
        
        if ultimo.endswith('.txt'):
            with open(ultimo, 'r', encoding='utf-8') as archivo:
                print("\n" + "="*60)
                print("   CONTENIDO DEL ÚLTIMO REPORTE")
                print("="*60)
                print(archivo.read())
        elif ultimo.endswith('.json'):
            import json
            with open(ultimo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                print(f"\n📊 Resumen:")
                print(f"  Total preguntas: {datos['estadisticas']['total_preguntas']}")
                print(f"  Correctas: {datos['estadisticas']['correctas']}")
                print(f"  Puntaje: {datos['estadisticas']['puntaje']:.1f}%")
    except Exception as e:
        print(f"\n⚠️ Error al leer el reporte: {e}")


def main():
    """Función principal del programa"""
    gestor = GestorPreguntas()
    simulador = Simulador()
    
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '1':
            menu_cargar_archivos(gestor)
            input("\nPresione Enter para continuar...")
        elif opcion == '2':
            ver_todas_preguntas(gestor)
            input("\nPresione Enter para continuar...")
        elif opcion == '3':
            ver_estadisticas(gestor)
            input("\nPresione Enter para continuar...")
        elif opcion == '4':
            cantidad = input("\n¿Cuántas preguntas desea en la simulación? (por defecto 10): ").strip()
            cantidad = int(cantidad) if cantidad.isdigit() else 10
            simulador.iniciar_simulacion(cantidad)
            input("\nPresione Enter para continuar...")
        elif opcion == '5':
            menu_exportar(gestor)
            input("\nPresione Enter para continuar...")
        elif opcion == '6':
            ver_reportes()
            input("\nPresione Enter para continuar...")
        elif opcion == '7':
            print("\n👋 ¡Gracias por usar el sistema!")
            break
        else:
            print("\n❌ Opción inválida. Intente de nuevo.")
            input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)