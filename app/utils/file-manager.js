const fs = require('fs-extra');
const path = require('path');
const crypto = require('crypto');
const { app } = require('electron');

class FileManager {
  constructor() {
    this.userDataPath = app.getPath('userData');
    this.referenceFilesPath = path.join(this.userDataPath, 'reference_files');
    this.tempFilesPath = path.join(this.userDataPath, 'temp');
    this.exportPath = path.join(this.userDataPath, 'exports');
  }

  async initialize() {
    try {
      // Crear directorios necesarios
      await fs.ensureDir(this.referenceFilesPath);
      await fs.ensureDir(this.tempFilesPath);
      await fs.ensureDir(this.exportPath);
      
      console.log('✅ Gestor de archivos inicializado');
      return true;
    } catch (error) {
      console.error('❌ Error al inicializar gestor de archivos:', error);
      throw error;
    }
  }

  async saveReferenceFile(fileData) {
    try {
      const { buffer, originalName, size, mimeType } = fileData;
      
      // Generar nombre único
      const fileExtension = path.extname(originalName);
      const baseName = path.basename(originalName, fileExtension);
      const timestamp = Date.now();
      const uniqueName = `${baseName}_${timestamp}${fileExtension}`;
      
      // Ruta completa del archivo
      const filePath = path.join(this.referenceFilesPath, uniqueName);
      
      // Guardar archivo
      await fs.writeFile(filePath, buffer);
      
      // Calcular checksum
      const checksum = this.calculateChecksum(buffer);
      
      // Obtener información adicional del archivo
      const fileInfo = await this.analyzeFile(filePath, mimeType);
      
      return {
        name: uniqueName,
        originalName: originalName,
        filePath: filePath,
        fileSize: size,
        mimeType: mimeType,
        checksum: checksum,
        rowCount: fileInfo.rowCount,
        columnCount: fileInfo.columnCount
      };
    } catch (error) {
      console.error('❌ Error al guardar archivo de referencia:', error);
      throw error;
    }
  }

  calculateChecksum(buffer) {
    return crypto.createHash('md5').update(buffer).digest('hex');
  }

  async analyzeFile(filePath, mimeType) {
    try {
      const fileInfo = {
        rowCount: 0,
        columnCount: 0
      };

      if (mimeType === 'text/csv') {
        const content = await fs.readFile(filePath, 'utf-8');
        const lines = content.split('\n').filter(line => line.trim() !== '');
        fileInfo.rowCount = Math.max(0, lines.length - 1); // Excluir header
        
        if (lines.length > 0) {
          // Detectar separador
          const separators = [',', ';', '\t', '|'];
          let maxColumns = 0;
          
          for (const sep of separators) {
            const columns = lines[0].split(sep).length;
            if (columns > maxColumns) {
              maxColumns = columns;
            }
          }
          
          fileInfo.columnCount = maxColumns;
        }
      } else if (mimeType.includes('spreadsheet') || mimeType.includes('excel')) {
        // Para archivos Excel, necesitaríamos una librería como exceljs
        // Por ahora, valores por defecto
        fileInfo.rowCount = 0;
        fileInfo.columnCount = 0;
      }

      return fileInfo;
    } catch (error) {
      console.warn('⚠️ No se pudo analizar el archivo:', error.message);
      return { rowCount: 0, columnCount: 0 };
    }
  }

  async getReferenceFilePath(fileName) {
    const filePath = path.join(this.referenceFilesPath, fileName);
    const exists = await fs.pathExists(filePath);
    return exists ? filePath : null;
  }

  async deleteReferenceFile(fileName) {
    try {
      const filePath = path.join(this.referenceFilesPath, fileName);
      await fs.remove(filePath);
      return true;
    } catch (error) {
      console.error('❌ Error al eliminar archivo:', error);
      return false;
    }
  }

  async saveTempFile(fileData, suffix = '') {
    try {
      const { buffer, originalName } = fileData;
      const fileExtension = path.extname(originalName);
      const baseName = path.basename(originalName, fileExtension);
      const timestamp = Date.now();
      const tempName = `${baseName}_temp_${timestamp}${suffix}${fileExtension}`;
      
      const tempPath = path.join(this.tempFilesPath, tempName);
      await fs.writeFile(tempPath, buffer);
      
      return tempPath;
    } catch (error) {
      console.error('❌ Error al guardar archivo temporal:', error);
      throw error;
    }
  }

  async cleanTempFiles() {
    try {
      await fs.emptyDir(this.tempFilesPath);
      console.log('✅ Archivos temporales limpiados');
    } catch (error) {
      console.warn('⚠️ No se pudieron limpiar archivos temporales:', error.message);
    }
  }

  async exportReport(reportData, fileName, format) {
    try {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const exportFileName = `${fileName}_${timestamp}.${format}`;
      const exportFilePath = path.join(this.exportPath, exportFileName);
      
      if (format === 'json') {
        await fs.writeFile(exportFilePath, JSON.stringify(reportData, null, 2), 'utf-8');
      } else if (format === 'txt') {
        const textContent = this.convertToText(reportData);
        await fs.writeFile(exportFilePath, textContent, 'utf-8');
      } else if (format === 'csv') {
        const csvContent = this.convertToCSV(reportData);
        await fs.writeFile(exportFilePath, csvContent, 'utf-8');
      }
      
      return exportFilePath;
    } catch (error) {
      console.error('❌ Error al exportar reporte:', error);
      throw error;
    }
  }

  convertToText(reportData) {
    let text = '=== REPORTE DE COMPARACIÓN ALTICE FILE COMPARATOR ===\n\n';
    
    if (reportData.metadata) {
      text += `Fecha: ${new Date(reportData.metadata.comparisonDate).toLocaleString('es-ES')}\n`;
      text += `Archivo de referencia: ${reportData.metadata.referenceFileName}\n`;
      text += `Archivo de comparación: ${reportData.metadata.compareFileName}\n`;
      text += `Tiempo de procesamiento: ${reportData.metadata.processingTime}\n\n`;
    }
    
    if (reportData.summary) {
      text += '=== RESUMEN ===\n';
      text += `Total de filas: ${reportData.summary.totalRows}\n`;
      text += `Total de columnas: ${reportData.summary.totalColumns}\n`;
      text += `Diferencias encontradas: ${reportData.summary.differences}\n`;
      text += `Archivos idénticos: ${reportData.identical ? 'Sí' : 'No'}\n\n`;
    }
    
    if (reportData.differences && reportData.differences.length > 0) {
      text += '=== DIFERENCIAS DETALLADAS ===\n';
      reportData.differences.forEach((diff, index) => {
        text += `${index + 1}. ${diff.type.toUpperCase()}\n`;
        text += `   Posición: ${diff.position}\n`;
        text += `   Descripción: ${diff.description}\n`;
        if (diff.referenceValue) text += `   Valor referencia: ${diff.referenceValue}\n`;
        if (diff.compareValue) text += `   Valor comparación: ${diff.compareValue}\n`;
        text += '\n';
      });
    }
    
    return text;
  }

  convertToCSV(reportData) {
    let csv = 'Tipo,Posición,Descripción,Valor Referencia,Valor Comparación\n';
    
    if (reportData.differences) {
      reportData.differences.forEach(diff => {
        const row = [
          diff.type || '',
          diff.position || '',
          (diff.description || '').replace(/"/g, '""'),
          (diff.referenceValue || '').replace(/"/g, '""'),
          (diff.compareValue || '').replace(/"/g, '""')
        ].map(field => `"${field}"`).join(',');
        csv += row + '\n';
      });
    }
    
    return csv;
  }

  async getDiskUsage() {
    try {
      const stats = {
        referenceFiles: 0,
        tempFiles: 0,
        exports: 0,
        total: 0
      };

      // Calcular uso de archivos de referencia
      const refFiles = await fs.readdir(this.referenceFilesPath);
      for (const file of refFiles) {
        const filePath = path.join(this.referenceFilesPath, file);
        const stat = await fs.stat(filePath);
        stats.referenceFiles += stat.size;
      }

      // Calcular uso de archivos temporales
      const tempFiles = await fs.readdir(this.tempFilesPath);
      for (const file of tempFiles) {
        const filePath = path.join(this.tempFilesPath, file);
        const stat = await fs.stat(filePath);
        stats.tempFiles += stat.size;
      }

      // Calcular uso de exports
      const exportFiles = await fs.readdir(this.exportPath);
      for (const file of exportFiles) {
        const filePath = path.join(this.exportPath, file);
        const stat = await fs.stat(filePath);
        stats.exports += stat.size;
      }

      stats.total = stats.referenceFiles + stats.tempFiles + stats.exports;
      
      return stats;
    } catch (error) {
      console.error('❌ Error al calcular uso de disco:', error);
      return { referenceFiles: 0, tempFiles: 0, exports: 0, total: 0 };
    }
  }

  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}

module.exports = FileManager;