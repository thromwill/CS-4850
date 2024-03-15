'''
Name: Will Throm
ID: 18186744
Pawprint: WRTKB8
Date: 03/15/2024
Description: (Windows) Opens two terminals, one for the server and one for a client
'''
import os

# Opens a terminal and runs the command
def run_terminal(command):
    os.system(f"start cmd /k {command}")

if __name__ == "__main__":
    
    # Open server terminal
    run_terminal("python ./server.py")

    # Open client terminal
    run_terminal("python ./menu.py")