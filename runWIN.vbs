Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c guiStarter.bat"
oShell.Run strArgs, 0, false