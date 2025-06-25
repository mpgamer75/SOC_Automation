const { execSync } = require('child_process');
const path = require('path');

function run(cmd, cwd) {
  console.log(`\n> ${cmd}`);
  execSync(cmd, { stdio: 'inherit', cwd });
}

try {
  // 1. Build frontend
  run('npm install', path.join(__dirname, '../frontend2'));
  run('npm run build', path.join(__dirname, '../frontend2'));

  // 2. Build backend (PyInstaller)
  try {
    run('pyinstaller --onefile --name altice-backend main.py', path.join(__dirname, '../backend'));
  } catch (e) {
    console.warn('⚠️ Erreur lors du packaging backend (PyInstaller). À corriger manuellement si besoin.');
  }

  // 3. Build/package Electron
  run('npm install', path.join(__dirname, '../app'));
  run('npm run package', path.join(__dirname, '../app'));

  console.log('\n✅ Build complet terminé.');
} catch (err) {
  console.error('❌ Build global échoué:', err);
  process.exit(1);
} 