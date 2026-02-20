Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "python telegram_bridge.py", 0, False
Set WshShell = Nothing
