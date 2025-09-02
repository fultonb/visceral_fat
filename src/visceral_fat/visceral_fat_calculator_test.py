"""
Author : Brad Fulton <fultonbd@gmail.com>
Date   : 2025-08-15
Purpose: Testing

This module performs all the pytest testing for our code.
"""

import os
from subprocess import getstatusoutput

# Look in current directory for visceral_fat_calculator module
import sys

sys.path.append(".")

from utilities import (
    ft_to_m,
    ft_in_to_float,
    get_bmi,
    get_female_visceral_fat,
    get_male_visceral_fat,
    in_to_cm,
    lbs_to_kg,
)

PRG = "./visceral_fat_calculator.py"
# PRG = "visceral_fat/visceral_fat_calculator.py"


# --------------------------------------------------
def test_exists():
    """Program exists"""
    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage():
    """Usage"""
    for flag in ["-h", "--help"]:
        retval, out = getstatusoutput(f"{PRG} {flag}")
        assert retval == 0
        assert out.lower().startswith("usage")


# --------------------------------------------------
def test_get_bmi() -> None:
    """Body Mass Index (BMI) in kilograms per meter squared (kg/m^2)"""
    height_ft = 6.1
    weight_lbs = 190.0
    bmi = "24.9"

    retval: float = get_bmi(weight_lbs, height_ft)
    formatted_retval = "{:.1f}".format(retval)
    assert formatted_retval == bmi


# --------------------------------------------------
def test_in_to_cm() -> None:
    """inches (in) to centimeters (cm)"""
    length_in = 36.0
    length_cm = "91.44"

    retval: float = in_to_cm(length_in)
    formatted_retval = "{:.2f}".format(retval)
    assert formatted_retval == length_cm


# --------------------------------------------------
def test_ft_to_m() -> None:
    """feet (ft) to meters (m)"""
    length_ft = 6.1
    length_m = "1.86"

    retval: float = ft_to_m(length_ft)
    formatted_retval = "{:.2f}".format(retval)
    assert formatted_retval == length_m


# --------------------------------------------------
def test_ft_in_to_float() -> None:
    ft = 6
    inches = 1
    length_f = "6.08"

    retval: float = ft_in_to_float(ft, inches)
    formatted_retval = "{:.2f}".format(retval)
    assert formatted_retval == length_f


# --------------------------------------------------
def test_lbs_to_kg() -> None:
    """pounds (lbs) to kilograms (kg)"""
    weight_lbs = 190.0
    weight_kg = "86.18"

    retval: float = lbs_to_kg(weight_lbs)
    formatted_retval = "{:.2f}".format(retval)
    assert formatted_retval == weight_kg


# --------------------------------------------------
def test_get_male_visceral_fat():
    """Total Visceral Fat for a male."""
    waist_cm: float = 91.44
    thigh_cm: float = 62.23
    age: int = 42
    visceral_fat: float = 110.54

    retval: float = get_male_visceral_fat(waist_cm, thigh_cm, age)
    assert abs(retval - visceral_fat) <= 0.10


# --------------------------------------------------
def test_get_male_visceral_fat_by_convesion():
    """Total Visceral Fat for a male.
    Convert waist and thigh measurements from inches to centimeters.
    """
    waist_in: float = 36.0
    thigh_in: float = 24.5
    waist_cm: float = in_to_cm(waist_in)
    thigh_cm: float = in_to_cm(thigh_in)
    age: int = 42
    visceral_fat: float = 110.54

    retval: float = get_male_visceral_fat(waist_cm, thigh_cm, age)
    print(retval)
    assert abs(retval - visceral_fat) <= 0.10


# --------------------------------------------------
def test_get_female_visceral_fat():
    """Total Visceral Fat for a male."""
    waist_cm: float = 91.44
    thigh_cm: float = 62.23
    age: int = 42
    bmi: float = 19.37
    visceral_fat: float = 59.78

    retval: float = get_female_visceral_fat(waist_cm, thigh_cm, age, bmi)
    assert abs(retval - visceral_fat) <= 0.10


# --------------------------------------------------
def test_get_female_visceral_fat_by_convesion():
    """Total Visceral Fat for a male.
    Convert waist and thigh measurements from inches to centimeters.
    """
    waist_in: float = 36.0
    thigh_in: float = 24.5
    waist_cm: float = in_to_cm(waist_in)
    thigh_cm: float = in_to_cm(thigh_in)
    age: int = 42
    weight_lb: float = 120.0
    height_ft: float = 5.5
    bmi: float = get_bmi(weight_lb, height_ft)
    visceral_fat: float = 59.78

    retval: float = get_female_visceral_fat(waist_cm, thigh_cm, age, bmi)
    assert abs(retval - visceral_fat) <= 0.25
