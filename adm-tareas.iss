[Setup]
AppName=Administrador de Tareas
AppVersion=1.0
DefaultDirName={pf}\Administrador de Tareas
DefaultGroupName=Administrador de Tareas
OutputDir=.
OutputBaseFilename=instalador_administrador_tareas
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\Alumno\Desktop\administrador-tareas.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Administrador de Tareas"; Filename: "{app}\administrador-tareas.exe"
Name: "{commondesktop}\Administrador de Tareas"; Filename: "{app}\administrador-tareas.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear un acceso directo en el escritorio"; GroupDescription: "Accesos directos"; Flags: unchecked

[Run]
Filename: "{app}\administrador-tareas.exe"; Description: "{cm:LaunchProgram,Administrador de Tareas}"; Flags: nowait postinstall skipifsilent
