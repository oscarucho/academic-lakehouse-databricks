# Databricks notebook source

from pyspark.sql import functions as F

# ======================================================
# ACADEMIC LAKEHOUSE ANALYTICS
# MODELO DIMENSIONAL - GOLD
# ======================================================

# 1. Leer tablas Silver
alumnos = spark.table("workspace.silver.alumnos")
cursos = spark.table("workspace.silver.cursos")
notas = spark.table("workspace.silver.notas")

# 2. Crear esquema Gold
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.gold")

# ======================================================
# DIMENSIÓN ALUMNO
# ======================================================

dim_alumno = (
    alumnos
    .select(
        "id_alumno",
        "nombre",
        "facultad",
        "fecha_ingreso"
    )
    .dropDuplicates(["id_alumno"])
)

dim_alumno.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("workspace.gold.dim_alumno")

print("DimAlumno creada correctamente")

# ======================================================
# DIMENSIÓN CURSO
# ======================================================

dim_curso = (
    cursos
    .dropDuplicates(["id_curso"])
)

dim_curso.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("workspace.gold.dim_curso")

print("DimCurso creada correctamente")

# ======================================================
# TABLA DE HECHOS - NOTAS
# ======================================================

fact_notas = (
    notas
    .select(
        "id_alumno",
        "id_curso",
        "periodo",
        "nota",
        "asistencia_pct",
        "estado_academico",
        "fecha_proceso"
    )
)

fact_notas.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("workspace.gold.fact_notas")

print("FactNotas creada correctamente")

# ======================================================
# VALIDACIÓN DEL MODELO
# ======================================================

tablas = [
    "workspace.gold.dim_alumno",
    "workspace.gold.dim_curso",
    "workspace.gold.fact_notas"
]

for tabla in tablas:
    total = spark.table(tabla).count()
    print(f"{tabla}: {total} registros")

print("MODELO DIMENSIONAL CREADO CORRECTAMENTE")
