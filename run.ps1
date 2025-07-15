Write-Host "🌟 DETECTOR DE PULSARES EDUCATIVO" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Escolha uma opção:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Aplicação Educativa Interativa (Recomendado)" -ForegroundColor Green
Write-Host "2. Demonstração Rápida" -ForegroundColor Green  
Write-Host "3. Sair" -ForegroundColor Red
Write-Host ""

$choice = Read-Host "Digite sua escolha (1-3)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🚀 Iniciando aplicação educativa..." -ForegroundColor Green
        & "./.venv/Scripts/python.exe" "src/main_app.py"
    }
    "2" {
        Write-Host ""
        Write-Host "⚡ Executando demonstração rápida..." -ForegroundColor Yellow
        & "./.venv/Scripts/python.exe" "src/demo_rapida.py"
    }
    "3" {
        Write-Host ""
        Write-Host "👋 Até logo!" -ForegroundColor Blue
        exit
    }
    default {
        Write-Host ""
        Write-Host "❌ Opção inválida. Tente novamente." -ForegroundColor Red
        Read-Host "Pressione Enter para continuar"
    }
}

Write-Host ""
Write-Host "✅ Execução concluída!" -ForegroundColor Green
Read-Host "Pressione Enter para sair"