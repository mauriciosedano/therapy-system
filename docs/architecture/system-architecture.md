# Arquitectura del Sistema

## 1. Componentes Principales

### 1.1 Frontend
- Alexa Skill
  - Manejo de voz
  - Procesamiento de intents
  - Diálogos multiturno

### 1.2 Backend
- AWS Lambda
  - Procesamiento de solicitudes
  - Validación de datos
  - Lógica de negocio

### 1.3 Base de Datos
- DynamoDB
  - Almacenamiento NoSQL
  - Índices secundarios
  - Alta disponibilidad

## 2. Flujos de Datos

### 2.1 Registro de Información
1. Captura por voz (Alexa)
2. Procesamiento de intent (Lambda)
3. Validación de datos
4. Almacenamiento en DynamoDB

### 2.2 Consultas
1. Solicitud por voz
2. Búsqueda en base de datos
3. Procesamiento de resultados
4. Respuesta formateada
