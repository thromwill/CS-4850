from client import *
from config import AUTHENTICATED_COMMANDS, UNAUTHENTICATED_COMMANDS
from utils import *

# Starts program execution and handles user input
def run_menu():
    
    # Boot client
    client = initialize_client()
    
    # Display menu in console
    clear_screen()
    print("My chat room client. Version One.\n")
    
    # Initialize values
    isAuthenticated = False
    userid = ""
    prompt = ""
    
    # Continue until user logs out
    while True:
        
        # Take user input
        command = input("> ")
        
        # Show command options based on authentication status
        if command == "h":
            print(get_commands(isAuthenticated))
        
        # Handle login, newuser commands   
        elif not isAuthenticated:
            prompt, isAuthenticated, userid = handle_unauthenticated_commands(client, command, isAuthenticated)
            print(f"> {prompt}")
            
        # Handle send, logout commands
        elif isAuthenticated:
            prompt, isAuthenticated = handle_authenticated_commands(client, command, isAuthenticated, userid)
            print(f"> {prompt}")
            
        # Somethings wrong
        else:
            print("[RUN MENU] Authentication Error")

# Handles login, newuser commands
def handle_unauthenticated_commands(client, command, isAuthenticated):
    
    # Initialize value
    userid = ""
    
    # Send request to server to log user in
    if command.startswith("login"):
        
        # Set prompt and update user id
        prompt, userid = client_login(client, command)
        
        # If confirmation is received from the server,
        # update authentication status
        if prompt == "login confirmed":
            isAuthenticated = True
            
    # Send request to server to add a new user
    elif command.startswith("newuser"):
        
        # Update prompt with response
        prompt = new_user(client, command)
        
    # If authenticated commands are used,
    # display denial message to the user
    elif command.startswith("send") or command == "logout":
        prompt = "Denied. Please login first."
    
    # Some other input was entered
    else:
        prompt = "Invalid command. Type 'h' for help."
    
    # Return user message, authentication status,
    # and userid if user is logged in otherwise empty string
    return prompt, isAuthenticated, userid

# Handles send, logout functions
def handle_authenticated_commands(client, command, isAuthenticated, userid):
    
    # Send request to send message to the server
    if command.startswith("send"):
        
        # Update prompt with response
        prompt = send(client, command, userid)
        
    # Send request to server to log user out
    elif command == "logout":
        
        # If confirmation is received, update
        # authentication status, display message, and disconnect client
        if logout(client, userid) == (f"{userid} logout"):
            if disconnect(client) == ("disconnect confirmed"):
                isAuthenticated = False
                print(f"> {userid} left.")
                exit()
            else:
                prompt = "Error disconnecting"
        else:
            prompt = "Error logging out."
            
    # If unauthenticated commands are used,
    # display denial message to the user
    elif command.startswith("login") or command.startswith("newuser"):
        prompt = "Denied. Please logout first."

    # Some other input was entered
    else:
        prompt = "Invalid command. Type 'h' for help."
        
    return prompt, isAuthenticated

# Returns available commands based on authentication status
def get_commands(isAuthenticated):
    return AUTHENTICATED_COMMANDS if isAuthenticated else UNAUTHENTICATED_COMMANDS

if __name__ == "__main__":
    run_menu()    
    