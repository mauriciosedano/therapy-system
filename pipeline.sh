#!/bin/bash
./infra/dynamodb/create-tables.sh
./infra/dynamodb/load-test-data.sh
./infra/lambda/update-code.sh
./infra/alexa/update-model.sh

