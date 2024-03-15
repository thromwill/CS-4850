ChatRoom Version 1

Submission:

The submission consists of this README file and one zip file. As the source code is broken into several files with shared components, splitting this into two zip files is not optimal.

Execution:

	- Simple execution (Windows only):

		"python run.py"

	- Otherwise:
		
		"python server.py" (once)
		"python menu.py" (for each client)

Directory Structure:
- v1:
  - client.py: client side logic
  - config.py: shared constants
  - menu.py: starts client and manages user CLI
  - run.py: (Windows) Opens two terminals, one for the server and one for a client
  - server.py: server side logic
  - utils.py: shared helper functions
  * - users.txt: database file for users (created at program execution)

Important Notes

1. An additional command "h" (help) is included. This will display any current valid commands offered to the user. This command follows the same style as all other output.

2. Based on the following instructions: "The following shows an example chat room session. Your client/server programs must reproduce this example exactly." a strong attempt was made to satisfy the required output. However, the given output includes things like inconsistant spacing and bolding that is not represented in this program. No text is bolded and all output begins with "> " as opposed to ">".

3. Based on the following ambiguous instructions, the decision was made to have 'users.txt' created on server start up instead of first account creation if it is not found. This is preferred as the given accounts will be immediately created if not found and the database file will always exist before any operations on it are attempted.

"When the server starts, it should first read the user account information from the given file users.txt. For grading purpose, the initial user
accounts (UserID, Password) are (Tom, Tom11), (David, David22) and (Beth, Beth33)."

"New user accounts should persist between sessions (i.e., the new user information needs to
be stored in the users.txt file by the server). If the file does not exist, the server should create
it when the first account is created."

4. The check for: "Message size can be between 1 and 256 characters." is was implemented as follows:

- For every request sent to the server, two messages are sent.
- First, a message of size 64 containing the size of the intended request is sent to the server.
- The server will check if the message contains a 'body' element, and if so, check that the body is between 1 and 256 characters in length.
- If the body is valid, the server will send an 'OK' respond, and the intended request will be sent
- Initially, it was my understanding that the server would only accept requests of total length 256 or less, but I now believe it is intended that requests of any lengtha are accepted such that message bodies must be between 1-256 characters.
- This method is more scalable than having the client check for message length. If the permitted length changes, only one check on the server has to change and each client does not require update.

5. This implentation is based on the following 'Tech With Tim' tutorial for Python Socket Programming and adapted/ expanded to meet the assignment requirements. Link: https://www.youtube.com/watch?v=3QiPPX-KeSc&t=2444s
