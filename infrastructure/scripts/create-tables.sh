#!/bin/bash

# Crear tabla de delegación de acceso
aws dynamodb create-table \
  --table-name AccessDelegation \
  --attribute-definitions \
    AttributeName=DelegationID,AttributeType=S \
    AttributeName=ApprenticeID,AttributeType=S \
  --key-schema \
    AttributeName=DelegationID,KeyType=HASH \
  --global-secondary-indexes \
    "[{
        \"IndexName\": \"ApprenticeIndex\",
        \"KeySchema\": [{\"AttributeName\":\"ApprenticeID\",\"KeyType\":\"HASH\"}],
        \"Projection\": {\"ProjectionType\":\"ALL\"},
        \"ProvisionedThroughput\": {\"ReadCapacityUnits\":5,\"WriteCapacityUnits\":5}
    }]" \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

# Crear tabla de auditoría
aws dynamodb create-table \
  --table-name AuditLog \
  --attribute-definitions \
    AttributeName=AuditID,AttributeType=S \
    AttributeName=PerformedBy,AttributeType=S \
    AttributeName=Timestamp,AttributeType=S \
  --key-schema \
    AttributeName=AuditID,KeyType=HASH \
  --global-secondary-indexes \
    "[{
        \"IndexName\": \"UserActionsIndex\",
        \"KeySchema\": [
            {\"AttributeName\":\"PerformedBy\",\"KeyType\":\"HASH\"},
            {\"AttributeName\":\"Timestamp\",\"KeyType\":\"RANGE\"}
        ],
        \"Projection\": {\"ProjectionType\":\"ALL\"},
        \"ProvisionedThroughput\": {\"ReadCapacityUnits\":5,\"WriteCapacityUnits\":5}
    }]" \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

# Agregar permisos en el template de CloudFormation
echo "Ahora actualiza el template de CloudFormation para incluir los permisos de las nuevas tablas"
