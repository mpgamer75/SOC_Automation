# 🔍 Altice File Comparator

## Descripción General

**Altice File Comparator** es una herramienta avanzada de comparación de archivos que permite analizar diferencias entre documentos CSV, Excel (.xlsx) y XLS de manera inteligente. La aplicación proporciona análisis detallados con visualizaciones interactivas y reportes completos.

## 🚀 Características Principales

- **Comparación Inteligente**: Analiza tanto la estructura como el contenido de los archivos
- **Visualizaciones Interactivas**: Gráficos y estadísticas en tiempo real
- **Múltiples Formatos**: Soporte para CSV, XLSX y XLS
- **Reportes Detallados**: Exportación en JSON, TXT, CSV y XLSX
- **Interfaz Moderna**: Diseño responsive y fácil de usar

## 📊 Explicación Detallada de las Estadísticas

### 1. **Resumen General (Summary)**

Esta sección proporciona una visión general de la comparación:

- **Total de Filas**: Número máximo de filas entre ambos archivos
- **Total de Columnas**: Número máximo de columnas entre ambos archivos
- **Diferencias Encontradas**: Cantidad total de discrepancias detectadas
- **Tiempo de Procesamiento**: Duración del análisis

### 2. **Gráfico de Diferencias (Differences Chart)**

Visualización en forma de gráfico circular que muestra:

- **🟢 Celdas Modificadas**: Valores que cambiaron entre los archivos
- **🟢 Filas Agregadas**: Nuevas filas presentes solo en el archivo de comparación
- **🔵 Filas Eliminadas**: Filas que existen en referencia pero no en comparación
- **🟡 Columnas Agregadas**: Nuevas columnas en el archivo de comparación
- **🟣 Columnas Eliminadas**: Columnas que faltan en el archivo de comparación
- **🟠 Únicos en Referencia**: Registros que solo existen en el archivo de referencia
- **🔵 Únicos en Comparación**: Registros que solo existen en el archivo de comparación

### 3. **Estructura de Datos (Data Structure)**

Compara las dimensiones de ambos archivos:

- **Referencia**: Número de filas y columnas del archivo base
- **Comparación**: Número de filas y columnas del archivo a analizar

### 4. **Tendencias de Datos (Data Trends)**

Gráfico de líneas que muestra la evolución de las dimensiones:

- **Línea Azul**: Número de filas por archivo
- **Línea Verde**: Número de columnas por archivo

### 5. **Diferencias Detalladas (Detailed Differences)**

Tabla que lista cada diferencia encontrada con:

- **Tipo**: Categoría de la diferencia (celda modificada, fila agregada, etc.)
- **Posición**: Ubicación exacta (fila y columna)
- **Descripción**: Explicación detallada de la diferencia
- **Valor Referencia**: Contenido original del archivo base
- **Valor Comparación**: Contenido del archivo analizado

### 6. **Contenido Diferenciador (Different Content)**

#### **Únicos en Referencia** 🔴

- **¿Qué son?**: Registros que existen **únicamente** en el archivo de referencia
- **¿Cuándo aparecen?**: Cuando hay filas completas que no tienen equivalente en el archivo de comparación
- **Ejemplo**: Si el archivo de referencia tiene 100 filas y el de comparación solo 95, las 5 filas faltantes aparecerán aquí
- **Importancia**: Indica datos que se perdieron o fueron eliminados

#### **Únicos en Comparación** 🔵

- **¿Qué son?**: Registros que existen **únicamente** en el archivo de comparación
- **¿Cuándo aparecen?**: Cuando hay filas nuevas que no existían en el archivo de referencia
- **Ejemplo**: Si el archivo de comparación tiene 105 filas y el de referencia solo 100, las 5 filas nuevas aparecerán aquí
- **Importancia**: Indica datos nuevos que fueron agregados

#### **Columnas Únicas**

- **Columnas solo en Referencia**: Campos que existen en el archivo base pero no en el de comparación
- **Columnas solo en Comparación**: Nuevos campos agregados en el archivo analizado

### 7. **Interpretación de Resultados**

#### **Archivos Idénticos** ✅

- **Condición**: Cuando no se encuentran diferencias
- **Indicador**: Mensaje verde "¡Archivos Idénticos!"
- **Significado**: Los archivos son exactamente iguales en estructura y contenido

#### **Diferencias Estructurales** ⚠️

- **Columnas faltantes**: Datos que se perdieron en el proceso
- **Columnas nuevas**: Información adicional agregada
- **Diferente número de filas**: Datos agregados o eliminados

#### **Diferencias de Contenido** 🔍

- **Celdas modificadas**: Valores que cambiaron
- **Filas únicas**: Registros completos que son exclusivos de cada archivo

## 🛠️ Instalación y Uso

### Requisitos Previos

- Python 3.8+
- Node.js 16+
- npm o yarn

### Instalación Backend

```bash
cd SOC_Automation/backend
pip install -r requirements.txt
```

### Instalación Frontend

```bash
cd SOC_Automation/frontend
npm install
```

### Ejecución

```bash
# Terminal 1 - Backend
cd SOC_Automation/backend
python main.py

# Terminal 2 - Frontend
cd SOC_Automation/frontend
npm run dev
```

## 📁 Formatos Soportados

- **CSV**: Archivos de valores separados por comas
- **XLSX**: Archivos Excel modernos
- **XLS**: Archivos Excel legacy

## 🔧 Configuración Avanzada

### Codificaciones Soportadas para CSV

- UTF-8
- Latin-1
- CP1252

### Límites de Rendimiento

- Máximo 50 registros únicos mostrados por archivo
- Máximo 100 diferencias detalladas
- Tiempo de procesamiento optimizado

## 📈 Casos de Uso Comunes

1. **Control de Calidad**: Verificar que los datos no se corrompieron durante transferencias
2. **Auditoría**: Comparar versiones de archivos para detectar cambios no autorizados
3. **Migración de Datos**: Validar que la migración de sistemas fue exitosa
4. **Análisis de Diferencias**: Identificar qué datos cambiaron entre versiones

## 🚨 Solución de Problemas

### Error de Importación de Recharts

```bash
cd SOC_Automation/frontend
npm install --save-dev @types/recharts
```

### Error de Codificación CSV

- Verificar que el archivo use una codificación soportada
- Convertir a UTF-8 si es necesario

### Archivos Muy Grandes

- Considerar dividir archivos grandes en secciones
- El sistema está optimizado para archivos de tamaño moderado

## 📞 Soporte

Pronto :D

## Author

- Charles Lantigua Jorge -mpgamer75

---

**Desarrollado para el equipo IT de Altice Dominicana - Herramienta de Comparación de Archivos Inteligente** 🔍
