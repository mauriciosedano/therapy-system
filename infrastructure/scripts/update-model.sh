#!/bin/bash

# Obtener la ruta base del proyecto
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MODEL_PATH="$BASE_DIR/alexa/model/interaction_model.json"

echo "🔄 Actualizando modelo de interacción..."
echo "📂 Usando archivo: $MODEL_PATH"

# Validar que el archivo existe
if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ Error: No se encuentra el archivo de modelo en: $MODEL_PATH"
    exit 1
fi

# Actualizar el modelo
ask smapi set-interaction-model \
  --skill-id amzn1.ask.skill.028ef8b0-b7cd-45e7-bc9c-08a4a213921e \
  --locale es-ES \
  --interaction-model "file://${MODEL_PATH}"

if [ $? -eq 0 ]; then
    echo "✅ Modelo actualizado exitosamente"
else
    echo "❌ Error actualizando el modelo"
    exit 1
fi
