"use client";

import React, { useState, useCallback } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts';

interface ComparisonResult {
  identical: boolean;
  summary: {
    totalRows: number;
    totalColumns: number;
    differences: number;
    addedRows: number;
    removedRows: number;
    modifiedCells: number;
    addedColumns: number;
    removedColumns: number;
    referenceRows: number;
    referenceColumns: number;
    compareRows: number;
    compareColumns: number;
    uniqueInReference: number;
    uniqueInCompare: number;
  };
  differences: Array<{
    type: string;
    position: string;
    description: string;
    referenceValue?: string;
    compareValue?: string;
    column?: string;
    row?: number;
    data?: Record<string, string>;
  }>;
  different_content: {
    unique_in_reference: Array<{
      row_index: number;
      data: Record<string, string>;
      key_columns: string[];
    }>;
    unique_in_compare: Array<{
      row_index: number;
      data: Record<string, string>;
      key_columns: string[];
    }>;
    columns_only_in_reference: string[];
    columns_only_in_compare: string[];
    total_unique_in_reference: number;
    total_unique_in_compare: number;
  };
  metadata: {
    comparisonDate: string;
    referenceFileName: string;
    compareFileName: string;
    processingTime: string;
  };
}

const FileComparatorDashboard: React.FC = () => {
  const [file1, setFile1] = useState<File | null>(null);
  const [file2, setFile2] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ComparisonResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>, fileNumber: 1 | 2) => {
    const file = e.target.files?.[0];
    if (file) {
      if (fileNumber === 1) {
        setFile1(file);
      } else {
        setFile2(file);
      }
      setError(null);
    }
  }, []);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent, fileNumber: 1 | 2) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      if (fileNumber === 1) {
        setFile1(files[0]);
      } else {
        setFile2(files[0]);
      }
      setError(null);
    }
  }, []);

  const compareFiles = async () => {
    if (!file1 || !file2) {
      setError('Por favor seleccione ambos archivos para comparar');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file1', file1);
      formData.append('file2', file2);

      const response = await fetch('http://localhost:8000/compare', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error en la comparación');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFile1(null);
    setFile2(null);
    setResult(null);
    setError(null);
  };

  const downloadReport = (format: 'json' | 'txt' | 'csv' | 'xlsx') => {
    if (!result) return;

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `comparison-report-${timestamp}.${format}`;

    if (format === 'json') {
      const dataStr = JSON.stringify(result, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.click();
      URL.revokeObjectURL(url);
    } else if (format === 'txt') {
      let textContent = `=== REPORTE DE COMPARACIÓN DE ARCHIVOS ===\n\n`;
      textContent += `Fecha: ${new Date(result.metadata.comparisonDate).toLocaleString('es-ES')}\n`;
      textContent += `Archivo de referencia: ${result.metadata.referenceFileName}\n`;
      textContent += `Archivo a comparar: ${result.metadata.compareFileName}\n`;
      textContent += `Tiempo de procesamiento: ${result.metadata.processingTime}\n\n`;
      
      textContent += `=== RESUMEN ===\n`;
      textContent += `Total de filas: ${result.summary.totalRows}\n`;
      textContent += `Total de columnas: ${result.summary.totalColumns}\n`;
      textContent += `Diferencias encontradas: ${result.summary.differences}\n`;
      textContent += `Celdas modificadas: ${result.summary.modifiedCells}\n`;
      textContent += `Filas agregadas: ${result.summary.addedRows}\n`;
      textContent += `Filas eliminadas: ${result.summary.removedRows}\n`;
      textContent += `Columnas agregadas: ${result.summary.addedColumns}\n`;
      textContent += `Columnas eliminadas: ${result.summary.removedColumns}\n`;
      textContent += `Elementos únicos en referencia: ${result.summary.uniqueInReference}\n`;
      textContent += `Elementos únicos en comparación: ${result.summary.uniqueInCompare}\n\n`;
      
      textContent += `=== CONTENIDO DIFERENCIADOR ===\n`;
      textContent += `Elementos únicos en archivo de referencia (${result.different_content.total_unique_in_reference}):\n`;
      result.different_content.unique_in_reference.forEach((item, index) => {
        textContent += `  ${index + 1}. Fila ${item.row_index + 1}:\n`;
        Object.entries(item.data).forEach(([key, value]) => {
          textContent += `     ${key}: ${value}\n`;
        });
        textContent += `\n`;
      });
      
      textContent += `Elementos únicos en archivo a comparar (${result.different_content.total_unique_in_compare}):\n`;
      result.different_content.unique_in_compare.forEach((item, index) => {
        textContent += `  ${index + 1}. Fila ${item.row_index + 1}:\n`;
        Object.entries(item.data).forEach(([key, value]) => {
          textContent += `     ${key}: ${value}\n`;
        });
        textContent += `\n`;
      });
      
      if (result.different_content.columns_only_in_reference.length > 0) {
        textContent += `Columnas solo en archivo de referencia: ${result.different_content.columns_only_in_reference.join(', ')}\n\n`;
      }
      
      if (result.different_content.columns_only_in_compare.length > 0) {
        textContent += `Columnas solo en archivo a comparar: ${result.different_content.columns_only_in_compare.join(', ')}\n\n`;
      }
      
      textContent += `=== DIFERENCIAS DETALLADAS ===\n`;
      result.differences.forEach((diff, index) => {
        textContent += `${index + 1}. ${diff.type.toUpperCase()}\n`;
        textContent += `   Posición: ${diff.position}\n`;
        textContent += `   Descripción: ${diff.description}\n`;
        if (diff.referenceValue) textContent += `   Valor referencia: ${diff.referenceValue}\n`;
        if (diff.compareValue) textContent += `   Valor comparación: ${diff.compareValue}\n`;
        textContent += `\n`;
      });

      const dataBlob = new Blob([textContent], { type: 'text/plain' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.click();
      URL.revokeObjectURL(url);
    } else if (format === 'csv') {
      let csvContent = `Tipo,Posición,Descripción,Valor Referencia,Valor Comparación\n`;
      
      // Agregar diferencias
      result.differences.forEach((diff) => {
        const row = [
          diff.type,
          diff.position,
          diff.description,
          diff.referenceValue || '',
          diff.compareValue || ''
        ].map(field => `"${field.replace(/"/g, '""')}"`).join(',');
        csvContent += row + '\n';
      });

      const dataBlob = new Blob([csvContent], { type: 'text/csv' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.click();
      URL.revokeObjectURL(url);
    } else if (format === 'xlsx') {
      // Para Excel, creamos un CSV que se puede abrir dans Excel
      let excelContent = `Reporte de Comparación de Archivos\n`;
      excelContent += `Fecha,${new Date(result.metadata.comparisonDate).toLocaleString('es-ES')}\n`;
      excelContent += `Archivo de referencia,${result.metadata.referenceFileName}\n`;
      excelContent += `Archivo a comparar,${result.metadata.compareFileName}\n`;
      excelContent += `Tiempo de procesamiento,${result.metadata.processingTime}\n\n`;
      
      excelContent += `Resumen\n`;
      excelContent += `Total de filas,${result.summary.totalRows}\n`;
      excelContent += `Total de columnas,${result.summary.totalColumns}\n`;
      excelContent += `Diferencias encontradas,${result.summary.differences}\n`;
      excelContent += `Celdas modificadas,${result.summary.modifiedCells}\n`;
      excelContent += `Filas agregadas,${result.summary.addedRows}\n`;
      excelContent += `Filas eliminadas,${result.summary.removedRows}\n`;
      excelContent += `Columnas agregadas,${result.summary.addedColumns}\n`;
      excelContent += `Columnas eliminadas,${result.summary.removedColumns}\n`;
      excelContent += `Elementos únicos en referencia,${result.summary.uniqueInReference}\n`;
      excelContent += `Elementos únicos en comparación,${result.summary.uniqueInCompare}\n\n`;
      
      excelContent += `Diferencias Detalladas\n`;
      excelContent += `Tipo,Posición,Descripción,Valor Referencia,Valor Comparación\n`;
      
      result.differences.forEach((diff) => {
        const row = [
          diff.type,
          diff.position,
          diff.description,
          diff.referenceValue || '',
          diff.compareValue || ''
        ].map(field => `"${field.replace(/"/g, '""')}"`).join(',');
        excelContent += row + '\n';
      });

      const dataBlob = new Blob([excelContent], { type: 'text/csv' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename.replace('.xlsx', '.csv');
      link.click();
      URL.revokeObjectURL(url);
    }
  };

  const getFileIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase();
    switch (ext) {
      case 'csv':
        return '📊';
      case 'xlsx':
      case 'xls':
        return '📈';
      default:
        return '📄';
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getDifferencesData = () => {
    if (!result) return [];
    
    const data = [
      { name: 'Celdas Modificadas', value: result.summary.modifiedCells, fill: '#ef4444' },
      { name: 'Filas Agregadas', value: result.summary.addedRows, fill: '#10b981' },
      { name: 'Filas Eliminadas', value: result.summary.removedRows, fill: '#3b82f6' },
      { name: 'Columnas Agregadas', value: result.summary.addedColumns, fill: '#f59e0b' },
      { name: 'Columnas Eliminadas', value: result.summary.removedColumns, fill: '#8b5cf6' },
      { name: 'Únicos en Referencia', value: result.summary.uniqueInReference, fill: '#ec4899' },
      { name: 'Únicos en Comparación', value: result.summary.uniqueInCompare, fill: '#06b6d4' },
    ];
    
    // Si no hay diferencias, mostrar un mensaje
    if (result.summary.differences === 0 && result.summary.uniqueInReference === 0 && result.summary.uniqueInCompare === 0) {
      return [{ name: 'Sin Diferencias', value: 1, fill: '#10b981' }];
    }
    
    return data.filter(item => item.value > 0);
  };

  const getStructureData = () => {
    if (!result) return [];
    
    return [
      { name: 'Referencia', filas: result.summary.referenceRows, columnas: result.summary.referenceColumns },
      { name: 'Comparación', filas: result.summary.compareRows, columnas: result.summary.compareColumns },
    ];
  };

  const getTrendData = () => {
    if (!result) return [];
    
    return [
      { name: 'Referencia', filas: result.summary.referenceRows, columnas: result.summary.referenceColumns },
      { name: 'Comparación', filas: result.summary.compareRows, columnas: result.summary.compareColumns },
    ];
  };

  const COLORS = ['#ef4444', '#10b981', '#3b82f6', '#f59e0b', '#8b5cf6'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full mb-6">
            <span className="text-2xl">🔍</span>
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent mb-4">
            Altice File Comparator
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Compara archivos CSV, Excel y XLS de manera inteligente con análisis detallado y visualizaciones avanzadas
          </p>
        </div>

        {/* File Upload Section */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-8 mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-8 flex items-center">
            <span className="text-3xl mr-3">📁</span>
            Selección de Archivos
          </h2>
          
          <div className="grid md:grid-cols-2 gap-8">
            {/* File 1 */}
            <div className="space-y-4">
              <label className="block text-lg font-medium text-gray-700 flex items-center">
                <span className="text-2xl mr-2">📋</span>
                Archivo de Referencia
              </label>
              <div
                className={`border-3 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
                  dragActive ? 'border-blue-500 bg-blue-50/50 scale-105' : 'border-gray-300 hover:border-gray-400 hover:scale-[1.02]'
                }`}
                onDragEnter={(e) => handleDrag(e)}
                onDragLeave={(e) => handleDrag(e)}
                onDragOver={(e) => handleDrag(e)}
                onDrop={(e) => handleDrop(e, 1)}
              >
                {file1 ? (
                  <div className="space-y-4">
                    <div className="text-4xl animate-bounce">{getFileIcon(file1.name)}</div>
                    <div className="font-semibold text-gray-900 text-lg">{file1.name}</div>
                    <div className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                      {formatFileSize(file1.size)}
                    </div>
                    <button
                      onClick={() => setFile1(null)}
                      className="text-red-500 hover:text-red-700 text-sm font-medium hover:bg-red-50 px-3 py-1 rounded-full transition-colors"
                    >
                      ✕ Eliminar
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="text-5xl text-gray-400">📁</div>
                    <div className="text-gray-600 text-lg">
                      Arrastra un archivo aquí o haz clic para seleccionar
                    </div>
                    <input
                      type="file"
                      accept=".csv,.xlsx,.xls"
                      onChange={(e) => handleFileChange(e, 1)}
                      className="hidden"
                      id="file1"
                    />
                    <label
                      htmlFor="file1"
                      className="inline-block bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-xl hover:from-blue-700 hover:to-indigo-700 cursor-pointer transition-all duration-300 transform hover:scale-105 shadow-lg"
                    >
                      Seleccionar Archivo
                    </label>
                  </div>
                )}
              </div>
            </div>

            {/* File 2 */}
            <div className="space-y-4">
              <label className="block text-lg font-medium text-gray-700 flex items-center">
                <span className="text-2xl mr-2">🔍</span>
                Archivo a Comparar
              </label>
              <div
                className={`border-3 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
                  dragActive ? 'border-blue-500 bg-blue-50/50 scale-105' : 'border-gray-300 hover:border-gray-400 hover:scale-[1.02]'
                }`}
                onDragEnter={(e) => handleDrag(e)}
                onDragLeave={(e) => handleDrag(e)}
                onDragOver={(e) => handleDrag(e)}
                onDrop={(e) => handleDrop(e, 2)}
              >
                {file2 ? (
                  <div className="space-y-4">
                    <div className="text-4xl animate-bounce">{getFileIcon(file2.name)}</div>
                    <div className="font-semibold text-gray-900 text-lg">{file2.name}</div>
                    <div className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                      {formatFileSize(file2.size)}
                    </div>
                    <button
                      onClick={() => setFile2(null)}
                      className="text-red-500 hover:text-red-700 text-sm font-medium hover:bg-red-50 px-3 py-1 rounded-full transition-colors"
                    >
                      ✕ Eliminar
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="text-5xl text-gray-400">📁</div>
                    <div className="text-gray-600 text-lg">
                      Arrastra un archivo aquí o haz clic para seleccionar
                    </div>
                    <input
                      type="file"
                      accept=".csv,.xlsx,.xls"
                      onChange={(e) => handleFileChange(e, 2)}
                      className="hidden"
                      id="file2"
                    />
                    <label
                      htmlFor="file2"
                      className="inline-block bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-xl hover:from-blue-700 hover:to-indigo-700 cursor-pointer transition-all duration-300 transform hover:scale-105 shadow-lg"
                    >
                      Seleccionar Archivo
                    </label>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-center space-x-6 mt-8">
            <button
              onClick={compareFiles}
              disabled={!file1 || !file2 || isLoading}
              className={`px-10 py-4 rounded-xl font-semibold text-lg transition-all duration-300 transform ${
                !file1 || !file2 || isLoading
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-gradient-to-r from-green-500 to-emerald-600 text-white hover:from-green-600 hover:to-emerald-700 hover:scale-105 shadow-lg'
              }`}
            >
              {isLoading ? (
                <span className="flex items-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                  Comparando...
                </span>
              ) : (
                <span className="flex items-center">
                  <span className="text-xl mr-2">🔍</span>
                  Comparar Archivos
                </span>
              )}
            </button>
            
            <button
              onClick={resetForm}
              className="px-8 py-4 bg-gradient-to-r from-gray-500 to-gray-600 text-white rounded-xl hover:from-gray-600 hover:to-gray-700 transition-all duration-300 transform hover:scale-105 shadow-lg font-semibold text-lg"
            >
              <span className="flex items-center">
                <span className="text-xl mr-2">🔄</span>
                Reiniciar
              </span>
            </button>
          </div>

          {/* Error Display */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl animate-pulse">
              <div className="flex items-center">
                <div className="text-red-500 mr-3 text-xl">❌</div>
                <span className="text-red-700 font-medium">{error}</span>
              </div>
            </div>
          )}
        </div>

        {/* Results Section */}
        {result && (
          <div className="space-y-8">
            {/* Summary Cards */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-white/20 hover:shadow-xl transition-all duration-300">
                <div className="flex items-center">
                  <div className="text-3xl mr-4">📊</div>
                  <div>
                    <div className="text-3xl font-bold text-gray-800">
                      {result.summary.differences}
                    </div>
                    <div className="text-gray-600 font-medium">Diferencias</div>
                  </div>
                </div>
              </div>

              <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-white/20 hover:shadow-xl transition-all duration-300">
                <div className="flex items-center">
                  <div className="text-3xl mr-4">📈</div>
                  <div>
                    <div className="text-3xl font-bold text-gray-800">
                      {result.summary.totalRows}
                    </div>
                    <div className="text-gray-600 font-medium">Total Filas</div>
                  </div>
                </div>
              </div>

              <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-white/20 hover:shadow-xl transition-all duration-300">
                <div className="flex items-center">
                  <div className="text-3xl mr-4">📋</div>
                  <div>
                    <div className="text-3xl font-bold text-gray-800">
                      {result.summary.totalColumns}
                    </div>
                    <div className="text-gray-600 font-medium">Total Columnas</div>
                  </div>
                </div>
              </div>

              <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-white/20 hover:shadow-xl transition-all duration-300">
                <div className="flex items-center">
                  <div className="text-3xl mr-4">⚡</div>
                  <div>
                    <div className="text-2xl font-bold text-gray-800">
                      {result.metadata.processingTime}
                    </div>
                    <div className="text-gray-600 font-medium">Tiempo Procesamiento</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Download Report Buttons */}
            <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-white/20">
              <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                <span className="text-2xl mr-3">📥</span>
                Descargar Reporte
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <button
                  onClick={() => downloadReport('json')}
                  className="px-4 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-300 transform hover:scale-105 shadow-lg font-medium text-sm"
                >
                  <div className="flex flex-col items-center">
                    <span className="text-lg mb-1">📄</span>
                    <span>JSON</span>
                  </div>
                </button>
                <button
                  onClick={() => downloadReport('txt')}
                  className="px-4 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-green-600 hover:to-green-700 transition-all duration-300 transform hover:scale-105 shadow-lg font-medium text-sm"
                >
                  <div className="flex flex-col items-center">
                    <span className="text-lg mb-1">📝</span>
                    <span>TXT</span>
                  </div>
                </button>
                <button
                  onClick={() => downloadReport('csv')}
                  className="px-4 py-3 bg-gradient-to-r from-yellow-500 to-yellow-600 text-white rounded-lg hover:from-yellow-600 hover:to-yellow-700 transition-all duration-300 transform hover:scale-105 shadow-lg font-medium text-sm"
                >
                  <div className="flex flex-col items-center">
                    <span className="text-lg mb-1">📊</span>
                    <span>CSV</span>
                  </div>
                </button>
                <button
                  onClick={() => downloadReport('xlsx')}
                  className="px-4 py-3 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg font-medium text-sm"
                >
                  <div className="flex flex-col items-center">
                    <span className="text-lg mb-1">📈</span>
                    <span>Excel</span>
                  </div>
                </button>
              </div>
            </div>

            {/* Charts Section */}
            <div className="grid lg:grid-cols-2 gap-8">
              {/* Structure Comparison Chart */}
              <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                  <span className="text-2xl mr-3">📊</span>
                  Comparación de Estructura
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={getStructureData()}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="name" stroke="#6b7280" />
                    <YAxis stroke="#6b7280" />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                        border: '1px solid #e5e7eb',
                        borderRadius: '8px'
                      }} 
                    />
                    <Legend />
                    <Bar dataKey="filas" fill="#3b82f6" name="Filas" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="columnas" fill="#10b981" name="Columnas" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Differences Pie Chart */}
              <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                  <span className="text-2xl mr-3">🥧</span>
                  Tipos de Diferencias
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={getDifferencesData()}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }: { name: string; percent: number }) => {
                        if (name === 'Sin Diferencias') {
                          return 'Archivos Idénticos';
                        }
                        return `${name} ${(percent * 100).toFixed(0)}%`;
                      }}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                      animationDuration={1000}
                      animationBegin={0}
                    >
                      {getDifferencesData().map((entry, index) => (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={COLORS[index % COLORS.length]}
                          stroke="#ffffff"
                          strokeWidth={2}
                        />
                      ))}
                    </Pie>
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                        border: '1px solid #e5e7eb',
                        borderRadius: '8px',
                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                      }}
                      formatter={(value: any, name: string) => {
                        if (name === 'Sin Diferencias') {
                          return ['Archivos Idénticos', 'No se encontraron diferencias'];
                        }
                        return [value, name];
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
                {result.summary.differences === 0 && (
                  <div className="text-center mt-4 p-4 bg-green-50 rounded-lg border border-green-200">
                    <div className="text-green-600 font-semibold text-lg">🎉 ¡Archivos Idénticos!</div>
                    <div className="text-green-500 text-sm">No se encontraron diferencias entre los archivos</div>
                  </div>
                )}
              </div>
            </div>

            {/* Trend Chart */}
            <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-white/20">
              <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                <span className="text-2xl mr-3">📈</span>
                Tendencias de Datos
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={getTrendData()}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="name" stroke="#6b7280" />
                  <YAxis stroke="#6b7280" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px'
                    }} 
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="filas" 
                    stroke="#3b82f6" 
                    strokeWidth={3}
                    name="Filas"
                    dot={{ fill: '#3b82f6', strokeWidth: 2, r: 6 }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="columnas" 
                    stroke="#10b981" 
                    strokeWidth={3}
                    name="Columnas"
                    dot={{ fill: '#10b981', strokeWidth: 2, r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Detailed Differences */}
            <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-white/20">
              <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                <span className="text-2xl mr-3">🔍</span>
                Diferencias Detalladas
              </h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50/50">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                        Tipo
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                        Posición
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                        Descripción
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                        Valor Referencia
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                        Valor Comparación
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white/50 divide-y divide-gray-200">
                    {result.differences.slice(0, 20).map((diff, index) => (
                      <tr key={index} className="hover:bg-gray-50/50 transition-colors">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            {diff.type}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {diff.position}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500">
                          {diff.description}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {diff.referenceValue || '-'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {diff.compareValue || '-'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {result.differences.length > 20 && (
                <div className="mt-4 text-center text-gray-500 bg-gray-50/50 py-3 rounded-lg">
                  Mostrando las primeras 20 diferencias de {result.differences.length} totales
                </div>
              )}
            </div>

            {/* Content Differences */}
            {(result.different_content.total_unique_in_reference > 0 || result.different_content.total_unique_in_compare > 0) && (
              <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                  <span className="text-2xl mr-3">📊</span>
                  Contenido Diferenciador
                </h3>
                
                <div className="grid md:grid-cols-2 gap-6">
                  {/* Elementos únicos en referencia */}
                  {result.different_content.total_unique_in_reference > 0 && (
                    <div className="bg-red-50/50 p-4 rounded-lg border border-red-200">
                      <h4 className="text-lg font-semibold text-red-800 mb-4 flex items-center">
                        <span className="text-xl mr-2">📋</span>
                        Únicos en Referencia ({result.different_content.total_unique_in_reference})
                      </h4>
                      <div className="space-y-3 max-h-60 overflow-y-auto">
                        {result.different_content.unique_in_reference.map((item, index) => (
                          <div key={index} className="bg-white/70 p-3 rounded-lg border border-red-100">
                            <div className="text-sm font-medium text-red-700 mb-2">
                              Fila {item.row_index + 1}:
                            </div>
                            <div className="space-y-1">
                              {Object.entries(item.data).map(([key, value]) => (
                                <div key={key} className="text-xs text-gray-600">
                                  <span className="font-medium">{key}:</span> {value}
                                </div>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Elementos únicos en comparación */}
                  {result.different_content.total_unique_in_compare > 0 && (
                    <div className="bg-blue-50/50 p-4 rounded-lg border border-blue-200">
                      <h4 className="text-lg font-semibold text-blue-800 mb-4 flex items-center">
                        <span className="text-xl mr-2">🔍</span>
                        Únicos en Comparación ({result.different_content.total_unique_in_compare})
                      </h4>
                      <div className="space-y-3 max-h-60 overflow-y-auto">
                        {result.different_content.unique_in_compare.map((item, index) => (
                          <div key={index} className="bg-white/70 p-3 rounded-lg border border-blue-100">
                            <div className="text-sm font-medium text-blue-700 mb-2">
                              Fila {item.row_index + 1}:
                            </div>
                            <div className="space-y-1">
                              {Object.entries(item.data).map(([key, value]) => (
                                <div key={key} className="text-xs text-gray-600">
                                  <span className="font-medium">{key}:</span> {value}
                                </div>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Columnas únicas */}
                {(result.different_content.columns_only_in_reference.length > 0 || result.different_content.columns_only_in_compare.length > 0) && (
                  <div className="mt-6 grid md:grid-cols-2 gap-6">
                    {result.different_content.columns_only_in_reference.length > 0 && (
                      <div className="bg-orange-50/50 p-4 rounded-lg border border-orange-200">
                        <h4 className="text-lg font-semibold text-orange-800 mb-2 flex items-center">
                          <span className="text-xl mr-2">📊</span>
                          Columnas solo en Referencia
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {result.different_content.columns_only_in_reference.map((col, index) => (
                            <span key={index} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                              {col}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {result.different_content.columns_only_in_compare.length > 0 && (
                      <div className="bg-purple-50/50 p-4 rounded-lg border border-purple-200">
                        <h4 className="text-lg font-semibold text-purple-800 mb-2 flex items-center">
                          <span className="text-xl mr-2">📊</span>
                          Columnas solo en Comparación
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {result.different_content.columns_only_in_compare.map((col, index) => (
                            <span key={index} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                              {col}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* Metadata */}
            <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-white/20">
              <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                <span className="text-2xl mr-3">📋</span>
                Información de la Comparación
              </h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-gray-50/50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 font-medium">Archivo de Referencia:</p>
                  <p className="font-semibold text-gray-900">{result.metadata.referenceFileName}</p>
                </div>
                <div className="bg-gray-50/50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 font-medium">Archivo a Comparar:</p>
                  <p className="font-semibold text-gray-900">{result.metadata.compareFileName}</p>
                </div>
                <div className="bg-gray-50/50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 font-medium">Fecha de Comparación:</p>
                  <p className="font-semibold text-gray-900">
                    {new Date(result.metadata.comparisonDate).toLocaleString('es-ES')}
                  </p>
                </div>
                <div className="bg-gray-50/50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 font-medium">Estado:</p>
                  <p className="font-semibold">
                    {result.identical ? (
                      <span className="text-green-600 flex items-center">
                        <span className="text-xl mr-2">✅</span>
                        Archivos Idénticos
                      </span>
                    ) : (
                      <span className="text-red-600 flex items-center">
                        <span className="text-xl mr-2">❌</span>
                        Archivos Diferentes
                      </span>
                    )}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileComparatorDashboard;