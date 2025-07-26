# gui_calculator.py

import tkinter as tk

# --- Function Definitions ---

def button_click(item):
    """
    This function is called when a number or operator button is clicked.
    It concatenates the clicked item to the string in the display.
    """
    global expression
    expression = expression + str(item)
    input_text.set(expression)

def button_clear():
    """
    This function is called when the 'C' button is clicked.
    It clears the display screen.
    """
    global expression
    expression = ""
    input_text.set("")

def button_equal():
    """
    This function is called when the '=' button is clicked.
    It evaluates the expression in the display using eval().
    It also handles potential errors like division by zero.
    """
    global expression
    try:
        # The eval() function evaluates the passed string as a Python expression
        # and returns the result. For example, eval("5 * 3") would return 15.
        result = str(eval(expression))
        input_text.set(result)
        # Reset the expression to the result for further calculations
        expression = result
    except ZeroDivisionError:
        input_text.set("Error: Div by 0")
        expression = ""
    except Exception:
        input_text.set("Error: Invalid eq")
        expression = ""


# --- UI Setup ---

# Create the main window
window = tk.Tk()
window.title("Simple Calculator")
window.geometry("320x400") # Set the size of the window
window.resizable(False, False) # Make the window not resizable
window.configure(bg="#f0f0f0") # Set a light grey background color

# Global variable to store the expression string
expression = ""

# StringVar is a Tkinter variable that holds a string;
# we use it to link the display Entry widget to our code.
input_text = tk.StringVar()

# Create the display screen (Entry widget)
display_frame = tk.Frame(window, bd=0, relief=tk.RIDGE)
display_frame.pack(pady=20)

display = tk.Entry(display_frame, font=('arial', 24, 'bold'), textvariable=input_text,
                   width=15, bg="#eee", bd=0, justify='right')
display.pack(ipady=10) # ipady adds padding inside the widget

# Create a frame for the buttons
button_frame = tk.Frame(window, bg="#f0f0f0")
button_frame.pack()

# --- Button Creation and Layout ---

# First row
btn_7 = tk.Button(button_frame, text="7", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: button_click(7)).grid(row=0, column=0, padx=1, pady=1)
btn_8 = tk.Button(button_frame, text="8", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: button_click(8)).grid(row=0, column=1, padx=1, pady=1)
btn_9 = tk.Button(button_frame, text="9", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: button_click(9)).grid(row=0, column=2, padx=1, pady=1)
btn_multiply = tk.Button(button_frame, text="*", fg="black", width=7, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: button_click("*")).grid(row=0, column=3, padx=1, pady=1)

# Second row
btn_4 = tk.Button(button_frame, text="4", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: button_click(4)).grid(row=1, column=0, padx=1, pady=1)
btn_5 = tk.Button(button_frame, text="5", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: button_click(5)).grid(row=1, column=1, padx=1, pady=1)
btn_6 = tk.Button(button_frame, text="6", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: button_click(6)).grid(row=1, column=2, padx=1, pady=1)
btn_subtract = tk.Button(button_frame, text="-", fg="black", width=7, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: button_click("-")).grid(row=1, column=3, padx=1, pady=1)

# Third row
btn_1 = tk.Button(button_frame, text="1", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: button_click(1)).grid(row=2, column=0, padx=1, pady=1)
btn_2 = tk.Button(button_frame, text="2", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: button_click(2)).grid(row=2, column=1, padx=1, pady=1)
btn_3 = tk.Button(button_frame, text="3", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: button_click(3)).grid(row=2, column=2, padx=1, pady=1)
btn_add = tk.Button(button_frame, text="+", fg="black", width=7, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: button_click("+")).grid(row=2, column=3, padx=1, pady=1)

# Fourth row
btn_clear = tk.Button(button_frame, text="C", fg="black", width=7, height=3, bd=0, bg="#eee", cursor="hand2", command=button_clear).grid(row=3, column=0, padx=1, pady=1)
btn_0 = tk.Button(button_frame, text="0", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: button_click(0)).grid(row=3, column=1, padx=1, pady=1)
btn_equal = tk.Button(button_frame, text="=", fg="black", width=7, height=3, bd=0, bg="#4CAF50", cursor="hand2", command=button_equal).grid(row=3, column=2, padx=1, pady=1)
btn_divide = tk.Button(button_frame, text="/", fg="black", width=7, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: button_click("/")).grid(row=3, column=3, padx=1, pady=1)


# Start the main event loop to make the window run
window.mainloop()
