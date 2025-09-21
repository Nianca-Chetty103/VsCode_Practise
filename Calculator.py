import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("400x600")
        self.root.resizable(0, 0)

        self.total_expression = ""
        self.current_expression = ""

        self.bg_color = "#222831"
        self.display_bg = "#393E46"
        self.button_bg = "#393E46"
        self.button_fg = "#EEEEEE"
        self.accent_color = "#00ADB5"
        self.operator_bg = "#00ADB5"
        self.operator_fg = "#222831"
        self.special_bg = "#F96D00"
        self.special_fg = "#FFFFFF"
        self.font_family = "Segoe UI"

        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()
        self.buttons_frame = self.create_buttons_frame()

        self.digits = {
            7: (1, 0), 8: (1, 1), 9: (1, 2),
            4: (2, 0), 5: (2, 1), 6: (2, 2),
            1: (3, 0), 2: (3, 1), 3: (3, 2),
            0: (4, 1), '.': (4, 0)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def create_display_frame(self):
        frame = tk.Frame(self.root, height=221, bg=self.display_bg, bd=0, highlightthickness=0)
        frame.pack(expand=True, fill="both")
        return frame

    def create_display_labels(self):
        total_label = tk.Label(
            self.display_frame, text=self.total_expression, anchor=tk.E,
            bg=self.display_bg, fg="#AAAAAA", padx=24,
            font=tkfont.Font(family=self.font_family, size=16)
        )
        total_label.pack(expand=True, fill='both')

        label = tk.Label(
            self.display_frame, text=self.current_expression, anchor=tk.E,
            bg=self.display_bg, fg="#FFFFFF", padx=24,
            font=tkfont.Font(family=self.font_family, size=40, weight="bold")
        )
        label.pack(expand=True, fill='both')
        return total_label, label

    def create_buttons_frame(self):
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        for x in range(5):
            frame.rowconfigure(x, weight=1, minsize=70)
            frame.columnconfigure(x, weight=1, minsize=70)
        return frame

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(
                self.buttons_frame, text=str(digit),
                bg=self.button_bg, fg=self.button_fg,
                font=tkfont.Font(family=self.font_family, size=24, weight="bold"),
                borderwidth=0, highlightthickness=0,
                activebackground="#222831", activeforeground=self.accent_color,
                relief="flat", cursor="hand2",
                command=lambda x=digit: self.add_to_expression(x)
            )
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW, padx=6, pady=6)
            button.configure(borderwidth=0, highlightbackground=self.bg_color)

    def create_operator_buttons(self):
        for i, (operator_symbol, operator_text) in enumerate(self.operations.items()):
            button = tk.Button(
                self.buttons_frame, text=operator_text,
                bg=self.operator_bg, fg=self.operator_fg,
                font=tkfont.Font(family=self.font_family, size=24, weight="bold"),
                borderwidth=0, highlightthickness=0,
                activebackground="#393E46", activeforeground="#FFFFFF",
                relief="flat", cursor="hand2",
                command=lambda x=operator_symbol: self.append_operator(x)
            )
            button.grid(row=i, column=3, sticky=tk.NSEW, padx=6, pady=6)
            button.configure(borderwidth=0, highlightbackground=self.bg_color)

    def create_special_buttons(self):
        clear_button = tk.Button(
            self.buttons_frame, text="C",
            bg=self.special_bg, fg=self.special_fg,
            font=tkfont.Font(family=self.font_family, size=24, weight="bold"),
            borderwidth=0, highlightthickness=0,
            activebackground="#F96D00", activeforeground="#FFFFFF",
            relief="flat", cursor="hand2",
            command=self.clear
        )
        clear_button.grid(row=0, column=0, sticky=tk.NSEW, padx=6, pady=6)
        clear_button.configure(borderwidth=0, highlightbackground=self.bg_color)

        equals_button = tk.Button(
            self.buttons_frame, text="=",
            bg=self.accent_color, fg="#FFFFFF",
            font=tkfont.Font(family=self.font_family, size=24, weight="bold"),
            borderwidth=0, highlightthickness=0,
            activebackground="#00ADB5", activeforeground="#222831",
            relief="flat", cursor="hand2",
            command=self.evaluate
        )
        equals_button.grid(row=4, column=2, columnspan=2, sticky=tk.NSEW, padx=6, pady=6)
        equals_button.configure(borderwidth=0, highlightbackground=self.bg_color)

        exit_button = tk.Button(
            self.buttons_frame, text="Exit",
            bg="#393E46", fg="#F96D00",
            font=tkfont.Font(family=self.font_family, size=24, weight="bold"),
            borderwidth=0, highlightthickness=0,
            activebackground="#222831", activeforeground="#F96D00",
            relief="flat", cursor="hand2",
            command=self.root.quit
        )
        exit_button.grid(row=0, column=1, sticky=tk.NSEW, padx=6, pady=6)
        exit_button.configure(borderwidth=0, highlightbackground=self.bg_color)

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def append_operator(self, operator):
        if self.current_expression == "" and self.total_expression == "":
            return
        if self.current_expression == "" and self.total_expression != "":
            self.total_expression = self.total_expression[:-1] + operator
        else:
            self.total_expression += self.current_expression + operator
            self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def clear(self, event=None):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def evaluate(self, event=None):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            expression = self.total_expression.replace("\u00F7", "/").replace("\u00D7", "*")
            self.current_expression = str(eval(expression))
            self.total_expression = ""
        except Exception:
            messagebox.showerror("Error", "Invalid Expression")
            self.current_expression = ""
            self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def update_total_label(self):
        expression = self.total_expression
        for operator_symbol, operator_text in self.operations.items():
            expression = expression.replace(operator_symbol, f' {operator_text} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def bind_keys(self):
        self.root.bind("<Return>", self.evaluate)
        self.root.bind("<BackSpace>", self.clear)
        for key in self.digits:
            self.root.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.root.bind(key, lambda event, operator=key: self.append_operator(operator))
        self.root.bind(".", lambda event: self.add_to_expression('.'))

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#222831")
    calc = Calculator(root)
    root.mainloop()
