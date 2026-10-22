# Databricks notebook source

from pyspark.sql import functions as F

# Crear esquema Gold
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.gold")

# Leer datos Silver
alumnos = spark.table("workspace.silver.alumnos")
cursos = spark.table("workspace.silver.cursos")
notas = spark.table("workspace.silver.notas")

# Unificar información académica
df = (
    notas
    .join(alumnos, "id_alumno", "inner")
    .join(cursos, "id_curso", "inner")
)

# GOLD 1: Rendimiento por facultad
rendimiento_facultad = (
    df.groupBy("facultad")
    .agg(
        F.count("*").alias("total_evaluaciones"),
        F.countDistinct("id_alumno").alias("total_alumnos"),
        F.round(F.avg("nota"), 2).alias("promedio_notas"),
        F.round(F.avg("asistencia_pct"), 2).alias("asistencia_promedio"),
        F.round(
            F.avg(
                F.when(F.col("nota") >= 11, 100.0)
                 .otherwise(0.0)
            ), 2
        ).alias("porcentaje_aprobacion")
    )
)

rendimiento_facultad.write.format("delta").mode("overwrite") \
    .saveAsTable("workspace.gold.rendimiento_facultad")

# GOLD 2: Rendimiento por curso
rendimiento_curso = (
    df.groupBy("id_curso")
    .agg(
        F.count("*").alias("total_evaluaciones"),
        F.round(F.avg("nota"), 2).alias("promedio_notas"),
        F.round(F.avg("asistencia_pct"), 2).alias("asistencia_promedio"),
        F.sum(
            F.when(F.col("nota") >= 11, 1).otherwise(0)
        ).alias("aprobados"),
        F.sum(
            F.when(F.col("nota") < 11, 1).otherwise(0)
        ).alias("desaprobados")
    )
)

rendimiento_curso.write.format("delta").mode("overwrite") \
    .saveAsTable("workspace.gold.rendimiento_curso")

# GOLD 3: Riesgo académico (regla demostrativa)
riesgo_academico = (
    df.groupBy("id_alumno", "nombre", "facultad")
    .agg(
        F.round(F.avg("nota"), 2).alias("promedio_notas"),
        F.round(F.avg("asistencia_pct"), 2).alias("asistencia_promedio")
    )
    .withColumn(
        "nivel_riesgo",
        F.when(
            (F.col("promedio_notas") < 11) |
            (F.col("asistencia_promedio") < 70),
            "Alto"
        ).otherwise("Bajo")
    )
)

riesgo_academico.write.format("delta").mode("overwrite") \
    .saveAsTable("workspace.gold.riesgo_academico")

print("GOLD: 3 tablas Delta creadas correctamente")

display(spark.table("workspace.gold.rendimiento_facultad"))
display(spark.table("workspace.gold.rendimiento_curso"))
display(spark.table("workspace.gold.riesgo_academico").limit(10))


# COMMAND ----------

