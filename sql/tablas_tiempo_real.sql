-- Tablas adicionales para funcionalidad en tiempo real
-- Ejecutar después de importar base_de_datos_metro.sql

-- Tabla de empleados para tracking en tiempo real
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    employee_code VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    status VARCHAR(20) DEFAULT 'offline', -- available, busy, offline
    current_latitude DECIMAL(10, 8),
    current_longitude DECIMAL(11, 8),
    current_station VARCHAR(100),
    current_line VARCHAR(50),
    last_update TIMESTAMP DEFAULT NOW()
);

-- Tabla de alertas del administrador
CREATE TABLE IF NOT EXISTS admin_alerts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    severity VARCHAR(20) NOT NULL, -- info, warning, critical
    category VARCHAR(50),
    line VARCHAR(50),
    station VARCHAR(100),
    send_to_public BOOLEAN DEFAULT true,
    send_to_manager BOOLEAN DEFAULT false,
    manager_category VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(100)
);

-- Tabla de asignaciones de incidentes
CREATE TABLE IF NOT EXISTS incident_assignments (
    id SERIAL PRIMARY KEY,
    incident_id INT REFERENCES datos_metro_cdmx(id),
    employee_id INT REFERENCES employees(id),
    assigned_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending', -- pending, in_progress, resolved
    notes TEXT
);

-- Índices para mejorar performance
CREATE INDEX IF NOT EXISTS idx_employees_status ON employees(status);
CREATE INDEX IF NOT EXISTS idx_employees_last_update ON employees(last_update);
CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON admin_alerts(created_at);
CREATE INDEX IF NOT EXISTS idx_assignments_employee ON incident_assignments(employee_id);
CREATE INDEX IF NOT EXISTS idx_assignments_incident ON incident_assignments(incident_id);

-- Datos de prueba: Empleados iniciales
INSERT INTO employees (employee_code, full_name, email, status, current_station, current_line) VALUES
('EMP-001', 'Juan Pérez', 'juan.perez@metro.cdmx.gob.mx', 'available', 'Pino Suárez', 'Línea 1'),
('EMP-002', 'María García', 'maria.garcia@metro.cdmx.gob.mx', 'available', 'Zaragoza', 'Línea 1'),
('EMP-003', 'Carlos López', 'carlos.lopez@metro.cdmx.gob.mx', 'busy', 'Balderas', 'Línea 3'),
('EMP-004', 'Ana Martínez', 'ana.martinez@metro.cdmx.gob.mx', 'available', 'Hidalgo', 'Línea 2'),
('EMP-005', 'Roberto Sánchez', 'roberto.sanchez@metro.cdmx.gob.mx', 'offline', 'Tacubaya', 'Línea 1'),
('EMP-006', 'Laura Torres', 'laura.torres@metro.cdmx.gob.mx', 'available', 'Insurgentes', 'Línea 1'),
('EMP-007', 'Miguel Ramírez', 'miguel.ramirez@metro.cdmx.gob.mx', 'busy', 'Pantitlán', 'Línea 5'),
('EMP-008', 'Patricia Flores', 'patricia.flores@metro.cdmx.gob.mx', 'available', 'Auditorio', 'Línea 7')
ON CONFLICT (employee_code) DO NOTHING;

-- Función para actualizar timestamp automáticamente
CREATE OR REPLACE FUNCTION update_last_update_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_update = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar last_update automáticamente
DROP TRIGGER IF EXISTS update_employees_last_update ON employees;
CREATE TRIGGER update_employees_last_update
    BEFORE UPDATE ON employees
    FOR EACH ROW
    EXECUTE FUNCTION update_last_update_column();

COMMENT ON TABLE employees IS 'Empleados del sistema con tracking en tiempo real';
COMMENT ON TABLE admin_alerts IS 'Alertas creadas por administradores';
COMMENT ON TABLE incident_assignments IS 'Asignaciones de incidentes a empleados';
