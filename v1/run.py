import os

# Opens a terminal and runs the command
def run_terminal(command):
    os.system(f"start cmd /k {command}")

if __name__ == "__main__":
    
    # Open server terminal
    run_terminal("python ./v1/server.py")

    # Open client terminal
    run_terminal("python ./v1/menu.py")