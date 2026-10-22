
# Academic Lakehouse Analytics
### Proyecto Final - Ingeniería de Datos con Databricks

## 1. Descripción del proyecto

Academic Lakehouse Analytics es una solución de ingeniería de datos orientada al análisis del rendimiento académico de estudiantes.

Implementa una arquitectura Lakehouse utilizando Databricks, Apache Spark, Delta Lake y Amazon S3, siguiendo el patrón Medallion (Bronze, Silver y Gold).

El proyecto permite analizar:
- Rendimiento académico por facultad.
- Rendimiento académico por curso.
- Promedio de notas de los estudiantes.
- Porcentaje de aprobación y desaprobación.
- Porcentaje promedio de asistencia.
- Identificación de estudiantes con riesgo académico.

Los datos utilizados son sintéticos y se emplean exclusivamente con fines educativos.

## 2. Arquitectura de la solución

```text
       AMAZON AWS S3
 academic-lakehouse-raw-2026
              |
              v
    IAM ROLE + UNITY CATALOG
              |
              v
      DATABRICKS SOBRE AWS
         PYSPARK + DELTA LAKE
              |
              v
        BRONZE LAYER
    Ingesta de datos originales
       alumnos / cursos / notas
              |
              v
        SILVER LAYER
    Limpieza y transformación
    Tipificación y validaciones
              |
              v
         GOLD LAYER
    Indicadores y agregaciones
              |
              v
      ANALÍTICA ACADÉMICA
    Consultas SQL y visualización
```

La automatización del despliegue y ejecución se realiza mediante GitHub Actions y Databricks CLI.

## 3. Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Amazon S3 | Almacenamiento de archivos originales CSV |
| AWS IAM Role | Autorización de acceso a S3 |
| Databricks | Plataforma de procesamiento de datos |
| Unity Catalog | Gobierno y acceso a los datos |
| Apache Spark / PySpark | Transformaciones distribuidas |
| Delta Lake | Persistencia de tablas analíticas |
| Databricks Workflows | Orquestación del ETL |
| Databricks Serverless | Ejecución sin clúster dedicado |
| GitHub | Control de versiones |
| GitHub Actions | Automatización CI/CD |
| Databricks CLI | Despliegue y ejecución remota |

## 4. Fuentes de datos

Los archivos CSV se encuentran en Amazon S3:

`s3://academic-lakehouse-raw-2026/raw/`

| Archivo | Descripción | Registros iniciales |
|---|---|---:|
| alumnos.csv | Información académica de estudiantes | 100 |
| cursos.csv | Catálogo de cursos | 6 |
| notas.csv | Evaluaciones y asistencia | 300 |

La lectura de los datos originales se realiza directamente desde S3 utilizando una credencial de almacenamiento de Unity Catalog asociada a un rol de AWS IAM.

No se utiliza DBFS ni Volumes como origen de los archivos originales.

## 5. Arquitectura Medallion

### Bronze

Notebook: `proceso/01_bronze.py`

Responsabilidades:
- Leer archivos CSV desde Amazon S3.
- Aplicar inferencia de esquema.
- Registrar los datos originales en tablas Delta.
- Mantener una capa inicial para el procesamiento posterior.

Tablas:
- `workspace.bronze.alumnos`
- `workspace.bronze.cursos`
- `workspace.bronze.notas`

### Silver

Notebook: `proceso/02_silver.py`

Responsabilidades:
- Procesar información proveniente de Bronze.
- Aplicar conversiones y transformaciones.
- Preparar información académica consistente.
- Calcular el estado académico de las evaluaciones.

Tablas:
- `workspace.silver.alumnos`
- `workspace.silver.cursos`
- `workspace.silver.notas`

### Gold

Notebook: `proceso/03_gold.py`

Responsabilidades:
- Calcular indicadores académicos.
- Generar agregaciones por facultad y curso.
- Calcular promedios de notas y asistencia.
- Clasificar estudiantes según riesgo académico.

Tablas:
- `workspace.gold.rendimiento_facultad`
- `workspace.gold.rendimiento_curso`
- `workspace.gold.riesgo_academico`

## 6. Orquestación con Databricks Workflows

Se implementó el job:

`job_academic_lakehouse_etl`

El flujo de ejecución es:

`bronze → silver → gold`

Cada tarea depende de la finalización correcta de la tarea anterior.

El procesamiento utiliza Databricks Serverless.

## 7. Integración y despliegue continuo (CI/CD)

El repositorio incluye un workflow de GitHub Actions:

`.github/workflows/deploy.yml`

El workflow se activa cuando se realizan cambios en la rama `main`, especialmente en la carpeta `proceso`.

### Etapas del pipeline

1. Descargar el repositorio mediante GitHub Actions.
2. Instalar Databricks CLI.
3. Validar la conexión con Databricks.
4. Desplegar los notebooks en la carpeta de producción.
5. Enviar una ejecución a Databricks con las tareas Bronze, Silver y Gold.

### Carpeta de producción

`/Shared/academic_lakehouse_prod/proceso/`

### Autenticación

Se utilizan secretos de GitHub Actions:

- `DATABRICKS_HOST`
- `DATABRICKS_TOKEN`

Los valores de autenticación no se almacenan directamente en el código fuente.

## 8. Estructura del repositorio

```text
academic-lakehouse-databricks/
|
|-- .github/
|   |-- workflows/
|       |-- deploy.yml
|
|-- proceso/
|   |-- 01_bronze.py
|   |-- 02_silver.py
|   |-- 03_gold.py
|
|-- README.md
```

## 9. Resultados obtenidos

Se implementó y ejecutó correctamente un proceso ETL completo sobre una arquitectura Medallion.

Resultados validados:

- Lectura de tres archivos CSV desde S3.
- Creación de tablas Delta en Bronze.
- Transformación de datos en Silver.
- Generación de indicadores académicos en Gold.
- Ejecución secuencial de tres tareas mediante Databricks Workflows.
- Despliegue automatizado mediante GitHub Actions.
- Ejecución del proceso en el entorno de producción de Databricks.

### Ejecución validada en producción

- Nombre: `academic_lakehouse_prod`
- Estado: `Succeeded`
- Duración aproximada: 2 minutos y 5 segundos.
- Tareas: Bronze, Silver y Gold completadas correctamente.

## 10. Conclusiones

Academic Lakehouse Analytics demuestra la implementación de una solución de ingeniería de datos utilizando tecnologías modernas de procesamiento, almacenamiento y gobierno de datos.

La arquitectura Medallion permite separar la ingesta, la transformación y el consumo analítico.

La integración entre GitHub Actions y Databricks permite automatizar el despliegue y la ejecución del proceso ETL, facilitando su mantenimiento y evolución.

---

**Proyecto académico desarrollado con fines educativos.**
