# 🔍 Altice File Comparator

[![Versión](https://img.shields.io/badge/versión-1.2.0-blue.svg)](https://github.com/altice-dominicana/file-comparator)
[![Licencia](https://img.shields.io/badge/licencia-Altice%20Proprietary-red.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/plataforma-Windows%2010+-brightgreen.svg)](https://microsoft.com/windows)

## 📋 Descripción

**Altice File Comparator** es una herramienta profesional desarrollada específicamente para el equipo de Altice Dominicana para comparar archivos CSV, Excel (.xlsx) y XLS de manera inteligente y precisa. La aplicación proporciona análisis detallados con visualizaciones interactivas, reportes completos y una biblioteca de archivos de referencia.

## ✨ Características Principales

### 🔍 **Comparación Inteligente**

- Análisis automático de estructura y contenido
- Detección precisa de diferencias celda por celda
- Identificación de filas y columnas agregadas/eliminadas
- Comparación de datos únicos entre archivos

### 📊 **Visualizaciones Avanzadas**

- Gráficos circulares de tipos de diferencias
- Gráficos de barras para comparación de estructura
- Líneas de tendencia de datos
- Estadísticas interactivas en tiempo real

### 📚 **Biblioteca de Referencias**

- Almacenamiento local de archivos de referencia
- Reutilización fácil para múltiples comparaciones
- Gestión de metadatos y etiquetas
- Búsqueda y filtrado avanzado

### 📈 **Reportes Profesionales**

- Exportación en múltiples formatos (JSON, Excel, CSV, PDF, TXT)
- Reportes detallados con gráficos incluidos
- Metadatos completos de comparación
- Plantillas personalizables

### 💾 **Base de Datos Integrada**

- SQLite embebido para almacenamiento local
- Historial completo de comparaciones
- Backup automático y restauración
- Optimización automática de rendimiento

## 🎯 Formatos Soportados

| Formato | Extensión | Descripción |
|---------|-----------|-------------|
| **CSV** | `.csv` | Valores separados por comas |
| **Excel Moderno** | `.xlsx` | Formato Excel 2007+ |
| **Excel Legacy** | `.xls` | Formato Excel 97-2003 |

## 💻 Requisitos del Sistema

### **Mínimos**

- Windows 10 de 64 bits
- 4 GB de RAM
- 500 MB de espacio libre
- Procesador de 2 GHz

### **Recomendados**

- Windows 11 de 64 bits
- 8 GB de RAM
- 2 GB de espacio libre
- Procesador de 3 GHz o superior

## 📦 Instalación

### **Instalación Automática**

1. Descargue `AlticeFileComparator-Setup.exe`
2. Ejecute como administrador
3. Siga el asistente de instalación
4. El acceso directo se creará automáticamente en el escritorio

### **Versión Portable**

1. Descargue `AlticeFileComparator-Portable.zip`
2. Extraiga en cualquier ubicación
3. Ejecute `AlticeFileComparator.exe`
4. No requiere instalación ni permisos de administrador

## 🚀 Inicio Rápido

### **Primera Comparación**

1. **Abra la aplicación** desde el acceso directo del escritorio
2. **Seleccione archivos**:
   - Archivo de referencia (lado izquierdo)
   - Archivo a comparar (lado derecho)
3. **Haga clic en "Iniciar Comparación"**
4. **Revise los resultados** en los gráficos y tablas
5. **Exporte el reporte** si es necesario

### **Usar la Biblioteca**

1. **Vaya a la sección "Biblioteca"**
2. **Agregue archivos de referencia** frecuentemente usados
3. **Use archivos de la biblioteca** para futuras comparaciones
4. **Gestione** con etiquetas y descripciones

## 📊 Interpretación de Resultados

### **Archivos Idénticos** ✅

- **Indicador**: Mensaje verde "¡Archivos Idénticos!"
- **Significado**: Los archivos son exactamente iguales en estructura y contenido

### **Tipos de Diferencias**

| Tipo | Color | Descripción |
|------|-------|-------------|
| **Celdas Modificadas** | 🔴 Rojo | Valores que cambiaron entre archivos |
| **Filas Agregadas** | 🟢 Verde | Nuevas filas en el archivo de comparación |
| **Filas Eliminadas** | 🔵 Azul | Filas que faltan en el archivo de comparación |
| **Columnas Agregadas** | 🟡 Amarillo | Nuevas columnas en el archivo de comparación |
| **Columnas Eliminadas** | 🟣 Púrpura | Columnas que faltan en el archivo de comparación |
| **Únicos en Referencia** | 🟠 Naranja | Registros solo en el archivo de referencia |
| **Únicos en Comparación** | 🔵 Cian | Registros solo en el archivo de comparación |

## 🛠️ Características Avanzadas

### **Configuración Personalizada**

- Ajustes de rendimiento
- Temas claro/oscuro
- Configuración de notificaciones
- Gestión de almacenamiento

### **Mantenimiento Automático**

- Limpieza automática de archivos temporales
- Optimización de base de datos
- Backup programado
- Actualización de estadísticas

### **Atajos de Teclado**

| Atajo | Acción |
|-------|--------|
| `Ctrl + N` | Nueva comparación |
| `Ctrl + O` | Abrir archivo |
| `Ctrl + S` | Guardar comparación |
| `Ctrl + E` | Exportar reporte |
| `F5` | Actualizar vista |
| `F1` | Mostrar ayuda |

## 📁 Estructura de Archivos

Altice File Comparator/
├── 📁 data/                    # Datos de aplicación
│   ├── database/               # Base de datos SQLite
│   ├── reference_files/        # Archivos de referencia
│   ├── exports/               # Reportes exportados
│   └── temp/                  # Archivos temporales
├── 📁 docs/                   # Documentación
├── 📁 examples/               # Archivos de ejemplo
└── 📁 logs/                   # Archivos de registro

## 🔧 Solución de Problemas

### **Problemas Comunes**

#### **Error al cargar archivo**

- ✅ Verifique que el archivo no esté abierto en otra aplicación
- ✅ Confirme que el formato es compatible (CSV, XLSX, XLS)
- ✅ Asegúrese de que el archivo no esté corrupto

#### **Comparación muy lenta**

- ✅ Verifique el tamaño del archivo (máximo 50 MB)
- ✅ Cierre otras aplicaciones pesadas
- ✅ Optimice la base de datos desde Configuración

#### **Error de base de datos**

- ✅ Reinicie la aplicación
- ✅ Ejecute optimización desde Herramientas > Configuración
- ✅ Restaure desde backup si es necesario

### **Obtener Ayuda**

1. **Documentación**: Menú Ayuda > Guía de Usuario
2. **Ejemplos**: Carpeta `examples` en la instalación
3. **Soporte técnico**: <it-support@altice.com.do>
4. **Teléfono**: +1 (809) 200-1000 ext. 1234

## 📈 Casos de Uso Comunes

### **Control de Calidad**

Verificar que los datos no se corrompieron durante transferencias o migraciones.

### **Auditoría de Datos**

Comparar versiones de archivos para detectar cambios no autorizados o identificar actualizaciones.

### **Validación de Procesos**

Confirmar que los procesos automatizados generan los resultados esperados.

### **Análisis de Diferencias**

Identificar qué datos específicos cambiaron entre diferentes versiones de un dataset.

## 🏢 Información Corporativa

### **Desarrollado para**

**Altice Dominicana** - Departamento de Tecnología de la Información

### **Desarrollador**

**Charles Lantigua Jorge**  
Pasante - IT Department  

### **Licencia**

Software propietario de Altice Dominicana. Todos los derechos reservados.  
Uso restringido al personal autorizado de Altice Dominicana.

### **Versión**

**2.1.0** - Junio 2025

### **Historial de Versiones**



## 🤝 Soporte y Contacto

### **Reportar Problemas**

Incluya la siguiente información al reportar problemas:

- Versión de la aplicación
- Sistema operativo
- Descripción detallada del problema
- Pasos para reproducir el error
- Archivos de ejemplo (si es posible)

---

**© 2025 Altice Dominicana. Todos los derechos reservados.**
