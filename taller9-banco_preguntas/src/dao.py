"""
Módulo que implementa el DAO para la base de datos SQLite
"""

import sqlite3
import os
from typing import List, Optional, Dict, Any
from entidad import Pregunta


class PreguntaDAO:
    """
    Data Access Object para la entidad Pregunta
    """
    
    def __init__(self, db_path="database/preguntas.db"):
        """
        Constructor del DAO
        
        Args:
            db_path (str): Ruta al archivo de la base de datos
        """
        self.db_path = db_path
        self._crear_directorio()
        self.crear_tabla()
    
    def _crear_directorio(self):
        """
        Crea el directorio de la base de datos si no existe
        """
        directorio = os.path.dirname(self.db_path)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
    
    def _get_connection(self):
        """
        Obtiene una conexión a la base de datos
        
        Returns:
            sqlite3.Connection: Conexión a la base de datos
        """
        return sqlite3.connect(self.db_path)
    
    def crear_tabla(self):
        """
        Crea la tabla de preguntas en la base de datos
        """
        query = """
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT NOT NULL,
            opcion_a TEXT NOT NULL,
            opcion_b TEXT NOT NULL,
            opcion_c TEXT NOT NULL,
            opcion_d TEXT NOT NULL,
            respuesta_correcta TEXT NOT NULL,
            dificultad TEXT NOT NULL,
            tema TEXT NOT NULL
        )
        """
        
        try:
            with self._get_connection() as conn:
                conn.execute(query)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")
    
    def insertar(self, pregunta: Pregunta) -> int:
        """
        Inserta una pregunta en la base de datos
        
        Args:
            pregunta (Pregunta): Objeto pregunta a insertar
        
        Returns:
            int: ID de la pregunta insertada
        """
        query = """
        INSERT INTO preguntas 
        (pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, dificultad, tema)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    pregunta.pregunta,
                    pregunta.opcion_a,
                    pregunta.opcion_b,
                    pregunta.opcion_c,
                    pregunta.opcion_d,
                    pregunta.respuesta_correcta,
                    pregunta.dificultad,
                    pregunta.tema
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al insertar pregunta: {e}")
            return -1
    
    def insertar_muchas(self, preguntas: List[Pregunta]) -> int:
        """
        Inserta múltiples preguntas en la base de datos
        
        Args:
            preguntas (List[Pregunta]): Lista de preguntas a insertar
        
        Returns:
            int: Número de preguntas insertadas
        """
        query = """
        INSERT INTO preguntas 
        (pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, dificultad, tema)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        datos = [
            (
                p.pregunta,
                p.opcion_a,
                p.opcion_b,
                p.opcion_c,
                p.opcion_d,
                p.respuesta_correcta,
                p.dificultad,
                p.tema
            )
            for p in preguntas
        ]
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(query, datos)
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Error al insertar preguntas: {e}")
            return 0
    
    def obtener_todas(self) -> List[Pregunta]:
        """
        Obtiene todas las preguntas de la base de datos
        
        Returns:
            List[Pregunta]: Lista de todas las preguntas
        """
        query = "SELECT * FROM preguntas ORDER BY id"
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                return self._rows_to_preguntas(rows)
        except sqlite3.Error as e:
            print(f"Error al obtener preguntas: {e}")
            return []
    
    def obtener_por_id(self, id: int) -> Optional[Pregunta]:
        """
        Obtiene una pregunta por su ID
        
        Args:
            id (int): ID de la pregunta
        
        Returns:
            Optional[Pregunta]: Pregunta encontrada o None
        """
        query = "SELECT * FROM preguntas WHERE id = ?"
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id,))
                row = cursor.fetchone()
                if row:
                    return self._row_to_pregunta(row)
                return None
        except sqlite3.Error as e:
            print(f"Error al obtener pregunta por ID: {e}")
            return None
    
    def obtener_por_tema(self, tema: str) -> List[Pregunta]:
        """
        Obtiene preguntas por tema
        
        Args:
            tema (str): Tema a buscar
        
        Returns:
            List[Pregunta]: Lista de preguntas del tema
        """
        query = "SELECT * FROM preguntas WHERE tema = ?"
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (tema,))
                rows = cursor.fetchall()
                return self._rows_to_preguntas(rows)
        except sqlite3.Error as e:
            print(f"Error al obtener preguntas por tema: {e}")
            return []
    
    def obtener_por_dificultad(self, dificultad: str) -> List[Pregunta]:
        """
        Obtiene preguntas por dificultad
        
        Args:
            dificultad (str): Dificultad a buscar
        
        Returns:
            List[Pregunta]: Lista de preguntas de la dificultad
        """
        query = "SELECT * FROM preguntas WHERE dificultad = ?"
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (dificultad,))
                rows = cursor.fetchall()
                return self._rows_to_preguntas(rows)
        except sqlite3.Error as e:
            print(f"Error al obtener preguntas por dificultad: {e}")
            return []
    
    def actualizar(self, pregunta: Pregunta) -> bool:
        """
        Actualiza una pregunta en la base de datos
        
        Args:
            pregunta (Pregunta): Pregunta con los datos actualizados
        
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        query = """
        UPDATE preguntas 
        SET pregunta = ?, opcion_a = ?, opcion_b = ?, opcion_c = ?, opcion_d = ?,
            respuesta_correcta = ?, dificultad = ?, tema = ?
        WHERE id = ?
        """
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    pregunta.pregunta,
                    pregunta.opcion_a,
                    pregunta.opcion_b,
                    pregunta.opcion_c,
                    pregunta.opcion_d,
                    pregunta.respuesta_correcta,
                    pregunta.dificultad,
                    pregunta.tema,
                    pregunta.id
                ))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar pregunta: {e}")
            return False
    
    def eliminar(self, id: int) -> bool:
        """
        Elimina una pregunta por su ID
        
        Args:
            id (int): ID de la pregunta a eliminar
        
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        query = "DELETE FROM preguntas WHERE id = ?"
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar pregunta: {e}")
            return False
    
    def contar_preguntas(self) -> int:
        """
        Cuenta el total de preguntas en la base de datos
        
        Returns:
            int: Número total de preguntas
        """
        query = "SELECT COUNT(*) FROM preguntas"
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error al contar preguntas: {e}")
            return 0
    
    def estadisticas_por_tema(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas agrupadas por tema
        
        Returns:
            Dict[str, Any]: Diccionario con estadísticas por tema
        """
        query = """
        SELECT 
            tema,
            COUNT(*) as total,
            SUM(CASE WHEN dificultad = 'Fácil' THEN 1 ELSE 0 END) as facil,
            SUM(CASE WHEN dificultad = 'Media' THEN 1 ELSE 0 END) as media,
            SUM(CASE WHEN dificultad = 'Difícil' THEN 1 ELSE 0 END) as dificil
        FROM preguntas
        GROUP BY tema
        ORDER BY tema
        """
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                
                estadisticas = {}
                for row in rows:
                    estadisticas[row[0]] = {
                        'total': row[1],
                        'facil': row[2],
                        'media': row[3],
                        'dificil': row[4]
                    }
                return estadisticas
        except sqlite3.Error as e:
            print(f"Error al obtener estadísticas: {e}")
            return {}
    
    def _row_to_pregunta(self, row: tuple) -> Pregunta:
        """
        Convierte una fila de la base de datos a un objeto Pregunta
        
        Args:
            row (tuple): Fila de la base de datos
        
        Returns:
            Pregunta: Objeto Pregunta creado
        """
        return Pregunta(
            id=row[0],
            pregunta=row[1],
            opcion_a=row[2],
            opcion_b=row[3],
            opcion_c=row[4],
            opcion_d=row[5],
            respuesta_correcta=row[6],
            dificultad=row[7],
            tema=row[8]
        )
    
    def _rows_to_preguntas(self, rows: List[tuple]) ->