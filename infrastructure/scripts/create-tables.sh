#!/bin/bash
aws dynamodb create-table \
  --table-name TherapySystem_Homeopathy \
  --attribute-definitions \
      AttributeName=RemedyID,AttributeType=S \
      AttributeName=RemedyName,AttributeType=S \
  --key-schema \
      AttributeName=RemedyID,KeyType=HASH \
  --global-secondary-indexes '[
    {
      "IndexName": "RemedyNameIndex",
      "KeySchema": [{"AttributeName": "RemedyName", "KeyType": "HASH"}],
      "Projection": {"ProjectionType": "ALL"},
      "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
    }
  ]' \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

