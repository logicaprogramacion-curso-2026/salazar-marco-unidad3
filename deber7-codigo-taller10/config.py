"""
Archivo de configuración del sistema
"""

class Configuracion:
    # Configuración de notas
    NOTA_MINIMA = 0
    NOTA_MAXIMA = 20
    NOTA_APROBACION = 14
    
    # Pesos para el cálculo del promedio
    PESO_PARCIAL1 = 0.3
    PESO_PARCIAL2 = 0.3
    PESO_EXAMEN = 0.4
    
    # Configuración de la interfaz
    MAXIMO_CARACTERES_NOMBRE = 100
    MAXIMO_CARACTERES_CARRERA = 50
    
    # Estados académicos
    ESTADO_APROBADO = "Aprobado"
    ESTADO_SUSPENSO = "Suspenso"
    ESTADO_REPROBADO = "Reprobado"
    
    @classmethod
    def obtener_estado(cls, promedio):
        """
        Determina el estado del estudiante según su promedio
        Args:
            promedio (float): Promedio del estudiante
        Returns:
            str: Estado del estudiante
        """
        if promedio >= cls.NOTA_APROBACION:
            return cls.ESTADO_APROBADO
        elif promedio >= 10:
            return cls.ESTADO_SUSPENSO
        else:
            return cls.ESTADO_REPROBADO