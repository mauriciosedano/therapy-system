#!/bin/bash
cd lambda/src && zip -j ../function.zip index.py
aws lambda update-function-code \
  --function-name therapy-system \
  --zip-file fileb://../function.zip

