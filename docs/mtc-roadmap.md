# ROADMAP MTC 2024-2025

## V1.0 CORE (ACTUAL)
Estado: ✅ Operativa

### Capacidades
- Registro básico de terapias
- Consultas simples
- Infraestructura base AWS
- Seguridad básica

### Limitaciones Identificadas
- No mantiene contexto conversacional
- No maneja confirmaciones naturales
- Referencias informales no soportadas
- Sin manejo de duplicados
- Sin validación de nombres similares
- Sin patrones de terapia

## V2.0 DIÁLOGO NATURAL + HOMEOPATÍA (Q1 2025)
Estado: 🟡 En Planificación

### Capacidades de Diálogo
1. **Procesamiento Natural**
   - Reconocimiento contextual
   - Referencias informales
   - Confirmaciones fluidas
   - Validación de nombres similares

2. **Base de Conocimientos**
   - Propiedades de remedios
   - Indicaciones y contraindicaciones
   - Combinaciones recomendadas
   - Dosificación y preparación

3. **Gestión de Fórmulas**
   - Registro de composiciones
   - Cálculo de proporciones
   - Variaciones personalizadas
   - Control de inventario

### Cambios Técnicos
1. **Base de Datos**
   ```yaml
   HomeopathicKnowledge:
     - RemedyID
     - Properties
     - Indications
     - Contraindications
     - Combinations
     - Dosage
   
   Formulas:
     - FormulaID
     - BaseComposition
     - Variations
     - Usage
     - Inventory
   ```

2. **Lambda Functions**
   - Procesamiento de lenguaje natural
   - Gestión de contexto
   - Validación de fórmulas
   - Control de inventario

## V3.0 DELEGACIÓN Y PERFILES (Q2 2025)
Estado: 🔵 Planificado

### Capacidades
1. **Gestión de Accesos**
   - Perfiles de usuario
   - Niveles de autorización
   - Reconocimiento de voz
   - Delegación temporal

2. **Seguridad**
   - Autenticación por voz
   - Tokens temporales
   - Registro de actividades
   - Control de accesos

### Cambios Técnicos
1. **Base de Datos**
   ```yaml
   UserProfiles:
     - UserID
     - VoiceSignature
     - AccessLevel
     - Permissions
   
   AccessLogs:
     - AccessID
     - UserID
     - ActionType
     - Timestamp
   ```

## PLAN DE IMPLEMENTACIÓN

### V2.0 (Q1 2025)
1. Sprint 1: Base de Conocimientos
   - Estructura de datos remedios
   - Migración de información
   - API de consulta

2. Sprint 2: Diálogo Natural
   - Procesamiento de lenguaje
   - Gestión de contexto
   - Validaciones de nombres

3. Sprint 3: Gestión de Fórmulas
   - Registro y composición
   - Control de inventario
   - Validación de combinaciones

4. Sprint 4: Integración
   - Pruebas end-to-end
   - Optimización de respuestas
   - Documentación

### V3.0 (Q2 2025)
1. Sprint 1: Perfiles Base
   - Estructura de usuarios
   - Niveles de acceso
   - Reconocimiento básico

2. Sprint 2: Delegación
   - Sistema de autorizaciones
   - Tokens temporales
   - Registro de actividades

3. Sprint 3: Seguridad
   - Autenticación por voz
   - Auditoría de accesos
   - Protección de datos

4. Sprint 4: Validación
   - Pruebas de seguridad
   - Optimización de accesos
   - Documentación final

## MÉTRICAS DE ÉXITO
1. Precisión en reconocimiento de intención > 95%
2. Tiempo de respuesta < 2 segundos
3. Tasa de error en fórmulas < 0.1%
4. Satisfacción de usuario > 90%

## DEPENDENCIAS CRÍTICAS
1. Datos de remedios homeopáticos validados
2. Infraestructura AWS escalada
3. Modelos de lenguaje natural entrenados
4. Sistema de reconocimiento de voz afinado

## RIESGOS IDENTIFICADOS
1. Complejidad en procesamiento de lenguaje natural
2. Precisión en validación de fórmulas
3. Latencia en reconocimiento de voz
4. Seguridad en delegación de accesos
