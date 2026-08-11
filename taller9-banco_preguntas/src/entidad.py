"""
Módulo que define la entidad Pregunta
"""

class Pregunta:
    """
    Clase que representa una pregunta de selección múltiple
    """
    
    def __init__(self, id=None, pregunta="", opcion_a="", opcion_b="", 
                 opcion_c="", opcion_d="", respuesta_correcta="", 
                 dificultad="", tema=""):
        """
        Constructor de la clase Pregunta
        
        Args:
            id (int): Identificador único de la pregunta
            pregunta (str): Enunciado de la pregunta
            opcion_a (str): Opción A
            opcion_b (str): Opción B
            opcion_c (str): Opción C
            opcion_d (str): Opción D
            respuesta_correcta (str): Letra de la respuesta correcta (A, B, C, D)
            dificultad (str): Nivel de dificultad (Fácil, Media, Difícil)
            tema (str): Tema al que pertenece la pregunta
        """
        self.id = id
        self.pregunta = pregunta
        self.opcion_a = opcion_a
        self.opcion_b = opcion_b
        self.opcion_c = opcion_c
        self.opcion_d = opcion_d
        self.respuesta_correcta = respuesta_correcta.upper() if respuesta_correcta else ""
        self.dificultad = dificultad
        self.tema = tema
    
    def __str__(self):
        """
        Representación en string de la pregunta
        """
        return f"ID: {self.id} | {self.pregunta} | {self.tema} | {self.dificultad}"
    
    def to_dict(self):
        """
        Convierte la pregunta a un diccionario
        
        Returns:
            dict: Diccionario con los atributos de la pregunta
        """
        return {
            'id': self.id,
            'pregunta': self.pregunta,
            'opcion_a': self.opcion_a,
            'opcion_b': self.opcion_b,
            'opcion_c': self.opcion_c,
            'opcion_d': self.opcion_d,
            'respuesta_correcta': self.respuesta_correcta,
            'dificultad': self.dificultad,
            'tema': self.tema
        }
    
    @classmethod
    def from_dict(cls, datos):
        """
        Crea una pregunta a partir de un diccionario
        
        Args:
            datos (dict): Diccionario con los datos de la pregunta
        
        Returns:
            Pregunta: Objeto Pregunta creado a partir del diccionario
        """
        # Manejar diferentes formatos de JSON
        if isinstance(datos.get('opciones'), dict):
            opciones = datos['opciones']
            return cls(
                id=datos.get('id'),
                pregunta=datos.get('pregunta', ''),
                opcion_a=opciones.get('A', ''),
                opcion_b=opciones.get('B', ''),
                opcion_c=opciones.get('C', ''),
                opcion_d=opciones.get('D', ''),
                respuesta_correcta=datos.get('respuesta_correcta', ''),
                dificultad=datos.get('dificultad', ''),
                tema=datos.get('tema', '')
            )
        else:
            return cls(
                id=datos.get('id'),
                pregunta=datos.get('pregunta', ''),
                opcion_a=datos.get('opcion_a', ''),
                opcion_b=datos.get('opcion_b', ''),
                opcion_c=datos.get('opcion_c', ''),
                opcion_d=datos.get('opcion_d', ''),
                respuesta_correcta=datos.get('respuesta_correcta', ''),
                dificultad=datos.get('dificultad', ''),
                tema=datos.get('tema', '')
            )
    
    def mostrar_pregunta(self):
        """
        Muestra la pregunta en formato legible
        """
        print(f"\n{'='*60}")
        print(f"PREGUNTA #{self.id} - {self.tema} ({self.dificultad})")
        print(f"{'='*60}")
        print(f"{self.pregunta}\n")
        print(f"A) {self.opcion_a}")
        print(f"B) {self.opcion_b}")
        print(f"C) {self.opcion_c}")
        print(f"D) {self.opcion_d}")
        print(f"{'='*60}")
    
    def validar_respuesta(self, respuesta):
        """
        Valida si la respuesta es correcta
        
        Args:
            respuesta (str): Respuesta del usuario
        
        Returns:
            bool: True si es correcta, False en caso contrario
        """
        return respuesta.upper() == self.respuesta_correcta