
# UDP Client-Server Trivia Game (Socket Programming Project)

## Overview

This project implements an interactive **Multiplayer Trivia Game** using **UDP Socket Programming**.  
It enables multiple players (clients) to compete by answering trivia questions while the server orchestrates the game flow: managing players, sending questions, collecting answers, scoring, and declaring winners.

✅ Built using **Python** with `socket`, `threading`, and `time` modules.

---

## Files

| File | Description |
|:-----|:------------|
| `server.py` | Server script that manages players, questions, answers, scoring, and broadcasts results. |
| `client.py` | Client script that connects to the server, submits answers, and displays game updates. |
| `Project_Discussion.pdf` | Project description and functionality requirements. |

---

## Features

### Server Responsibilities:
- Listen for incoming client connections on port `5689`.
- Maintain a list of active clients (IP address + port number).
- Start a new round when at least 2 players are connected.
- Send random questions to all players.
- Collect and validate player answers (only first response counted).
- Score players based on correct answers and response time.
- Broadcast scores and correct answers after each question.
- Announce the winner at the end of each round.
- Disconnect inactive players.

### Client Responsibilities:
- Connect to server using IP and port.
- Send username upon connection.
- Receive and display server messages (notifications, questions, scores).
- Submit answers within the given time frame.
- Receive updates about game status and leaderboard.

---


## Requirements

- Python 3.8 or newer
- Standard Python libraries (`socket`, `threading`, `time`)

---

## Notes

- Each round consists of **3 questions**.
- Points are awarded more for faster correct answers.
- Players who don't respond are removed after each round.
- The server and clients use **UDP protocol** for communication (connectionless).


