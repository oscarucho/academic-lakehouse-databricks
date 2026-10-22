
-- =====================================================
-- VALIDACION DEL AMBIENTE DATABRICKS
-- =====================================================

USE CATALOG workspace;

-- Tablas Bronze
SELECT 'bronze_alumnos' AS tabla, COUNT(*) AS registros
FROM workspace.bronze.alumnos
UNION ALL
SELECT 'bronze_cursos', COUNT(*)
FROM workspace.bronze.cursos
UNION ALL
SELECT 'bronze_notas', COUNT(*)
FROM workspace.bronze.notas;

-- Tablas Silver
SELECT 'silver_alumnos' AS tabla, COUNT(*) AS registros
FROM workspace.silver.alumnos
UNION ALL
SELECT 'silver_cursos', COUNT(*)
FROM workspace.silver.cursos
UNION ALL
SELECT 'silver_notas', COUNT(*)
FROM workspace.silver.notas;

-- Modelo dimensional Gold
SELECT 'dim_alumno' AS tabla, COUNT(*) AS registros
FROM workspace.gold.dim_alumno
UNION ALL
SELECT 'dim_curso', COUNT(*)
FROM workspace.gold.dim_curso
UNION ALL
SELECT 'fact_notas', COUNT(*)
FROM workspace.gold.fact_notas;
