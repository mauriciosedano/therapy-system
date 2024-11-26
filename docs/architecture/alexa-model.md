# Modelo de Interacción de Alexa

## 1. Estructura Principal

### 1.1 Invocación
- Nombre: "terapias homeopáticas"
- Ejemplo: "Alexa, abre terapias homeopáticas"

### 1.2 Intents Principales
- RegistrarPacienteIntent
- RegistrarTerapiaIntent
- ConsultarTerapiaIntent
- RegistrarFormulaIntent
- ConsultarHistorialIntent

### 1.3 Slots
- Paciente (AMAZON.Person)
- TipoTerapia (TerapiaType)
- Fecha (AMAZON.DATE)
- Telefono (AMAZON.PhoneNumber)

## 2. Flujos de Diálogo

### 2.1 Registro de Paciente
```text
Usuario: "Registra nuevo paciente"
Alexa: "¿Cuál es el nombre del paciente?"
Usuario: [nombre]
Alexa: "¿Cuál es su teléfono?"
Usuario: [teléfono]
Alexa: "Paciente registrado correctamente"
```

### 2.2 Registro de Terapia
```text
Usuario: "Registra una terapia"
Alexa: "¿Para qué paciente?"
Usuario: [paciente]
Alexa: "¿Qué tipo de terapia?"
Usuario: [tipo]
Alexa: "Terapia registrada"
```

## 3. Tipos Personalizados

### 3.1 TerapiaType
- Homeopatía
- Moxibustión
- Acupuntura
- Flores de Bach

### 3.2 FormulaType
- Arnica Montana
- Belladona
- Calendula
- Chamomilla
- Rescue Remedy
