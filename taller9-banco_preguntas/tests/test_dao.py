"""
Pruebas unitarias para el DAO
"""

import unittest
import sys
import os
import tempfile
import shutil

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from entidad import Pregunta
from dao import PreguntaDAO


class TestPreguntaDAO(unittest.TestCase):
    """Pruebas para la clase PreguntaDAO"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear una base de datos temporal
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test.db')
        self.dao = PreguntaDAO(self.db_path)
        
        # Crear preguntas de prueba
        self.pregunta1 = Pregunta(
            id=1,
            pregunta="Pregunta 1",
            opcion_a="A1",
            opcion_b="B1",
            opcion_c="C1",
            opcion_d="D1",
            respuesta_correcta="A",
            dificultad="Fácil",
            tema="Tema1"
        )
        self.pregunta2 = Pregunta(
            id=2,
            pregunta="Pregunta 2",
            opcion_a="A2",
            opcion_b="B2",
            opcion_c="C2",
            opcion_d="D2",
            respuesta_correcta="B",
            dificultad="Media",
            tema="Tema2"
        )
        self.pregunta3 = Pregunta(
            id=3,
            pregunta="Pregunta 3",
            opcion_a="A3",
            opcion_b="B3",
            opcion_c="C3",
            opcion_d="D3",
            respuesta_correcta="C",
            dificultad="Difícil",
            tema="Tema1"
        )
    
    def tearDown(self):
        """Limpieza después de las pruebas"""
        shutil.rmtree(self.temp_dir)
    
    def test_crear_tabla(self):
        """Prueba la creación de la tabla"""
        self.dao.crear_tabla()
        # Verificar que la tabla existe
        with self.dao._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='preguntas'")
            result = cursor.fetchone()
            self.assertIsNotNone(result)
    
    def test_insertar(self):
        """Prueba la inserción de una pregunta"""
        id_insertado = self.dao.insertar(self.pregunta1)
        self.assertGreater(id_insertado, 0)
        
        # Verificar que se insertó correctamente
        pregunta = self.dao.obtener_por_id(id_insertado)
        self.assertIsNotNone(pregunta)
        self.assertEqual(pregunta.pregunta, "Pregunta 1")
    
    def test_insertar_muchas(self):
        """Prueba la inserción de múltiples preguntas"""
        preguntas = [self.pregunta1, self.pregunta2, self.pregunta3]
        insertadas = self.dao.insertar_muchas(preguntas)
        self.assertEqual(insertadas, 3)
        
        # Verificar que se insertaron todas
        todas = self.dao.obtener_todas()
        self.assertEqual(len(todas), 3)
    
    def test_obtener_todas(self):
        """Prueba la obtención de todas las preguntas"""
        self.dao.insertar_muchas([self.pregunta1, self.pregunta2, self.pregunta3])
        
        todas = self.dao.obtener_todas()
        self.assertEqual(len(todas), 3)
    
    def test_obtener_por_id(self):
        """Prueba la obtención de una pregunta por ID"""
        id_insertado = self.dao.insertar(self.pregunta1)
        
        pregunta = self.dao.obtener_por_id(id_insertado)
        self.assertIsNotNone(pregunta)
        self.assertEqual(pregunta.pregunta, "Pregunta 1")
        
        # Buscar ID inexistente
        pregunta = self.dao.obtener_por_id(999)
        self.assertIsNone(pregunta)
    
    def test_obtener_por_tema(self):
        """Prueba la obtención de preguntas por tema"""
        self.dao.insertar_muchas([self.pregunta1, self.pregunta2, self.pregunta3])
        
        preguntas_tema1 = self.dao.obtener_por_tema("Tema1")
        self.assertEqual(len(preguntas_tema1), 2)
        
        preguntas_tema2 = self.dao.obtener_por_tema("Tema2")
        self.assertEqual(len(preguntas_tema2), 1)
    
    def test_obtener_por_dificultad(self):
        """Prueba la obtención de preguntas por dificultad"""
        self.dao.insertar_muchas([self.pregunta1, self.pregunta2, self.pregunta3])
        
        facil = self.dao.obtener_por_dificultad("Fácil")
        self.assertEqual(len(facil), 1)
        
        media = self.dao.obtener_por_dificultad("Media")
        self.assertEqual(len(media), 1)
        
        dificil = self.dao.obtener_por_dificultad("Difícil")
        self.assertEqual(len(dificil), 1)
    
    def test_actualizar(self):
        """Prueba la actualización de una pregunta"""
        id_insertado = self.dao.insertar(self.pregunta1)
        
        # Actualizar la pregunta
        pregunta_actualizada = Pregunta(
            id=id_insertado,
            pregunta="Pregunta 1 Actualizada",
            opcion_a="A1",
            opcion_b="B1",
            opcion_c="C1",
            opcion_d="D1",
            respuesta_correcta="A",
            dificultad="Fácil",
            tema="Tema1"
        )
        
        resultado = self.dao.actualizar(pregunta_actualizada)
        self.assertTrue(resultado)
        
        # Verificar la actualización
        pregunta = self.dao.obtener_por_id(id_insertado)
        self.assertEqual(pregunta.pregunta, "Pregunta 1 Actualizada")
    
    def test_eliminar(self):
        """Prueba la eliminación de una pregunta"""
        id_insertado = self.dao.insertar(self.pregunta1)
        
        # Verificar que existe
        pregunta = self.dao.obtener_por_id(id_insertado)
        self.assertIsNotNone(pregunta)
        
        # Eliminar
        resultado = self.dao.eliminar(id_insertado)
        self.assertTrue(resultado)
        
        # Verificar que ya no existe
        pregunta = self.dao.obtener_por_id(id_insertado)
        self.assertIsNone(pregunta)
    
    def test_contar_preguntas(self):
        """Prueba el conteo de preguntas"""
        self.dao.insertar_muchas([self.pregunta1, self.pregunta2, self.pregunta3])
        
        total = self.dao.contar_preguntas()
        self.assertEqual(total, 3)
    
    def test_estadisticas_por_tema(self):
        """Prueba la obtención de estadísticas por tema"""
        self.dao.insertar_muchas([self.pregunta1, self.pregunta2, self.pregunta3])
        
        estadisticas = self.dao.estadisticas_por_tema()
        
        self.assertIn("Tema1", estadisticas)
        self.assertIn("Tema2", estadisticas)
        
        self.assertEqual(estadisticas["Tema1"]["total"], 2)
        self.assertEqual(estadisticas["Tema2"]["total"], 1)


if __name__ == '__main__':
    unittest.main()