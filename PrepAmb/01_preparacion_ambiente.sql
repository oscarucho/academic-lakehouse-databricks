
-- =====================================================
-- PROYECTO: Academic Lakehouse Analytics
-- PLATAFORMA: Databricks sobre AWS
-- PREPARACION DEL AMBIENTE
-- =====================================================

-- Catalogo utilizado por el proyecto
USE CATALOG workspace;

-- Crear esquemas de arquitectura Medallion
CREATE SCHEMA IF NOT EXISTS workspace.bronze;
CREATE SCHEMA IF NOT EXISTS workspace.silver;
CREATE SCHEMA IF NOT EXISTS workspace.gold;

-- Validar los esquemas
SHOW SCHEMAS IN workspace;

-- Validar las tablas generadas
SHOW TABLES IN workspace.bronze;
SHOW TABLES IN workspace.silver;
SHOW TABLES IN workspace.gold;
