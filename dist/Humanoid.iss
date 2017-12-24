; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{619EBA73-4908-4793-8E8D-B2506D46E8EF}
AppName=Humanoid
AppVersion=1.0
;AppVerName=Humanoid 1.0
AppPublisher=LAB2LINCH
AppPublisherURL=https://github.com/LAB2LINCH/2DGame_Python
AppSupportURL=https://github.com/LAB2LINCH/2DGame_Python
AppUpdatesURL=https://github.com/LAB2LINCH/2DGame_Python
DefaultDirName={pf}\Humanoid
DisableProgramGroupPage=yes
OutputDir=D:\Project\2DGame_Python\dist
OutputBaseFilename=Humanoid_Setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "D:\Project\2DGame_Python\dist\Humanoid.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Project\2DGame_Python\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\Humanoid"; Filename: "{app}\Humanoid.exe"
Name: "{commondesktop}\Humanoid"; Filename: "{app}\Humanoid.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Humanoid.exe"; Description: "{cm:LaunchProgram,Humanoid}"; Flags: nowait postinstall skipifsilent

