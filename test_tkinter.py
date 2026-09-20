import tkinter as tk

# Create window
root = tk.Tk()
root.geometry("800x350")
root.title("Tkinter App")
root.configure(bg="#faf602")

# Function for button click
def button_click():
    print("Button clicked!")
    label.config(text="Button was clicked!")

# Create label
label = tk.Label(
    root,
    text="Welcome! This a simple APP to test CustomTK Working | To check Click the button below",
    font=("Arial", 14),
    fg="black",
    bg="#03f734"
)
label.pack(pady=30)

# Create button
button = tk.Button(
    root,
    text="Click Me!",
    command=button_click,
    width=20,
    height=2,
    font=("Arial", 14),
    bg="#0C0B00",
    fg="black",
    activebackground="#0051D5",
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)
button.pack(pady=20)

root.mainloop()
