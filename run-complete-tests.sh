#!/bin/bash

# Activar entorno conda
eval "$(conda shell.bash hook)"
conda activate ds4x

echo "🚀 Iniciando proceso completo de pruebas..."

# 1. Generar payloads
echo "📝 Generando payloads de prueba..."
python tests/generate_test_payloads.py

# 2. Ejecutar pruebas de integración
echo "🔄 Ejecutando pruebas de integración..."
python tests/test_alexa_integration.py

# Verificar si hubo errores
if [ $? -eq 0 ]; then
    echo "✅ Proceso completo finalizado exitosamente"
    echo "📄 Ver resultados detallados en tests/results/"
    echo "📄 Ver logs en tests/logs/alexa_integration.log"
else
    echo "❌ Se encontraron errores durante las pruebas"
    echo "📄 Ver detalles del error en tests/logs/alexa_integration.log"
    tail -n 20 tests/logs/alexa_integration.log
fi

# Desactivar entorno conda
conda deactivate
