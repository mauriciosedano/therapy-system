#!/bin/bash

# Eliminar recursos AWS
for TABLE in Patients Therapies Formulas AccessDelegation; do
    aws dynamodb delete-table --table-name $TABLE
done

aws lambda delete-function --function-name therapy-system

# No eliminamos el skill de Alexa, solo deshabilitamos el endpoint
aws lambda remove-permission     --function-name therapy-system     --statement-id alexa-skill-kit

echo "Resources cleaned up successfully"
