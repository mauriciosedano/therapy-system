#!/bin/bash

echo "🚀 Creando tablas core del sistema..."

# Crear tabla de Pacientes
echo "📋 Creando tabla Patients..."
aws dynamodb create-table \
  --table-name Patients \
  --attribute-definitions \
    AttributeName=PatientID,AttributeType=S \
    AttributeName=Name,AttributeType=S \
  --key-schema \
    AttributeName=PatientID,KeyType=HASH \
  --global-secondary-indexes \
    "[{
        \"IndexName\": \"NameIndex\",
        \"KeySchema\": [{\"AttributeName\":\"Name\",\"KeyType\":\"HASH\"}],
        \"Projection\": {\"ProjectionType\":\"ALL\"},
        \"ProvisionedThroughput\": {\"ReadCapacityUnits\":5,\"WriteCapacityUnits\":5}
    }]" \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

# Crear tabla de Terapias
echo "📋 Creando tabla Therapies..."
aws dynamodb create-table \
  --table-name Therapies \
  --attribute-definitions \
    AttributeName=TherapyID,AttributeType=S \
    AttributeName=PatientID,AttributeType=S \
    AttributeName=Date,AttributeType=S \
  --key-schema \
    AttributeName=TherapyID,KeyType=HASH \
  --global-secondary-indexes \
    "[{
        \"IndexName\": \"PatientIndex\",
        \"KeySchema\": [
            {\"AttributeName\":\"PatientID\",\"KeyType\":\"HASH\"},
            {\"AttributeName\":\"Date\",\"KeyType\":\"RANGE\"}
        ],
        \"Projection\": {\"ProjectionType\":\"ALL\"},
        \"ProvisionedThroughput\": {\"ReadCapacityUnits\":5,\"WriteCapacityUnits\":5}
    }]" \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

echo "✅ Tablas creadas exitosamente"

# Insertar algunos datos de prueba
echo "📝 Insertando datos de prueba..."

# Paciente de prueba
aws dynamodb put-item \
  --table-name Patients \
  --item '{
    "PatientID": {"S": "TEST_PATIENT_1"},
    "Name": {"S": "Juan Pérez"},
    "Phone": {"S": "123-456-7890"},
    "RegisterDate": {"S": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"}
  }'

# Terapia de prueba
aws dynamodb put-item \
  --table-name Therapies \
  --item '{
    "TherapyID": {"S": "TEST_THERAPY_1"},
    "PatientID": {"S": "TEST_PATIENT_1"},
    "TherapyType": {"S": "Acupuntura"},
    "Date": {"S": "'$(date -u +"%Y-%m-%d")'"},
    "Timestamp": {"S": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"}
  }'

echo "✅ Datos de prueba insertados exitosamente"
