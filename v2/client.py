'''
Name: Will Throm
ID: 18186744
Pawprint: WRTKB8
Date: 03/15/2024
Description: client side logic
'''
import json
import socket
import threading
import queue
from config import *

# Temporary incoming message storage
messageQueue = queue.Queue()

# Returns new client socket
def initialize_client():
    try:
        
        # Create new socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDRESS)
        
        # Start a thread to continuously receive messages from the server
        threading.Thread(target=handle_incoming_messages, args=(client,), daemon=True).start()
        
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
        return ("Denied. Please use format 'newuser <UserID> <Password>'.")

    # Check for valid userid and password length
    # Assume these do not include spaces
    if len(userid) < 3 or len(userid) > 32:
        return("Denied. UserID must be 3-32 characters long")
    if len(password) < 4 or len(password) > 8:
        return("Denied. Password must be 4-8 characters long")
    
    # Send request to server and return result to user
    return send_request(client, {"command": "newuser", "userid": userid, "password": password})

# Sends message to all active users
def sendAll(client, command, userid):
    
    # Parse message from command
    try:
        _, _, message = command.split(' ', 2)
        
    # Command was invalid
    except ValueError:
        return ("Denied. Please use format 'send all <message>'.")

    # Send request to server and return result to user
    return send_request(client, {"command": "sendAll", "userid": userid, "body": message})

# Sends message to specific user
def sendUser(client, command, userid):
    
    # Parse message from command
    try:
        _, to, message = command.split(' ', 2)
    
    # Command was invalid
    except ValueError:
        return ("Denied. Please use format 'send <UserID> <message>'.")

    # Send request to server and return result to user
    return send_request(client, {"command": "sendUser", "from": userid, "to": to, "body": message})

# Returns list of active users
def who(client, userid):
    # Send request to server and return result to user
    return send_request(client, {"command": "who", "userid": userid})

# Logs out user
def logout(client, userid):    
    
    # Send request to server and return result to user
    return send_request(client, {"command": "logout", "userid": userid} )

# Disconnects user
def disconnect(client):
    try:

        send_message(client, {"body": DISCONNECT_MESSAGE})
        client.close()
        
        return "disconnect confirmed"
        
    except Exception as e:
        return f"[CLIENT DISCONNECT] Error: {e}"

# Sends command request to the server
def send_request(client, message):
    try:
        
        # Send JSON message to indicate to the server
        # the requested command and user data
        send_message(client, message)
        
        # Return the server's response to the client
        response = messageQueue.get()
        return response
    
    except Exception as e:
        return f"[CLIENT REQUEST] Error: {e}"

# Sends two messages to the server
# The first message is an indication of the size of the intended message
# This allows the server to reject the intended message
# The second message is the intended message
def send_message(client, message):
    
    # Get message body
    body = message.get("body")
    
    # Convert message from dict to JSON
    messageJson = json.dumps(message)
        
    # Get the size of the intended message
    messageSize = len(messageJson)
    bodySize = len(body) if body else None
    
    # Store size information
    sizeInfo = json.dumps({
        "messageSize": messageSize,
        "bodySize": bodySize
    }).encode(FORMAT)
    
    # Check that the size is less than the max indicator size
    if len(sizeInfo) <= HEADER:
        
        # Pad size with whitespace to be size of HEADER
        sizeInfo += b' ' * (HEADER - len(sizeInfo))
        
        # Send indicator
        client.send(sizeInfo)
        
        # Store response
        response = messageQueue.get()
        
        # Send message
        if response == ("OK"):
            client.send(messageJson.encode(FORMAT))
            
        # Reponse was not OK, put it back into queue
        else:
            messageQueue.put(response)
            
        
    # The indicator size was larger than HEADER
    else:
        print("[CLIENT SEND_MESSAGE] indicator size too large")

# Handles incoming messages from the server
def handle_incoming_messages(client):
    while True:
        
        # Get response from server
        response = client.recv(MAX_SIZE).decode(FORMAT)
        if response:
            
            # Print message
            if response.startswith("[ALL]"):
                print(f"{response[5:]}\n> ", end="")
            elif response.startswith("[USER]"):
                print(f"{response[6:]}\n> ", end="")
                
            # End thread
            elif response.endswith("logout."):
                return
            
            # Add message to queue for other functions
            else:
                messageQueue.put(response)
            