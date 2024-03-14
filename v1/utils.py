from os import system, name

def clear_screen():
    system("cls" if name == "nt" else "clear")
