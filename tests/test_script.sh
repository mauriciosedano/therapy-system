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
    
    echo "=== Ejecutando prueba: ${test_name} ===" | tee -a ${LOG_FILE}
    echo "$(date) - Iniciando prueba ${test_name}" >> ${LOG_FILE}
    
    # Invocar Lambda
    aws lambda invoke \
        --function-name ${FUNCTION_NAME} \
        --payload file://${TEST_DIR}/payloads/${payload_file} \
        --cli-binary-format raw-in-base64-out \
        ${output_file} 2>> ${LOG_FILE}
    
    # Mostrar respuesta
    echo "Respuesta:" | tee -a ${LOG_FILE}
    cat ${output_file} | tee -a ${LOG_FILE}
    echo "===" | tee -a ${LOG_FILE}
    
    # Obtener logs específicos
    aws logs get-log-events \
        --log-group-name /aws/lambda/${FUNCTION_NAME} \
        --log-stream-name $(aws logs describe-log-streams \
            --log-group-name /aws/lambda/${FUNCTION_NAME} \
            --order-by LastEventTime \
            --descending \
            --limit 1 \
            --query 'logStreams[0].logStreamName' \
            --output text) >> ${LOG_FILE}
}

# Ejecutar suite de pruebas
echo "=== Iniciando pruebas $(date) ===" > ${LOG_FILE}

run_test "launch" "launch.json"
run_test "register_tortuga" "register_tortuga.json"
run_test "register_tortuga_moxa" "register_tortuga_moxa.json"
run_test "query_all" "query_all.json"

echo "=== Fin de pruebas $(date) ===" >> ${LOG_FILE}
echo "Resultados guardados en: ${RESULTS_DIR}"
