#!/bin/bash

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/therapy_system_${TIMESTAMP}"
SKILL_ID="amzn1.ask.skill.028ef8b0-b7cd-45e7-bc9c-08a4a213921e"

mkdir -p "${BACKUP_DIR}"/{aws,alexa}

# Backup DynamoDB
for TABLE in Patients Therapies Formulas AccessDelegation; do
    aws dynamodb create-backup         --table-name $TABLE         --backup-name "${TABLE}_${TIMESTAMP}"
    
    aws dynamodb scan         --table-name $TABLE > "${BACKUP_DIR}/aws/${TABLE}_data.json"
done

# Backup Lambda
aws lambda get-function     --function-name therapy-system     --query 'Code.Location'     --output text | xargs curl -o "${BACKUP_DIR}/aws/lambda.zip"

# Backup Alexa Skill
ask api get-skill -s $SKILL_ID > "${BACKUP_DIR}/alexa/skill_manifest.json"
ask api get-interaction-model -s $SKILL_ID -l es-ES > "${BACKUP_DIR}/alexa/interaction_model.json"

tar -czf "therapy_system_${TIMESTAMP}.tar.gz" "${BACKUP_DIR}"
