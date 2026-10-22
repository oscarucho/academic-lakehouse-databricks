
-- =====================================================
-- PROYECTO: Academic Lakehouse Analytics
-- REVERSION DE TABLAS DEL ETL
-- AWS DATABRICKS - UNITY CATALOG
-- =====================================================

-- ATENCION:
-- Script destructivo. Ejecutar solamente cuando
-- se requiera reconstruir el proyecto.
-- No ejecutar durante la entrega.

-- 1. Eliminar tablas del modelo dimensional
DROP TABLE IF EXISTS workspace.gold.fact_notas;
DROP TABLE IF EXISTS workspace.gold.dim_alumno;
DROP TABLE IF EXISTS workspace.gold.dim_curso;

-- 2. Eliminar tablas analiticas Gold
DROP TABLE IF EXISTS workspace.gold.rendimiento_facultad;
DROP TABLE IF EXISTS workspace.gold.rendimiento_curso;
DROP TABLE IF EXISTS workspace.gold.riesgo_academico;

-- 3. Eliminar tablas Silver
DROP TABLE IF EXISTS workspace.silver.notas;
DROP TABLE IF EXISTS workspace.silver.alumnos;
DROP TABLE IF EXISTS workspace.silver.cursos;

-- 4. Eliminar tablas Bronze
DROP TABLE IF EXISTS workspace.bronze.notas;
DROP TABLE IF EXISTS workspace.bronze.alumnos;
DROP TABLE IF EXISTS workspace.bronze.cursos;
