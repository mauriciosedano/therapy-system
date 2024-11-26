#!/bin/bash

# Insertar una delegación de prueba
aws dynamodb put-item \
  --table-name AccessDelegation \
  --item '{
    "DelegationID": {"S": "D1"},
    "MasterID": {"S": "M1"},
    "ApprenticeID": {"S": "A1"},
    "Permissions": {"SS": ["consultar pacientes"]},
    "ExpirationDate": {"S": "2024-12-31T23:59:59Z"},
    "Status": {"S": "ACTIVE"},
    "CreatedAt": {"S": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"}'
  }'

# Insertar una entrada de auditoría de prueba
aws dynamodb put-item \
  --table-name AuditLog \
  --item '{
    "AuditID": {"S": "A1"},
    "ActionType": {"S": "CONSULTA_PACIENTE"},
    "PerformedBy": {"S": "A1"},
    "Timestamp": {"S": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"},
    "Details": {"S": "{\"paciente\":\"Juan Pérez\"}"}'
  }'

echo "✅ Datos de prueba insertados exitosamente"
