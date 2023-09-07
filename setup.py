import sys
import subprocess

def setup():
    packages = ["colorama", "inquirer", "gspread"]

    for package in packages:
        print(f"Installing {package}")
        print(" ")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', f'{package}'])

setup()