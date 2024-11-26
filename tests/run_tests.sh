#!/bin/bash

# Configuración
FUNCTION_NAME="TherapySystem"
TEST_DIR="tests"
RESULTS_DIR="${TEST_DIR}/results"
LOG_FILE="${RESULTS_DIR}/test_run.log"

# Crear directorio de resultados
mkdir -p ${RESULTS_DIR}

# Función para ejecutar prueba
run_test() {
    local test_name=$1
    local payload_file=$2
    local output_file="${RESULTS_DIR}/${test_name}_response.json"
    
    echo "=== Ejecutando prueba: ${test_name} ==="
    echo "Payload:"
    cat ${TEST_DIR}/payloads/${payload_file}
    
    # Invocar Lambda
    aws lambda invoke \
        --function-name ${FUNCTION_NAME} \
        --payload file://${TEST_DIR}/payloads/${payload_file} \
        --cli-binary-format raw-in-base64-out \
        ${output_file}
    
    # Mostrar respuesta
    echo "Respuesta:"
    cat ${output_file}
    echo "==="
    
    # Esperar un momento entre pruebas
    sleep 2
}

# Inicio de pruebas
echo "=== Iniciando pruebas completas $(date) ==="

# 1. Prueba básica de inicio
run_test "launch" "launch.json"

# 2. Registro de terapia simple
run_test "register_tortuga" "register_tortuga.json"

# 3. Registro de terapia compuesta
run_test "register_complex" "register_complex.json"

# 4. Consulta de terapias
run_test "query_specific" "query_specific.json"

# Ver los últimos logs
echo "=== Últimos logs de CloudWatch ==="
aws logs get-log-events \
    --log-group-name /aws/lambda/${FUNCTION_NAME} \
    --log-stream-name $(aws logs describe-log-streams \
        --log-group-name /aws/lambda/${FUNCTION_NAME} \
        --order-by LastEventTime \
        --descending \
        --limit 1 \
        --query 'logStreams[0].logStreamName' \
        --output text) \
    --limit 20

echo "=== Fin de pruebas $(date) ==="
