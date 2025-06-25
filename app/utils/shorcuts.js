const { shell } = require('electron');
const fs = require('fs-extra');
const path = require('path');
const os = require('os');

class ShortcutManager {
  constructor() {
    this.desktopPath = path.join(os.homedir(), 'Desktop');
    this.startMenuPath = path.join(os.homedir(), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs');
  }

  createDesktopShortcut(options) {
    try {
      const { name, description, target, icon } = options;
      const shortcutPath = path.join(this.desktopPath, `${name}.lnk`);
      
      // En Windows, usar shell.writeShortcutLink
      const success = shell.writeShortcutLink(shortcutPath, {
        target: target,
        description: description,
        icon: icon,
        iconIndex: 0
      });
      
      if (success) {
        console.log(`✅ Acceso directo creado: ${shortcutPath}`);
        return shortcutPath;
      } else {
        throw new Error('No se pudo crear el acceso directo');
      }
    } catch (error) {
      console.error('❌ Error al crear acceso directo:', error);
      throw error;
    }
  }

  createStartMenuShortcut(options) {
    try {
      const { name, description, target, icon, folder } = options;
      const menuFolder = folder ? path.join(this.startMenuPath, folder) : this.startMenuPath;
      const shortcutPath = path.join(menuFolder, `${name}.lnk`);
      
      // Asegurar que el directorio existe
      fs.ensureDirSync(menuFolder);
      
      const success = shell.writeShortcutLink(shortcutPath, {
        target: target,
        description: description,
        icon: icon,
        iconIndex: 0
      });
      
      if (success) {
        console.log(`✅ Acceso directo en menú inicio creado: ${shortcutPath}`);
        return shortcutPath;
      } else {
        throw new Error('No se pudo crear el acceso directo en el menú de inicio');
      }
    } catch (error) {
      console.error('❌ Error al crear acceso directo en menú de inicio:', error);
      throw error;
    }
  }

  removeDesktopShortcut(name) {
    try {
      const shortcutPath = path.join(this.desktopPath, `${name}.lnk`);
      if (fs.existsSync(shortcutPath)) {
        fs.unlinkSync(shortcutPath);
        console.log(`✅ Acceso directo eliminado: ${shortcutPath}`);
        return true;
      }
      return false;
    } catch (error) {
      console.error('❌ Error al eliminar acceso directo:', error);
      return false;
    }
  }

  checkShortcutExists(name, location = 'desktop') {
    try {
      const basePath = location === 'desktop' ? this.desktopPath : this.startMenuPath;
      const shortcutPath = path.join(basePath, `${name}.lnk`);
      return fs.existsSync(shortcutPath);
    } catch (error) {
      console.error('❌ Error al verificar acceso directo:', error);
      return false;
    }
  }
}

module.exports = ShortcutManager;