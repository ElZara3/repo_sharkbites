-- ========================================
-- Script de datos de prueba para tiempo real
-- ========================================

-- Insertar empleados de prueba
INSERT INTO employees (employee_code, full_name, status, current_latitude, current_longitude, current_station, current_line, last_update)
VALUES 
    ('EMP-001', 'Juan Pérez García', 'available', 19.432608, -99.133209, 'Pino Suárez', 'Línea 1', NOW()),
    ('EMP-002', 'María López Hernández', 'available', 19.426019, -99.167571, 'Chapultepec', 'Línea 1', NOW()),
    ('EMP-003', 'Carlos Ramírez Soto', 'busy', 19.434453, -99.141272, 'Zócalo', 'Línea 2', NOW()),
    ('EMP-004', 'Ana Martínez Cruz', 'available', 19.425689, -99.173423, 'Sevilla', 'Línea 1', NOW()),
    ('EMP-005', 'Roberto González Díaz', 'offline', 19.436794, -99.154573, 'Bellas Artes', 'Línea 2', NOW()),
    ('EMP-006', 'Laura Sánchez Ruiz', 'available', 19.427234, -99.155678, 'Insurgentes', 'Línea 1', NOW()),
    ('EMP-007', 'Diego Torres Vega', 'busy', 19.432867, -99.147234, 'Pino Suárez', 'Línea 1', NOW()),
    ('EMP-008', 'Carmen Flores Mora', 'available', 19.428456, -99.168923, 'Juanacatlán', 'Línea 1', NOW())
ON CONFLICT (employee_code) DO UPDATE SET
    full_name = EXCLUDED.full_name,
    status = EXCLUDED.status,
    current_latitude = EXCLUDED.current_latitude,
    current_longitude = EXCLUDED.current_longitude,
    current_station = EXCLUDED.current_station,
    current_line = EXCLUDED.current_line,
    last_update = EXCLUDED.last_update;

-- Insertar incidentes de prueba
INSERT INTO incidents (
    title, 
    description, 
    category, 
    severity, 
    line, 
    station, 
    station_latitude, 
    station_longitude, 
    status, 
    assigned_employee_id,
    sentiment,
    priority_score,
    created_at
)
VALUES 
    (
        'Torniquete dañado en acceso principal',
        'El torniquete del acceso norte no está funcionando correctamente, los usuarios deben usar el acceso sur',
        'Infraestructura',
        'high',
        'Línea 1',
        'Pino Suárez',
        19.432608,
        -99.133209,
        'in_progress',
        1,
        'negative',
        85.5,
        NOW() - INTERVAL '30 minutes'
    ),
    (
        'Limpieza requerida en andén',
        'Se requiere limpieza urgente en el andén dirección Pantitlán',
        'Limpieza',
        'medium',
        'Línea 1',
        'Pino Suárez',
        19.432608,
        -99.133209,
        'pending',
        NULL,
        'neutral',
        65.0,
        NOW() - INTERVAL '15 minutes'
    ),
    (
        'Falla en sistema de ventilación',
        'El sistema de ventilación presenta problemas, temperatura elevada en el área',
        'Mantenimiento',
        'critical',
        'Línea 2',
        'Zócalo',
        19.434453,
        -99.141272,
        'in_progress',
        3,
        'negative',
        92.0,
        NOW() - INTERVAL '45 minutes'
    ),
    (
        'Iluminación deficiente en escaleras',
        'Varias lámparas fundidas en las escaleras de acceso',
        'Infraestructura',
        'low',
        'Línea 1',
        'Chapultepec',
        19.426019,
        -99.167571,
        'pending',
        NULL,
        'neutral',
        45.0,
        NOW() - INTERVAL '1 hour'
    ),
    (
        'Queja por servicio al cliente',
        'Usuario reporta trato inadecuado por parte del personal de taquilla',
        'Servicio al Cliente',
        'medium',
        'Línea 1',
        'Insurgentes',
        19.427234,
        -99.155678,
        'pending',
        NULL,
        'negative',
        70.0,
        NOW() - INTERVAL '20 minutes'
    ),
    (
        'Pantalla de información no funciona',
        'La pantalla principal de horarios está apagada',
        'Tecnología',
        'medium',
        'Línea 2',
        'Bellas Artes',
        19.436794,
        -99.154573,
        'pending',
        NULL,
        'neutral',
        55.0,
        NOW() - INTERVAL '10 minutes'
    ),
    (
        'Congestión en horario pico',
        'Exceso de personas en andén, se requiere apoyo para ordenar el flujo',
        'Seguridad',
        'high',
        'Línea 1',
        'Pino Suárez',
        19.432608,
        -99.133209,
        'pending',
        NULL,
        'neutral',
        80.0,
        NOW() - INTERVAL '5 minutes'
    );

-- Verificar datos insertados
SELECT 
    'Empleados insertados:' AS info, 
    COUNT(*) AS total 
FROM employees;

SELECT 
    'Incidentes insertados:' AS info, 
    COUNT(*) AS total 
FROM incidents;

-- Mostrar resumen de empleados
SELECT 
    employee_code,
    full_name,
    status,
    current_station,
    current_line
FROM employees
ORDER BY full_name;

-- Mostrar resumen de incidentes
SELECT 
    id,
    title,
    severity,
    status,
    station,
    line,
    CASE 
        WHEN assigned_employee_id IS NOT NULL THEN 'Asignado'
        ELSE 'Sin asignar'
    END as assignment_status
FROM incidents
ORDER BY created_at DESC;
