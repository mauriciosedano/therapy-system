#!/bin/bash

# Configuración
TEST_DIR="tests"
LAMBDA_FUNCTION="TherapySystem"
LOG_FILE="${TEST_DIR}/logs/test_results.log"

# Función para ejecutar prueba y registrar resultado
run_test() {
    local test_name=$1
    local payload_file=$2
    
    echo "=== Ejecutando prueba: ${test_name} ===" | tee -a ${LOG_FILE}
    echo "Payload:" | tee -a ${LOG_FILE}
    cat ${payload_file} | tee -a ${LOG_FILE}
    
    aws lambda invoke \
        --function-name ${LAMBDA_FUNCTION} \
        --payload file://${payload_file} \
        --log-type Tail \
        /tmp/${test_name}_output.json | tee -a ${LOG_FILE}
    
    echo "Respuesta:" | tee -a ${LOG_FILE}
    cat /tmp/${test_name}_output.json | tee -a ${LOG_FILE}
    echo "===" | tee -a ${LOG_FILE}
}

# Limpiar archivo de logs
echo "=== Iniciando pruebas $(date) ===" > ${LOG_FILE}

# Ejecutar pruebas
run_test "register_complex" "${TEST_DIR}/payloads/register_complex_therapy.json"
run_test "query_simple" "${TEST_DIR}/payloads/query_simple.json"

# Obtener logs de CloudWatch
echo "=== Logs de CloudWatch ===" | tee -a ${LOG_FILE}
aws logs get-log-events \
    --log-group-name /aws/lambda/TherapySystem \
    --log-stream-name $(aws logs describe-log-streams \
        --log-group-name /aws/lambda/TherapySystem \
        --order-by LastEventTime \
        --descending \
        --limit 1 \
        --query 'logStreams[0].logStreamName' \
        --output text) | tee -a ${LOG_FILE}

echo "=== Fin de pruebas $(date) ===" | tee -a ${LOG_FILE}
