import tkinter as tk
import tkinter.filedialog as fdialog

def save_as():

    # From line 1, char 0 to end - 1 char (avoid last newline)
    content = text.get("1.0", "end-1c")
    path = fdialog.asksaveasfilename(defaultextension=".txt", filetypes=
                                     [("Text Files", "*.txt"), ("All Files", "*.*")],
                                     initialfile="Untitled.txt")
    
    # Save to file
    if path:
        with open(path, "w") as file:
            file.write(content)
        update_status("File Saved")

def open_file():
    path = fdialog.askopenfilename(defaultextension=".txt", filetypes=
                                   [("Text Files", "*.txt"), ("All Files", "*.*")])
    if path:
        with open(path, "r") as file:
            # Clear current text and write over it
            text.delete("1.0", "end")
            text.insert("1.0", file.read())
            update_status(f"Opened {path}")

def set_font(font_name):
    text.config(font=(font_name, 12))

def create_menu():
    menu_bar = tk.Menu(root)

    # Create file menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save As", command=save_as)
    
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Create edit menu
    edit_menu = tk.Menu(menu_bar, tearoff=0)

    # Create font
    font_menu = tk.Menu(edit_menu, tearoff=0)
    font_names = ["Helvetica", "Courier", "Times", "Arial", "Comic Sans MS"]

    for name in font_names:
        font_menu.add_command(label=name, command=lambda font_name=name: set_font(font_name))
    
    edit_menu.add_cascade(label="Font", menu=font_menu)
    
    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    root.config(menu=menu_bar)

def update_status(message):
    status.config(text=message)

def word_count(event=None):
    content = text.get("1.0", "end-1c")
    char_count = len(content)
    word_count = len(content.split())
    update_status(f"{char_count} characters, {word_count} words")

def main():
    global root, text, status

    # Create main aplication window
    root = tk.Tk()
    root.title("Text editor")

    # Start size
    root.geometry("640x480")

    # Use keybinds
    root.bind("<Control-s>", lambda event: save_as())
    root.bind("<Control-o>", lambda event: open_file())

    # Status bar
    status = tk.Label(root, text="Ready", anchor="w")
    status.grid(row=3, column=0, columnspan=2, sticky="ew")

    # Configure grid to expand properly
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Text editor area
    text = tk.Text(root, wrap="word")
    text.grid(row=0, column=0, sticky="nsew")
    
    # Add word counter to status bar
    text.bind("<KeyRelease>", word_count)

    # Add scrollbar
    scollbar = tk.Scrollbar(root, orient="vertical", command=text.yview)
    scollbar.grid(row=0, column=1, sticky="ns")
    text.config(yscrollcommand=scollbar.set)

    # Create the menu bar
    create_menu()

    # App loop
    root.mainloop()

if __name__ == "__main__":
    main()