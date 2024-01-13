import tkinter as tk
from tkinter import filedialog
class TextEditorApp:
    """
    Simple text editor application using Tkinter.
    """
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the TextEditorApp.
        Parameters:
        - root (tk.Tk): The Tkinter root window.
        """
        self.root = root
        self.root.title("My Text Editor")
        self.root.geometry('1000x700')
        self.my_frame: tk.Frame = tk.Frame(root)
        self.my_frame.pack()
        self.text_scroll: tk.Scrollbar = tk.Scrollbar(self.my_frame)
        self.text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.my_text: tk.Text = tk.Text(self.my_frame, width=97, height=25, font=('Times', 16), selectbackground='green', selectforeground='black', undo=True, yscrollcommand=self.text_scroll.set)
        self.my_text.pack()
        self.text_scroll.config(command=self.my_text.yview)
        '''Menu'''
        self.create_menu()
        self.status_bar: tk.Label = tk.Label(root, text="Start", anchor=tk.E)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, ipady=5)
        self.open_status_name: str = ""
        self.selected: str = ""
    def create_menu(self) -> None:
        """
        Create the menu for the Text Editor.
        """
        # Creating Menu
        self.my_menu: tk.Menu = tk.Menu(self.root)
        self.root.config(menu=self.my_menu)
        self.file_menu: tk.Menu = tk.Menu(self.my_menu)
        self.my_menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='New', command=self.new_file)
        self.file_menu.add_command(label='Open', command=self.open_file)
        self.file_menu.add_command(label='Save', command=self.save_file)
        self.file_menu.add_command(label='Save as', command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.root.quit)
        self.edit_menu: tk.Menu = tk.Menu(self.my_menu)
        self.my_menu.add_cascade(label='Edit', menu=self.edit_menu)
        self.edit_menu.add_command(label='Cut', command=lambda: self.cut_text(False))
        self.edit_menu.add_command(label='Copy', command=lambda: self.copy_text(False))
        self.edit_menu.add_command(label='Paste', command=lambda: self.paste_text(False))
        self.edit_menu.add_command(label='Undo', command=self.my_text.edit_undo)
        self.edit_menu.add_command(label='Redo', command=self.my_text.edit_redo)
    def new_file(self) -> None:
        """
        Create a new file by clearing the text area and resetting the title.
        """
        self.my_text.delete('1.0', tk.END)
        self.root.title("Text Editor")
        self.update_status_bar("Ready")
        self.open_status_name = ""
    def open_file(self) -> None:
        """
        Open an existing file by loading its content into the text area.
        """
        self.my_text.delete("1.0", tk.END)
        text_file: str = filedialog.askopenfilename(title="Open File", filetypes=(("Text Files", "*.txt"), ("All Files", "*"), ("Python Files", "*.py"), ("HTML Files", "*.html")))
        if text_file:
            self.open_status_name = text_file
        with open(text_file, 'r') as file:
            reading: str = file.read()
            self.my_text.insert(tk.END, reading)
    def save_as_file(self) -> None:
        """
        Save the current text as a new file.
        """
        text_file: str = filedialog.asksaveasfilename(defaultextension=".*", title="Save File as", filetypes=(("Text Files", "*.txt"), ("All Files", "*"), ("Python Files", "*.py"), ("HTML Files", "*.html")))
        with open(text_file, 'w') as file:
            file.write(self.my_text.get("1.0", tk.END))
        self.update_status_bar("File saved successfully!")
    def save_file(self) -> None:
        """
        Save the current text to the existing or newly specified file.
        """
        if self.open_status_name:
            with open(self.open_status_name, 'w') as file:
                file.write(self.my_text.get("1.0", tk.END))
            self.update_status_bar("File saved successfully!")
        else:
            self.save_as_file()
    def cut_text(self, e: bool) -> None:
        """
        Cut the selected text and store it in the clipboard.
        Parameters:
        - e (bool): True if cut is performed via keyboard shortcut, False otherwise.
        """
        if e:
            self.selected = self.root.selection_get()
        else:
            if self.my_text.selection_get():
                self.selected = self.my_text.selection_get()
                self.my_text.delete("sel.first", "sel.last")
    def copy_text(self, e: bool) -> None:
        """
        Copy the selected text and store it in the clipboard.
        Parameters:
        - e (bool): True if copy is performed via keyboard shortcut, False otherwise.
        """
        if e:
            self.selected = self.root.clipboard_get()
        if self.my_text.selection_get():
            self.selected = self.my_text.selection_get()
            self.root.clipboard_clear()
            self.root.clipboard_append(self.selected)
    def paste_text(self, e: bool) -> None:
        """
        Paste the text from the clipboard at the current cursor position.
        Parameters:
        - e (bool): True if paste is performed via keyboard shortcut, False otherwise.
        """
        if e:
            self.selected = self.root.clipboard_get()
        else:
            if self.selected:
                position: str = self.my_text.index(tk.INSERT)
                self.my_text.insert(position, self.selected)
    def update_status_bar(self, text: str) -> None:
        """
        Update the status bar with the specified text.
        Parameters:
        - text (str): The text to be displayed in the status bar.
        """
        self.status_bar.config(text=text)
if __name__ == "__main__":
    root: tk.Tk = tk.Tk()
    app: TextEditorApp = TextEditorApp(root)
    root.mainloop()
