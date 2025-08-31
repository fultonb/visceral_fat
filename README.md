# Visceral Fat

This application calculates the visceral fat and body mass index (BMI) using a command line interface (CLI) or a graphical user interface (GUI)

The following YouTube video inspired this program:
        https://www.youtube.com/watch?v=WlVbeXCMHRI

Using this program will allow you to enter all data in english measurements (ie. lbs., inches, feet) instead of converting them to metric values as the video has you do.

## Installation

Clone from GitHub.
```

```


## Dependencies
To install Python, Tkinter, and Pytest on a computer, follow these steps:

<h5>Install Python:</h5>

Visit the official [Python Website](https://www.python.org/downloads/) and download the latest stable version of Python for your operating system (Windows, macOS, or Linux).
<h6>Windows:</h6>

Run the downloaded installer. Crucially, ensure you check the "Add Python to PATH" option during installation to easily run Python from the command line.
<h6>macOS:</h6>

Python often comes pre-installed, but it might be an older version. It is recommended to install a newer version via the official installer or using a package manager like [Homebrew](https://brew.sh).

To install Python on macOS using Homebrew, perform the following steps:

Open Terminal:
Launch the Terminal application on your Mac. This can be done by pressing Command + Space to open Spotlight Search, then typing "Terminal" and pressing Enter.

Ensure Homebrew is Installed:
If Homebrew is not already installed, follow the instructions on the official [Homebrew website](https://brew.sh) to install it. If it is installed, you can optionally run brew update to ensure Homebrew is up-to-date.

```bash
    brew update
```
Install the latest stable version of Python: 

  ```bash
      brew install python
  ```
This command will download and install Python along with its dependencies.

After the installation completes, you can verify the installed Python version by running:

```bash
    $ python3 --version
    Python 3.13.7
```
This command should display the version number of the Python 3 installation.

<h6>Linux:</h6> 
Use your distribution's package manager (e.g., sudo apt install python3 on Debian/Ubuntu, sudo dnf install python3 on Fedora, sudo pacman -S python on Arch Linux).
<p>
<h5>Install Tkinter:</h5>
To verify if Tkinter is installed and accessible:<br>
1. Open a command prompt or terminal.<br>
2. Type python or python3 to enter the Python interpreter.<br>
3. Type import tkinter and press Enter.<br>
4. If no error message appears, Tkinter is installed and ready to use.<br>
5. If Tkinter is not found (e.g., on some Linux distributions or if Python was installed without it)

Ex. tkinter is installed:

```python
$ python3
Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import tkinter
>>> 
```
<h6>On Mac:</h6>
To install Tkinter on macOS using Homebrew, the primary step involves installing the tcl-tk package, which provides the underlying Tcl/Tk libraries that Tkinter relies on.<br>
Installation Steps:<br>
Open Terminal: Launch the Terminal application on your macOS device.<br>
Use Homebrew to install the tcl-tk package:

```
$ brew install tcl-tk
```
<h6>On Windows:</h6>
Ensure you installed Python with the "tcl/tk and IDLE" component selected during the installation process. If not, you may need to reinstall Python and select this option.
<h6>On Linux:</h6>
On Debian-based Linux distributions (like Ubuntu), use your package manager to install the Tkinter package:

```
$ sudo apt-get install python3-tk
```
On other Linux distributions: 
Consult your distribution's documentation for the correct package name and installation command (e.g., python-tk or tk-devel).
<b>Note:</b> While pip install tk might appear in some older resources, it is generally not the recommended way to install Tkinter as it's part of Python's standard library. The methods above ensure proper integration with your Python installation.
<p> 
Verify Tkinter Installation:<br>
Open your Python interpreter or create a test.py file with the following code and run it:

```python

    import tkinter as tk

    root = tk.Tk()
    root.title("Tkinter Test")
    label = tk.Label(root, text="Tkinter is working!")
    label.pack()
    root.mainloop()
```

Run it:
```bash
$ python3 test.py
```
A small window should appear if Tkinter is correctly installed.
![Alt text](/images/tkinter_test_window.jpg?raw=true)

<h5>Install Pytest:</h5>
Open your command prompt or terminal.
Use pip to install Pytest by running: pip install pytest (or pip3 install pytest).
<p>
To install Pytest on a Mac using 
Update Homebrew (optional but recommended): Open your terminal and run:

```
    brew update
```
Use the following command to install Pytest via Homebrew:

```
    brew install pytest
```
Homebrew will handle the installation of Pytest and any necessary dependencies, including a compatible Python version if one is not already managed by Homebrew.
After the installation is complete, you can verify that Pytest is installed and accessible by running:
```
    $ pytest --version
      pytest 8.4.1
```
This command should display the installed Pytest version, confirming a successful installation.

## Installation

Unzip tar.gz file

```bash
$ mkdir project
$ mv visceral_fat-1.0.0.tar.gz project
$ cd project
$ tar -xf visceral_fat-1.0.0.tar.gz
```

## Usage
Move to directory holding visceral_fat code. I assume you are in project directory created above:
```bash
$ cd visceral_fat-1.0.0/src/visceral_fat/
```

Using default values:
```bash
$ uv run visceral_fat_calculator.py 
               or
$ ./visceral_fat_calculator.py
name = Tony
gender = male
age = 42
weight = 190.0 lbs.
height = 6.1 ft
waist = 36.0 inches, 91.44 cm
thigh = 24.5 inches, 62.23 cm
bmi = 24.93 kg/m^2 - You are normal
visceral fat = 110.54 cm^2 - You have the Absence of Visceral Obesity
```


Bring up graphical user interface (GUI):
```bash
$ uv run visceral_fat_calculator.py -g 
               or
$ ./visceral_fat_calculator.py -g
```
![Alt text](/images/visceral_fat_GUI.jpg?raw=true)

Bring up help menu:
```bash
$ uv run visceral_fat_calculator.py -h
               or
$ ./visceral_fat_calculator.py -h
usage: visceral_fat_calculator.py [-h] [-n str] [-m | -f] [-a int] [-wt float] [-ht float] [-wc float] [-tc float]
                                  [-d] [-g] [-sd]

Visceral Fat Calculator

options:
  -h, --help           show this help message and exit
  -n, --name str       User Name (one word)
  -m, --male           Gender
  -f, --female         Gender
  -a, --age int        Age
  -wt, --weight float  Weight in lbs. (ie. 190.0 lbs.)
  -ht, --height float  Height in feet (ie. 6.1 ft.)
  -wc, --waist float   Waist Circumference in inches (ie. 36.0 in.)
  -tc, --thigh float   Thigh Circumference in inches (ie. 24.5 in.)
  -d, --debug          Creates the .log file
  -g, --gui            Use GUI to enter data
  -sd, --store_data    Stores data to the database

        The following YouTube video inspired this program:
        https://www.youtube.com/watch?v=WlVbeXCMHRI

        Using this program will allow you to enter all data
        in english measurements (ie. lbs., inches, feet) 
        instead of converting them to metric values as the 
        video has you do.
```

By using the flags any and all values can be changed. Here is an example that changes the name, weight, and gender from the default values:
```bash
$ uv run visceral_fat_calculator.py -f -n Mary -wt 120.0
               or
$ ./visceral_fat_calculator.py -f -n Mary -wt 120.0 -ht 5.5
name = Mary
gender = female
age = 42
weight = 120.0 lbs.
height = 5.5 ft
waist = 36.0 inches, 91.44 cm
thigh = 24.5 inches, 62.23 cm
bmi = 19.37 kg/m^2 - You are normal
visceral fat = 59.78 cm^2 - You have the Absence of Visceral Obesity
```
Run all tests:
```bash
$ uv run pytest 
               or
$ pytest
```
## License
[MIT](/LICENSE)
