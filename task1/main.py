# main.py
import tkinter as tk
from gui import EmergencyGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = EmergencyGUI(root)
    root.mainloop()