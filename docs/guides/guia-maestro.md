# docs/guides/master-guide.md

# Guía del Maestro - Sistema de Terapias Homeopáticas

## Comandos Principales

### 1. Gestión de Pacientes
```
"Alexa, registra un nuevo paciente [nombre] con teléfono [número]"
"Alexa, actualiza el teléfono de [paciente]"
"Alexa, consulta los datos de [paciente]"
```

### 2. Registro de Terapias
```
"Alexa, registra una terapia de [tipo] para [paciente]"
"Alexa, anota que [paciente] recibió [terapia]"
"Alexa, registra una sesión para [paciente]"
```

### 3. Fórmulas y Recetas
```
"Alexa, registra una fórmula de [tipo] para [paciente]"
"Alexa, consulta la última fórmula de [paciente]"
"Alexa, qué lleva la fórmula [nombre]"
```

### 4. Delegación y Supervisión
```
"Alexa, permite que [aprendiz] consulte las terapias de [paciente]"
"Alexa, autoriza a [aprendiz] para registrar terapias"
"Alexa, qué ha registrado [aprendiz] hoy"
```

## Flujos de Trabajo

### 1. Consulta Típica
1. Verificar historial del paciente
   ```
   "Alexa, cuándo vino [paciente] la última vez"
   "Alexa, qué terapia recibió [paciente]"
   ```

2. Registrar nueva terapia
   ```
   "Alexa, registra terapia para [paciente]"
   - Alexa preguntará el tipo de terapia
   "Acupuntura"
   - Alexa confirmará el registro
   ```

### 2. Supervisión de Aprendices
1. Autorizar acceso
   ```
   "Alexa, permite que Ana consulte las terapias de hoy"
   ```

2. Verificar actividades
   ```
   "Alexa, muestra el registro de Ana"
   ```

## Mejores Prácticas

1. **Registro de Pacientes**
   - Usar nombres completos
   - Verificar duplicados
   - Confirmar datos

2. **Delegación**
   - Especificar alcance temporal
   - Verificar actividades delegadas
   - Revocar accesos no necesarios

3. **Fórmulas**
   - Registrar componentes específicos
   - Incluir observaciones relevantes
   - Verificar historial de uso
