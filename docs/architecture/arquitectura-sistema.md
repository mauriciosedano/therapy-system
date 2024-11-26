# docs/architecture/arquitectura-sistema.md

# Arquitectura del Sistema de Terapias Homeopáticas

## 1. Visión General

El sistema está construido sobre AWS, utilizando servicios serverless para maximizar escalabilidad y minimizar costos operativos. La interacción principal se realiza a través de Alexa, permitiendo un control por voz natural e intuitivo.

## 2. Componentes Principales

### 2.1 Interfaz de Usuario (Alexa Skill)
- **Invocación**: "Alexa, abre terapias homeopáticas"
- **Intents Principales**:
  ```
  - Registro de pacientes y terapias
  - Consulta de historiales
  - Gestión de fórmulas
  - Delegación de accesos
  ```

### 2.2 Backend (AWS Lambda)
- **Funciones Core**:
  ```
  - Procesamiento de intents
  - Validación de datos
  - Gestión de sesiones
  - Control de acceso
  ```

### 2.3 Base de Datos (DynamoDB)
```
Patients
├── PatientID (PK)
├── Name
├── Phone
├── RegisterDate
└── LastUpdate

Therapies
├── TherapyID (PK)
├── PatientID (SK)
├── Type
├── Date
└── Observations

Formulas
├── FormulaID (PK)
├── Name
├── Components
└── Instructions
```

## 3. Flujos de Interacción

### 3.1 Registro de Terapia
- Usuario dice: "Registra terapia para Juan"
- Alexa procesa intent y solicita tipo de terapia
- Lambda valida datos y registra en DynamoDB
- Alexa confirma el registro

### 3.2 Delegación de Acceso
- Maestro solicita: "Permite a Ana consultar"
- Sistema verifica permisos del maestro
- Se registran permisos temporales
- Se confirma la delegación

## 4. Seguridad y Permisos

### 4.1 Niveles de Acceso
1. **Maestro**
   - Acceso completo al sistema
   - Capacidad de delegación
   - Gestión de permisos

2. **Aprendiz**
   - Consulta de información autorizada
   - Registro supervisado de terapias
   - Sin acceso a delegación

## 5. Monitoreo

### 5.1 CloudWatch Metrics
- Latencia de respuestas
- Errores de procesamiento
- Uso de intents
- Patrones de acceso

### 5.2 Alertas Configuradas
- Errores críticos
- Latencia elevada
- Fallos de autenticación
