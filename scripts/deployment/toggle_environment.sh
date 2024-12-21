#!/bin/bash

STAGE=$1
SKILL_ID="amzn1.ask.skill.028ef8b0-b7cd-45e7-bc9c-08a4a213921e"
CONFIG_FILE="config/environments/${STAGE}.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file $CONFIG_FILE not found"
    exit 1
fi

# Cargar configuración
DYNAMO_READ=$(jq -r '.dynamodb.readCapacityUnits' "$CONFIG_FILE")
DYNAMO_WRITE=$(jq -r '.dynamodb.writeCapacityUnits' "$CONFIG_FILE")
LAMBDA_MEMORY=$(jq -r '.lambda.memorySize' "$CONFIG_FILE")
LAMBDA_TIMEOUT=$(jq -r '.lambda.timeout' "$CONFIG_FILE")
CW_RETENTION=$(jq -r '.cloudwatch.retentionDays' "$CONFIG_FILE")

# Actualizar DynamoDB
for TABLE in Patients Therapies Formulas AccessDelegation; do
    aws dynamodb update-table         --table-name $TABLE         --provisioned-throughput ReadCapacityUnits=$DYNAMO_READ,WriteCapacityUnits=$DYNAMO_WRITE
done

# Actualizar Lambda
aws lambda update-function-configuration     --function-name therapy-system     --memory-size $LAMBDA_MEMORY     --timeout $LAMBDA_TIMEOUT     --environment Variables={STAGE=$STAGE}

# Actualizar CloudWatch
aws logs put-retention-policy     --log-group-name /aws/lambda/therapy-system     --retention-in-days $CW_RETENTION

echo "Environment switched to $STAGE mode"
