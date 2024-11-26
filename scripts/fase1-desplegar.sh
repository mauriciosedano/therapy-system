#!/bin/bash

# Configurar variables
export NOMBRE_PILA="sistema-terapias"
export ENTORNO="produccion"
export REGION="us-east-1"

# Crear red base
aws cloudformation deploy \
  --template-file infrastructure/cloudformation/red.yml \
  --stack-name ${NOMBRE_PILA}-red \
  --parameter-overrides Entorno=${ENTORNO}

# Desplegar almacenamiento
aws cloudformation deploy \
  --template-file infrastructure/cloudformation/almacenamiento.yml \
  --stack-name ${NOMBRE_PILA}-almacenamiento \
  --parameter-overrides \
    Entorno=${ENTORNO} \
    PilaRed=${NOMBRE_PILA}-red

# Crear tablas principales
aws dynamodb create-table \
  --cli-input-json file://infrastructure/dynamodb/tablas/recetas.json

aws dynamodb create-table \
  --cli-input-json file://infrastructure/dynamodb/tablas/esencias.json

aws dynamodb create-table \
  --cli-input-json file://infrastructure/dynamodb/tablas/componentes.json
