@echo off
echo 🌟 DETECTOR DE PULSARES EDUCATIVO
echo ================================
echo.
echo Escolha uma opção:
echo.
echo 1. Aplicação Educativa Interativa (Recomendado)
echo 2. Demonstração Rápida
echo 3. Sair
echo.
set /p choice="Digite sua escolha (1-3): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Iniciando aplicação educativa...
    ".venv\Scripts\python.exe" src\main_app.py
) else if "%choice%"=="2" (
    echo.
    echo ⚡ Executando demonstração rápida...
    ".venv\Scripts\python.exe" src\demo_rapida.py
) else if "%choice%"=="3" (
    echo.
    echo 👋 Até logo!
    exit /b
) else (
    echo.
    echo ❌ Opção inválida. Tente novamente.
    pause
    goto :eof
)

echo.
echo ✅ Execução concluída!
pause