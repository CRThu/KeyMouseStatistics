C:\Anaconda3\Scripts\pyinstaller.exe ..\entrance.py -p ..\DataStorage.py -p ..\GetAdmin.py -p ..\KeyboardHookListenerClass.py -p ..\MouseHookListenerClass.py -p ..\SQLite_oper.py -p ..\stdout_to_log.py -p ..\tkinter_gui.py -n KeyMouseStatistics -F -d --uac-admin
copy .\KeyMouseStatistics.exe.manifest .\dist\KeyMouseStatistics.exe.manifest
del .\dist\debug_out.log
del .\dist\kmstat.db
pause