#!/bin/bash

SKILL_ID="amzn1.ask.skill.028ef8b0-b7cd-45e7-bc9c-08a4a213921e"

echo "🚀 Iniciando despliegue..."

# 1. Actualizar Lambda
echo "📦 Empaquetando y actualizando función Lambda..."
cd lambda/src
zip -r ../function.zip .
cd ..
aws lambda update-function-code \
  --function-name therapy-system \
  --zip-file fileb://function.zip

if [ $? -eq 0 ]; then
    echo "✅ Función Lambda actualizada exitosamente"
else
    echo "❌ Error actualizando Lambda"
    exit 1
fi

# 2. Actualizar modelo de interacción de Alexa
cd ../alexa/model
echo "🔄 Actualizando modelo de interacción de Alexa Skill..."
ask smapi set-interaction-model \
  --skill-id $SKILL_ID \
  --locale es-ES \
  --interaction-model file:./interaction_model.json

if [ $? -eq 0 ]; then
    echo "✅ Modelo de interacción actualizado exitosamente"
else
    echo "❌ Error actualizando modelo de interacción"
    exit 1
fi

# 3. Verificar despliegue
echo "🔍 Verificando despliegue..."

echo "Verificando Lambda..."
aws lambda get-function \
  --function-name therapy-system \
  --query 'Configuration.LastModified'

echo "Verificando Skill..."
ask smapi get-interaction-model \
  --skill-id $SKILL_ID \
  --locale es-ES

echo "✨ Despliegue completado"

# 4. Volver al directorio raíz
cd ../..
