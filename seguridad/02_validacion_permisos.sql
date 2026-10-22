
-- =====================================================
-- VALIDACION DE PERMISOS UNITY CATALOG
-- =====================================================

SHOW GRANTS ON CATALOG workspace;

SHOW GRANTS ON SCHEMA workspace.gold;

SHOW GRANTS ON TABLE workspace.gold.dim_alumno;

SHOW GRANTS ON TABLE workspace.gold.dim_curso;

SHOW GRANTS ON TABLE workspace.gold.fact_notas;

SHOW GRANTS ON TABLE workspace.gold.rendimiento_facultad;

SHOW GRANTS ON TABLE workspace.gold.rendimiento_curso;

SHOW GRANTS ON TABLE workspace.gold.riesgo_academico;
