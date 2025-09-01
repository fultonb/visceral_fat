"""
Author : Brad Fulton <fultonbd@gmail.com>
Date   : 2025-08-15
Purpose: GUI

This module creates a Graphical User Interface (GUI) for the user to fill in
appropriate data and shows the Visceral Fat content and Body Mass Index (BMI)
values in colorful charts.
"""

import re
import tkinter as tk

from utilities import (
    create_bmi_chart,
    create_vf_chart,
    get_bmi,
    get_female_visceral_fat,
    get_male_visceral_fat,
    in_to_cm,
    ft_in_to_float,
    store_user_data,
)

# Global variables
vf_canvas: tk.Canvas
bmi_canvas: tk.Canvas
vf_chart_frame: tk.LabelFrame
bmi_chart_frame: tk.LabelFrame


def calculate_data():
    # Get data
    name = name_entry.get()
    gender = selected_option.get()
    age = int(age_value.get())
    weight = float(weight_entry.get())
    height_ft = int(height_ft_value.get())
    height_in = int(height_in_value.get())
    height = ft_in_to_float(height_ft, height_in)
    waist_in = float(waist_entry.get())
    thigh_in = float(thigh_entry.get())
    waist_cm = in_to_cm(waist_in)
    thigh_cm = in_to_cm(thigh_in)
    bmi = get_bmi(weight, height)
    visceral_fat = 0.0
    store_data = store_var.get()  # 1 represents "checked" and 0 represents "unchecked"

    # The formula for the amount of visceral fat a person has is different
    # for a man than the one for a woman.
    if gender == "male":
        visceral_fat: float = get_male_visceral_fat(waist_cm, thigh_cm, age)
    # Uses the female formula for getting the amount of visceral fat they have.
    elif gender == "female":
        visceral_fat: float = get_female_visceral_fat(waist_cm, thigh_cm, age, bmi)

    # Check to see if the user wants to store all of their data in the database.
    if store_data == 1:
        store_user_data(
            name,
            gender,
            age,
            weight,
            height_ft,
            height_in,
            waist_in,
            thigh_in,
            round(bmi, 2),
            round(visceral_fat, 2),
        )
        print("Data is stored in vf_data.db")

    global vf_canvas, bmi_canvas, vf_chart_frame, bmi_chart_frame
    # Create the visceral fat chart
    vf_chart_frame = tk.LabelFrame(frame, text="Visceral Fat")
    vf_chart_frame.grid(row=2, column=0, padx=20, pady=5, sticky="news")
    vf_canvas = create_vf_chart(vf_chart_frame, visceral_fat)  # type: ignore

    # Create the BMI chart
    bmi_chart_frame = tk.LabelFrame(frame, text="BMI")
    bmi_chart_frame.grid(row=3, column=0, padx=20, pady=5, sticky="news")
    bmi_canvas = create_bmi_chart(bmi_chart_frame, bmi)  # type: ignore


# --------------------------------------------------
def reset_data():
    """Return gui data to default values.
    Remove charts by clearing the entire vf_canvas and bmi_canvas from GUI.
    """
    # Set the name_entry Label
    name_entry.delete(0, tk.END)  # Empties the str.
    name_entry.insert(0, "Tony")  # Inserts "Tony" at beginning of str.

    # Set the weight_entry Label
    weight_entry.delete(0, tk.END)
    weight_entry.insert(0, "190.0")

    # Set the height_entry Label
    # height_entry.delete(0, tk.END)
    # height_entry.insert(0, "6.1")
    
    # Set the waist_entry Label
    waist_entry.delete(0, tk.END)
    waist_entry.insert(0, "36.0")

    # Set the thigh_entry Label
    thigh_entry.delete(0, tk.END)
    thigh_entry.insert(0, "24.5")
    

    # Checkbutton (gender)
    store_var.set(0)
    # Radiobutton
    selected_option.set("male")
    # Spinbox values
    age_value.set(42)
    height_ft_value.set(6)
    height_in_value.set(1)

    # Remove Error message
    validation_label.config(text="")

    # Clear the entire vf_canvas and bmi_canvas
    global vf_canvas, bmi_canvas, vf_chart_frame, bmi_chart_frame

    try:
        vf_canvas.delete("all")
        vf_canvas.destroy()
        vf_chart_frame.destroy()

        bmi_canvas.delete("all")
        bmi_canvas.destroy()
        bmi_chart_frame.destroy()
    except NameError:
        # No need to do anything because 'vf_chart_frame' is not defined.
        pass

    # Set focus to name_entry label
    name_entry.focus_set()


# --------------------------------------------------
# Create the main window
window = tk.Tk()

# Set window properties
window.title("Visceral Fat Calculator")
window.geometry("650x750")

# Create a Frame widget
frame = tk.Frame(window)
frame.pack()

user_info_frame = tk.LabelFrame(frame, text="User Information")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)

# Create a label to hold validation error messaages.
validation_label = tk.Label(user_info_frame)
validation_label.grid(row=8, column=1)

# Create buttons
button_frame = tk.LabelFrame(frame, borderwidth=0, highlightthickness=0)
button_frame.grid(row=1, column=0, padx=20, pady=5)

calculate_button = tk.Button(button_frame, text="Calculate", command=calculate_data)
calculate_button.grid(row=0, column=0, padx=20, pady=5)

reset_button = tk.Button(
    button_frame, text="Reset (default values)", command=reset_data
)
reset_button.grid(row=0, column=1, padx=20, pady=5)


# Validation functions
# --------------------------------------------------
def validate_name(name_input: str):
    # Accepts single name.
    # No special symbols or numbers.
    regex = r"^(\s*(?!0)|[\-a-zA-Z]+)$"
    if re.search(regex, name_input):
        validation_label.config(text=" ")
        calculate_button.config(state="active")
        return True
    else:
        validation_label.config(
            text="Accepts single name. No symbols or numbers.",
            foreground="red",
        )
        calculate_button.config(state="disabled")
        return False


# --------------------------------------------------
def validate_age(age_input: str):
    # Accepts only numbers > 1.
    regex = r"^(\s*(?!0)|[1-9]\d*)$"
    if re.search(regex, age_input):
        validation_label.config(text=" ")
        calculate_button.config(state="active")
        return True
    else:
        validation_label.config(
            text="Accepts only numbers > 1.",
            foreground="red",
        )
        calculate_button.config(state="disabled")
        return False


# --------------------------------------------------
def validate_weight(weight_input: str):
    # Accepts only numbers > 1.
    regex = r"^(\s*(?!0)|[1-9][0-9]*)[.]?\d*$"
    if re.search(regex, weight_input):
        validation_label.config(text=" ")
        calculate_button.config(state="active")
        return True
    else:
        validation_label.config(
            text="Accepts only numbers >= 1.",
            foreground="red",
        )
        calculate_button.config(state="disabled")
        return False


# --------------------------------------------------
def validate_height(height_input: str):
    # Accepts only numbers > 1.
    regex = r"^(\s*(?!0)|[1-9][0-9]*)[.]?\d*$"
    if re.search(regex, height_input):
        validation_label.config(text=" ")
        calculate_button.config(state="active")
        return True
    else:
        validation_label.config(
            text="Accepts only numbers >= 1.",
            foreground="red",
        )
        calculate_button.config(state="disabled")
        return False


# --------------------------------------------------
def validate_height_ft(height_ft_input: str):
    # Accepts only numbers > 1.
    regex = r"^(\s*(?!0)|[1-9]\d*)$"
    if re.search(regex, height_ft_input):
        validation_label.config(text=" ")
        calculate_button.config(state="active")
        return True
    else:
        validation_label.config(
            text="Accepts only numbers > 1.",
            foreground="red",
        )
        calculate_button.config(state="disabled")
        return False
    

# --------------------------------------------------
def validate_height_in(height_in_input: str):
    # Accepts only numbers > 1.
    regex = r"^(0|[1-9][0-9]*)$"
    if re.search(regex, height_in_input):
        validation_label.config(text=" ")
        calculate_button.config(state="active")
        return True
    else:
        validation_label.config(
            text="Accepts only numbers >= 0.",
            foreground="red",
        )
        calculate_button.config(state="disabled")
        return False
    

# --------------------------------------------------
def validate_waist(waist_input: str):
    # Accepts only numbers > 1.
    regex = r"^(\s*(?!0)|[1-9][0-9]*)[.]?\d*$"
    if re.search(regex, waist_input):
        validation_label.config(text=" ")
        calculate_button.config(state="active")
        return True
    else:
        validation_label.config(
            text="Accepts only numbers >= 1.",
            foreground="red",
        )
        calculate_button.config(state="disabled")
        return False


# --------------------------------------------------
def validate_thigh(thigh_input: str):
    # Accepts only numbers > 1.
    regex = r"^(\s*(?!0)|[1-9]+[0-9]*)[.]?\d*$"
    if re.search(regex, thigh_input):
        validation_label.config(text=" ")
        calculate_button.config(state="active")
        return True
    else:
        validation_label.config(
            text="Accepts only numbers >= 1.",
            foreground="red",
        )
        calculate_button.config(state="disabled")
        return False


# Register your validation functions.
name_valid: str = user_info_frame.register(validate_name)
age_valid: str = user_info_frame.register(validate_age)
weight_valid: str = user_info_frame.register(validate_weight)
height_ft_valid: str = user_info_frame.register(validate_height_ft)
height_in_valid: str = user_info_frame.register(validate_height_in)
waist_valid: str = user_info_frame.register(validate_waist)
thigh_valid: str = user_info_frame.register(validate_thigh)


# Create radiobuttons
selected_option = tk.StringVar()
selected_option.set("male")  # Set a default selected option

radio1 = tk.Radiobutton(
    user_info_frame,
    text="Male",
    value="male",
    variable=selected_option,
)
radio2 = tk.Radiobutton(
    user_info_frame,
    text="Female",
    value="female",
    variable=selected_option,
)

radio1.grid(row=1, column=0)
radio2.grid(row=1, column=1)


# create Name label
name_label = tk.Label(user_info_frame, text="Name")
name_label.grid(row=2, column=0, sticky="w")
name_entry = tk.Entry(
    user_info_frame, validate="all", validatecommand=(name_valid, "%P")
)
name_entry.insert(tk.END, "Tony")
name_entry.grid(row=2, column=1, sticky="w")

# Create Age label
age_label = tk.Label(user_info_frame, text="Age")

# Create a DoubleVar to hold the Spinbox value
age_value = tk.DoubleVar()
# Set the initial default value
age_value.set(42)
age_spinbox = tk.Spinbox(
    user_info_frame,
    from_=1,
    to=110,
    textvariable=age_value,
    validate="all",
    validatecommand=(age_valid, "%P"),
)

age_label.grid(row=3, column=0, sticky="w")
age_spinbox.grid(row=3, column=1)

# Create Weight, Height, Waist Circumference, Thigh Circumfeerence labels
weight_label = tk.Label(user_info_frame, text="Weight (lbs)")
weight_label.grid(row=4, column=0, sticky="w")
height_label = tk.Label(user_info_frame, text="Height (feet, inches)")
height_label.grid(row=5, column=0, sticky="w")
waist_label = tk.Label(user_info_frame, text="Waist (inches)")
waist_label.grid(row=6, column=0, sticky="w")
thigh_label = tk.Label(user_info_frame, text="Thigh (inches)")
thigh_label.grid(row=7, column=0, sticky="w")

weight_entry = tk.Entry(
    user_info_frame, validate="all", validatecommand=(weight_valid, "%P")
)
weight_entry.insert(tk.END, "190.0")
weight_entry.grid(row=4, column=1, sticky="w")

""" height_entry = tk.Entry(
    user_info_frame, validate="all", validatecommand=(height_valid, "%P")
)
height_entry.insert(tk.END, "6.1")
height_entry.grid(row=5, column=1) """

# Create a DoubleVar to hold the Spinbox value
height_ft_value = tk.DoubleVar()
# Set the initial default value
height_ft_value.set(6)
height_ft_spinbox = tk.Spinbox(
    user_info_frame,
    from_=1,
    to=10,
    width=5,
    textvariable=height_ft_value,
    validate="all",
    validatecommand=(height_ft_valid, "%P"),
)
height_ft_spinbox.grid(row=5, column=1, sticky="w")

# Create a DoubleVar to hold the Spinbox value
height_in_value = tk.DoubleVar()
# Set the initial default value
height_in_value.set(1)
height_in_spinbox = tk.Spinbox(
    user_info_frame,
    from_=0,
    to=11,
    width=5,
    textvariable=height_in_value,
    validate="all",
    validatecommand=(height_in_valid, "%P"),
)
height_in_spinbox.grid(row=5, column=1, sticky="e")

waist_entry = tk.Entry(
    user_info_frame, validate="all", validatecommand=(waist_valid, "%P")
)
waist_entry.insert(tk.END, "36.0")
waist_entry.grid(row=6, column=1, sticky="w")

thigh_entry = tk.Entry(
    user_info_frame, validate="all", validatecommand=(thigh_valid, "%P")
)
thigh_entry.insert(tk.END, "24.5")
thigh_entry.grid(row=7, column=1, sticky="w")

# Create a checkbox.
store_var = tk.IntVar()
store_checkbox = tk.Checkbutton(user_info_frame, text="Store Data", variable=store_var)
store_checkbox.grid(row=8, column=0, sticky="w")

# Add padding
for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Start the Tkinter event loop
window.mainloop()
