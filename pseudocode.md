## Rock, Paper, Scissors Microbit Pseudocode

**Imports and Variables:**

- Import the `radio`, `os`, and `random` libraries.
- Initialize variables for `score`, `choices` (list containing "rock", "paper", "scissors"), `hostmode`, `input1`, `connected` (list of connected users), `allchoices` (list of current player choices and player IDs), `rpslizspock` (flag for playing with or without lizard and spock), `playerid`, `poll` (flag for extended choices), `breakfromloop`, and `ainum` (number of AI players).

**Game Mode Selection:**

- Ask the user to press button A to host a game or button B to join a game.
- Store the button press as `input1`.
- Set `hostmode` to "host" if A is pressed, "search" if B is pressed.

**Host Mode:**

- If `hostmode` is "host":
    - Send "join" message over radio.
    - Wait for a response of "accepted" to confirm a player has joined.
    - Send the number of connected players back to the joining player.
    - Ask the host to choose the number of AI players using buttons A and B.
    - Store the choice in `ainum`.
    - Ask the host to choose either RPS or RPSLIZSPOCK using buttons A and B.
    - Store the choice in `rpslizspock`.
    - Send "True" to the player if RPSLIZSPOCK is chosen.
    - Send "starting" message to signal the game start.
    - Wait for 300 milliseconds.
    - For each connected player:
        - If it's the host's turn:
            - Get the host's choice using `getrpschoice(False)`.
            - Add the choice and player ID (0) to `allchoices`.
        - For each AI player:
            - Add a random choice (with or without lizard and spock based on `rpslizspock`) and a negative player ID to `allchoices`.
    - Enter the game loop:
        - While there is more than one player remaining:
            - For each choice in `allchoices`:
                - Compare the choices using a modulo operation to determine the winner.
                - Send elimination messages to eliminated players or a tie message if there is no winner.
                - If a player is eliminated, update `allchoices` accordingly.
                - If it's the host's turn again:
                    - Get the host's new choice.
                    - Add the choice to `allchoices`.
                - For each AI player:
                    - Add a new random choice to `allchoices`.
        - Determine the winner based on the remaining player ID in `allchoices`.
        - Send a "win" message with the winner ID.
        - Display and print the winner message.

**Join Mode:**

- If `hostmode` is "search":
    - Display a message indicating searching for a host.
    - Wait for a "join" message from a host.
    - Send "accepted" message to confirm joining.
    - Wait for the host to send the number of connected players.
    - Wait for the host to send a "True" message if RPSLIZSPOCK is chosen.
    - Wait for the "starting" message to signal the game start.
    - Enter the game loop:
        - While the player is not eliminated:
            - Wait for a message indicating it's the player's turn ("p"+player ID+"turn").
            - Send the player's choice using `getrpschoice(poll)`.
            - Process received messages:
                - If eliminated, display and print an elimination message.
                - If another player is eliminated, display and print the elimination message.
                - If a tie message is received, display and print a tie message.
                - If a "win" message is received, determine the winner and display and print the winner message.
