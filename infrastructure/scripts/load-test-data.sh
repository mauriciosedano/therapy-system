#!/bin/bash
aws dynamodb put-item \
  --table-name TherapySystem_Homeopathy \
  --item '{
    "RemedyID": {"S": "WC001"},
    "RemedyName": {"S": "White Chestnut"},
    "Properties": {"S": "pensamientos recurrentes, insomnio por mente activa"},
    "Indications": {"S": "dificultad para dormir, pensamientos circulares"},
    "Contraindications": {"S": "no usar con sedantes fuertes"},
    "Combinations": {"S": "Cherry Plum para ansiedad, Star of Bethlehem para trauma"}
  }'

