import tkinter as tk
import tkinter.filedialog as fdialog
import tkinter.font as font
import tkinter.simpledialog as dialog


def save_as():
    global current_path

    # From line 1, char 0 to end - 1 char (avoid last newline)
    content = text.get("1.0", "end-1c")
    path = fdialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        initialfile="Untitled.txt",
    )

    # Save to file
    if path:
        with open(path, "w") as file:
            file.write(content)
        current_path = path
        update_status("File Saved")


def save_file(event=None):
    global current_path
    content = text.get("1.0", "end-1c")

    if current_path:
        with open(current_path, "w") as file:
            file.write(content)
        update_status(f"Saved to {current_path}")
    else:
        save_as()


def open_file():
    global current_path

    path = fdialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if path:
        with open(path, "r") as file:
            # Clear current text and write over it
            text.delete("1.0", "end")
            text.insert("1.0", file.read())
        current_path = path
        update_status(f"Opened {path}")


def set_font(font_name):
    global current_font
    new_font = font.Font(font=(font_name, current_size))
    current_font = font_name
    text.config(font=new_font)


def set_size(font_size):
    global current_size
    new_font = font.Font(font=(current_font, font_size))
    current_size = font_size
    text.config(font=new_font)


def create_menu():
    menu_bar = tk.Menu(root)

    # Create file menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_command(label="Save As", command=save_as)

    menu_bar.add_cascade(label="File", menu=file_menu)

    # Create edit menu
    edit_menu = tk.Menu(menu_bar, tearoff=0)

    # Create font menu
    font_menu = tk.Menu(edit_menu, tearoff=0)
    font_names = ["Helvetica", "Courier", "Times", "Arial", "Comic Sans MS"]
    for name in font_names:
        font_menu.add_command(
            label=name, command=lambda font_name=name: set_font(font_name)
        )
    edit_menu.add_cascade(label="Font", menu=font_menu)

    # Create size menu
    size_menu = tk.Menu(edit_menu, tearoff=0)
    sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 30, 40]
    for size in sizes:
        size_menu.add_command(
            label=size, command=lambda font_size=size: set_size(font_size)
        )
    edit_menu.add_cascade(label="Size", menu=size_menu)
    edit_menu.add_command(label="Bold", command=toggle_bold)
    edit_menu.add_command(label="Italic", command=toggle_italic)
    edit_menu.add_command(label="Strikethrough", command=toggle_strikethrough)
    edit_menu.add_command(label="Underline", command=toggle_underline)

    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    root.config(menu=menu_bar)


def update_status(message):
    status.config(text=message)


def word_count(event=None):
    content = text.get("1.0", "end-1c")
    char_count = len(content)
    word_count = len(content.split())
    update_status(f"{char_count} characters, {word_count} words")


def toggle_bold():
    current_font = font.Font(font=text.cget("font"))
    if current_font.cget("weight") == "normal":
        current_font.config(weight="bold")
    else:
        current_font.config(weight="normal")
    text.config(font=current_font)


def toggle_italic():
    current_font = font.Font(font=text.cget("font"))
    if current_font.cget("slant") == "roman":
        current_font.config(slant="italic")
    else:
        current_font.config(slant="roman")
    text.config(font=current_font)


def toggle_strikethrough():
    current_font = font.Font(font=text.cget("font"))
    if current_font.cget("overstrike") == 0:
        current_font.config(overstrike=1)
    else:
        current_font.config(overstrike=0)
    text.config(font=current_font)


def toggle_underline():
    current_font = font.Font(font=text.cget("font"))
    if current_font.cget("underline") == 0:
        current_font.config(underline=1)
    else:
        current_font.config(underline=0)
    text.config(font=current_font)


def on_close():
    answer = tk.messagebox.askyesnocancel("Quit", "Do you want to save before exiting?")

    if answer:
        save_file()
        root.destroy()
    elif answer is False:
        root.destroy()
    else:
        return


def undo():
    try:
        text.edit_undo()
    except tk.TclError:
        pass


def redo():
    try:
        text.edit_redo()
    except tk.TclError:
        pass

def find():
    text_to_find = dialog.askstring("Find", "Enter text to find: ")

    if text_to_find:
        start_index = text.index("1.0")
        while start_index:
            start_index = text.search(text_to_find, start_index, stopindex="end")
            if not start_index:
                    break
            end_index = f"{start_index}+{len(text_to_find)}c"
            text.tag_add("highlight", start_index, end_index)
            text.tag_config("highlight", background="yellow")
            start_index = end_index
            root.after(10000, lambda: text.tag_remove("highlight", "1.0", "end"))
    

def replace():
    text_to_find = dialog.askstring("Find", "Enter text to find: ")
    if text_to_find:
        text_to_replace = dialog.askstring("Replace", "Enter text to replace with: ")
        if text_to_replace:
            start_index = text.index("1.0")
            while start_index:
                start_index = text.search(text_to_find, start_index, stopindex="end")
                if not start_index:
                    break
                end_index = f"{start_index}+{len(text_to_find)}c"
                text.delete(start_index, end_index)
                text.insert(start_index, text_to_replace)
                start_index = f"{start_index}+{len(text_to_replace)}c"
        
            

def main():
    global root, text, status, current_font, current_size, current_path

    current_path = None

    # Default font and size
    current_font = "Helvetica"
    current_size = 12

    # Create main aplication window
    root = tk.Tk()
    root.title("Text editor")

    # Start size
    root.geometry("640x480")

    # Keybinds
    root.bind("<Control-s>", lambda event: save_file())
    root.bind("<Control-o>", lambda event: open_file())
    root.bind("<Control-b>", lambda event: toggle_bold())
    root.bind("<Control-i>", lambda event: toggle_italic())
    root.bind("<Control-t>", lambda event: toggle_strikethrough())
    root.bind("<Control-u>", lambda event: toggle_underline())
    root.bind("<Control-plus>", lambda event: set_size(current_size + 2))
    root.bind(
        "<Control-minus>",
        lambda event: set_size(current_size - 2) if current_size > 2 else None,
    )
    root.bind("<Control-z>", lambda event: undo())
    root.bind("<Control-y>", lambda event: redo())
    root.bind("<Control-f>", lambda event: find())
    root.bind("<Control-h>", lambda event: replace())

    # Status bar
    status = tk.Label(root, text="Ready", anchor="w")
    status.grid(row=3, column=0, columnspan=2, sticky="ew")

    # Configure grid to expand properly
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Text editor area
    text = tk.Text(root, wrap="word", undo=True, maxundo=-1)
    text.grid(row=0, column=0, sticky="nsew")

    # Add word counter to status bar
    text.bind("<KeyRelease>", word_count)

    # Add scrollbar
    scollbar = tk.Scrollbar(root, orient="vertical", command=text.yview)
    scollbar.grid(row=0, column=1, sticky="ns")
    text.config(yscrollcommand=scollbar.set)

    # Create the menu bar
    create_menu()

    # Ask before exit
    root.protocol("WM_DELETE_WINDOW", on_close)

    # App loop
    root.mainloop()


if __name__ == "__main__":
    main()
