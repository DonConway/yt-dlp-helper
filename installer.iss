
[Setup]
AppId=YT-DLP Helper
AppName=YT-DLP Helper
AppVersion=1.0.1
DefaultDirName={localappdata}\Programs\YT-DLP Helper
DefaultGroupName=YT-DLP Helper
OutputDir=installer-output
OutputBaseFilename=YT-DLP-Helper-v1.0.1-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
UninstallDisplayName=YT-DLP Helper

[Files]
Source: "dist\YT-DLP-Helper-v1.0.1.exe"; DestDir: "{app}"; DestName: "YT-DLP-Helper.exe"; Flags: ignoreversion
Source: "dist\bin\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "THIRD_PARTY_LICENSES.txt"; DestDir: "{app}"; Flags: ignoreversion

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Icons]
Name: "{group}\YT-DLP Helper"; Filename: "{app}\YT-DLP-Helper.exe"
Name: "{autodesktop}\YT-DLP Helper"; Filename: "{app}\YT-DLP-Helper.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\YT-DLP-Helper.exe"; Description: "Launch YT-DLP Helper"; Flags: nowait postinstall skipifsilent

[InstallDelete]
Type: files; Name: "{app}\YT-DLP-Helper-v1.0.0.exe"
Type: files; Name: "{app}\YT-DLP-Helper-v1.0.1.exe"