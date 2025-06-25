; Script de instalación para Altice File Comparator
; Creado por Charles Lantigua Jorge para Altice Dominicana

#define MyAppName "Altice File Comparator"
#define MyAppVersion "2.1.0"
#define MyAppPublisher "Altice Dominicana"
#define MyAppExeName "Altice File Comparator.exe"
#define MyAppURL "https://altice.com.do"
#define MyAppId "{{B8C8E5A1-7F2D-4B3C-8D9E-1A2B3C4D5E6F}"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/soporte
AppUpdatesURL={#MyAppURL}/actualizaciones
DefaultDirName={autopf}\Altice File Comparator
DefaultGroupName=Altice File Comparator
LicenseFile=installer\license-es.txt
InfoBeforeFile=installer\info-antes-es.txt
InfoAfterFile=installer\info-despues-es.txt
OutputDir=..\dist
OutputBaseFilename=AlticeFileComparator-Setup
SetupIconFile=installer\assets\icon.ico
UninstallDisplayIcon={app}\installer\assets\uninstall.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
WizardImageFile=installer\assets\setup-banner.bmp
WizardSmallImageFile=installer\assets\setup-sidebar.bmp
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no
DisableReadyPage=no
DisableFinishedPage=no
CreateAppDir=yes
CreateUninstallRegKey=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
MinVersion=0,6.1sp1
Languages=spanish
ShowLanguageDialog=no

; Páginas personalizadas del wizard
WizardImageStretch=no
WizardImageBackColor=$FFFFFF
WindowResizable=no
WindowShowCaption=yes
WindowStartMaximized=no
WindowVisible=yes

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"; LicenseFile: "installer\license-es.txt"; InfoBeforeFile: "installer\info-antes-es.txt"; InfoAfterFile: "installer\info-despues-es.txt"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
spanish.WelcomeLabel2=Este asistente lo guiará a través de la instalación de [name/ver]%n%nEsta herramienta profesional le permitirá comparar archivos CSV, Excel y XLS de manera eficiente y precisa.%n%nDesarrollado específicamente para el equipo de Altice Dominicana.%n%nSe recomienda cerrar todas las demás aplicaciones antes de continuar.
spanish.FinishedHeadingLabel=Completando la instalación de [name]
spanish.FinishedLabelNoIcons=La instalación de [name] se ha completado exitosamente.%n%nLa aplicación está lista para usar y se ha creado un acceso directo en su escritorio.
spanish.FinishedLabel=La instalación de [name] se ha completado exitosamente.%n%nLa aplicación puede ejecutarse seleccionando los íconos instalados.
spanish.ClickFinish=Haga clic en Finalizar para salir del asistente de instalación.
spanish.RunEntryExec=Ejecutar {#MyAppName}
spanish.RunEntryShellExec=Abrir guía de usuario

[Tasks]
Name: "desktopicon"; Description: "Crear un acceso directo en el &escritorio"; GroupDescription: "Accesos directos adicionales:"
Name: "quicklaunchicon"; Description: "Crear un acceso directo en la &barra de inicio rápido"; GroupDescription: "Accesos directos adicionales:"; Flags: unchecked; OnlyBelowVersion: 0,6.1
Name: "associate"; Description: "Asociar archivos CSV y Excel con {#MyAppName}"; GroupDescription: "Asociaciones de archivos:"

[Files]
; Archivos principales de la aplicación
Source: "..\dist\win-unpacked\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Documentación
Source: "..\docs\USER_GUIDE_ES.pdf"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\docs\INSTALLATION_GUIDE_ES.pdf"; DestDir: "{app}\docs"; Flags: ignoreversion
; Archivos de ejemplo
Source: "..\examples\*"; DestDir: "{app}\examples"; Flags: ignoreversion recursesubdirs createallsubdirs
; Visual C++ Redistributable (si es necesario)
Source: "redist\VC_redist.x64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall; Check: VCRedistNeedsInstall

[Registry]
; Asociaciones de archivos
Root: HKCR; Subkey: ".csv"; ValueType: string; ValueName: ""; ValueData: "AlticeComparator.CSVFile"; Flags: uninsdeletevalue; Tasks: associate
Root: HKCR; Subkey: ".xlsx"; ValueType: string; ValueName: ""; ValueData: "AlticeComparator.ExcelFile"; Flags: uninsdeletevalue; Tasks: associate
Root: HKCR; Subkey: ".xls"; ValueType: string; ValueName: ""; ValueData: "AlticeComparator.ExcelFile"; Flags: uninsdeletevalue; Tasks: associate

Root: HKCR; Subkey: "AlticeComparator.CSVFile"; ValueType: string; ValueName: ""; ValueData: "Archivo CSV de Altice Comparator"; Flags: uninsdeletekey; Tasks: associate
Root: HKCR; Subkey: "AlticeComparator.CSVFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"; Tasks: associate
Root: HKCR; Subkey: "AlticeComparator.CSVFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Tasks: associate

Root: HKCR; Subkey: "AlticeComparator.ExcelFile"; ValueType: string; ValueName: ""; ValueData: "Archivo Excel de Altice Comparator"; Flags: uninsdeletekey; Tasks: associate
Root: HKCR; Subkey: "AlticeComparator.ExcelFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"; Tasks: associate
Root: HKCR; Subkey: "AlticeComparator.ExcelFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Tasks: associate

; Entradas del registro para la aplicación
Root: HKLM; Subkey: "Software\Altice\FileComparator"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Altice\FileComparator"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Altice\FileComparator"; ValueType: dword; ValueName: "Installed"; ValueData: 1; Flags: uninsdeletekey

[Icons]
; Accesos directos en el menú de inicio
Name: "{group}\Altice File Comparator"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Comment: "Comparador de archivos profesional para Altice"
Name: "{group}\Guía de Usuario"; Filename: "{app}\docs\USER_GUIDE_ES.pdf"; Comment: "Manual de usuario completo"
Name: "{group}\Archivos de Ejemplo"; Filename: "{app}\examples"; Comment: "Archivos de ejemplo para pruebas"
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"; Comment: "Desinstalar {#MyAppName}"

; Acceso directo en el escritorio
Name: "{commondesktop}\Altice File Comparator"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Comment: "Comparador de archivos Altice"; Tasks: desktopicon

; Acceso directo en la barra de inicio rápido
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; Instalar Visual C++ Redistributable si es necesario
Filename: "{tmp}\VC_redist.x64.exe"; Parameters: "/quiet /norestart"; StatusMsg: "Instalando Visual C++ Redistributable..."; Check: VCRedistNeedsInstall

; Ejecutar la aplicación después de la instalación
Filename: "{app}\{#MyAppExeName}"; Description: "Ejecutar {#MyAppName} ahora"; Flags: nowait postinstall skipifsilent shellexec

; Abrir la guía de usuario
Filename: "{app}\docs\USER_GUIDE_ES.pdf"; Description: "Abrir guía de usuario"; Flags: nowait postinstall skipifsilent shellexec unchecked

[UninstallDelete]
Type: filesandordirs; Name: "{app}\temp"
Type: filesandordirs; Name: "{app}\logs"
Type: files; Name: "{app}\*.log"

[Code]
// Función para verificar si Visual C++ Redistributable está instalado
function VCRedistNeedsInstall: Boolean;
var
  Version: String;
begin
  Result := not RegQueryStringValue(HKLM, 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Version', Version);
end;

// Función personalizada para la página de bienvenida
procedure InitializeWizard();
var
  WelcomePage: TWizardPage;
  LogoImage: TBitmapImage;
  WelcomeLabel: TLabel;
  DescriptionLabel: TLabel;
begin
  // Crear página de bienvenida personalizada
  WelcomePage := CreateCustomPage(wpWelcome, 'Bienvenido a Altice File Comparator', 'Instalación de herramienta profesional de comparación de archivos');
  
  // Logo de Altice
  LogoImage := TBitmapImage.Create(WelcomePage);
  LogoImage.Parent := WelcomePage.Surface;
  LogoImage.Left := 20;
  LogoImage.Top := 20;
  LogoImage.Width := 100;
  LogoImage.Height := 60;
  try
    LogoImage.Bitmap.LoadFromFile(ExpandConstant('{tmp}\logo-altice.bmp'));
  except
    // Si no se puede cargar el logo, continuar sin él
  end;
  
  // Etiqueta de bienvenida
  WelcomeLabel := TLabel.Create(WelcomePage);
  WelcomeLabel.Parent := WelcomePage.Surface;
  WelcomeLabel.Left := 140;
  WelcomeLabel.Top := 30;
  WelcomeLabel.Width := 300;
  WelcomeLabel.Height := 30;
  WelcomeLabel.Font.Size := 14;
  WelcomeLabel.Font.Style := [fsBold];
  WelcomeLabel.Caption := 'Altice File Comparator v' + '{#MyAppVersion}';
  
  // Descripción
  DescriptionLabel := TLabel.Create(WelcomePage);
  DescriptionLabel.Parent := WelcomePage.Surface;
  DescriptionLabel.Left := 20;
  DescriptionLabel.Top := 100;
  DescriptionLabel.Width := 420;
  DescriptionLabel.Height := 180;
  DescriptionLabel.WordWrap := True;
  DescriptionLabel.Caption := 
    'Esta herramienta profesional le permitirá:' + #13#10 + #13#10 +
    '• Comparar archivos CSV, Excel (.xlsx) y XLS de manera precisa' + #13#10 +
    '• Identificar diferencias automáticamente con análisis detallado' + #13#10 +
    '• Generar reportes profesionales en múltiples formatos' + #13#10 +
    '• Mantener una biblioteca de archivos de referencia' + #13#10 +
    '• Visualizar diferencias con gráficos interactivos' + #13#10 + #13#10 +
    'Desarrollado especialmente para el equipo de Altice Dominicana.' + #13#10 + #13#10 +
    'Haga clic en "Siguiente" para continuar con la instalación.';
end;

// Función para mostrar progreso personalizado
procedure CurPageChanged(CurPageID: Integer);
begin
  case CurPageID of
    wpInstalling:
    begin
      WizardForm.StatusLabel.Caption := 'Instalando archivos de la aplicación...';
    end;
    wpFinished:
    begin
      WizardForm.StatusLabel.Caption := '¡Instalación completada exitosamente!';
    end;
  end;
end;

// Función para validar la instalación
function InitializeSetup(): Boolean;
var
  Version: String;
begin
  Result := True;
  
  // Verificar si ya está instalada una versión
  if RegQueryStringValue(HKLM, 'SOFTWARE\Altice\FileComparator', 'Version', Version) then
  begin
    if MsgBox('Se detectó una versión anterior de ' + '{#MyAppName}' + ' (v' + Version + ').' + #13#10 + #13#10 + 
              '¿Desea continuar con la instalación? Esta acción actualizará la versión existente.',
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
  
  // Verificar requisitos del sistema
  if not IsWin64 then
  begin
    MsgBox('Este programa requiere Windows de 64 bits.' + #13#10 + 
           'Su sistema actual no es compatible.',
           mbError, MB_OK);
    Result := False;
  end;
end;

// Función ejecutada al completar la instalación
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  case CurStep of
    ssPostInstall:
    begin
      // Crear archivos de configuración inicial
      StringChangeEx('{app}\config\default.json', '{INSTALL_PATH}', ExpandConstant('{app}'), True);
      
      // Registrar la aplicación en el firewall de Windows (si es necesario)
      Exec('netsh', 'advfirewall firewall add rule name="Altice File Comparator" dir=in action=allow program="' + ExpandConstant('{app}\{#MyAppExeName}') + '"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    end;
  end;
end;

// Función para personalizar la página de finalización
procedure DeinitializeSetup();
begin
  // Limpiar archivos temporales
  DeleteFile(ExpandConstant('{tmp}\logo-altice.bmp'));
end;