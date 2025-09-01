"""
Author : Brad Fulton <fultonbd@gmail.com>
Date   : 2025-08-15
Purpose: Utilities

This module holds all of the functions that perform work used by the Command
Line Interface (CLI) and Graphical User Interface (GUI) modules. This inclueds
conversion calculations and creating GUI charts.
"""

import sqlite3
import tkinter as tk
from contextlib import contextmanager


# --------------------------------------------------
def get_bmi(weight_lbs: float, height_ft: float) -> float:
    """Gets the Body Mass Index (BMI) in kilograms per meter squared (kg/m^2).
    BMI = Weight (kg) / Height (m)^2
    """
    weight_kg = lbs_to_kg(weight_lbs)
    height_m = ft_to_m(height_ft)

    return weight_kg / (height_m**2)


# --------------------------------------------------
def in_to_cm(inches: float) -> float:
    """Converts inches (in) to centimeters (cm).
    1 in = 2.54 cm
    """
    return inches * 2.54


# --------------------------------------------------
def ft_to_m(ft: float) -> float:
    """Converts feet (ft) to meters (m).
    1 ft = 0.3048 m
    """
    return ft * 0.3048


# --------------------------------------------------
def ft_in_to_float(ft: int, inches: int) -> float:
    """Converts feet (ft) and inches to a floating point value (ft).
    1 ft  6 inches = 1.5 ft
    """
    return (inches / 12) + ft


# --------------------------------------------------
def lbs_to_kg(lbs: float) -> float:
    """Converts pounds (lbs) to kilograms (kg).
    1 lbs = 0.45359237 kg
    """
    return lbs * 0.45359237


# --------------------------------------------------
def get_gender(is_male: bool, is_female: bool) -> str:
    """Returns gender as a string ("male", or "female")"""
    if is_male:
        return "male"
    elif is_female:
        return "female"
    else:
        return ""


# --------------------------------------------------
def get_male_visceral_fat(waist_cm: float, thigh_cm: float, age: int) -> float:
    """Returns the amount of bodily visceral fat (fat around your organs) in
    centimeters squared (cm^2).

    NOTE: waist and thigh measurements are in centimeters (cm).

    Men: 6 * Waist C - 4.41 * proximal thigh C + 1.19 * Age - 213.65
       ((6 * waist) - (4.41 * thigh)) + ((1.19 * age) - 213.65)

    waist_cm - waist circumference (cm)
    thigh_cm - thigh circumgerence (cm)
    age - present age (years)
    """
    return ((6 * waist_cm) - (4.41 * thigh_cm)) + ((1.19 * age) - 213.65)


# --------------------------------------------------
def get_female_visceral_fat(
    waist_cm: float, thigh_cm: float, age: int, bmi: float
) -> float:
    """Returns the amount of bodily visceral fat (fat around your organs) in
    centimeters squared (cm^2).

    NOTE: waist and thigh measurements are in centimeters (cm).

    Women: 2.15 * Waist C - 3.63 * Proximal Thigh C + 1.46 * Age + 6.22 * BMI - 92.713
         ((2.15 * waist) - (3.63 * thigh)) + (1.46 * age) + ((6.22 * bmi) - 92.713)

    waist_cm - waist circumference (cm)
    thigh_cm - thigh circumgerence (cm)
    age - present age (years)
    bmi - body mass index (kg/m^2)
    """
    return (
        ((2.15 * waist_cm) - (3.63 * thigh_cm)) + (1.46 * age) + ((6.22 * bmi) - 92.713)
    )


# --------------------------------------------------
@contextmanager
def open_db(file_name: str):
    """This is a context manager that will make sure the your data is committed
    and the database is closed in case of any errors.

    See:  https://www.youtube.com/watch?v=14z_Tf3p2Mw
    """
    conn = sqlite3.connect(file_name)
    try:
        yield conn.cursor()
    finally:
        conn.commit()
        conn.close()


# --------------------------------------------------
def store_user_data(
    name: str,
    gender: str,
    age: float,
    weight: float,
    height_ft: int,
    height_in: int,
    waist: float,
    thigh: float,
    bmi: float,
    visceral_fat: float,
) -> None:
    """ Stores user data into sqlite database."""
    with open_db(file_name="vf_data.db") as cursor:
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, timestamp_utc DATETIME DEFAULT CURRENT_TIMESTAMP, 
            gender TEXT NOT NULL, age INTEGER NOT NULL, weight_lbs REAL NOT NULL, 
            height_ft INTEGER NOT NULL, height_in INTEGER NOT NULL, waist_in REAL NOT NULL, thigh_in REAL NOT NULL, 
            bmi REAL NOT NULL, visceral_fat REAL NOT NULL); """
        )

        cursor.execute(
            """INSERT INTO users(name, gender, age, weight_lbs, height_ft, height_in, waist_in, thigh_in, 
            bmi, visceral_fat)VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, gender, age, weight, height_ft, height_in, waist, thigh, bmi, visceral_fat),
        )


# --------------------------------------------------
def get_vf_category(visceral_fat: float) -> str:
    """Returns the bmi category with a str warning."""
    if visceral_fat < 130.0:
        return str("You have the Absence of Visceral Obesity")
    elif visceral_fat >= 130.0:
        return "You have Visceral Obesity"
    else:
        return ""


# --------------------------------------------------
def get_vf_bg_color(bmi: float) -> str:
    """Returns the bmi category with a str warning."""
    if bmi < 130.0:
        return str("sky blue")
    elif bmi >= 130.0:
        return "red2"
    else:
        return ""


# --------------------------------------------------
def create_vf_chart(frame: tk.LabelFrame, visceral_fat: float):
    """Creates a GUI visceral fat chart.

    frame - This is the LabelFrame that our chart will be placed in.
    visceral_fat - your visceral fat value
    """
    vf_canvas = tk.Canvas(frame, width=600, height=140, bg="lightgray")
    vf_canvas.pack()

    # Define sections: (x1, y1, x2, y2, color, text)
    sections = [
        (50, 50, 300, 100, "sky blue", "< 130.0"),
        (300, 50, 550, 100, "red2", ">= 130.0"),
    ]

    for x1, y1, x2, y2, color, text in sections:
        # Draw the rectangle section
        vf_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        # Calculate text position (center of the rectangle)
        text_x = (x1 + x2) / 2
        text_y = (y1 + y2) / 2

        # Add text to the section
        vf_canvas.create_text(
            text_x, text_y, text=text, fill="black", font=("Arial", 16, "bold")
        )

    # Draw heading
    heading_label = tk.Label(
        vf_canvas,
        text=f"Your Visceral Fat is {visceral_fat:.2f} cm^2 - {get_vf_category(visceral_fat)}",
        bg=get_vf_bg_color(visceral_fat),
        font=("Arial", 16, "bold"),
    )
    heading_label.pack(pady=20)
    heading_label.place(x=(50 + 550) / 2, y=20, anchor="n")

    # Draw label below each rectangle
    label1 = tk.Label(
        vf_canvas,
        text="Absence of Visceral Obesity",
        font=("Helvetica", 12, "bold"),
    )
    label1.pack(pady=20)
    label1.place(x=(50 + 300) / 2, y=100 + 10, anchor="n")

    label2 = tk.Label(
        vf_canvas, text="Visceral Obesity", font=("Helvetica", 12, "bold")
    )
    label2.pack(pady=20)
    label2.place(x=(300 + 550) / 2, y=100 + 10, anchor="n")

    return vf_canvas


# --------------------------------------------------
def get_bmi_category(bmi: float) -> str:
    """Returns the bmi category with a str warning."""
    if bmi < 18.5:
        return str("You are under weight")
    elif bmi < 25:
        return "You are normal"
    elif bmi < 30:
        return "You are overweight"
    elif bmi < 35:
        return "You are obese"
    elif bmi >= 35:
        return "You are extremely obese"
    else:
        return ""


# --------------------------------------------------
def get_bmi_bg_color(bmi: float) -> str:
    """Returns the bmi category with a str warning."""
    if bmi < 18.5:
        return str("sky blue")
    elif bmi < 25:
        return "green2"
    elif bmi < 30:
        return "yellow2"
    elif bmi < 35:
        return "orange2"
    elif bmi >= 35:
        return "red2"
    else:
        return ""


# --------------------------------------------------
def create_bmi_chart(frame: tk.LabelFrame, bmi: float):
    """Creates a GUI bmi chart.

    frame - This is the LabelFrame that our chart will be placed in.
    bmi - your BMI value
    """

    bmi_canvas = tk.Canvas(frame, width=600, height=140, bg="lightgray")
    bmi_canvas.pack()

    # Define sections: (x1, y1, x2, y2, color, text)
    sections = [
        (50, 50, 150, 100, "sky blue", "< 18.4"),
        (150, 50, 250, 100, "green2", "18.5 - 24.9"),
        (250, 50, 350, 100, "yellow2", "25 - 29.9"),
        (350, 50, 450, 100, "orange2", "30 - 34.9"),
        (450, 50, 550, 100, "red2", "> 35"),
    ]

    for x1, y1, x2, y2, color, text in sections:
        # Draw the rectangle section
        bmi_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        # Calculate text position (center of the rectangle)
        text_x = (x1 + x2) / 2
        text_y = (y1 + y2) / 2

        # Add text to the section
        bmi_canvas.create_text(
            text_x, text_y, text=text, fill="black", font=("Arial", 16, "bold")
        )

    # Draw heading
    heading_label = tk.Label(
        bmi_canvas,
        text=f"Your BMI is {bmi:.2f} kg/m^2 - {get_bmi_category(bmi)}",
        bg=get_bmi_bg_color(bmi),
        font=("Arial", 16, "bold"),
    )
    heading_label.pack(pady=20)
    heading_label.place(x=(50 + 550) / 2, y=20, anchor="n")

    # Draw label below each rectangle
    label1 = tk.Label(bmi_canvas, text="UNDERWEIGHT", font=("Helvetica", 12, "bold"))
    label1.pack(pady=20)
    label1.place(x=(50 + 150) / 2, y=100 + 10, anchor="n")

    label2 = tk.Label(bmi_canvas, text="NORMAL", font=("Helvetica", 12, "bold"))
    label2.pack(pady=20)
    label2.place(x=(150 + 250) / 2, y=100 + 10, anchor="n")

    label3 = tk.Label(bmi_canvas, text="OVERWEIGHT", font=("Helvetica", 12, "bold"))
    label3.pack(pady=20)
    label3.place(x=(250 + 350) / 2, y=100 + 10, anchor="n")

    label4 = tk.Label(bmi_canvas, text="OBESE", font=("Helvetica", 12, "bold"))
    label4.pack(pady=20)
    label4.place(x=(350 + 450) / 2, y=100 + 10, anchor="n")

    label5 = tk.Label(
        bmi_canvas, text="EXTREMELY OBESE", font=("Helvetica", 12, "bold")
    )
    label5.pack(pady=20)
    label5.place(x=(450 + 550) / 2, y=100 + 10, anchor="n")

    return bmi_canvas
