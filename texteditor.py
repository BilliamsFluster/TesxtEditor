import tkinter as tk
from tkinter import filedialog, Text, Menu, simpledialog

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        
        # Define colors for dark mode and syntax highlighting
        self.bg_color = '#2e2e2e'
        self.fg_color = '#f5f5f5'
        self.keyword_color = '#00aaff'
        self.string_color = '#ffa500'
        self.comment_color = '#00ff00'
        
        # Create the main text widget for writing code or text
        self.text_widget = Text(self.root, wrap='word', undo=True, bg=self.bg_color, fg=self.fg_color, insertbackground='white', selectbackground='#4a4a4a')
        self.text_widget.pack(expand=1, fill='both', side='right')
        
        # Bind events for line numbers and syntax highlighting
        self.text_widget.bind('<Any-KeyPress>', self.update_line_numbers)  # Bind to Any-KeyPress for line numbers
        self.text_widget.bind('<KeyRelease>', self.syntax_highlighting, add='+' )
        
        # Create a widget for line numbers
        self.line_numbers = tk.Text(self.root, width=4, padx=3, takefocus=0, highlightthickness=0, bd=0, bg='#1c1c1c', fg=self.fg_color, state='disabled')
        self.line_numbers.pack(side='left', fill='y')
        
        # Create Open, Save, and New buttons
        self.create_buttons()
        
        # Create the main menu
        self.create_menu()
        
        # Create a status bar for displaying the current line number
        self.create_status_bar()

    def create_buttons(self):
        """Create buttons for New, Open, and Save operations."""
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill='x')
        
        new_button = tk.Button(button_frame, text="New", command=self.new_file, bg=self.bg_color, fg=self.fg_color)
        new_button.pack(side='left')
        
        open_button = tk.Button(button_frame, text="Open", command=self.open_file, bg=self.bg_color, fg=self.fg_color)
        open_button.pack(side='left')
        
        save_button = tk.Button(button_frame, text="Save", command=self.save_file, bg=self.bg_color, fg=self.fg_color)
        save_button.pack(side='left')

    def create_menu(self):
        """Create the main menu with File and Edit options."""
        menu = Menu(self.root, bg=self.bg_color, fg=self.fg_color)
        self.root.config(menu=menu)
        
        file_menu = Menu(menu, bg=self.bg_color, fg=self.fg_color)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Close", command=self.root.quit)
        
        edit_menu = Menu(menu, bg=self.bg_color, fg=self.fg_color)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)

    def new_file(self):
        """Clear the text widget for a new file."""
        self.text_widget.delete(1.0, tk.END)

    def open_file(self):
        """Open a file and display its content in the text widget."""
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.INSERT, content)
            self.update_line_numbers()
            self.syntax_highlighting()

    def save_file(self):
        """Save the content of the text widget to a file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)

    def copy_text(self):
        """Copy selected text."""
        self.text_widget.event_generate("<<Copy>>")

    def cut_text(self):
        """Cut selected text."""
        self.text_widget.event_generate("<<Cut>>")

    def paste_text(self):
        """Paste text from clipboard."""
        self.text_widget.event_generate("<<Paste>>")

    def create_status_bar(self):
        """Create a status bar to display the current line number."""
        self.status_bar = tk.Label(self.root, text="Line 1", anchor='w', bg=self.bg_color, fg=self.fg_color)
        self.status_bar.pack(fill='x')
        self.text_widget.bind('<KeyRelease>', self.update_status_bar)

    def update_status_bar(self, event=None):
        """Update the status bar with the current line number."""
        line, _ = self.text_widget.index(tk.INSERT).split('.')
        self.status_bar.config(text=f"Line {line}")

    def update_line_numbers(self, event=None):
        """Update the line numbers widget."""
        lines = self.text_widget.get("1.0", tk.END).split("\n")
        line_number_string = "\n".join(str(i) for i in range(1, len(lines)))
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        self.line_numbers.insert('1.0', line_number_string)
        self.line_numbers.config(state='disabled')

    def syntax_highlighting(self, event=None):
        """Apply syntax highlighting for Python code."""
        # Reset all tags
        self.text_widget.tag_remove("keyword", "1.0", tk.END)
        self.text_widget.tag_remove("string", "1.0", tk.END)
        self.text_widget.tag_remove("comment", "1.0", tk.END)

        # Highlight Python keywords
        keywords = ["def", "import", "as", "if", "elif", "else", "for", "while", "return", "class", "and", "or", "not", "in", "is", "print", "break", "continue", "pass", "raise", "try", "except", "finally", "with", "yield", "lambda"]
        for keyword in keywords:
            idx = '1.0'
            while True:
                idx = self.text_widget.search(keyword, idx, nocase=1, stopindex=tk.END)
                if not idx:
                    break
                endidx = f"{idx.split('.')[0]}.{int(idx.split('.')[1])+len(keyword)}"
                self.text_widget.tag_add("keyword", idx, endidx)
                idx = endidx
        self.text_widget.tag_config("keyword", foreground=self.keyword_color)

        # Highlight strings
        idx = '1.0'
        while True:
            idx = self.text_widget.search(r'\".*?\"', idx, nocase=1, stopindex=tk.END, regexp=True)
            if not idx:
                break
            endidx = self.text_widget.search(r'\"', idx + '+1c', nocase=1, stopindex=tk.END)
            if not endidx:
                break
            endidx = f"{endidx.split('.')[0]}.{int(endidx.split('.')[1])+1}"
            self.text_widget.tag_add("string", idx, endidx)
            idx = endidx
        self.text_widget.tag_config("string", foreground=self.string_color)

        # Highlight comments
        idx = '1.0'
        while True:
            idx = self.text_widget.search(r'\#.*', idx, nocase=1, stopindex=tk.END, regexp=True)
            if not idx:
                break
            endidx = f"{idx.split('.')[0]}.{len(self.text_widget.get(idx, tk.END).splitlines()[0])}"
            self.text_widget.tag_add("comment", idx, endidx)
            idx = endidx
        self.text_widget.tag_config("comment", foreground=self.comment_color)

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
