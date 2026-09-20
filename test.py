import customtkinter as ctk
import sys

# Fix for macOS rendering issues - REQUIRED!
ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("blue")

# Create window
root = ctk.CTk()
root.geometry("500x350")
root.title("CustomTkinter Test")

# Force window update
root.update()

# Create button with explicit colors (needed for macOS Tk 8.6)
button = ctk.CTkButton(
    master=root,
    text="Click Me!",
    width=200,
    height=40,
    fg_color=("gray75", "gray25"),  # (light mode, dark mode) - REQUIRED for visibility
    text_color=("black", "white")
)
button.place(relx=0.5, rely=0.5, anchor="center")

# Force update again
root.update_idletasks()

root.mainloop()
