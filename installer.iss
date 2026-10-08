
[Setup]
AppName=YT-DLP Helper
AppVersion=1.0.0
DefaultDirName={localappdata}\Programs\YT-DLP Helper
DefaultGroupName=YT-DLP Helper
OutputDir=installer-output
OutputBaseFilename=YT-DLP-Helper-v1.0.0-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
UninstallDisplayName=YT-DLP Helper

[Files]
Source: "dist\YT-DLP-Helper-v1.0.0.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\bin\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "THIRD_PARTY_LICENSES.txt"; DestDir: "{app}"; Flags: ignoreversion

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Icons]
Name: "{group}\YT-DLP Helper"; Filename: "{app}\YT-DLP-Helper-v1.0.0.exe"
Name: "{autodesktop}\YT-DLP Helper"; Filename: "{app}\YT-DLP-Helper-v1.0.0.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\YT-DLP-Helper-v1.0.0.exe"; Description: "Launch YT-DLP Helper"; Flags: nowait postinstall skipifsilent
