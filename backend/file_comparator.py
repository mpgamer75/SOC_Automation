import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
import io
from datetime import datetime

class FileComparator:
    """
    Motor principal para comparar archivos CSV y Excel
    Analiza diferencias estructurales y de contenido entre documentos
    """
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls']
    
    def read_file(self, file_content: bytes, filename: str) -> pd.DataFrame:
        """
        Procesa y carga un archivo en memoria, manejando diferentes codificaciones
        """
        file_extension = filename.lower().split('.')[-1]
        
        try:
            if file_extension == 'csv':
                # Probar diferentes codificaciones para archivos CSV
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        df = pd.read_csv(io.BytesIO(file_content), encoding=encoding)
                        return df
                    except UnicodeDecodeError:
                        continue
                raise ValueError("No se pudo decodificar el archivo CSV")
                
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(io.BytesIO(file_content))
                return df
            else:
                raise ValueError(f"Formato de archivo no soportado: {file_extension}")
                
        except Exception as e:
            raise ValueError(f"Error al leer el archivo {filename}: {str(e)}")
    
    def _extract_different_content(self, df1: pd.DataFrame, df2: pd.DataFrame) -> Dict[str, Any]:
        """
        Identifica y extrae el contenido que hace únicos a cada documento
        Encuentra registros que solo existen en uno de los archivos
        """
        # Normalizar datos como strings para comparación consistente
        df1_str = df1.astype(str)
        df2_str = df2.astype(str)
        
        # Buscar columnas que comparten ambos archivos
        common_cols = list(set(df1.columns) & set(df2.columns))
        
        # Preparar listas para almacenar elementos únicos
        unique_in_reference = []
        unique_in_compare = []
        
        if common_cols:
            # Generar claves únicas basadas en las columnas compartidas
            df1_key = df1_str[common_cols].apply(lambda x: '|'.join(x), axis=1)
            df2_key = df2_str[common_cols].apply(lambda x: '|'.join(x), axis=1)
            
            # Encontrar registros que solo existen en cada archivo
            df1_unique_keys = set(df1_key) - set(df2_key)
            df2_unique_keys = set(df2_key) - set(df1_key)
            
            # Extraer los datos completos de los registros únicos
            for key in df1_unique_keys:
                row_idx = df1_key[df1_key == key].index[0]
                unique_in_reference.append({
                    'row_index': int(row_idx),
                    'data': df1.iloc[row_idx].to_dict(),
                    'key_columns': common_cols
                })
            
            for key in df2_unique_keys:
                row_idx = df2_key[df2_key == key].index[0]
                unique_in_compare.append({
                    'row_index': int(row_idx),
                    'data': df2.iloc[row_idx].to_dict(),
                    'key_columns': common_cols
                })
        
        # Identificar columnas que solo existen en cada archivo
        cols_only_in_reference = list(set(df1.columns) - set(df2.columns))
        cols_only_in_compare = list(set(df2.columns) - set(df1.columns))
        
        return {
            'unique_in_reference': unique_in_reference[:50],  # Limitar para evitar sobrecarga en el frontend
            'unique_in_compare': unique_in_compare[:50],      # Limitar para evitar sobrecarga en el frontend
            'columns_only_in_reference': cols_only_in_reference,
            'columns_only_in_compare': cols_only_in_compare,
            'total_unique_in_reference': len(unique_in_reference),
            'total_unique_in_compare': len(unique_in_compare)
        }
    
    def compare_dataframes(self, df1: pd.DataFrame, df2: pd.DataFrame, 
                          ref_filename: str, comp_filename: str) -> Dict[str, Any]:
        """
        Ejecuta la comparación completa entre dos DataFrames
        Retorna un reporte detallado con todas las diferencias encontradas
        """
        start_time = datetime.now()
        
        # Limpiar nombres de columnas para evitar problemas de espacios
        df1.columns = df1.columns.str.strip()
        df2.columns = df2.columns.str.strip()
        
        # Convertir todo a string para comparación uniforme
        df1 = df1.astype(str)
        df2 = df2.astype(str)
        
        differences = []
        
        # Primero analizar la estructura de los archivos
        struct_diff = self._compare_structure(df1, df2)
        differences.extend(struct_diff)
        
        # Si la estructura es compatible, analizar el contenido
        if not struct_diff:  # Solo proceder si no hay diferencias estructurales críticas
            content_diff = self._compare_content(df1, df2)
            differences.extend(content_diff)
        
        # Extraer el contenido que diferencia los documentos
        different_content = self._extract_different_content(df1, df2)
        
        # Generar estadísticas del análisis
        summary = self._generate_summary(df1, df2, differences, different_content)
        
        # Calcular tiempo total de procesamiento
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "identical": len(differences) == 0,
            "summary": summary,
            "differences": differences[:100],  # Limitar para evitar sobrecarga en el frontend
            "different_content": different_content,
            "metadata": {
                "comparisonDate": datetime.now().isoformat(),
                "referenceFileName": ref_filename,
                "compareFileName": comp_filename,
                "processingTime": f"{processing_time:.2f} segundos"
            }
        }
    
    def _compare_structure(self, df1: pd.DataFrame, df2: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Analiza las diferencias estructurales entre los archivos
        Compara columnas, dimensiones y organización de datos
        """
        differences = []
        
        # Verificar si el número de columnas coincide
        if len(df1.columns) != len(df2.columns):
            differences.append({
                "type": "structure_difference",
                "position": "Estructura",
                "description": f"Diferente número de columnas: {len(df1.columns)} vs {len(df2.columns)}",
                "referenceValue": f"{len(df1.columns)} columnas",
                "compareValue": f"{len(df2.columns)} columnas"
            })
        
        # Comparar nombres específicos de columnas
        cols1 = set(df1.columns)
        cols2 = set(df2.columns)
        
        missing_cols = cols1 - cols2
        extra_cols = cols2 - cols1
        
        # Registrar columnas que faltan en el archivo de comparación
        for col in missing_cols:
            differences.append({
                "type": "column_missing",
                "position": f"Columna",
                "description": f"Columna '{col}' falta en archivo a comparar",
                "referenceValue": f"Columna '{col}' presente",
                "compareValue": "Columna faltante"
            })
        
        # Registrar columnas nuevas en el archivo de comparación
        for col in extra_cols:
            differences.append({
                "type": "column_added",
                "position": f"Columna",
                "description": f"Columna '{col}' agregada en archivo a comparar",
                "referenceValue": "Columna no presente",
                "compareValue": f"Columna '{col}' agregada"
            })
        
        return differences
    
    def _compare_content(self, df1: pd.DataFrame, df2: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Compara el contenido celda por celda entre los archivos
        Identifica valores modificados, filas agregadas o eliminadas
        """
        differences = []
        
        # Obtener columnas que existen en ambos archivos
        common_cols = list(set(df1.columns) & set(df2.columns))
        
        # Determinar rangos de comparación
        max_rows = max(len(df1), len(df2))
        min_rows = min(len(df1), len(df2))
        
        # Comparar cada celda en las filas comunes
        for i in range(min_rows):
            for col in common_cols:
                val1 = df1.iloc[i][col] if i < len(df1) else "N/A"
                val2 = df2.iloc[i][col] if i < len(df2) else "N/A"
                
                if str(val1) != str(val2):
                    differences.append({
                        "type": "cell_modified",
                        "position": f"Fila {i+1}, Columna '{col}'",
                        "column": col,
                        "row": i+1,
                        "referenceValue": str(val1),
                        "compareValue": str(val2)
                    })
        
        # Identificar filas nuevas en el archivo de comparación
        if len(df2) > len(df1):
            for i in range(len(df1), len(df2)):
                row_data = {}
                for col in common_cols:
                    if col in df2.columns:
                        row_data[col] = str(df2.iloc[i][col])
                
                differences.append({
                    "type": "row_added",
                    "position": f"Fila {i+1}",
                    "row": i+1,
                    "data": row_data,
                    "description": f"Fila {i+1} agregada en archivo a comparar"
                })
        
        # Identificar filas que faltan en el archivo de comparación
        elif len(df1) > len(df2):
            for i in range(len(df2), len(df1)):
                row_data = {}
                for col in common_cols:
                    if col in df1.columns:
                        row_data[col] = str(df1.iloc[i][col])
                
                differences.append({
                    "type": "row_removed",
                    "position": f"Fila {i+1}",
                    "row": i+1,
                    "data": row_data,
                    "description": f"Fila {i+1} falta en archivo a comparar"
                })
        
        return differences
    
    def _generate_summary(self, df1: pd.DataFrame, df2: pd.DataFrame, 
                         differences: List[Dict[str, Any]], 
                         different_content: Dict[str, Any]) -> Dict[str, int]:
        """
        Genera estadísticas resumidas del análisis de comparación
        Cuenta diferentes tipos de diferencias encontradas
        """
        # Contar cada tipo de diferencia encontrada
        cell_modifications = len([d for d in differences if d["type"] == "cell_modified"])
        rows_added = len([d for d in differences if d["type"] == "row_added"])
        rows_removed = len([d for d in differences if d["type"] == "row_removed"])
        columns_added = len([d for d in differences if d["type"] == "column_added"])
        columns_removed = len([d for d in differences if d["type"] == "column_missing"])
        
        return {
            "totalRows": max(len(df1), len(df2)),
            "totalColumns": max(len(df1.columns), len(df2.columns)),
            "differences": len(differences),
            "addedRows": rows_added,
            "removedRows": rows_removed,
            "modifiedCells": cell_modifications,
            "addedColumns": columns_added,
            "removedColumns": columns_removed,
            "referenceRows": len(df1),
            "referenceColumns": len(df1.columns),
            "compareRows": len(df2),
            "compareColumns": len(df2.columns),
            "uniqueInReference": different_content.get('total_unique_in_reference', 0),
            "uniqueInCompare": different_content.get('total_unique_in_compare', 0)
        }
    
    def compare_files(self, file1_content: bytes, file1_name: str, 
                     file2_content: bytes, file2_name: str) -> Dict[str, Any]:
        """
        Punto de entrada principal para comparar dos archivos
        Coordina todo el proceso de análisis y comparación
        """
        try:
            # Cargar ambos archivos en memoria
            df1 = self.read_file(file1_content, file1_name)
            df2 = self.read_file(file2_content, file2_name)
            
            # Ejecutar la comparación completa
            result = self.compare_dataframes(df1, df2, file1_name, file2_name)
            
            return result
            
        except Exception as e:
            raise ValueError(f"Error en la comparación: {str(e)}") 