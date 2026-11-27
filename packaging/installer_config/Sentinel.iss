; Template only. Build and validate on Windows with Inno Setup before distribution.
#define MyAppName "Sentinel"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Sentinel"
#define MyAppExeName "Sentinel.exe"
[Setup]
AppId={{A4181907-8B27-4654-A548-2743439F66DF}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Sentinel
DefaultGroupName=Sentinel
OutputDir=output
OutputBaseFilename=Sentinel-Setup
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
Uninstallable=yes

[Files]
Source: "..\..\dist\Sentinel\Sentinel.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Sentinel"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Sentinel"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Sentinel"; Flags: nowait postinstall skipifsilent
