# main.py
import tkinter as tk
from gui import FIFA_GUI_PLUS

def main():
    root = tk.Tk()
    app = FIFA_GUI_PLUS(root)
    root.mainloop()

if __name__ == "__main__":
    main()
