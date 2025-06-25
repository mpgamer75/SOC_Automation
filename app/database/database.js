const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs-extra');
const { app } = require('electron');

class Database {
  constructor() {
    this.db = null;
    this.dbPath = null;
  }

  async initialize() {
    try {
      // Crear directorio de base de datos
      const userDataPath = app.getPath('userData');
      const dbDir = path.join(userDataPath, 'database');
      await fs.ensureDir(dbDir);
      
      this.dbPath = path.join(dbDir, 'altice_comparator.db');
      
      // Conectar a la base de datos
      this.db = new sqlite3.Database(this.dbPath);
      
      // Configurar la base de datos
      await this.setupDatabase();
      
      console.log('✅ Base de datos inicializada en:', this.dbPath);
      return true;
    } catch (error) {
      console.error('❌ Error al inicializar la base de datos:', error);
      throw error;
    }
  }

  setupDatabase() {
    return new Promise((resolve, reject) => {
      this.db.serialize(() => {
        // Configuraciones de SQLite
        this.db.run("PRAGMA foreign_keys = ON");
        this.db.run("PRAGMA journal_mode = WAL");
        this.db.run("PRAGMA synchronous = NORMAL");
        this.db.run("PRAGMA cache_size = 10000");
        this.db.run("PRAGMA temp_store = MEMORY");
        
        // Tabla de archivos de referencia
        this.db.run(`
          CREATE TABLE IF NOT EXISTS reference_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            original_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            mime_type TEXT NOT NULL,
            row_count INTEGER DEFAULT 0,
            column_count INTEGER DEFAULT 0,
            description TEXT,
            tags TEXT,
            upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_used DATETIME,
            usage_count INTEGER DEFAULT 0,
            checksum TEXT,
            is_active BOOLEAN DEFAULT 1
          )
        `, (err) => {
          if (err) {
            reject(err);
            return;
          }
        });

        // Tabla de comparaciones
        this.db.run(`
          CREATE TABLE IF NOT EXISTS comparisons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference_file_id INTEGER,
            compare_file_name TEXT NOT NULL,
            compare_file_path TEXT,
            compare_file_size INTEGER,
            comparison_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            processing_time REAL NOT NULL,
            total_differences INTEGER NOT NULL DEFAULT 0,
            modified_cells INTEGER DEFAULT 0,
            added_rows INTEGER DEFAULT 0,
            removed_rows INTEGER DEFAULT 0,
            added_columns INTEGER DEFAULT 0,
            removed_columns INTEGER DEFAULT 0,
            unique_in_reference INTEGER DEFAULT 0,
            unique_in_compare INTEGER DEFAULT 0,
            identical BOOLEAN NOT NULL DEFAULT 0,
            result_data TEXT,
            summary_data TEXT,
            exported BOOLEAN DEFAULT 0,
            export_format TEXT,
            export_date DATETIME,
            notes TEXT,
            FOREIGN KEY (reference_file_id) REFERENCES reference_files (id) ON DELETE CASCADE
          )
        `, (err) => {
          if (err) {
            reject(err);
            return;
          }
        });

        // Tabla de configuraciones de la aplicación
        this.db.run(`
          CREATE TABLE IF NOT EXISTS app_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT,
            description TEXT,
            updated_date DATETIME DEFAULT CURRENT_TIMESTAMP
          )
        `, (err) => {
          if (err) {
            reject(err);
            return;
          }
        });

        // Tabla de logs de actividad
        this.db.run(`
          CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            details TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            file_name TEXT,
            success BOOLEAN DEFAULT 1,
            error_message TEXT
          )
        `, (err) => {
          if (err) {
            reject(err);
            return;
          }
        });

        // Crear índices para mejorar el rendimiento
        this.db.run("CREATE INDEX IF NOT EXISTS idx_reference_files_name ON reference_files(name)");
        this.db.run("CREATE INDEX IF NOT EXISTS idx_reference_files_upload_date ON reference_files(upload_date)");
        this.db.run("CREATE INDEX IF NOT EXISTS idx_comparisons_date ON comparisons(comparison_date)");
        this.db.run("CREATE INDEX IF NOT EXISTS idx_comparisons_reference ON comparisons(reference_file_id)");
        this.db.run("CREATE INDEX IF NOT EXISTS idx_activity_logs_timestamp ON activity_logs(timestamp)");

        // Insertar configuraciones por defecto
        this.insertDefaultSettings((err) => {
          if (err) {
            reject(err);
          } else {
            resolve();
          }
        });
      });
    });
  }

  insertDefaultSettings(callback) {
    const defaultSettings = [
      { key: 'app_version', value: '1.2.0', description: 'Versión de la aplicación' },
      { key: 'max_file_size', value: '52428800', description: 'Tamaño máximo de archivo en bytes (50MB)' },
      { key: 'auto_backup', value: 'true', description: 'Backup automático de la base de datos' },
      { key: 'backup_frequency', value: '7', description: 'Frecuencia de backup en días' },
      { key: 'max_history_records', value: '1000', description: 'Máximo de registros en historial' },
      { key: 'default_export_format', value: 'excel', description: 'Formato de exportación por defecto' },
      { key: 'theme', value: 'light', description: 'Tema de la aplicación' },
      { key: 'language', value: 'es', description: 'Idioma de la aplicación' },
      { key: 'auto_save_comparisons', value: 'true', description: 'Guardar comparaciones automáticamente' },
      { key: 'notification_enabled', value: 'true', description: 'Notificaciones habilitadas' }
    ];

    let completed = 0;
    const total = defaultSettings.length;

    if (total === 0) {
      callback(null);
      return;
    }

    defaultSettings.forEach(setting => {
      this.db.run(
        `INSERT OR IGNORE INTO app_settings (key, value, description) VALUES (?, ?, ?)`,
        [setting.key, setting.value, setting.description],
        (err) => {
          completed++;
          if (completed === total) {
            callback(err);
          }
        }
      );
    });
  }

  // Métodos para archivos de referencia
  async addReferenceFile(fileData) {
    return new Promise((resolve, reject) => {
      const stmt = this.db.prepare(`
        INSERT INTO reference_files 
        (name, original_name, file_path, file_size, mime_type, row_count, column_count, description, tags, checksum)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `);
      
      stmt.run([
        fileData.name,
        fileData.originalName,
        fileData.filePath,
        fileData.fileSize,
        fileData.mimeType,
        fileData.rowCount || 0,
        fileData.columnCount || 0,
        fileData.description || null,
        fileData.tags || null,
        fileData.checksum || null
      ], function(err) {
        stmt.finalize();
        if (err) {
          reject(err);
        } else {
          // Log de actividad
          this.logActivity('REFERENCE_ADDED', `Archivo de referencia agregado: ${fileData.name}`, fileData.name, true);
          resolve(this.lastID);
        }
      }.bind(this));
    });
  }

  async getReferenceFiles() {
    return new Promise((resolve, reject) => {
      this.db.all(`
        SELECT 
          id,
          name,
          original_name,
          file_path,
          file_size,
          mime_type,
          row_count,
          column_count,
          description,
          tags,
          upload_date,
          last_used,
          usage_count,
          is_active
        FROM reference_files 
        WHERE is_active = 1
        ORDER BY upload_date DESC
      `, (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }

  async updateReferenceFileUsage(fileId) {
    return new Promise((resolve, reject) => {
      this.db.run(`
        UPDATE reference_files 
        SET last_used = CURRENT_TIMESTAMP, usage_count = usage_count + 1
        WHERE id = ?
      `, [fileId], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve(this.changes);
        }
      });
    });
  }

  async deleteReferenceFile(fileId) {
    return new Promise((resolve, reject) => {
      // Primero obtener información del archivo
      this.db.get('SELECT name FROM reference_files WHERE id = ?', [fileId], (err, row) => {
        if (err) {
          reject(err);
          return;
        }

        // Marcar como inactivo en lugar de eliminar
        this.db.run(`
          UPDATE reference_files 
          SET is_active = 0
          WHERE id = ?
        `, [fileId], function(err) {
          if (err) {
            reject(err);
          } else {
            // Log de actividad
            const fileName = row ? row.name : 'Archivo desconocido';
            this.logActivity('REFERENCE_DELETED', `Archivo de referencia eliminado: ${fileName}`, fileName, true);
            resolve(this.changes);
          }
        }.bind(this));
      });
    });
  }

  // Métodos para comparaciones
  async saveComparison(comparisonData) {
    return new Promise((resolve, reject) => {
      const stmt = this.db.prepare(`
        INSERT INTO comparisons 
        (reference_file_id, compare_file_name, compare_file_path, compare_file_size,
         processing_time, total_differences, modified_cells, added_rows, removed_rows,
         added_columns, removed_columns, unique_in_reference, unique_in_compare,
         identical, result_data, summary_data, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `);
      
      stmt.run([
        comparisonData.referenceFileId,
        comparisonData.compareFileName,
        comparisonData.compareFilePath || null,
        comparisonData.compareFileSize || null,
        comparisonData.processingTime,
        comparisonData.totalDifferences,
        comparisonData.modifiedCells || 0,
        comparisonData.addedRows || 0,
        comparisonData.removedRows || 0,
        comparisonData.addedColumns || 0,
        comparisonData.removedColumns || 0,
        comparisonData.uniqueInReference || 0,
        comparisonData.uniqueInCompare || 0,
        comparisonData.identical,
        JSON.stringify(comparisonData.resultData),
        JSON.stringify(comparisonData.summaryData || {}),
        comparisonData.notes || null
      ], function(err) {
        stmt.finalize();
        if (err) {
          reject(err);
        } else {
          // Actualizar uso del archivo de referencia
          if (comparisonData.referenceFileId) {
            this.updateReferenceFileUsage(comparisonData.referenceFileId);
          }
          
          // Log de actividad
          this.logActivity('COMPARISON_SAVED', 
            `Comparación guardada: ${comparisonData.compareFileName}`, 
            comparisonData.compareFileName, true);
          
          resolve(this.lastID);
        }
      }.bind(this));
    });
  }

  async getComparisonHistory(limit = 50, offset = 0) {
    return new Promise((resolve, reject) => {
      this.db.all(`
        SELECT 
          c.id,
          c.reference_file_id,
          c.compare_file_name,
          c.compare_file_size,
          c.comparison_date,
          c.processing_time,
          c.total_differences,
          c.modified_cells,
          c.added_rows,
          c.removed_rows,
          c.added_columns,
          c.removed_columns,
          c.unique_in_reference,
          c.unique_in_compare,
          c.identical,
          c.exported,
          c.export_format,
          c.export_date,
          c.notes,
          rf.name as reference_file_name,
          rf.original_name as reference_original_name
        FROM comparisons c
        LEFT JOIN reference_files rf ON c.reference_file_id = rf.id
        ORDER BY c.comparison_date DESC
        LIMIT ? OFFSET ?
      `, [limit, offset], (err, rows) => {
        if (err) {
          reject(err);
        } else {
          // Parsear datos JSON
          const history = rows.map(row => ({
            ...row,
            result_data: null, // No cargar datos completos en el listado
            summary_data: null
          }));
          resolve(history);
        }
      });
    });
  }

  async getComparisonDetails(comparisonId) {
    return new Promise((resolve, reject) => {
      this.db.get(`
        SELECT 
          c.*,
          rf.name as reference_file_name,
          rf.original_name as reference_original_name,
          rf.file_path as reference_file_path
        FROM comparisons c
        LEFT JOIN reference_files rf ON c.reference_file_id = rf.id
        WHERE c.id = ?
      `, [comparisonId], (err, row) => {
        if (err) {
          reject(err);
        } else if (!row) {
          reject(new Error('Comparación no encontrada'));
        } else {
          // Parsear datos JSON
          const comparison = {
            ...row,
            result_data: row.result_data ? JSON.parse(row.result_data) : null,
            summary_data: row.summary_data ? JSON.parse(row.summary_data) : null
          };
          resolve(comparison);
        }
      });
    });
  }

  async markComparisonAsExported(comparisonId, format) {
    return new Promise((resolve, reject) => {
      this.db.run(`
        UPDATE comparisons 
        SET exported = 1, export_format = ?, export_date = CURRENT_TIMESTAMP
        WHERE id = ?
      `, [format, comparisonId], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve(this.changes);
        }
      });
    });
  }

  // Métodos para configuraciones
  async getSetting(key) {
    return new Promise((resolve, reject) => {
      this.db.get('SELECT value FROM app_settings WHERE key = ?', [key], (err, row) => {
        if (err) {
          reject(err);
        } else {
          resolve(row ? row.value : null);
        }
      });
    });
  }

  async setSetting(key, value, description = null) {
    return new Promise((resolve, reject) => {
      this.db.run(`
        INSERT OR REPLACE INTO app_settings (key, value, description, updated_date)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
      `, [key, value, description], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve(this.changes);
        }
      });
    });
  }

  async getAllSettings() {
    return new Promise((resolve, reject) => {
      this.db.all('SELECT * FROM app_settings ORDER BY key', (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }

  // Métodos para logs de actividad
  async logActivity(action, details = null, fileName = null, success = true, errorMessage = null) {
    return new Promise((resolve, reject) => {
      this.db.run(`
        INSERT INTO activity_logs (action, details, file_name, success, error_message)
        VALUES (?, ?, ?, ?, ?)
      `, [action, details, fileName, success, errorMessage], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve(this.lastID);
        }
      });
    });
  }

  async getActivityLogs(limit = 100, offset = 0) {
    return new Promise((resolve, reject) => {
      this.db.all(`
        SELECT * FROM activity_logs 
        ORDER BY timestamp DESC 
        LIMIT ? OFFSET ?
      `, [limit, offset], (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }

  // Métodos de mantenimiento y estadísticas
  async getStatistics() {
    return new Promise((resolve, reject) => {
      const stats = {};
      
      const queries = [
        { key: 'totalReferenceFiles', query: 'SELECT COUNT(*) as count FROM reference_files WHERE is_active = 1' },
        { key: 'totalComparisons', query: 'SELECT COUNT(*) as count FROM comparisons' },
        { key: 'identicalComparisons', query: 'SELECT COUNT(*) as count FROM comparisons WHERE identical = 1' },
        { key: 'differentComparisons', query: 'SELECT COUNT(*) as count FROM comparisons WHERE identical = 0' },
        { key: 'avgProcessingTime', query: 'SELECT AVG(processing_time) as avg FROM comparisons' },
        { key: 'totalDifferencesFound', query: 'SELECT SUM(total_differences) as total FROM comparisons' },
        { key: 'mostUsedReference', query: `
          SELECT rf.name, rf.usage_count 
          FROM reference_files rf 
          WHERE rf.is_active = 1 
          ORDER BY rf.usage_count DESC 
          LIMIT 1
        ` },
        { key: 'lastComparison', query: `
          SELECT comparison_date 
          FROM comparisons 
          ORDER BY comparison_date DESC 
          LIMIT 1
        ` }
      ];

      let completed = 0;
      const total = queries.length;

      queries.forEach(({ key, query }) => {
        this.db.get(query, (err, row) => {
          if (!err && row) {
            if (key === 'avgProcessingTime') {
              stats[key] = row.avg ? parseFloat(row.avg).toFixed(2) : 0;
            } else if (key === 'totalDifferencesFound') {
              stats[key] = row.total || 0;
            } else if (key === 'mostUsedReference') {
              stats[key] = row.name || 'N/A';
              stats.mostUsedReferenceCount = row.usage_count || 0;
            } else if (key === 'lastComparison') {
              stats[key] = row.comparison_date || null;
            } else {
              stats[key] = row.count || 0;
            }
          } else {
            stats[key] = 0;
          }
          
          completed++;
          if (completed === total) {
            resolve(stats);
          }
        });
      });
    });
  }

  async cleanOldData() {
    return new Promise((resolve, reject) => {
      this.db.serialize(() => {
        // Limpiar logs antiguos (más de 30 días)
        this.db.run(`
          DELETE FROM activity_logs 
          WHERE timestamp < datetime('now', '-30 days')
        `);

        // Limpiar comparaciones muy antiguas si hay muchas
        this.db.get('SELECT COUNT(*) as count FROM comparisons', (err, row) => {
          if (row && row.count > 1000) {
            this.db.run(`
              DELETE FROM comparisons 
              WHERE id IN (
                SELECT id FROM comparisons 
                ORDER BY comparison_date ASC 
                LIMIT ${row.count - 1000}
              )
            `);
          }
        });

        // Optimizar la base de datos
        this.db.run('VACUUM', (err) => {
          if (err) {
            reject(err);
          } else {
            this.logActivity('MAINTENANCE', 'Limpieza automática de base de datos completada', null, true);
            resolve();
          }
        });
      });
    });
  }

  async backup() {
    return new Promise((resolve, reject) => {
      const backupPath = path.join(path.dirname(this.dbPath), `backup_${Date.now()}.db`);
      
      fs.copyFile(this.dbPath, backupPath, (err) => {
        if (err) {
          reject(err);
        } else {
          this.logActivity('BACKUP', `Backup creado: ${backupPath}`, null, true);
          resolve(backupPath);
        }
      });
    });
  }

  async clean() {
    return new Promise((resolve, reject) => {
      this.db.serialize(() => {
        this.db.run('DELETE FROM comparisons');
        this.db.run('DELETE FROM reference_files');
        this.db.run('DELETE FROM activity_logs');
        this.db.run('UPDATE sqlite_sequence SET seq = 0 WHERE name IN ("comparisons", "reference_files", "activity_logs")');
        this.db.run('VACUUM', (err) => {
          if (err) {
            reject(err);
          } else {
            this.logActivity('CLEAN', 'Base de datos limpiada completamente', null, true);
            resolve();
          }
        });
      });
    });
  }

  async close() {
    return new Promise((resolve, reject) => {
      if (this.db) {
        this.db.close((err) => {
          if (err) {
            reject(err);
          } else {
            console.log('✅ Base de datos cerrada correctamente');
            resolve();
          }
        });
      } else {
        resolve();
      }
    });
  }
}

module.exports = Database;