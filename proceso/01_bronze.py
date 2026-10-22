# Databricks notebook source

from pyspark.sql import functions as F

# Configuración del proyecto
S3_RAW = "s3://academic-lakehouse-raw-2026/raw/"

# Lectura directa de los archivos originales desde S3
df_alumnos = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(S3_RAW + "alumnos.csv")
)

df_cursos = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(S3_RAW + "cursos.csv")
)

df_notas = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(S3_RAW + "notas.csv")
)

print("Alumnos:", df_alumnos.count())
print("Cursos:", df_cursos.count())
print("Notas:", df_notas.count())

display(df_alumnos.limit(5))


# COMMAND ----------


from pyspark.sql import functions as F

# Crear esquema Bronze en el catálogo workspace
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.bronze")

# Agregar fecha de procesamiento
df_alumnos_bronze = df_alumnos.withColumn(
    "fecha_proceso", F.current_timestamp()
)

df_cursos_bronze = df_cursos.withColumn(
    "fecha_proceso", F.current_timestamp()
)

df_notas_bronze = df_notas.withColumn(
    "fecha_proceso", F.current_timestamp()
)

# Guardar tablas Delta Lake
df_alumnos_bronze.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.bronze.alumnos")

df_cursos_bronze.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.bronze.cursos")

df_notas_bronze.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.bronze.notas")

print("BRONZE: 3 tablas Delta creadas correctamente")

# Verificar registros
spark.sql("""
SELECT 'alumnos' AS tabla, COUNT(*) AS registros
FROM workspace.bronze.alumnos
UNION ALL
SELECT 'cursos', COUNT(*)
FROM workspace.bronze.cursos
UNION ALL
SELECT 'notas', COUNT(*)
FROM workspace.bronze.notas
""").show()


# COMMAND ----------

