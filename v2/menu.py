from client import *
from config import AUTHENTICATED_COMMANDS, UNAUTHENTICATED_COMMANDS
from utils import *

# Manages program execution
def run_menu():
    
    # Boot client
    client = initialize_client()
    
    # Initialize values
    isAuthenticated = False
    userid = ""
    prompt = ""
    
    # Display menu in console
    clear_screen()
    print("My chat room client. Version Two.\n")
    
    # Continue until user exists
    while True:
        
        # Take user input
        command = input("> ")
        
        # Show command options based on authentication status
        if command == "h":
            print(get_commands(isAuthenticated))
            continue
        
        # Handle login, newuser commands   
        if not isAuthenticated:
            prompt, isAuthenticated, userid = handle_unauthenticated_commands(client, command, isAuthenticated)
            
        # Handle send, logout commands
        elif isAuthenticated:
            prompt, isAuthenticated = handle_authenticated_commands(client, command, isAuthenticated, userid)

        if prompt != "None":
            print(f"> {prompt}")
        
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
            
    # Send request to server to add a user
    elif command.startswith("newuser"):
        
        # Update prompt with response
        prompt = new_user(client, command)
        
    # If authenticated commands are used,
    # display denial message to the user
    elif command.startswith("send") or command == "logout":
        prompt = "Denied. Please login first."
    
    # If any other input is entered, indicate invalid command
    else:
        prompt = "Invalid command. Type 'h' for help."
    
    # Return user message, authentication status,
    # and userid if user logged in otherwise empty string
    return prompt, isAuthenticated, userid

# Handles send, logout functions
def handle_authenticated_commands(client, command, isAuthenticated, userid):

    # if command.startswith("send"):
    #     prompt = send(client, command, userid)
    
    if command.startswith("send all"):
        # prompt = send(client, command, userid)
        prompt = sendAll(client, command, userid)
        if not prompt.startswith("Denied"):
            prompt = "None"
        #print("[SEND ALL -> DONE]")
    
    elif command.startswith("send") and not command.startswith("send all"):
        prompt = sendUser(client, command, userid)
        if not prompt.startswith("Denied"):
            prompt = "None"
        #print("[SEND USER -> DONE]")
        #print(f"[PROMPT] {prompt}")

    elif command == "who":
        prompt = who(client, userid)
        #print("[WHO -> DONE]")

    # Send request to server to log user out
    elif command == "logout":
        
        # If confirmation is received, update
        # authentication status and prompt
        if logout(client, userid) == (f"{userid} logout"):
            if disconnect(client) == ("disconnect confirmed"):
                isAuthenticated = False
                prompt = f"{userid} left."
                exit()
            else:
                prompt = "Error logging out"
        else:
            prompt = "Error logging out."
            
    # If unauthenticated commands are used,
    # display denial message to the user
    elif command.startswith("login") or command == "newuser":
        prompt = "Denied. Please logout first."

    # If any other input is entered, indicate invalid command
    else:
        prompt = "Invalid command. Type 'h' for help."
        
    return prompt, isAuthenticated

# Returns available commands string based on authentication status
def get_commands(isAuthenticated):
    return AUTHENTICATED_COMMANDS if isAuthenticated else UNAUTHENTICATED_COMMANDS
    