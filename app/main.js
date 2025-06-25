const { app, BrowserWindow, ipcMain, shell, dialog, Menu } = require('electron');
const path = require('path');
const fs = require('fs-extra');
const { spawn } = require('child_process');
const Database = require('./database/database');
const FileManager = require('./utils/file-manager');
const ShortcutManager = require('./utils/shortcuts');
const i18n = require('./locales/es.json');

class AlticeFileComparator {
  constructor() {
    this.mainWindow = null;
    this.backendProcess = null;
    this.frontendProcess = null;
    this.database = new Database();
    this.fileManager = new FileManager();
    this.isDevelopment = process.env.NODE_ENV === 'development';
    
    // Configuración de la aplicación
    app.setName(i18n.app.name);
    app.setPath('userData', path.join(app.getPath('appData'), 'AlticeFileComparator'));
  }

  async initialize() {
    try {
      console.log('🚀 Iniciando Altice File Comparator...');
      
      // Inicializar base de datos
      await this.database.initialize();
      console.log('✅ Base de datos inicializada');
      
      // Inicializar gestor de archivos
      await this.fileManager.initialize();
      console.log('✅ Gestor de archivos inicializado');
      
      // Crear directorio de datos si no existe
      await this.createDataDirectories();
      
      return true;
    } catch (error) {
      console.error('❌ Error durante la inicialización:', error);
      await this.showErrorDialog('Error de Inicialización', 
        'No se pudo inicializar la aplicación correctamente.');
      return false;
    }
  }

  async createDataDirectories() {
    const userDataPath = app.getPath('userData');
    const directories = [
      path.join(userDataPath, 'reference_files'),
      path.join(userDataPath, 'comparison_files'),
      path.join(userDataPath, 'exports'),
      path.join(userDataPath, 'temp')
    ];

    for (const dir of directories) {
      await fs.ensureDir(dir);
    }
  }

  async createMainWindow() {
    this.mainWindow = new BrowserWindow({
      width: 1600,
      height: 1000,
      minWidth: 1200,
      minHeight: 800,
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        enableRemoteModule: false,
        preload: path.join(__dirname, 'preload.js')
      },
      icon: path.join(__dirname, '../installer/assets/icon.ico'),
      title: i18n.app.title,
      titleBarStyle: 'default',
      show: false,
      backgroundColor: '#ffffff',
      webSecurity: true
    });

    // Configurar menú de la aplicación
    this.setupApplicationMenu();

    // Cargar la aplicación
    if (this.isDevelopment) {
      await this.mainWindow.loadURL('http://localhost:3000');
      this.mainWindow.webContents.openDevTools();
    } else {
      await this.mainWindow.loadFile(path.join(__dirname, '../frontend2/out/index.html'));
    }

    // Mostrar ventana cuando esté lista
    this.mainWindow.once('ready-to-show', () => {
      this.mainWindow.show();
      
      // Crear acceso directo en el escritorio si es la primera vez
      this.createDesktopShortcut();
    });

    // Manejar cierre de ventana
    this.mainWindow.on('closed', () => {
      this.mainWindow = null;
    });

    // Prevenir navegación externa
    this.mainWindow.webContents.setWindowOpenHandler(({ url }) => {
      shell.openExternal(url);
      return { action: 'deny' };
    });
  }

  setupApplicationMenu() {
    const template = [
      {
        label: i18n.menu.file,
        submenu: [
          {
            label: i18n.menu.newComparison,
            accelerator: 'CmdOrCtrl+N',
            click: () => this.mainWindow.webContents.send('menu-new-comparison')
          },
          {
            label: i18n.menu.openReference,
            accelerator: 'CmdOrCtrl+O',
            click: () => this.mainWindow.webContents.send('menu-open-reference')
          },
          { type: 'separator' },
          {
            label: i18n.menu.exit,
            accelerator: 'CmdOrCtrl+Q',
            click: () => app.quit()
          }
        ]
      },
      {
        label: i18n.menu.tools,
        submenu: [
          {
            label: i18n.menu.exportHistory,
            click: () => this.mainWindow.webContents.send('menu-export-history')
          },
          {
            label: i18n.menu.cleanDatabase,
            click: () => this.showCleanDatabaseDialog()
          },
          { type: 'separator' },
          {
            label: i18n.menu.settings,
            click: () => this.mainWindow.webContents.send('menu-settings')
          }
        ]
      },
      {
        label: i18n.menu.help,
        submenu: [
          {
            label: i18n.menu.userGuide,
            click: () => shell.openExternal('https://docs.altice.do/file-comparator')
          },
          {
            label: i18n.menu.about,
            click: () => this.showAboutDialog()
          }
        ]
      }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
  }

  async startServices() {
    if (!this.isDevelopment) {
      try {
        // Iniciar backend
        await this.startBackend();
        console.log('✅ Backend iniciado');
        
        // El frontend está empaquetado como archivos estáticos
        console.log('✅ Frontend listo');
        
        return true;
      } catch (error) {
        console.error('❌ Error al iniciar servicios:', error);
        return false;
      }
    }
    return true; // En desarrollo, los servicios se inician externamente
  }

  async startBackend() {
    return new Promise((resolve, reject) => {
      const backendPath = path.join(__dirname, '../backend/dist/altice-backend.exe');
      
      if (!fs.existsSync(backendPath)) {
        reject(new Error('Backend non trouvé en: ' + backendPath));
        return;
      }
      this.backendProcess = spawn(backendPath, [], {
        cwd: path.dirname(backendPath),
        stdio: ['ignore', 'pipe', 'pipe']
      });
      this.backendProcess.on('error', (error) => {
        reject(new Error('Erreur au démarrage du backend: ' + error.message));
      });
      setTimeout(() => {
        if (this.backendProcess && !this.backendProcess.killed) {
          resolve();
        } else {
          reject(new Error('Le backend ne s\'est pas lancé correctement'));
        }
      }, 3000);
    });
  }

  createDesktopShortcut() {
    try {
      const shortcutManager = new ShortcutManager();
      shortcutManager.createDesktopShortcut({
        name: i18n.app.shortcutName,
        description: i18n.app.description,
        target: process.execPath,
        icon: path.join(__dirname, '../installer/assets/icon.ico')
      });
      console.log('✅ Acceso directo creado en el escritorio');
    } catch (error) {
      console.warn('⚠️ No se pudo crear el acceso directo:', error.message);
    }
  }

  async showAboutDialog() {
    await dialog.showMessageBox(this.mainWindow, {
      type: 'info',
      title: i18n.dialogs.about.title,
      message: i18n.app.title,
      detail: i18n.dialogs.about.message
        .replace('{version}', app.getVersion())
        .replace('{author}', 'Charles Lantigua Jorge')
        .replace('{company}', 'Altice Dominicana'),
      buttons: [i18n.dialogs.buttons.close],
      defaultId: 0
    });
  }

  async showCleanDatabaseDialog() {
    const result = await dialog.showMessageBox(this.mainWindow, {
      type: 'warning',
      title: i18n.dialogs.cleanDatabase.title,
      message: i18n.dialogs.cleanDatabase.message,
      detail: i18n.dialogs.cleanDatabase.detail,
      buttons: [i18n.dialogs.buttons.cancel, i18n.dialogs.buttons.clean],
      defaultId: 0,
      cancelId: 0
    });

    if (result.response === 1) {
      try {
        await this.database.clean();
        await dialog.showMessageBox(this.mainWindow, {
          type: 'info',
          title: i18n.dialogs.success.title,
          message: i18n.dialogs.cleanDatabase.success,
          buttons: [i18n.dialogs.buttons.ok]
        });
        
        // Recargar la aplicación
        this.mainWindow.webContents.reload();
      } catch (error) {
        await this.showErrorDialog(i18n.dialogs.error.title, 
          i18n.dialogs.cleanDatabase.error + ': ' + error.message);
      }
    }
  }

  async showErrorDialog(title, message) {
    await dialog.showMessageBox(this.mainWindow, {
      type: 'error',
      title: title,
      message: message,
      buttons: [i18n.dialogs.buttons.ok],
      defaultId: 0
    });
  }

  setupIpcHandlers() {
    // Manejador para obtener información de la aplicación
    ipcMain.handle('app:get-info', () => ({
      version: app.getVersion(),
      name: app.getName(),
      userDataPath: app.getPath('userData')
    }));

    // Manejador para operaciones de base de datos
    ipcMain.handle('db:get-reference-files', async () => {
      return await this.database.getReferenceFiles();
    });

    ipcMain.handle('db:add-reference-file', async (event, fileData) => {
      return await this.database.addReferenceFile(fileData);
    });

    ipcMain.handle('db:get-comparison-history', async (event, limit) => {
      return await this.database.getComparisonHistory(limit);
    });

    ipcMain.handle('db:save-comparison', async (event, comparisonData) => {
      return await this.database.saveComparison(comparisonData);
    });

    // Manejador para operaciones de archivos
    ipcMain.handle('file:save-reference', async (event, fileData) => {
      return await this.fileManager.saveReferenceFile(fileData);
    });

    ipcMain.handle('file:open-dialog', async (event, options) => {
      const result = await dialog.showOpenDialog(this.mainWindow, options);
      return result;
    });

    ipcMain.handle('file:save-dialog', async (event, options) => {
      const result = await dialog.showSaveDialog(this.mainWindow, options);
      return result;
    });

    // Manejador para notificaciones
    ipcMain.handle('notification:show', (event, title, body) => {
      new Notification({ title, body }).show();
    });
  }

  async cleanup() {
    console.log('🧹 Limpiando recursos...');
    
    if (this.backendProcess && !this.backendProcess.killed) {
      this.backendProcess.kill();
      console.log('✅ Backend detenido');
    }

    if (this.frontendProcess && !this.frontendProcess.killed) {
      this.frontendProcess.kill();
      console.log('✅ Frontend detenido');
    }

    // Limpiar archivos temporales
    try {
      const tempDir = path.join(app.getPath('userData'), 'temp');
      await fs.emptyDir(tempDir);
      console.log('✅ Archivos temporales limpiados');
    } catch (error) {
      console.warn('⚠️ No se pudieron limpiar los archivos temporales:', error.message);
    }
  }
}

// Instancia principal de la aplicación
const appInstance = new AlticeFileComparator();

// Configuración de eventos de Electron
app.whenReady().then(async () => {
  console.log('📱 Electron listo, inicializando aplicación...');
  
  const initialized = await appInstance.initialize();
  if (!initialized) {
    app.quit();
    return;
  }

  const servicesStarted = await appInstance.startServices();
  if (!servicesStarted) {
    await appInstance.showErrorDialog('Error de Servicios', 
      'No se pudieron iniciar los servicios de la aplicación.');
    app.quit();
    return;
  }

  await appInstance.createMainWindow();
  appInstance.setupIpcHandlers();
  
  console.log('🎉 Aplicación iniciada exitosamente');
});

app.on('window-all-closed', async () => {
  await appInstance.cleanup();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', async () => {
  await appInstance.cleanup();
});

app.on('activate', async () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    await appInstance.createMainWindow();
  }
});

// Manejar errores no capturados
process.on('uncaughtException', (error) => {
  console.error('❌ Error no capturado:', error);
  if (appInstance.mainWindow) {
    appInstance.showErrorDialog('Error Inesperado', 
      'Se produjo un error inesperado. La aplicación se cerrará.');
  }
  app.quit();
});