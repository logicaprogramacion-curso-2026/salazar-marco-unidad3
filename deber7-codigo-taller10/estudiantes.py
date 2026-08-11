"""
Módulo para la gestión de estudiantes
"""

class GestionEstudiantes:
    def __init__(self):
        """Inicializa la lista de estudiantes"""
        self.estudiantes = []
    
    def agregar_estudiante(self, estudiante):
        """
        Agrega un nuevo estudiante a la lista
        Args:
            estudiante (dict): Diccionario con los datos del estudiante
        Returns:
            bool: True si se agregó correctamente, False en caso contrario
        """
        try:
            self.estudiantes.append(estudiante)
            return True
        except Exception:
            return False
    
    def buscar_estudiante(self, cedula):
        """
        Busca un estudiante por su cédula
        Args:
            cedula (str): Cédula del estudiante a buscar
        Returns:
            dict: Datos del estudiante si lo encuentra, None en caso contrario
        """
        for estudiante in self.estudiantes:
            if estudiante['cedula'] == cedula:
                return estudiante
        return None
    
    def verificar_existencia(self, cedula):
        """
        Verifica si existe un estudiante con la cédula dada
        Args:
            cedula (str): Cédula a verificar
        Returns:
            bool: True si existe, False en caso contrario
        """
        return self.buscar_estudiante(cedula) is not None
    
    def listar_estudiantes(self):
        """
        Retorna la lista completa de estudiantes
        Returns:
            list: Lista de estudiantes
        """
        return self.estudiantes
    
    def eliminar_estudiante(self, cedula):
        """
        Elimina un estudiante por su cédula
        Args:
            cedula (str): Cédula del estudiante a eliminar
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        estudiante = self.buscar_estudiante(cedula)
        if estudiante:
            self.estudiantes.remove(estudiante)
            return True
        return False