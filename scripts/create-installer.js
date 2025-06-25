const fs = require('fs-extra');
const path = require('path');
const { execSync } = require('child_process');

class InstallerCreator {
  constructor() {
    this.rootDir = path.resolve(__dirname, '..');
    this.distDir = path.join(this.rootDir, 'dist');
    this.installerDir = path.join(this.rootDir, 'installer');
    this.outputDir = path.join(this.distDir, 'installers');
  }

  async createInstaller() {
    console.log('🎯 Creando instalador para Altice File Comparator...');

    try {
      // Preparar directorios
      await fs.ensureDir(this.outputDir);
      
      // Verificar archivos necesarios
      await this.validateFiles();
      
      // Crear instalador con Inno Setup
      await this.createInnoSetupInstaller();
      
      // Crear instalador NSIS como alternativa
      await this.createNSISInstaller();
      
      console.log('✅ Instaladores creados exitosamente');
      console.log(`📁 Ubicación: ${this.outputDir}`);
      
    } catch (error) {
      console.error('❌ Error al crear instalador:', error);
      throw error;
    }
  }

  async validateFiles() {
    console.log('🔍 Validando archivos necesarios...');
    
    const requiredFiles = [
      path.join(this.distDir, 'win-unpacked'),
      path.join(this.installerDir, 'installer-config.iss'),
      path.join(this.installerDir, 'assets', 'icon.ico')
    ];

    for (const filePath of requiredFiles) {
      if (!await fs.pathExists(filePath)) {
        throw new Error(`Archivo requerido no encontrado: ${filePath}`);
      }
    }

    console.log('✅ Todos los archivos necesarios están presentes');
  }

  async createInnoSetupInstaller() {
    console.log('📦 Creando instalador con Inno Setup...');
    
    try {
      const issScript = path.join(this.installerDir, 'installer-config.iss');
      const command = `iscc "${issScript}"`;
      
      execSync(command, { 
        cwd: this.installerDir,
        stdio: 'inherit'
      });
      
      // Mover el instalador generado al directorio de salida
      const generatedInstaller = path.join(this.installerDir, 'Output', 'AlticeFileComparator-1.2.0-Instalador.exe');
      const targetInstaller = path.join(this.outputDir, 'AlticeFileComparator-Setup.exe');
      
      if (await fs.pathExists(generatedInstaller)) {
        await fs.move(generatedInstaller, targetInstaller);
        console.log('✅ Instalador Inno Setup creado');
      }
      
    } catch (error) {
      console.warn('⚠️ Inno Setup no disponible, creando instalador NSIS');
    }
  }

  async createNSISInstaller() {
    console.log('📦 Creando instalador NSIS...');
    
    try {
      // Usar electron-builder para crear instalador NSIS
      const command = 'npx electron-builder --win nsis --publish=never';
      
      execSync(command, {
        cwd: this.rootDir,
        stdio: 'inherit'
      });
      
      console.log('✅ Instalador NSIS creado');
      
    } catch (error) {
      console.warn('⚠️ Error al crear instalador NSIS:', error.message);
    }
  }

  async createPortableVersion() {
    console.log('💼 Creando versión portable...');
    
    try {
      const sourceDir = path.join(this.distDir, 'win-unpacked');
      const portableDir = path.join(this.outputDir, 'AlticeFileComparator-Portable');
      
      // Copiar archivos
      await fs.copy(sourceDir, portableDir);
      
      // Crear archivo de configuración para versión portable
      const portableConfig = {
        portable: true,
        dataPath: './data',
        configPath: './config'
      };
      
      await fs.writeJSON(
        path.join(portableDir, 'portable.json'),
        portableConfig,
        { spaces: 2 }
      );
      
      // Crear archivo README para versión portable
      const readmeContent = `# Altice File Comparator - Versión Portable

## Instrucciones de Uso

1. Ejecute AlticeFileComparator.exe
2. No requiere instalación
3. Todos los datos se guardan en la carpeta 'data'
4. La configuración se guarda en la carpeta 'config'

## Características

- ✅ No requiere permisos de administrador
- ✅ No modifica el registro de Windows
- ✅ Puede ejecutarse desde USB
- ✅ Fácil de transportar

## Requisitos del Sistema

- Windows 10 de 64 bits o superior
- 4 GB de RAM
- 500 MB de espacio libre

## Soporte

Email: it-support@altice.com.do
Teléfono: +1 (809) 200-1000

© 2024 Altice Dominicana
Desarrollado por: Charles Lantigua Jorge
`;

      await fs.writeFile(
        path.join(portableDir, 'README.txt'),
        readmeContent,
        'utf-8'
      );
      
      // Comprimir en ZIP
      const archiver = require('archiver');
      const zipPath = path.join(this.outputDir, 'AlticeFileComparator-Portable.zip');
      
      await this.createZip(portableDir, zipPath);
      
      console.log('✅ Versión portable creada');
      
    } catch (error) {
      console.warn('⚠️ Error al crear versión portable:', error.message);
    }
  }

  async createZip(sourceDir, outputPath) {
    return new Promise((resolve, reject) => {
      const output = fs.createWriteStream(outputPath);
      const archive = archiver('zip', { zlib: { level: 9 } });

      output.on('close', () => {
        console.log(`📦 Archivo ZIP creado: ${archive.pointer()} bytes`);
        resolve();
      });

      archive.on('error', (err) => {
        reject(err);
      });

      archive.pipe(output);
      archive.directory(sourceDir, false);
      archive.finalize();
    });
  }

  async generateChecksums() {
    console.log('🔒 Generando checksums...');
    
    try {
      const crypto = require('crypto');
      const files = await fs.readdir(this.outputDir);
      const checksums = {};

      for (const file of files) {
        if (file.endsWith('.exe') || file.endsWith('.zip')) {
          const filePath = path.join(this.outputDir, file);
          const buffer = await fs.readFile(filePath);
          const hash = crypto.createHash('sha256').update(buffer).digest('hex');
          checksums[file] = hash;
        }
      }

      await fs.writeJSON(
        path.join(this.outputDir, 'checksums.json'),
        checksums,
        { spaces: 2 }
      );

      console.log('✅ Checksums generados');
      
    } catch (error) {
      console.warn('⚠️ Error al generar checksums:', error.message);
    }
  }
}

// Ejecutar si se llama directamente
if (require.main === module) {
  const creator = new InstallerCreator();
  creator.createInstaller()
    .then(() => creator.createPortableVersion())
    .then(() => creator.generateChecksums())
    .catch(console.error);
}

module.exports = InstallerCreator;