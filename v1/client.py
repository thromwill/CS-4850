from config import *
import json
import socket

# Returns new client socket
def initialize_client():
    try:
        
        # Create new socket for the client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDRESS)
        
        return client
    
    # Could not create socket
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

        # Send disconnect message
        send_message(client, {"body": DISCONNECT_MESSAGE})
        client.close()
        
        return "disconnect confirmed"
    
    # Message failed
    except Exception as e:
        return f"[CLIENT DISCONNECT] Error: {e}"

# Sends command request to the server
def send_request(client, message):
    try:
        
        # Send JSON message to indicate to the server
        # the requested command and user data and
        # return response
        return(send_message(client, message))
            
    except Exception as e:
        return f"[CLIENT REQUEST] Error: {e}"

# Sends two messages to the server
# 1) Indicates message size and body size
# This allows the server to reject messages of certain size
# 2) Intended message
# * Initially, this was implemented such that the total message
# size could be no larger than 256 characters. After reading
# the instructions more carefully, it has changed such that
# any command length is allowed such that any command body
# is 256 characters or less
def send_message(client, message):
    
    # Get message body
    body = message.get("body")

    # Convert message from dict to JSON
    messageJson = json.dumps(message)
        
    # Get total message size and body size if applicable
    messageSize = len(messageJson)
    bodySize = len(body) if body else None
    
    # Store size information
    sizeInfo = json.dumps({
        "messageSize": messageSize,
        "bodySize": bodySize
    }).encode(FORMAT)
    
    # Check that sizeInfo is less than max indicator size
    if len(sizeInfo) <= HEADER:
        
        # Pad size with whitespace to be size of HEADER
        sizeInfo += b' ' * (HEADER - len(sizeInfo))
        
        # Send inidicator
        client.send(sizeInfo)
        
        # If server allows message, send message and return response
        response = client.recv(MAX_SIZE).decode(FORMAT)
        if response == ("OK"):
            client.send(messageJson.encode(FORMAT))
            response = client.recv(MAX_SIZE).decode(FORMAT)
    
        return response
        
    # The indicator size was larger than HEADER
    else:
        return("[CLIENT SEND_MESSAGE] indicator size too large")
