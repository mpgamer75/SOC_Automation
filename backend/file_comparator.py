import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
import io
from datetime import datetime

class FileComparator:
    """
    Clase para comparar diferentes tipos de archivos (CSV, Excel)
    Detecta diferencias y genera reportes detallados
    """
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls']
    
    def read_file(self, file_content: bytes, filename: str) -> pd.DataFrame:
        """
        Lee un archivo y retorna un DataFrame de pandas
        """
        file_extension = filename.lower().split('.')[-1]
        
        try:
            if file_extension == 'csv':
                # Intentar diferentes encodings para CSV
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
    
    def compare_dataframes(self, df1: pd.DataFrame, df2: pd.DataFrame, 
                          ref_filename: str, comp_filename: str) -> Dict[str, Any]:
        """
        Compara dos DataFrames y retorna un diccionario con las diferencias
        """
        start_time = datetime.now()
        
        # Limpiar nombres de columnas (eliminar espacios)
        df1.columns = df1.columns.str.strip()
        df2.columns = df2.columns.str.strip()
        
        # Convertir a string para evitar problemas de tipos
        df1 = df1.astype(str)
        df2 = df2.astype(str)
        
        differences = []
        
        # Comparar estructura
        struct_diff = self._compare_structure(df1, df2)
        differences.extend(struct_diff)
        
        # Comparar contenido si tienen la misma estructura básica
        if not struct_diff:  # Solo si no hay diferencias estructurales
            content_diff = self._compare_content(df1, df2)
            differences.extend(content_diff)
        
        # Estadísticas
        summary = self._generate_summary(df1, df2, differences)
        
        # Tiempo de procesamiento
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "identical": len(differences) == 0,
            "summary": summary,
            "differences": differences[:100],  # Limitar a 100 diferencias para el frontend
            "metadata": {
                "comparisonDate": datetime.now().isoformat(),
                "referenceFileName": ref_filename,
                "compareFileName": comp_filename,
                "processingTime": f"{processing_time:.2f} segundos"
            }
        }
    
    def _compare_structure(self, df1: pd.DataFrame, df2: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Compara la estructura de los DataFrames (columnas, dimensiones)
        """
        differences = []
        
        # Comparar número de columnas
        if len(df1.columns) != len(df2.columns):
            differences.append({
                "type": "structure_difference",
                "position": "Estructura",
                "description": f"Diferente número de columnas: {len(df1.columns)} vs {len(df2.columns)}",
                "referenceValue": f"{len(df1.columns)} columnas",
                "compareValue": f"{len(df2.columns)} columnas"
            })
        
        # Comparar nombres de columnas
        cols1 = set(df1.columns)
        cols2 = set(df2.columns)
        
        missing_cols = cols1 - cols2
        extra_cols = cols2 - cols1
        
        for col in missing_cols:
            differences.append({
                "type": "column_missing",
                "position": f"Columna",
                "description": f"Columna '{col}' falta en archivo a comparar",
                "referenceValue": f"Columna '{col}' presente",
                "compareValue": "Columna faltante"
            })
        
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
        Compara el contenido de los DataFrames celda por celda
        """
        differences = []
        
        # Obtener columnas comunes
        common_cols = list(set(df1.columns) & set(df2.columns))
        
        # Comparar número de filas
        max_rows = max(len(df1), len(df2))
        min_rows = min(len(df1), len(df2))
        
        # Comparar contenido de celdas
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
        
        # Filas adicionales en df2
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
        
        # Filas faltantes en df2
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
                         differences: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Genera un resumen estadístico de las diferencias
        """
        # Contar tipos de diferencias
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
            "compareColumns": len(df2.columns)
        }
    
    def compare_files(self, file1_content: bytes, file1_name: str, 
                     file2_content: bytes, file2_name: str) -> Dict[str, Any]:
        """
        Método principal para comparar dos archivos
        """
        try:
            # Leer los archivos
            df1 = self.read_file(file1_content, file1_name)
            df2 = self.read_file(file2_content, file2_name)
            
            # Comparar los DataFrames
            result = self.compare_dataframes(df1, df2, file1_name, file2_name)
            
            return result
            
        except Exception as e:
            raise ValueError(f"Error en la comparación: {str(e)}")