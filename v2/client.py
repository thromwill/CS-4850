import json
import socket
import threading
import queue
from config import *

message_queue = queue.Queue()

# Returns new client socket
def initialize_client():
    try:
        
        # Create new socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDRESS)
        
        # Start a thread to continuously receive messages from the server
        threading.Thread(target=handle_incoming_messages, args=(client,), daemon=True).start()
        
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
        return ("Denied. Please use format 'newuser <UserID> <Password>'.")

    # Check for valid userid and password length
    # Assume these do not include spaces
    if len(userid) < 3 or len(userid) > 32:
        return("Denied. UserID must be 3-32 characters long")
    if len(password) < 4 or len(password) > 8:
        return("Denied. Password must be 4-8 characters long")
    
    # Send request to server and return result to user
    return send_request(client, {"command": "newuser", "userid": userid, "password": password})

def sendAll(client, command, userid):
    
    # Parse message from command
    try:
        _, _, message = command.split(' ', 2)
        
    # Command was invalid
    except ValueError:
        return ("Denied. Please use format 'send all <message>'.")

    # Send request to server and return result to user
    return send_request(client, {"command": "sendAll", "userid": userid, "body": message})

def sendUser(client, command, userid):
    
    # Parse message from command
    try:
        _, to, message = command.split(' ', 2)
    
    # Command was invalid
    except ValueError:
        return ("Denied. Please use format 'send <UserID> <message>'.")

    # Send request to server and return result to user
    return send_request(client, {"command": "sendUser", "from": userid, "to": to, "body": message})

def who(client, userid):
    # Send request to server and return result to user
    return send_request(client, {"command": "who", "userid": userid})

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
        send_json(client, message)
        
        # Return the server's response to the client
        #return receive_message(client)
        response = message_queue.get()
        # print(f"[RESPONSE] = {response}")
        # print(f"[[DEQUEUE] {response}")
        return response
    
    except Exception as e:
        return f"[CLIENT REQUEST] Error: {e}"

# Sends message as JSON
def send_json(client, message):
    send_message(client, json.dumps(message))

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
        
        #if receive_message(client) == ("OK"):
        response = message_queue.get()
        # print(f"[DEQUEUE] {response}")
        
        # print(f"[MESSAGE] {message}")
        if response == ("OK"):
            client.send(message.encode(FORMAT))
            # print(f"[SENT MESSAGE] {message}")
        else:
            message_queue.put(response)
            
        
    # The indicator size was larger than HEADER
    else:
        print("[CLIENT SEND_MESSAGE] indicator size too large")

# Handles incoming messages from the server
def handle_incoming_messages(client):
    while True:
        response = client.recv(MAX_SIZE).decode(FORMAT)
        # print(f"[RECEIVED] {response}")
        if response:
            if response.startswith("[USER]"):
                print(f"{response[6:]}\n> ", end="")
                
            elif response.endswith("logout."):
                return
            else:
                message_queue.put(response)
                #print(f"[ENQUEUE] {response}")
            