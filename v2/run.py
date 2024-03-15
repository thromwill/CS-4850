import os

# Opens a terminal and runs the command
def run_terminal(command):
    os.system(f"start cmd /k {command}")

if __name__ == "__main__":
    
    # Open server terminal
    run_terminal("python ./v2/server.py")

    # Open three client terminals
    for _ in range(3):
        run_terminal("python ./v2/menu.py")
        