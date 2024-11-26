#!/bin/bash

# Activar entorno conda
eval "$(conda shell.bash hook)"
conda activate ds4x

echo "🚀 Iniciando pruebas de integración de Alexa..."

# Ejecutar pruebas
python tests/test_alexa_integration.py

# Verificar si hubo errores
if [ $? -eq 0 ]; then
    echo "✅ Pruebas de integración completadas"
    echo "📄 Ver resultados detallados en tests/results/"
    echo "📄 Ver logs en tests/logs/alexa_integration.log"
else
    echo "❌ Algunas pruebas fallaron"
    echo "📄 Ver detalles del error en tests/logs/alexa_integration.log"
    tail -n 20 tests/logs/alexa_integration.log
fi

# Desactivar entorno conda
conda deactivate
