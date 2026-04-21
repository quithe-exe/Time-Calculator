[Setup]
AppName=Time Calculator
AppVersion=1.0
DefaultDirName={pf}\TimeCalculator
DefaultGroupName=Time Calculator
OutputDir=output
OutputBaseFilename=setup
SetupIconFile=icon.ico

[Files]
Source: "dist\\app.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\Time Calculator"; Filename: "{app}\\app.exe"
Name: "{commondesktop}\\Time Calculator"; Filename: "{app}\\app.exe"
