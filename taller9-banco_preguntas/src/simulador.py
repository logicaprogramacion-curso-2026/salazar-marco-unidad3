"""
Módulo que implementa el simulador de evaluación
"""

import random
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from entidad import Pregunta
from gestor import GestorPreguntas


class Simulador:
    """
    Simulador de evaluación de preguntas
    """
    
    def __init__(self):
        """Constructor del simulador"""
        self.gestor = GestorPreguntas()
        self.preguntas_seleccionadas = []
        self.respuestas_usuario = {}
        self.resultados = {
            'fecha': datetime.now().isoformat(),
            'total_preguntas': 0,
            'correctas': 0,
            'incorrectas': 0,
            'puntaje': 0.0,
            'detalle': []
        }
    
    def iniciar_simulacion(self, cantidad: int = 10):
        """
        Inicia la simulación de evaluación
        
        Args:
            cantidad (int): Número de preguntas a mostrar
        """
        # Obtener todas las preguntas de la BD
        todas = self.gestor.obtener_todas()
        
        if not todas:
            print("❌ No hay preguntas en la base de datos.")
            print("Por favor, cargue preguntas primero.")
            return
        
        if len(todas) < cantidad:
            print(f"⚠️ Solo hay {len(todas)} preguntas disponibles. Se usarán todas.")
            cantidad = len(todas)
        
        # Seleccionar preguntas aleatoriamente
        self.preguntas_seleccionadas = random.sample(todas, cantidad)
        self.respuestas_usuario = {}
        self.resultados = {
            'fecha': datetime.now().isoformat(),
            'total_preguntas': cantidad,
            'correctas': 0,
            'incorrectas': 0,
            'puntaje': 0.0,
            'detalle': []
        }
        
        print("\n" + "="*70)
        print(f"   🎯 SIMULADOR DE EVALUACIÓN - {cantidad} PREGUNTAS")
        print("="*70)
        print("Responda con la letra de la opción (A, B, C o D)")
        print("="*70)
        
        # Presentar preguntas
        for i, pregunta in enumerate(self.preguntas_seleccionadas, 1):
            print(f"\n📝 PREGUNTA {i}/{cantidad}")
            pregunta.mostrar_pregunta()
            
            respuesta = ""
            while respuesta not in ['A', 'B', 'C', 'D']:
                respuesta = input("Su respuesta (A/B/C/D): ").upper().strip()
                if respuesta not in ['A', 'B', 'C', 'D']:
                    print("❌ Respuesta inválida. Ingrese A, B, C o D.")
            
            self.respuestas_usuario[pregunta.id] = respuesta
            es_correcta = pregunta.validar_respuesta(respuesta)
            
            # Guardar detalle
            detalle = {
                'id': pregunta.id,
                'pregunta': pregunta.pregunta[:100] + '...' if len(pregunta.pregunta) > 100 else pregunta.pregunta,
                'tema': pregunta.tema,
                'dificultad': pregunta.dificultad,
                'respuesta_usuario': respuesta,
                'respuesta_correcta': pregunta.respuesta_correcta,
                'es_correcta': es_correcta
            }
            self.resultados['detalle'].append(detalle)
            
            if es_correcta:
                self.resultados['correctas'] += 1
                print("✅ ¡Correcto!")
            else:
                self.resultados['incorrectas'] += 1
                print(f"❌ Incorrecto. La respuesta correcta es: {pregunta.respuesta_correcta}")
        
        # Calcular puntaje
        total = self.resultados['total_preguntas']
        correctas = self.resultados['correctas']
        self.resultados['puntaje'] = (correctas / total) * 100 if total > 0 else 0
        
        # Mostrar resumen
        self._mostrar_resumen()
        
        # Guardar reporte
        self.generar_reporte()
    
    def _mostrar_resumen(self):
        """
        Muestra el resumen de la evaluación
        """
        total = self.resultados['total_preguntas']
        correctas = self.resultados['correctas']
        incorrectas = self.resultados['incorrectas']
        puntaje = self.resultados['puntaje']
        
        print("\n" + "="*70)
        print("   📊 RESUMEN DE EVALUACIÓN")
        print("="*70)
        print(f"Total preguntas: {total}")
        print(f"✅ Correctas: {correctas}")
        print(f"❌ Incorrectas: {incorrectas}")
        print(f"📈 Puntaje: {puntaje:.1f}%")
        
        if puntaje >= 80:
            print("🎉 ¡Excelente desempeño!")
        elif puntaje >= 60:
            print("👍 Buen desempeño, pero puede mejorar.")
        elif puntaje >= 40:
            print("📚 Necesita estudiar más.")
        else:
            print("⚠️ Es recomendable repasar los temas.")
        print("="*70)
    
    def generar_reporte(self):
        """
        Genera reportes en diferentes formatos
        """
        # Crear directorio de resultados
        os.makedirs('resultados', exist_ok=True)
        
        # Generar timestamp para los archivos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Reporte TXT
        self._generar_reporte_txt(timestamp)
        
        # Reporte CSV
        self._generar_reporte_csv(timestamp)
        
        # Reporte JSON
        self._generar_reporte_json(timestamp)
        
        print(f"\n✅ Reportes generados en la carpeta 'resultados/'")
    
    def _generar_reporte_txt(self, timestamp: str):
        """
        Genera el reporte en formato TXT
        """
        ruta = f"resultados/respuestas_usuario_{timestamp}.txt"
        
        with open(ruta, 'w', encoding='utf-8') as archivo:
            archivo.write("="*70 + "\n")
            archivo.write("   📝 INFORME DE RESPUESTAS DEL USUARIO\n")
            archivo.write("="*70 + "\n")
            archivo.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            archivo.write(f"Total preguntas: {self.resultados['total_preguntas']}\n")
            archivo.write(f"Correctas: {self.resultados['correctas']}\n")
            archivo.write(f"Incorrectas: {self.resultados['incorrectas']}\n")
            archivo.write(f"Puntaje: {self.resultados['puntaje']:.1f}%\n")
            archivo.write("\n" + "="*70 + "\n")
            archivo.write("   📋 DETALLE DE RESPUESTAS\n")
            archivo.write("="*70 + "\n\n")
            
            for detalle in self.resultados['detalle']:
                estado = "✅ CORRECTA" if detalle['es_correcta'] else "❌ INCORRECTA"
                archivo.write(f"Pregunta #{detalle['id']} - {detalle['tema']} ({detalle['dificultad']})\n")
                archivo.write(f"  Pregunta: {detalle['pregunta']}\n")
                archivo.write(f"  Su respuesta: {detalle['respuesta_usuario']}\n")
                archivo.write(f"  Correcta: {detalle['respuesta_correcta']}\n")
                archivo.write(f"  Estado: {estado}\n")
                archivo.write("-"*70 + "\n")
        
        print(f"✅ Reporte TXT: {ruta}")
    
    def _generar_reporte_csv(self, timestamp: str):
        """
        Genera el reporte en formato CSV
        """
        import csv
        
        ruta = f"resultados/estadisticas_{timestamp}.csv"
        
        with open(ruta, 'w', encoding='utf-8', newline='') as archivo:
            campos = ['Fecha', 'Total Preguntas', 'Correctas', 'Incorrectas', 'Puntaje %']
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            
            escritor.writerow({
                'Fecha': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'Total Preguntas': self.resultados['total_preguntas'],
                'Correctas': self.resultados['correctas'],
                'Incorrectas': self.resultados['incorrectas'],
                'Puntaje %': f"{self.resultados['puntaje']:.1f}"
            })
        
        print(f"✅ Reporte CSV: {ruta}")
    
    def _generar_reporte_json(self, timestamp: str):
        """
        Genera el reporte en formato JSON
        """
        ruta = f"resultados/reporte_{timestamp}.json"
        
        reporte = {
            'timestamp': datetime.now().isoformat(),
            'fecha_formateada': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'estadisticas': {
                'total_preguntas': self.resultados['total_preguntas'],
                'correctas': self.resultados['correctas'],
                'incorrectas': self.resultados['incorrectas'],
                'puntaje': self.resultados['puntaje']
            },
            'detalle': self.resultados['detalle'],
            'estadisticas_por_tema': self._calcular_estadisticas_por_tema(),
            'estadisticas_por_dificultad': self._calcular_estadisticas_por_dificultad()
        }
        
        with open(ruta, 'w', encoding='utf-8') as archivo:
            json.dump(reporte, archivo, ensure_ascii=False, indent=2)
        
        print(f"✅ Reporte JSON: {ruta}")
    
    def _calcular_estadisticas_por_tema(self) -> Dict[str, Any]:
        """
        Calcula estadísticas agrupadas por tema
        """
        stats = {}
        
        for detalle in self.resultados['detalle']:
            tema = detalle['tema']
            if tema not in stats:
                stats[tema] = {'total': 0, 'correctas': 0, 'incorrectas': 0}
            
            stats[tema]['total'] += 1
            if detalle['es_correcta']:
                stats[tema]['correctas'] += 1
            else:
                stats[tema]['incorrectas'] += 1
        
        # Calcular porcentajes
        for tema in stats:
            total = stats[tema]['total']
            stats[tema]['porcentaje'] = (stats[tema]['correctas'] / total * 100) if total > 0 else 0
        
        return stats
    
    def _calcular_estadisticas_por_dificultad(self) -> Dict[str, Any]:
        """
        Calcula estadísticas agrupadas por dificultad
        """
        stats = {}
        
        for detalle in self.resultados['detalle']:
            dificultad = detalle['dificultad']
            if dificultad not in stats:
                stats[dificultad] = {'total': 0, 'correctas': 0, 'incorrectas': 0}
            
            stats[dificultad]['total'] += 1
            if detalle['es_correcta']:
                stats[dificultad]['correctas'] += 1
            else:
                stats[dificultad]['incorrectas'] += 1
        
        # Calcular porcentajes
        for dificultad in stats:
            total = stats[dificultad]['total']
            stats[dificultad]['porcentaje'] = (stats[dificultad]['correctas'] / total * 100) if total > 0 else 0
        
        return stats