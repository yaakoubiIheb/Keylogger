import win32gui, win32con, win32api

# Hide the console window
win = win32gui.GetForegroundWindow()
win32gui.ShowWindow(win, win32con.SW_HIDE)

# Run your Python code
# Replace "python my_python_code.py" with the command to run your Python script
win32api.ShellExecute(0, 'open', 'cmd.exe', '/c python C:/Users/iheby/Desktop/scripting/pscript.py', None, 0)
