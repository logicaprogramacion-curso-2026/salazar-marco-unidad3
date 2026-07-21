# Taller 8 - Análisis de Datos de Aprendizaje

## Grupo 6

### Integrantes

- Marco Emilio Salazar Chiriboga
- Roberto Steven Banchón Muñoz
- Ruth Naomi Holguín Suárez
- Thiago Alexander Vera Macarlupo

---

# Descripción del proyecto

Este proyecto consiste en desarrollar una aplicación en Python para analizar datos históricos de evaluaciones académicas a partir de un archivo CSV. El sistema permitirá procesar la información, calcular estadísticas descriptivas, detectar patrones de rendimiento y generar reportes que faciliten la toma de decisiones por parte del docente.

---

# Objetivo general

Analizar datos históricos de evaluaciones para detectar patrones de aprendizaje, generar estadísticas y elaborar reportes que permitan identificar fortalezas, debilidades y posibles alertas tempranas en el rendimiento de los estudiantes.

---

# Objetivos específicos

- Leer y procesar archivos CSV con registros de evaluaciones.
- Validar y limpiar los datos antes de realizar el análisis.
- Calcular estadísticas generales como media, mediana y desviación estándar.
- Obtener estadísticas individuales por estudiante.
- Obtener estadísticas por pregunta.
- Identificar las preguntas con mayor índice de fallo.
- Detectar estudiantes con bajo rendimiento sostenido.
- Presentar los resultados mediante un menú interactivo en consola (CLI).
- Implementar, como extensión, gráficos utilizando Matplotlib.
- Implementar, como extensión, un resumen automático del análisis mediante un modelo de lenguaje (LLM).

---

# Tecnologías utilizadas

- Python 3
- Git
- GitHub
- CSV (módulo estándar de Python)
- Estadística descriptiva
- Matplotlib *(extensión opcional)*

---

# Arquitectura del proyecto

El proyecto se desarrolla siguiendo una arquitectura por capas para mejorar la organización, el mantenimiento y la escalabilidad del código.

## Capa 1: Carga y limpieza de datos

Responsabilidades:

- Leer archivos CSV.
- Validar registros.
- Limpiar datos incompletos o inconsistentes.

## Capa 2: Procesamiento y análisis

Responsabilidades:

- Calcular media.
- Calcular mediana.
- Calcular desviación estándar.
- Calcular estadísticas por estudiante.
- Calcular estadísticas por pregunta.
- Detectar patrones de rendimiento.
- Identificar estudiantes en riesgo.

## Capa 3: Interfaz de usuario (CLI)

Responsabilidades:

- Mostrar un menú interactivo.
- Permitir la ejecución de los diferentes reportes.
- Presentar los resultados al usuario.

---

# Estructura del proyecto

```
taller8_analisis_datos/
│
├── main.py
├── menu.py
├── README.md
│
├── datos/
│   └── evaluaciones.csv
│
├── carga/
│   └── lector_csv.py
│
├── estadisticas/
│   └── calculos.py
│
├── patrones/
│   └── analisis.py
│
├── reportes/
│   └── reporte.py
│
└── graficos/
    └── grafico.py
```

---

# Formato esperado del archivo CSV

El archivo deberá contener registros con la siguiente estructura:

| estudiante | pregunta | puntaje | fecha | tiempo |
|------------|----------|----------|------------|---------|
| Ana | P1 | 10 | 2026-06-01 | 45 |
| Luis | P2 | 6 | 2026-06-01 | 60 |
| Carla | P3 | 8 | 2026-06-02 | 39 |

**Descripción de los campos:**

- **estudiante:** Nombre del estudiante.
- **pregunta:** Identificador de la pregunta evaluada.
- **puntaje:** Calificación obtenida.
- **fecha:** Fecha de la evaluación.
- **tiempo:** Tiempo invertido para responder (en segundos o minutos, según el conjunto de datos).

---

# Funcionalidades del sistema

## Funcionalidades mínimas

- Cargar un archivo CSV.
- Validar y limpiar los datos.
- Calcular estadísticas generales.
- Mostrar estadísticas por estudiante.
- Mostrar estadísticas por pregunta.
- Identificar la pregunta con mayor índice de error.
- Detectar estudiantes con bajo rendimiento.
- Mostrar reportes desde un menú en consola (CLI).

## Funcionalidades adicionales (Extensiones)

- Generación de gráficos mediante Matplotlib.
- Exportación de reportes.
- Generación de reportes en formato HTML.
- Simulación de alertas para el docente.
- Generación automática de un resumen mediante un modelo de lenguaje (LLM).

---

# Flujo general del sistema

```
Archivo CSV
      │
      ▼
Carga de datos
      │
      ▼
Limpieza y validación
      │
      ▼
Cálculos estadísticos
      │
      ▼
Detección de patrones
      │
      ▼
Generación de reportes
      │
      ▼
Visualización de resultados
```

---

# Cómo ejecutar el proyecto

1. Clonar el repositorio.

```bash
git clone <URL_DEL_REPOSITORIO>
```

2. Ingresar al directorio del proyecto.

```bash
cd taller8_analisis_datos
```

3. Ejecutar el programa.

```bash
python main.py
```

---

# Control de versiones

El proyecto utiliza Git para el control de versiones y GitHub como plataforma para el trabajo colaborativo.

Flujo recomendado:

```bash
git pull
git status
git add .
git commit -m "Descripción del cambio"
git push
```

---

# Estado del proyecto

🚧 **En desarrollo**

Actualmente se encuentra implementada la estructura inicial del proyecto. Las siguientes etapas incluyen el desarrollo de los módulos de lectura de datos, procesamiento estadístico, detección de patrones y generación de reportes.

---

# Licencia

Proyecto académico desarrollado para fines educativos.