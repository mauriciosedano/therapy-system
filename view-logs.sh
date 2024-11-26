#!/bin/bash

echo "🔍 Obteniendo logs más recientes..."

# Obtener el nombre del último stream
LAST_STREAM=$(aws logs describe-log-streams \
    --log-group-name /aws/lambda/therapy-system \
    --order-by LastEventTime \
    --descending \
    --limit 1 \
    --query 'logStreams[0].logStreamName' \
    --output text)

if [ -z "$LAST_STREAM" ]; then
    echo "❌ No se encontraron streams de log"
    exit 1
fi

echo "📄 Mostrando logs del stream: $LAST_STREAM"

# Obtener los eventos del stream
aws logs get-log-events \
    --log-group-name /aws/lambda/therapy-system \
    --log-stream-name "$LAST_STREAM" \
    --limit 20

echo "✅ Logs mostrados exitosamente"
