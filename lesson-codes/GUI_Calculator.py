"""
    A modern, dark-themed GUI calculator using Tkinter and ttk.

    Attributes:
        root (tk.Tk): The main Tkinter window.
        expression (str): The current mathematical expression being entered.
        recent_label (tk.Label): Label displaying the most recent calculation.
        result_label (tk.Label): Label displaying the current input or result.

    Methods:
        __init__(root):
            Initializes the calculator UI, sets up styles, display, and buttons.

        on_button_click(char):
            Handles button click events:
                - 'C': Clears the current expression and display.
                - '=': Evaluates the current expression and displays the result.
                - Other: Appends the character to the expression and updates the display.

    Keyboard Shortcuts:
        - Digits and operators (+, -, *, /, .) can be entered directly from the keyboard.
        - Enter or Return: Evaluate the current expression.
        - Escape: Clear the current expression.
        - Backspace: Delete the last character.
"""

import tkinter as tk
from tkinter import ttk
import ast, operator

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.expression = ""

        # Set fixed squared window size
        window_size = 400
        self.root.geometry(f"{window_size}x{window_size}")
        self.root.minsize(window_size, window_size)
        self.root.maxsize(window_size, window_size)

        # Center the window on the screen
        self.center_window(window_size, window_size)

        # Modern dark theme colors
        bg_main = "#23272f"
        bg_display = "#2c313c"
        fg_display = "#f8f8f2"
        fg_recent = "#bbbbbb"
        btn_bg = "#1e1e2e"       
        btn_fg = "#f8f8f2"       
        btn_active_bg = "#44475a"
        btn_special_bg = "#ff5555"
        btn_special_fg = "#ffffff"
        eq_bg = "#50fa7b"
        eq_fg = "#23272f"

        self.root.configure(bg=bg_main)

        # ttk style override
        style = ttk.Style()
        style.theme_use("clam")  # Use 'clam' to avoid macOS-specific 'aqua'
        style.configure("Calc.TButton",
                        background=btn_bg,
                        foreground=btn_fg,
                        font=("Segoe UI", 16, "bold"),
                        borderwidth=0,
                        focusthickness=0)
        style.map("Calc.TButton",
                  background=[("active", btn_active_bg)],
                  foreground=[("active", btn_fg)])

        style.configure("Special.TButton",
                        background=btn_special_bg,
                        foreground=btn_special_fg,
                        font=("Segoe UI", 16, "bold"))
        style.map("Special.TButton",
                  background=[("active", "#ff6b6b")])

        style.configure("Equal.TButton",
                        background=eq_bg,
                        foreground=eq_fg,
                        font=("Segoe UI", 18, "bold"))
        style.map("Equal.TButton",
                  background=[("active", "#69ff94")])

        # Display frame
        display_frame = tk.Frame(root, bg=bg_display, bd=0, highlightthickness=0)
        display_frame.grid(row=0, column=0, columnspan=5, padx=16, pady=(16,8), sticky='ew')
        display_frame.grid_columnconfigure(0, weight=1)

        self.recent_label = tk.Label(
            display_frame, text="", anchor='e',
            font=("Segoe UI", 12), padx=8, pady=2,
            bg=bg_display, fg=fg_recent
        )
        self.recent_label.grid(row=0, column=0, sticky='ew')

        self.result_label = tk.Label(
            display_frame, text="", anchor='e',
            font=("Segoe UI", 22, "bold"), padx=8, pady=8,
            bg=bg_display, fg=fg_display
        )
        self.result_label.grid(row=1, column=0, sticky='ew')

        # Button layout
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['C', '0', '.', '+']
        ]

        btn_frame = tk.Frame(root, bg=bg_main)
        btn_frame.grid(row=1, column=0, columnspan=5, padx=16, pady=(0,16), sticky="nsew")

        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                action = lambda x=char: self.on_button_click(x)
                style_name = "Special.TButton" if char == "C" else "Calc.TButton"
                ttk.Button(
                    btn_frame, text=char, command=action, style=style_name
                ).grid(row=r, column=c, padx=6, pady=6, sticky='nsew')

        equal_action = lambda x='=': self.on_button_click(x)
        ttk.Button(
            btn_frame, text='=', command=equal_action, style="Equal.TButton"
        ).grid(row=0, column=4, rowspan=4, padx=(12,0), pady=6, sticky='nsew')

        # Expand evenly
        for i in range(5):
            btn_frame.grid_columnconfigure(i, weight=1, minsize=60)
        for i in range(4):
            btn_frame.grid_rowconfigure(i, weight=1, minsize=60)

        # Center content in window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=3)
        self.root.grid_columnconfigure(0, weight=1)

        # Keyboard bindings
        root.bind("<Key>", self.on_key_press)
        root.bind("<Return>", lambda event: self.on_button_click('='))
        root.bind("<KP_Enter>", lambda event: self.on_button_click('='))
        root.bind("<Escape>", lambda event: self.on_button_click('C'))

    def center_window(self, width, height):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.result_label.config(text="")
            self.recent_label.config(text="")
        elif char == '=':
            try:
                if self.expression and self.expression[-1] not in '+-*/.':
                    allowed_operators = {
                        ast.Add: operator.add,
                        ast.Sub: operator.sub,
                        ast.Mult: operator.mul,
                        ast.Div: operator.truediv,
                        ast.USub: operator.neg,
                        ast.Pow: operator.pow,
                    }
                    def safe_eval(node):
                        if isinstance(node, ast.Constant):  # <number>
                            return node.value
                        elif isinstance(node, ast.BinOp):
                            return allowed_operators[type(node.op)](
                                safe_eval(node.left), safe_eval(node.right)
                            )
                        elif isinstance(node, ast.UnaryOp):
                            return allowed_operators[type(node.op)](safe_eval(node.operand))
                        else:
                            raise ValueError("Invalid expression")

                    result = str(safe_eval(ast.parse(self.expression, mode='eval').body))
                    self.recent_label.config(text=self.expression)
                    self.expression = result
                    self.result_label.config(text=result)
                else:
                    self.result_label.config(text="Error")
                    self.recent_label.config(text=self.expression)
                    self.expression = ""
            except Exception:
                self.result_label.config(text="Error")
                self.recent_label.config(text=self.expression)
                self.expression = ""
        else:
            self.expression += str(char)
            self.result_label.config(text=self.expression)

    def on_key_press(self, event):
        char = event.char
        if char in "0123456789+-*/.":
            self.on_button_click(char)
        elif event.keysym == "BackSpace":
            self.expression = self.expression[:-1]
            self.result_label.config(text=self.expression)
        # Ignore other keys


if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.resizable(False, False)
    root.mainloop()
