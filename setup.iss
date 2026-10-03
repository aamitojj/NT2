[Setup]
AppName=NETBOOST
AppVersion=0.3
DefaultDirName={autopf}\NETBOOST
DefaultGroupName=NETBOOST
OutputBaseFilename=NETBOOST-setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "dist\NETBOOST.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\NETBOOST"; Filename: "{app}\NETBOOST.exe"
Name: "{autodesktop}\NETBOOST"; Filename: "{app}\NETBOOST.exe"
