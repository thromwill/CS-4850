'''
Name: Will Throm
ID: 18186744
Pawprint: WRTKB8
Date: 03/15/2024
Description: shared helper functions
'''
from os import system, name

def clear_screen():
    system("cls" if name == "nt" else "clear")
