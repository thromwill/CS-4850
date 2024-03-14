import json
import socket
from config import *

# Returns new client socket
def initialize_client():
    try:
        
        # Create new socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDRESS)
        
        return client
    
    except socket.error as err:
        print(f"[CLIENT INITIALIZE_CLIENT] Socket error: {err}")
        
# Sends login message to the server
def client_login(client, command):
    
    # Seperate command into userid and password
    try:
        _, userid, password = command.split()
        
    # Command was invalid
    except ValueError:
        return "Denied. Please use format 'login <userid> <password>'.", ""

    # Send request to server and return result to user
    return send_request(client, {"command": "login", "userid": userid, "password": password}), userid

# Sends new user message to the server
def new_user(client, command):
    
    # Seperate command into userid and password
    try:
        _, userid, password = command.split()
        
    # Command was invalid
    except ValueError:
        return ("Denied. Please use format 'newuser <userid> <password>'.")

    # Check for valid userid and password length
    # Assume these do not include spaces
    if len(userid) < 3 or len(userid) > 32:
        return("Denied. UserID must be 3-32 characters long")
    if len(password) < 4 or len(password) > 8:
        return("Denied. Password must be 4-8 characters long")
    
    # Send request to server and return result to user
    return send_request(client, {"command": "newuser", "userid": userid, "password": password})

# Sends send message to the server
def send(client, command, userid):
    
    # Parse message from command
    try:
        _, message = command.split(' ', 1)
    
    # Command was invalid
    except ValueError:
        return ("Denied. Please use format 'send <message>'.")

    # Send request to server and return result to user
    return send_request(client, {"command": "send", "userid": userid, "body": message})


# Sends logout message to the server
def logout(client, userid):    
    
    # Send request to server and return result to user
    return send_request(client, {"command": "logout", "userid": userid} )

# Sends disconnect message to the server
def disconnect(client):
    try:

        send_message(client, DISCONNECT_MESSAGE)
        client.close()
        
        return "disconnect confirmed"
        
    except Exception as e:
        return f"[CLIENT DISCONNECT] Error: {e}"

# Sends command request to the server
def send_request(client, message):
    try:
        
        # Send JSON message to indicate to the server
        # the requested command and user data
        return(send_json(client, message))
        
        # Return the server's response to the client
        # return receive_message(client)
    
    except Exception as e:
        return f"[CLIENT REQUEST] Error: {e}"

# Sends two messages to the server
# The first message is an indication of the size of the intended message
# This allows the server to reject the intended message
# The second message is the intended message
def send_message(client, message):
    
    # Get the size of the intended message
    messageSizeIndicator = str(len(message)).encode(FORMAT)
    
    # Check that the size is less than the max indicator size
    if len(messageSizeIndicator) <= HEADER:
        
        # Pad the size with whitespace so it is always of size HEADER
        messageSizeIndicator += b' ' * (HEADER - len(messageSizeIndicator))
        
        # Send the inidicator and the message
        client.send(messageSizeIndicator)
        
        response = receive_message(client)
        if response == ("OK"):
            client.send(message.encode(FORMAT))
            response = receive_message(client)
            
        return response
        
    # The indicator size was larger than HEADER
    else:
        return("[CLIENT SEND_MESSAGE] indicator size too large")

# Sends message as JSON
def send_json(client, message):
    return send_message(client, json.dumps(message))

# Recieves message from the server
def receive_message(client):
    response = client.recv(HEADER).decode(FORMAT)
    return response if response else None
   