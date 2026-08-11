"""
Módulo que implementa la lógica de negocio del sistema
"""

import csv
import json
import os
from typing import List, Optional
from entidad import Pregunta
from dao import PreguntaDAO


class GestorPreguntas:
    """
    Gestor que maneja la lógica de negocio del banco de preguntas
    """
    
    def __init__(self):
        """Constructor del gestor"""
        self.dao = PreguntaDAO()
    
    def cargar_desde_txt(self, ruta: str) -> List[Pregunta]:
        """
        Carga preguntas desde un archivo TXT
        
        Args:
            ruta (str): Ruta al archivo TXT
        
        Returns:
            List[Pregunta]: Lista de preguntas cargadas
        """
        preguntas = []
        
        if not os.path.exists(ruta):
            print(f"Error: El archivo {ruta} no existe.")
            return []
        
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea or linea.startswith('=') or linea.startswith('-'):
                        continue
                    
                    partes = linea.split('|')
                    if len(partes) >= 9:
                        try:
                            id_pregunta = int(partes[0].strip())
                            pregunta = partes[1].strip()
                            opcion_a = partes[2].strip()
                            opcion_b = partes[3].strip()
                            opcion_c = partes[4].strip()
                            opcion_d = partes[5].strip()
                            respuesta = partes[6].strip()
                            dificultad = partes[7].strip()
                            tema = partes[8].strip()
                            
                            p = Pregunta(
                                id=id_pregunta,
                                pregunta=pregunta,
                                opcion_a=opcion_a,
                                opcion_b=opcion_b,
                                opcion_c=opcion_c,
                                opcion_d=opcion_d,
                                respuesta_correcta=respuesta,
                                dificultad=dificultad,
                                tema=tema
                            )
                            preguntas.append(p)
                        except (ValueError, IndexError) as e:
                            print(f"Error al procesar línea: {linea[:50]}... - {e}")
                            continue
            
            print(f"✅ Cargadas {len(preguntas)} preguntas desde {ruta}")
            return preguntas
            
        except Exception as e:
            print(f"Error al cargar archivo TXT: {e}")
            return []
    
    def cargar_desde_csv(self, ruta: str) -> List[Pregunta]:
        """
        Carga preguntas desde un archivo CSV
        
        Args:
            ruta (str): Ruta al archivo CSV
        
        Returns:
            List[Pregunta]: Lista de preguntas cargadas
        """
        preguntas = []
        
        if not os.path.exists(ruta):
            print(f"Error: El archivo {ruta} no existe.")
            return []
        
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                
                for fila in lector:
                    try:
                        p = Pregunta(
                            id=int(fila.get('ID', 0)),
                            pregunta=fila.get('Pregunta', ''),
                            opcion_a=fila.get('OpcionA', ''),
                            opcion_b=fila.get('OpcionB', ''),
                            opcion_c=fila.get('OpcionC', ''),
                            opcion_d=fila.get('OpcionD', ''),
                            respuesta_correcta=fila.get('RespuestaCorrecta', ''),
                            dificultad=fila.get('Dificultad', ''),
                            tema=fila.get('Tema', '')
                        )
                        preguntas.append(p)
                    except (ValueError, KeyError) as e:
                        print(f"Error al procesar fila: {e}")
                        continue
            
            print(f"✅ Cargadas {len(preguntas)} preguntas desde {ruta}")
            return preguntas
            
        except Exception as e:
            print(f"Error al cargar archivo CSV: {e}")
            return []
    
    def cargar_desde_json(self, ruta: str) -> List[Pregunta]:
        """
        Carga preguntas desde un archivo JSON
        
        Args:
            ruta (str): Ruta al archivo JSON
        
        Returns:
            List[Pregunta]: Lista de preguntas cargadas
        """
        preguntas = []
        
        if not os.path.exists(ruta):
            print(f"Error: El archivo {ruta} no existe.")
            return []
        
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                
                # Manejar diferentes formatos de JSON
                if isinstance(datos, list):
                    items = datos
                elif isinstance(datos, dict):
                    if 'preguntas' in datos:
                        items = datos['preguntas']
                    elif 'cuestionario' in datos and 'preguntas' in datos['cuestionario']:
                        items = datos['cuestionario']['preguntas']
                    else:
                        items = [datos]
                else:
                    items = []
                
                for item in items:
                    try:
                        p = Pregunta.from_dict(item)
                        if p.pregunta:  # Solo agregar si tiene contenido
                            preguntas.append(p)
                    except Exception as e:
                        print(f"Error al procesar item: {e}")
                        continue
            
            print(f"✅ Cargadas {len(preguntas)} preguntas desde {ruta}")
            return preguntas
            
        except Exception as e:
            print(f"Error al cargar archivo JSON: {e}")
            return []
    
    def guardar_en_base_datos(self, preguntas: List[Pregunta]) -> int:
        """
        Guarda las preguntas en la base de datos
        
        Args:
            preguntas (List[Pregunta]): Lista de preguntas a guardar
        
        Returns:
            int: Número de preguntas guardadas
        """
        if not preguntas:
            print("No hay preguntas para guardar.")
            return 0
        
        # Verificar si ya hay preguntas en la BD
        existentes = self.dao.contar_preguntas()
        if existentes > 0:
            respuesta = input(f"Ya hay {existentes} preguntas en la base de datos. ¿Desea eliminar y reemplazar? (s/n): ")
            if respuesta.lower() != 's':
                return 0
            # Limpiar la tabla
            with self.dao._get_connection() as conn:
                conn.execute("DELETE FROM preguntas")
                conn.commit()
        
        return self.dao.insertar_muchas(preguntas)
    
    def exportar_a_txt(self, ruta: str, preguntas: Optional[List[Pregunta]] = None):
        """
        Exporta preguntas a un archivo TXT
        
        Args:
            ruta (str): Ruta del archivo de salida
            preguntas (Optional[List[Pregunta]]): Lista de preguntas a exportar (None = todas)
        """
        if preguntas is None:
            preguntas = self.dao.obtener_todas()
        
        if not preguntas:
            print("No hay preguntas para exportar.")
            return
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        
        try:
            with open(ruta, 'w', encoding='utf-8') as archivo:
                archivo.write("ID|Pregunta|Opción A|Opción B|Opción C|Opción D|Respuesta Correcta|Dificultad|Tema\n")
                for p in preguntas:
                    archivo.write(f"{p.id}|{p.pregunta}|{p.opcion_a}|{p.opcion_b}|{p.opcion_c}|{p.opcion_d}|{p.respuesta_correcta}|{p.dificultad}|{p.tema}\n")
            
            print(f"✅ Exportadas {len(preguntas)} preguntas a {ruta}")
        except Exception as e:
            print(f"Error al exportar a TXT: {e}")
    
    def exportar_a_csv(self, ruta: str, preguntas: Optional[List[Pregunta]] = None):
        """
        Exporta preguntas a un archivo CSV
        
        Args:
            ruta (str): Ruta del archivo de salida
            preguntas (Optional[List[Pregunta]]): Lista de preguntas a exportar (None = todas)
        """
        if preguntas is None:
            preguntas = self.dao.obtener_todas()
        
        if not preguntas:
            print("No hay preguntas para exportar.")
            return
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        
        try:
            with open(ruta, 'w', encoding='utf-8', newline='') as archivo:
                campos = ['ID', 'Pregunta', 'OpcionA', 'OpcionB', 'OpcionC', 'OpcionD', 
                         'RespuestaCorrecta', 'Dificultad', 'Tema']
                escritor = csv.DictWriter(archivo, fieldnames=campos)
                escritor.writeheader()
                
                for p in preguntas:
                    escritor.writerow({
                        'ID': p.id,
                        'Pregunta': p.pregunta,
                        'OpcionA': p.opcion_a,
                        'OpcionB': p.opcion_b,
                        'OpcionC': p.opcion_c,
                        'OpcionD': p.opcion_d,
                        'RespuestaCorrecta': p.respuesta_correcta,
                        'Dificultad': p.dificultad,
                        'Tema': p.tema
                    })
            
            print(f"✅ Exportadas {len(preguntas)} preguntas a {ruta}")
        except Exception as e:
            print(f"Error al exportar a CSV: {e}")
    
    def exportar_a_json(self, ruta: str, preguntas: Optional[List[Pregunta]] = None):
        """
        Exporta preguntas a un archivo JSON
        
        Args:
            ruta (str): Ruta del archivo de salida
            preguntas (Optional[List[Pregunta]]): Lista de preguntas a exportar (None = todas)
        """
        if preguntas is None:
            preguntas = self.dao.obtener_todas()
        
        if not preguntas:
            print("No hay preguntas para exportar.")
            return
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        
        try:
            datos = {
                'total': len(preguntas),
                'preguntas': [p.to_dict() for p in preguntas]
            }
            
            with open(ruta, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            
            print(f"✅ Exportadas {len(preguntas)} preguntas a {ruta}")
        except Exception as e:
            print(f"Error al exportar a JSON: {e}")
    
    def obtener_todas(self) -> List[Pregunta]:
        """
        Obtiene todas las preguntas de la base de datos
        
        Returns:
            List[Pregunta]: Lista de preguntas
        """
        return self.dao.obtener_todas()
    
    def contar_preguntas(self) -> int:
        """
        Cuenta el total de preguntas en la base de datos
        
        Returns:
            int: Número total de preguntas
        """
        return self.dao.contar_preguntas()
    
    def estadisticas_por_tema(self) -> dict:
        """
        Obtiene estadísticas por tema
        
        Returns:
            dict: Estadísticas por tema
        """
        return self.dao.estadisticas_por_tema()