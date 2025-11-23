@echo off
echo ========================================
echo   Sistema de Reportes Metro CDMX
echo   Iniciando servicios...
echo ========================================
echo.

REM Verificar si Docker esta corriendo
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Desktop no esta corriendo
    echo.
    echo Por favor inicia Docker Desktop y vuelve a intentar.
    pause
    exit /b 1
)

echo [OK] Docker Desktop esta corriendo
echo.

echo Iniciando servicios (esto puede tardar unos minutos la primera vez)...
echo.

docker-compose up --build

pause
