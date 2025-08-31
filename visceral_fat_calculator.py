#!/usr/bin/env python3
"""
Author : Brad Fulton <fultonbd@gmail.com>
Date   : 2025-08-15
Purpose: Visceral Fat Calculator CLI

This module creates the Commanad Line Interface (CLI) that will perform calculations,
based on values passed to it, and return Visceral Fat content and Body Mass Index (BMI)
values. A Graphical User Interface (GUI) version of the program can also be instantiated
from this CLI.

This program is based on information gleaned from:
    https://www.youtube.com/watch?v=WlVbeXCMHRI
"""

import argparse
import logging
import subprocess
import sys
from typing import NamedTuple

from utilities import (
    get_bmi,
    get_bmi_category,
    get_female_visceral_fat,
    get_gender,
    get_male_visceral_fat,
    get_vf_category,
    in_to_cm,
    store_user_data,
)


class Args(NamedTuple):
    """Command-line arguments"""

    name: str
    male: bool
    female: bool
    age: int
    weight: float
    height: float
    waist: float
    thigh: float
    gui: bool
    store_data: bool


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Visceral Fat Calculator",
        epilog="""
        The following YouTube video inspired this program:
        https://www.youtube.com/watch?v=WlVbeXCMHRI

        Using this program will allow you to enter all data
        in english measurements (ie. lbs., inches, feet) 
        instead of converting them to metric values as the 
        video has you do.
        """,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-n",
        "--name",
        help="User Name (one word)",
        metavar="str",
        type=str,
        default="Tony",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-m", "--male", help="Gender", action="store_true", default=True
    )
    group.add_argument(
        "-f", "--female", help="Gender", action="store_true"
    )

    parser.add_argument("-a", "--age", help="Age", metavar="int", type=int, default=42)

    parser.add_argument(
        "-wt",
        "--weight",
        help="Weight in lbs. (ie. 190.0 lbs.)",
        metavar="float",
        type=float,
        default=190.0,
    )

    parser.add_argument(
        "-ht",
        "--height",
        help="Height in feet (ie. 6.1 ft.)",
        metavar="float",
        type=float,
        default=6.1,
    )

    parser.add_argument(
        "-wc",
        "--waist",
        help="Waist Circumference in inches (ie. 36.0 in.)",
        metavar="float",
        type=float,
        default=36.0,
    )

    parser.add_argument(
        "-tc",
        "--thigh",
        help="Thigh Circumference in inches (ie. 24.5 in.)",
        metavar="float",
        type=float,
        default=24.5,
    )

    parser.add_argument(
        "-d",
        "--debug",
        help="Creates the .log file",
        action="store_true",  # default=False
    )

    parser.add_argument(
        "-g",
        "--gui",
        help="Use GUI to enter data",
        action="store_true",  # default=False
    )

    parser.add_argument(
        "-sd",
        "--store_data",
        help="Stores data to the database",
        action="store_true",  # default=False
    )

    args = parser.parse_args()
    debug = args.debug

    logging.basicConfig(
        filename=".log",
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%d %B %Y %H:%M:%S",
        filemode="a",  # append
        # filemode='w',  # overwrite
        level=logging.DEBUG if debug else logging.CRITICAL,
    )

    # The find() method returns -1 if the value is not found. No spaces found.
    if args.name.strip().find(" ") != -1:
        parser.error(f'--name "{args.name}" must be one word"')

    if args.female:
        args.male = False
    
    if args.age <= 0:
        parser.error(f'--age "{args.age}" must be a positive number greater than 0')

    if args.weight <= 0:
        parser.error(
            f'--weight "{args.weight}" must be a positive number greater than 0'
        )

    if args.height <= 0:
        parser.error(
            f'--height "{args.height}" must be a positive number greater than 0'
        )

    if args.waist <= 0:
        parser.error(f'--waist "{args.waist}" must be a positive number greater than 0')

    if args.thigh <= 0:
        parser.error(f'--thigh "{args.thigh}" must be a positive number greater than 0')

    return Args(
        args.name,
        args.male,
        args.female,
        args.age,
        args.weight,
        args.height,
        args.waist,
        args.thigh,
        args.gui,
        args.store_data,
    )


# --------------------------------------------------
def main() -> float:
    """Run program."""

    args = get_args()
    name = args.name
    is_male = args.male
    is_female = args.female
    age = args.age
    weight = args.weight
    height = args.height
    waist_in = args.waist
    thigh_in = args.thigh
    waist_cm = in_to_cm(waist_in)
    thigh_cm = in_to_cm(thigh_in)
    bmi = get_bmi(weight, height)
    use_gui = args.gui
    store_data = args.store_data

    logging.debug("Look in the .log file to see this message.")
    print(f"name = {name}")
    print(f"gender = {get_gender(is_male, is_female)}")
    print(f"age = {age}")
    print(f"weight = {weight} lbs.")
    print(f"height = {height} ft")
    print(f"waist = {waist_in} inches, {waist_cm:.2f} cm")
    print(f"thigh = {thigh_in} inches, {thigh_cm:.2f} cm")
    print(f"bmi = {bmi:.2f} kg/m^2 - {get_bmi_category(bmi)}")

    # The formula for the amount of visceral fat a person has is different
    # for a man than the one for a woman.
    visceral_fat: float = 0.0

    # if gender == "male":
    if is_male:
        visceral_fat = get_male_visceral_fat(waist_cm, thigh_cm, age)
    # elif gender == "female":
    elif is_female:
        visceral_fat = get_female_visceral_fat(waist_cm, thigh_cm, age, bmi)

    print(f"visceral fat = {visceral_fat:.2f} cm^2 - {get_vf_category(visceral_fat)}")
    # Check to see if the user wants to use the GUI instead of the command line.
    if use_gui:
        print("\n***** Now using GUI *****\n")
        subprocess.run(["python3", "gui_interface.py"])
        sys.exit(0)
    # Check to see if the user wants to store all of their data in the database.

    if store_data:
        gender: str = get_gender(is_male, is_female)
        store_user_data(
            name,
            gender,
            age,
            weight,
            height,
            waist_in,
            thigh_in,
            round(bmi, 2),
            round(visceral_fat, 2),
        )
        print("Data is stored in vf_data.db")
    return visceral_fat


# --------------------------------------------------
if __name__ == "__main__":
    visceral_fat = main()
