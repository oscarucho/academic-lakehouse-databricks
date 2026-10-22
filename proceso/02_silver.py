# Databricks notebook source

from pyspark.sql import functions as F

# 1. Crear esquema Silver
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.silver")

# 2. Leer las tablas Bronze
alumnos = spark.table("workspace.bronze.alumnos")
cursos = spark.table("workspace.bronze.cursos")
notas = spark.table("workspace.bronze.notas")

# 3. Limpiar alumnos
alumnos_silver = (
    alumnos
    .dropDuplicates(["id_alumno"])
    .filter(F.col("id_alumno").isNotNull())
    .withColumn("nombre", F.trim(F.col("nombre")))
    .withColumn("facultad", F.trim(F.col("facultad")))
    .withColumn("fecha_ingreso", F.to_date("fecha_ingreso"))
)

# 4. Limpiar cursos
cursos_silver = (
    cursos
    .dropDuplicates(["id_curso"])
    .filter(F.col("id_curso").isNotNull())
)

# 5. Limpiar notas y validar relaciones
notas_silver = (
    notas
    .dropDuplicates()
    .filter(F.col("id_alumno").isNotNull())
    .filter(F.col("id_curso").isNotNull())
    .filter(F.col("nota").between(0, 20))
    .join(
        alumnos_silver.select("id_alumno"),
        "id_alumno",
        "inner"
    )
    .join(
        cursos_silver.select("id_curso"),
        "id_curso",
        "inner"
    )
    .withColumn(
        "estado_academico",
        F.when(F.col("nota") >= 11, "Aprobado")
         .otherwise("Desaprobado")
    )
)

# 6. Guardar tablas Silver
alumnos_silver.write.format("delta").mode("overwrite") \
    .saveAsTable("workspace.silver.alumnos")

cursos_silver.write.format("delta").mode("overwrite") \
    .saveAsTable("workspace.silver.cursos")

notas_silver.write.format("delta").mode("overwrite") \
    .saveAsTable("workspace.silver.notas")

# 7. Verificar resultados
print("SILVER: procesamiento finalizado correctamente")

print("Alumnos:", spark.table("workspace.silver.alumnos").count())
print("Cursos:", spark.table("workspace.silver.cursos").count())
print("Notas:", spark.table("workspace.silver.notas").count())

display(spark.table("workspace.silver.notas").limit(10))


# COMMAND ----------

