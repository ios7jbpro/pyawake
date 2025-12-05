[Setup]
AppName=PyAwake
AppVersion=1.0
DefaultDirName={userdocs}\PyAwake
DisableProgramGroupPage=yes
OutputDir=.
Compression=lzma

[Files]
Source: "pyawake.exe"; DestDir: "{userdocs}\PyAwake"; Flags: ignoreversion

[Icons]
Name: "{userstartup}\PyAwake"; Filename: "{userdocs}\PyAwake\pyawake.exe"

[Run]
Filename: "{userdocs}\PyAwake\pyawake.exe"; Flags: postinstall nowait
