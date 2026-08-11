"""
Módulo para la gestión de notas de estudiantes
"""

class GestionNotas:
    def __init__(self):
        """Inicializa la lista de notas"""
        self.notas = []
    
    def agregar_notas(self, notas):
        """
        Agrega notas para un estudiante
        Args:
            notas (dict): Diccionario con las notas del estudiante
        Returns:
            bool: True si se agregó correctamente, False en caso contrario
        """
        try:
            self.notas.append(notas)
            return True
        except Exception:
            return False
    
    def consultar_notas(self, cedula):
        """
        Consulta todas las notas de un estudiante
        Args:
            cedula (str): Cédula del estudiante
        Returns:
            list: Lista de notas del estudiante
        """
        notas_estudiante = []
        for nota in self.notas:
            if nota['cedula'] == cedula:
                notas_estudiante.append(nota)
        return notas_estudiante
    
    def calcular_promedio_general(self, cedula):
        """
        Calcula el promedio general de un estudiante
        Args:
            cedula (str): Cédula del estudiante
        Returns:
            float: Promedio general del estudiante
        """
        notas = self.consultar_notas(cedula)
        if not notas:
            return 0.0
        
        total_promedios = 0
        for nota in notas:
            promedio = (nota['parcial1'] * 0.3 + 
                       nota['parcial2'] * 0.3 + 
                       nota['examen'] * 0.4)
            total_promedios += promedio
        
        return total_promedios / len(notas)
    
    def obtener_mejores_promedios(self, n=5):
        """
        Obtiene los N mejores promedios
        Args:
            n (int): Número de mejores promedios a obtener
        Returns:
            list: Lista de estudiantes con sus mejores promedios
        """
        promedios = []
        cedulas_procesadas = set()
        
        for nota in self.notas:
            cedula = nota['cedula']
            if cedula not in cedulas_procesadas:
                promedio = self.calcular_promedio_general(cedula)
                promedios.append({
                    'cedula': cedula,
                    'promedio': promedio
                })
                cedulas_procesadas.add(cedula)
        
        promedios.sort(key=lambda x: x['promedio'], reverse=True)
        return promedios[:n]