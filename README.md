# PrimaFace_Chatbot



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What libraries you need to install the software and how to install them

* Python 3.7 or higher
* openai
* socket
* json
* python-dotenv
* fastapi
* uvicorn

run this command to install the libraries 
```pip install openai socket json python-dotenv fastapi uvicorn```


### Installing

A step by step series of examples that tell you how to get a development env running

1. Clone the repository

```https://github.com/soumyadeeproy12/PrimaFace_Chatbot.git```

2. Install the Python library dependencies( can create a virtual environment and do the same)

### How to run the code and see the output


1. Run the server.py on a separate terminal 
2. Run with this command 
```uvicorn server:app --reload```
3. Now go to the websocket extension: and run this ```ws://localhost:8000/ws```
4. Interact with the bot as you do. for next topic type next_topic, for end the session type 'conclude_session', for bot type: select from 0: traditional QnA bot 1: Mild creative 2:Completely creative gpt bot ; input persona; input if any previous conversation there or not 0: no prev conversation 1: there is a previous conversation 
