from config import *
from utils import *
import json
import socket
import threading

# Store users that are logged in
authenticatedUsers = {} # { userid : password }

# Returns new server socket
def initialize_server():
    try:
        
        # Create and bind server socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((SERVER, PORT))
        
        return server

    # Log error message
    except socket.error as err:
        print(f"[SERVER INITIALIZE_SERVER] Socket error: {err}")

# Starts server to allow client connection
def start(server):
    
    # Listen for server activity 
    server.listen()
    
    # Print intial console output
    clear_screen()
    print("My chat room server. Version One.\n")
    
    # Handle each client connection in a new thread
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args = (connection, address))
        thread.start()
        # print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# Handles incoming client messages
def handle_client(connection, address):
    # print(f"[NEW CONNECTION] {address} connected.")

    # Continue until client disconnects
    connected = True
    while connected:
        
        # Recieve size indicator
        messageLength = connection.recv(HEADER).decode(FORMAT)
        
        # Check that the indicator was recieved
        if messageLength:
            try: 
                
                # Only allow messages of length 1-256
                messageLength = int(messageLength)
                if 1 <= messageLength <= 256:
                    
                    # Alert the client to send full message
                    connection.send("OK".encode(FORMAT))
                    
                    # If the indicator indicated valid message size,
                    # recieve the intended message
                    message = connection.recv(messageLength).decode(FORMAT)
                    
                    # Stop if we the user wants to disconnect
                    if message == DISCONNECT_MESSAGE:
                        connected = False
                        
                    # Read message as json
                    try:
                        messageJson = json.loads(message)
                        
                        # Execute primary user commands
                        if isinstance(messageJson, dict):
                            command = messageJson.get("command")
                            
                            # Login
                            if command == "login":
                                userid = messageJson.get("userid")
                                password = messageJson.get("password")
                                response = login(userid, password)
                                connection.send(response.encode(FORMAT))
                            
                            # New User
                            elif command == "newuser":
                                userid = messageJson.get("userid")
                                password = messageJson.get("password")
                                response = newuser(userid, password)
                                connection.send(response.encode(FORMAT))
                            
                            # Send message
                            elif command == "send":
                                userid = messageJson.get("userid")
                                message = messageJson.get("body")
                                print(f"{userid}: {message}")
                                connection.send(f'{userid}: {message}'.encode(FORMAT))
                            
                            # Logout
                            elif command == "logout":
                                userid = messageJson.get("userid")
                                logout(userid)
                                connection.send(f'{userid} logout'.encode(FORMAT))
                                
                            else:
                                # Command was not a valid field
                                connection.send("[FAILURE] Invalid command".encode(FORMAT))
                        else:
                            # messageJson was not a dictionary
                            connection.send("[FAILURE] Invalid JSON format".encode(FORMAT))
                            
                    # Could not decode message as JSON
                    except json.JSONDecodeError as err:
                        connection.send(f"[FAILURE] {err}".encode(FORMAT))
                
                else:
                    connection.send("Denied. Message must be bewteen 1-256 characters".encode(FORMAT))
                    # connection.recieve(MAX_BUFFER_SIZE) # Clear large incoming message
            
            except ValueError as e:
                connection.send(f"[SERVER HANDLE CLIENT] Error: {e}".encode(FORMAT))
                
    # print(f"[CONNECTION CLOSED] {address} disconnected.")
    connection.close()
    
# Authenticates user given userid and password
def login(userid, password):
    try:
        
        # Read the file
        with open(DATABASE, 'r') as f:
            
            # Check for valid credentials
            for line in f:
                u, p = line.strip()[1:-1].split(', ')

                if u == userid and p == password:
                    
                    # Update list of users, display in console, and return confirmation
                    authenticatedUsers[u] = p
                    print(f"{userid} login.")
                    return f"login confirmed"
    # File was not found
    except FileNotFoundError:
        # Create file and add default users
        with open(DATABASE, 'w') as f:
            f.write(DEFAULT_USERS)
    
    # Return denial
    return "Denied. User name or password incorrect."

# Adds user to 'database' aka 'users.txt'
def newuser(userid, password):
    try:
        
        # Check for userid in file
        with open(DATABASE, 'r') as f:
            for line in f:
                existing_userid, _ = line.strip()[1:-1].split(', ')
                
                # If it exists, return denial
                if existing_userid == userid:
                    return "Denied. User account already exists."
        
        # Add new user to file
        with open(DATABASE, 'a') as f:
            f.write(f"({userid}, {password})\n")
            
    # File was not found        
    except FileNotFoundError:
        # Create file, add default users, then add new user
        with open(DATABASE, 'w') as f:
            f.write(DEFAULT_USERS)
            f.write(f"({userid}, {password})\n")
    
    # Display in console and return confirmation
    print("New user account created.")
    return f"New user account created. Please login."

# Removes user from user list
def logout(userid):
    authenticatedUsers.pop(userid)
    print(f"{userid} logout.")
    
if __name__ == "__main__":
    server = initialize_server()
    
    # print("[STARTING] Server is starting...")
    start(server)
    