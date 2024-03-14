STUDENT_ID = 18186744
HEADER = 64
FORMAT = 'utf-8'
SERVER = "127.0.0.1"
PORT = int(f"1{str(STUDENT_ID)[-4:]}")
ADDRESS = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
DATABASE = "users.txt"
DEFAULT_USERS = "(Tom, Tom11)\n(David, David22)\n(Beth, Beth33)\n"
AUTHENTICATED_COMMANDS ='''
Available Commands:
-------------------
send -- <message> - Send a prompt to the chatroom
logout ------------ Sign out of the chatroom

'''
UNAUTHENTICATED_COMMANDS = '''
Available Commands:
login --- <UserID> <Password> - Log in to the chatroom
newuser --- <UserID> <Password> - Create a new account
'''
