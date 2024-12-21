#!/bin/bash

# Obtener costos DynamoDB
aws cloudwatch get-metric-statistics     --namespace AWS/DynamoDB     --metric-name ConsumedWriteCapacityUnits     --dimensions Name=TableName,Value=Patients     --start-time $(date -v-1d +%Y-%m-%dT%H:%M:%S)     --end-time $(date +%Y-%m-%dT%H:%M:%S)     --period 86400     --statistics Sum

# Obtener invocaciones Lambda
aws cloudwatch get-metric-statistics     --namespace AWS/Lambda     --metric-name Invocations     --dimensions Name=FunctionName,Value=therapy-system     --start-time $(date -v-1d +%Y-%m-%dT%H:%M:%S)     --end-time $(date +%Y-%m-%dT%H:%M:%S)     --period 86400     --statistics Sum
