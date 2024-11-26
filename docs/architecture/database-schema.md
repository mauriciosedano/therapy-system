# Esquema de Base de Datos

## 1. Tablas Principales

### 1.1 Patients
- PatientID (PK)
- Name
- Phone
- RegisterDate
- LastUpdate

### 1.2 Therapies
- TherapyID (PK)
- PatientID (FK)
- TherapyType
- Date
- Notes
- CreatedBy

### 1.3 Formulas
- FormulaID (PK)
- PatientID (FK)
- FormulaType
- Components
- Date
- CreatedBy

## 2. Índices

### 2.1 Patients
- NameIndex (GSI)
  - Name (PK)
  - PatientID (SK)

### 2.2 Therapies
- PatientTherapyIndex (GSI)
  - PatientID (PK)
  - Date (SK)

## 3. Relaciones y Constraints
[Diagrama de relaciones aquí]
