import os
import time
import threading
import tkinter as tk
from tkinter import messagebox
import sys
import winreg

# Script running
running = False

def kill_process():
    
    global running
    running = True
    while running:
        os.system("taskkill /F /IM WpcUapApp.exe")
        time.sleep(1)

def start_script():
    """Starts the process-killing script in a separate thread"""
    global running
    if not running:
        threading.Thread(target=kill_process, daemon=True).start()
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

def stop_script():
    """Stops the process-killing script"""
    global running
    running = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def add_to_startup():
    """Adds the script to Windows Startup"""
    try:
        script_path = os.path.abspath(sys.argv[0])
        startup_name = "KillWpcUapApp"
        key = winreg.HKEY_CURRENT_USER
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        with winreg.OpenKey(key, reg_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, startup_name, 0, winreg.REG_SZ, script_path)

        messagebox.showinfo("Success", "Script added to startup.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add to startup: {e}")

def remove_from_startup():
    """Removes the script from Windows Startup"""
    try:
        startup_name = "KillWpcUapApp"
        key = winreg.HKEY_CURRENT_USER
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        with winreg.OpenKey(key, reg_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.DeleteValue(reg_key, startup_name)

        messagebox.showinfo("Success", "Script removed from startup.")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "Script is not in startup.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove from startup: {e}")

# GUI Setup
root = tk.Tk()
root.title("No more screentime")
root.geometry("300x200")

start_button = tk.Button(root, text="Start Script", command=start_script)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Script", command=stop_script, state=tk.DISABLED)
stop_button.pack(pady=5)

startup_button = tk.Button(root, text="Start on boot", command=add_to_startup)
startup_button.pack(pady=5)

remove_startup_button = tk.Button(root, text="Remove from boot", command=remove_from_startup)
remove_startup_button.pack(pady=5)

root.mainloop()
