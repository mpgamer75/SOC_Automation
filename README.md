# 🔍 Altice File Comparator - Comparador Inteligente de Archivos

Una aplicación web avanzada para comparar archivos CSV, Excel y XLS con análisis detallado y visualizaciones interactivas. Desarrollada para equipos SOC (Security Operations Center) y administradores de sistemas que necesitan identificar diferencias precisas entre conjuntos de datos.

## ✨ Características Principales

### 🔄 Comparación Inteligente
- **Comparación de múltiples formatos**: CSV, Excel (.xlsx, .xls)
- **Análisis estructural**: Detección de diferencias en columnas y filas
- **Comparación de contenido**: Análisis celda por celda
- **Contenido diferenciador**: Identificación de elementos únicos en cada archivo

### 📊 Visualizaciones Avanzadas
- **Gráficos interactivos**: Gráficos de barras, líneas y circular
- **Estadísticas en tiempo real**: Métricas detalladas de diferencias
- **Dashboard responsivo**: Interfaz moderna y fácil de usar
- **Reportes exportables**: Múltiples formatos (JSON, TXT, CSV, Excel)

### 🎯 Funcionalidades Especializadas

#### Contenido Diferenciador
La aplicación ahora incluye una funcionalidad avanzada que identifica y muestra el contenido que diferencia los dos documentos:

- **Elementos únicos en referencia**: Datos presentes solo en el archivo de referencia
- **Elementos únicos en comparación**: Datos presentes solo en el archivo a comparar
- **Columnas únicas**: Identificación de columnas específicas de cada archivo
- **Análisis de filas**: Detección de registros únicos basada en columnas comunes

#### Casos de Uso Especializados
- **Inventario de máquinas**: Comparar listas de equipos en Active Directory
- **Control de acceso**: Identificar usuarios nuevos o eliminados
- **Auditoría de datos**: Detectar cambios en bases de datos
- **Análisis de logs**: Comparar archivos de registro de seguridad

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- Node.js 16+
- npm o yarn

### Instalación Rápida

#### Opción 1: Script Automático (Recomendado)
```bash
# Ejecutar el script de instalación automática
./demarrer_application.bat
```

#### Opción 2: Instalación Manual

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd SOC_Automation
```

2. **Configurar el Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configurar el Frontend**
```bash
cd ../frontend
npm install
```

## 🎮 Uso de la Aplicación

### Inicio Rápido

#### Desarrollo
```bash
python start_dev.py
```

#### Producción
```bash
python start_production.py
```

### Interfaz de Usuario

1. **Selección de Archivos**
   - Arrastra y suelta archivos o haz clic para seleccionar
   - Soporte para múltiples formatos (CSV, Excel)
   - Validación automática de archivos

2. **Análisis de Comparación**
   - Comparación automática al hacer clic en "Comparar Archivos"
   - Procesamiento en tiempo real con indicador de progreso
   - Detección automática de diferencias estructurales y de contenido

3. **Visualización de Resultados**
   - **Dashboard principal**: Estadísticas generales y gráficos
   - **Diferencias detalladas**: Tabla con todas las diferencias encontradas
   - **Contenido diferenciador**: Elementos únicos en cada archivo
   - **Información de comparación**: Metadatos del proceso

### Exportación de Reportes

La aplicación permite exportar reportes en múltiples formatos:

- **JSON**: Datos completos en formato estructurado
- **TXT**: Reporte legible con formato de texto
- **CSV**: Datos tabulares para análisis posterior
- **Excel**: Formato compatible con Microsoft Excel

## 📁 Estructura del Proyecto

```
SOC_Automation/
├── backend/                 # API FastAPI
│   ├── main.py             # Servidor principal
│   ├── file_comparator.py  # Lógica de comparación
│   ├── config.py           # Configuración
│   └── requirements.txt    # Dependencias Python
├── frontend/               # Aplicación Next.js
│   ├── src/
│   │   ├── app/           # Páginas de la aplicación
│   │   └── components/    # Componentes React
│   ├── package.json       # Dependencias Node.js
│   └── tailwind.config.ts # Configuración de estilos
├── examples/              # Archivos de ejemplo
│   ├── maquinas_referencia.csv
│   └── maquinas_nuevas.csv
├── start_dev.py          # Script de desarrollo
├── start_production.py   # Script de producción
├── test_app.py           # Script de pruebas
└── demarrer_application.bat # Script de inicio Windows
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Backend
BACKEND_HOST=localhost
BACKEND_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Personalización de Estilos
El frontend utiliza Tailwind CSS para estilos. Puedes personalizar:
- Colores del tema en `tailwind.config.ts`
- Componentes en `src/components/`
- Páginas en `src/app/`

## 🧪 Pruebas

### Archivos de Ejemplo
El proyecto incluye archivos de ejemplo para probar la funcionalidad:

1. **maquinas_referencia.csv**: Lista de máquinas en Active Directory
2. **maquinas_nuevas.csv**: Lista actualizada con nuevas máquinas

### Ejecutar Pruebas
```bash
python test_app.py
```

## 📊 Funcionalidades de Comparación

### Análisis Estructural
- **Columnas**: Detección de columnas agregadas, eliminadas o modificadas
- **Filas**: Identificación de filas nuevas, eliminadas o modificadas
- **Tipos de datos**: Validación de formatos y tipos

### Análisis de Contenido
- **Comparación celda por celda**: Detección de valores modificados
- **Elementos únicos**: Identificación de registros únicos en cada archivo
- **Claves de comparación**: Análisis basado en columnas comunes

### Reportes Detallados
- **Estadísticas generales**: Totales, diferencias, tiempo de procesamiento
- **Diferencias específicas**: Ubicación exacta de cada diferencia
- **Contenido diferenciador**: Elementos únicos con datos completos

## 🛠️ Desarrollo

### Backend (FastAPI)
- **Arquitectura**: API REST con FastAPI
- **Procesamiento**: Pandas para análisis de datos
- **Validación**: Pydantic para validación de datos
- **Logging**: Sistema de logs configurable

### Frontend (Next.js + React)
- **Framework**: Next.js 14 con App Router
- **UI**: Tailwind CSS para estilos
- **Gráficos**: Recharts para visualizaciones
- **Estado**: React Hooks para gestión de estado

### Tecnologías Utilizadas
- **Backend**: Python, FastAPI, Pandas, NumPy
- **Frontend**: TypeScript, React, Next.js, Tailwind CSS
- **Gráficos**: Recharts
- **Build**: Vite, Webpack

## 🔒 Seguridad

- **Validación de archivos**: Verificación de tipos y tamaños
- **CORS configurado**: Control de acceso entre dominios
- **Sanitización de datos**: Limpieza de entradas de usuario
- **Logs de seguridad**: Registro de actividades importantes

## 📈 Rendimiento

- **Procesamiento optimizado**: Algoritmos eficientes para archivos grandes
- **Límites de memoria**: Control de uso de recursos
- **Caché inteligente**: Optimización de comparaciones repetidas
- **Procesamiento asíncrono**: No bloqueo de la interfaz

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

### Problemas Comunes

1. **Error de CORS**: Verificar configuración de CORS en `config.py`
2. **Archivo no encontrado**: Verificar rutas y permisos de archivos
3. **Error de memoria**: Reducir tamaño de archivos o aumentar memoria disponible

### Contacto
- **Issues**: Crear un issue en GitHub
- **Documentación**: Ver archivos de configuración y comentarios en el código
- **Ejemplos**: Usar archivos de ejemplo en la carpeta `examples/`

# Author 

- Charles Lantigua Jorge -mpgamer75

**Desarrollado para el equipo de IT de Altice Dominicana**
