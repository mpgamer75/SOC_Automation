const { contextBridge, ipcRenderer } = require('electron');

// API segura expuesta al frontend
contextBridge.exposeInMainWorld('electronAPI', {
  // Información de la aplicación
  app: {
    getInfo: () => ipcRenderer.invoke('app:get-info')
  },

  // Operaciones de base de datos
  database: {
    getReferenceFiles: () => ipcRenderer.invoke('db:get-reference-files'),
    addReferenceFile: (fileData) => ipcRenderer.invoke('db:add-reference-file', fileData),
    getComparisonHistory: (limit) => ipcRenderer.invoke('db:get-comparison-history', limit),
    saveComparison: (comparisonData) => ipcRenderer.invoke('db:save-comparison', comparisonData)
  },

  // Operaciones de archivos
  files: {
    saveReference: (fileData) => ipcRenderer.invoke('file:save-reference', fileData),
    openDialog: (options) => ipcRenderer.invoke('file:open-dialog', options),
    saveDialog: (options) => ipcRenderer.invoke('file:save-dialog', options)
  },

  // Notificaciones
  notification: {
    show: (title, body) => ipcRenderer.invoke('notification:show', title, body)
  },

  // Eventos del menú
  menu: {
    onNewComparison: (callback) => ipcRenderer.on('menu-new-comparison', callback),
    onOpenReference: (callback) => ipcRenderer.on('menu-open-reference', callback),
    onExportHistory: (callback) => ipcRenderer.on('menu-export-history', callback),
    onSettings: (callback) => ipcRenderer.on('menu-settings', callback)
  }
});