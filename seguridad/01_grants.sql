
-- =====================================================
-- PROYECTO: Academic Lakehouse Analytics
-- PLATAFORMA: Databricks sobre AWS
-- SEGURIDAD: UNITY CATALOG
-- =====================================================

-- Grupo de ejemplo:
-- academic_analysts
--
-- IMPORTANTE:
-- El grupo debe existir previamente en Databricks.
-- Reemplazarlo por el nombre real antes de ejecutar.

-- Acceso al catalogo
GRANT USE CATALOG ON CATALOG workspace
TO `academic_analysts`;

-- Acceso al esquema Gold
GRANT USE SCHEMA ON SCHEMA workspace.gold
TO `academic_analysts`;

-- Lectura de las tablas finales
GRANT SELECT ON TABLE workspace.gold.dim_alumno
TO `academic_analysts`;

GRANT SELECT ON TABLE workspace.gold.dim_curso
TO `academic_analysts`;

GRANT SELECT ON TABLE workspace.gold.fact_notas
TO `academic_analysts`;

GRANT SELECT ON TABLE workspace.gold.rendimiento_facultad
TO `academic_analysts`;

GRANT SELECT ON TABLE workspace.gold.rendimiento_curso
TO `academic_analysts`;

GRANT SELECT ON TABLE workspace.gold.riesgo_academico
TO `academic_analysts`;
