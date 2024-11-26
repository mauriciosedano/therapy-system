#!/bin/bash

# Activar el entorno conda
eval "$(conda shell.bash hook)"
conda activate ds4x

echo "🚀 Iniciando pruebas con entorno Conda: ds4x"

# Verificar activación del entorno
CURRENT_ENV=$(conda info --envs | grep '*' | awk '{print $1}')
if [ "$CURRENT_ENV" != "ds4x" ]; then
    echo "❌ Error: El entorno ds4x no está activado"
    exit 1
fi

# Crear directorios necesarios
mkdir -p tests/results
mkdir -p tests/logs

# Ejecutar pruebas
python tests/test_scenarios.py > tests/logs/test_run.log 2>&1

# Verificar resultado
if [ $? -eq 0 ]; then
    echo "✅ Pruebas completadas exitosamente"
    echo "📄 Ver resultados detallados en tests/results/"
    echo "📄 Ver logs en tests/logs/test_run.log"
else
    echo "❌ Algunas pruebas fallaron"
    echo "📄 Ver detalles del error en tests/logs/test_run.log"
    tail -n 20 tests/logs/test_run.log
fi

# Desactivar el entorno conda
conda deactivate
