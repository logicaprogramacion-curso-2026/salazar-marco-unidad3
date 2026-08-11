"""
Pruebas unitarias para la entidad Pregunta
"""

import unittest
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from entidad import Pregunta


class TestPregunta(unittest.TestCase):
    """Pruebas para la clase Pregunta"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.pregunta = Pregunta(
            id=1,
            pregunta="¿Cuál es la capital de Ecuador?",
            opcion_a="Quito",
            opcion_b="Guayaquil",
            opcion_c="Cuenca",
            opcion_d="Ambato",
            respuesta_correcta="A",
            dificultad="Fácil",
            tema="Geografía"
        )
    
   