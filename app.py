import websockets
import openai
import socket
import json
from dotenv import load_dotenv
import os
load_dotenv()

# Set up OpenAI API key
api_key = os.getenv("API_KEY")
openai.api_key = api_key

# Set up the list of questions to ask the user
questions = [
    "I’d love to hear more about __ (recent event in their life). What was your favorite part/best thing that happened?",
"How do you feel about today?", 
"What can I help you with this week?",
"It seems like you’ve been going through a lot lately. I know how hard it is to be resilient in difficult times. Do you want to talk about it?",
"What has made you feel embarrassed lately?", "What is your biggest fear?",
"Who at your school would you like to get to know better?",
"Tell me about someone who made you feel special today. What did they do or say?",
"What was one nice thing you did for someone today?",
"Do you know anyone at your school who’s being treated badly? How do you think they are feeling right now?",
"Who did you sit with at lunch?",
"What was your favorite thing that you did today?",
"Can you show me something you learned how to do today?",
"What was your favorite part of the day?",
"Name a high and a low (or a rose and a thorn) from your day.",
"What was the most unexpected thing that happened today?",
"Did everything go exactly as planned today?",
"What challenges did you face today?",
"What made you laugh today?",
"Did anyone do something weird today?",
"Did you do something kind for anyone today?",
"What kind of person were you today?",
"What are you looking forward to about tomorrow?",
"Where did you grow up, and what did you like about it?",
"What do you do for fun?",
"Did you have a pet growing up? Tell me about it.",
"It seems like you love __. What is it you love about it?",
"What does your name mean?",
"Can you believe the weather we’ve been having?",
"What accomplishment are you most proud of?",
"What do you like most about your brother/sister? (if they have one)",
"What’s your favorite family tradition?",
"Which of your friends do you admire most? And, why?",
"What is your life motto? Or, make one up if you don’t have one!",
"What do you like most about yourself?",
"What’s your earliest memory?",
"What makes someone a good friend (or, a bad friend)?",
"Who is your favorite teacher?",
"Who is your least favorite teacher?"
]
message_log = []
def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=380,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content

def run_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()

        print(f"Server listening on {host}:{port}")
        first_message = True
        message_log.append(
        {"role": "system", "content": "Hello, I'm your virtual therapist. I'm here to listen to you and help you feel better."}
    )
        while True:
            conn, addr = server.accept()
            with conn:
                print(f"Connected by {addr}")

                # Send the initial message
              #  initial_message = send_initial_message()
               # conn.sendall(initial_message.encode('utf-8'))

                # Loop to receive and respond to messages from the client
                
                while True:
                    # Receive a message from the client
                    data = conn.recv(1024)
                    if not data:
                        break

                    request = json.loads(data.decode('utf-8'))
                    user_input = request['user_input']
                   # print(user_input)
                    if user_input =="first_res":
                        first_message == True

                    # If the user input is "quit", close the connection
                    if user_input.lower() == "quit":
                        response = "Goodbye!"
                        conn.sendall(response.encode('utf-8'))
                        break

                    # Pass the user input to the main function
                    if first_message == True:
                        response = main(user_input, True)
                    else:
                        response = main(user_input, False)
                    conn.sendall(response.encode('utf-8'))
                    
                    first_message = False
                    
            conn.close()
                

# Function to send a message to the OpenAI chatbot model and return its response


# Define the handler for each new client connection
def main(user_input, first_request):
    
    response_log= []
    emotion_log = []
    # Set a flag to keep track of whether this is the first request in the conversation
    
    flag = 0
    # Start a loop that runs until the user types "quit"
    while True:
        if first_request == True:
            # If this is the first request, get the user's input and add it to the conversation history
            
            message_log.append({"role": "user", "content": "Talk like a therapist. Ask the best question out of the following according to the context. Ask a maximum 4-5 follow-up questions and then again choose it from the list.Question list after receiving the initial response - "+ str(questions)+"if you get the rules, print some introductory pleasentory phrase and then say just say This is your PrimaFace virtual partner, Let's start today's session! and ask a question and rephrase it from the list above "})
            #user_input = input("You: ")
            # Send the conversation history to the chatbot and get its response
            response = send_message(message_log)
          #  print("mission1")
            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})
            first_request = False
            return f"AI assistant: {response}"

            # Set the flag to False so that this branch is not executed again
            
        elif first_request == False :
            # If this is not the first request, get the user's input and add it to the conversation history
           # user_input = input("You: ")
            response_ = send_message([{"role":"user","content":"classify the statement into these following emotions without giving any reasoning- Happiness, Sadness,Anger, Fear,Disgust,Surprise,Excitement,Calmness  the statement:"+ user_input}])
            emotion_log.append(response_)
            response_log.append(user_input)
           # print("mission2")
            # If the user types "quit", end the loop and print a goodbye message
            if user_input.lower() == "quit":
                
                return f"AI assistant: Goodbye!"
                break

               # print(message_log)
                
            
            if user_input.lower() == "next_question":
                message_log.append({"role": "user", "content": "ask another best suited question from the list above and rephrase it and output only the rephrased question without saying anything else" })
               # print(message_log)
                response = send_message(message_log)
                flag = 0
                return f"AI assistant: {response}"

            
            else:

                message_log.append({"role": "user", "content": user_input})
 
                # Send the conversation history to the chatbot and get its response
                response = send_message(message_log)
                #print(message_log)
                # Add the chatbot's response to the conversation history and print it to the console
                message_log.append({"role": "assistant", "content": response})
                flag = flag + 1
                return f"AI assistant: {response}"

   # response_final = send_message([{"role":"user","content":"classify the statement into these following emotions without giving any reasoning- Happiness, Sadness,Anger, Fear,Disgust,Surprise,Excitement,Calmness  the statement:"+ response_log}])
    
              


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12354
    run_server(host, port)