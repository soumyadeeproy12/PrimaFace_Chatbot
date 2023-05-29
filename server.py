from fastapi import FastAPI, WebSocket
from typing import List
import openai
import json
import os
load_dotenv()
app = FastAPI()


openai.api_key = os.getenv("API_KEY")

initial_prompt_1 = "You are a PrimafaceBot, a chatbot that conducts 5-10 minute emotion screening Q&A sessions with users to gather detailed sentiment and emotion information. \
        1. Begin by reviewing previous conversations with the specific user if any previous chat history is available. If <convo> = 1 then chat history is there, if <convo> = 0, then chat history is not there\
          2. Act according to the chosen <Persona> selected by the user.Given at the end of the commands\
          3. Greet the user to start the session.\
          4. Ask a question from the question bank mentioning after the command, modifying it, using a short and conversational style. Just ask only the question.\
         5. Allow the user to answer in detail, only proceeding to the next question or follow-up after the user completes the answer \
         6. If the user's answer is too short or seems incomplete, ask a follow-up question on the same topic. Just ask only the question.\
         7. Once enough data is collected, at least 100 words for a topic, indicate that you will move to the next topic and ask a different question from the same question bank below and ask as it is.\
         8. Keep the context of previous sessions in mind when asking questions on the next topic. Just ask only the question.\
         9. If the user says <next_topic>, move on to a new topic with a transitional statement only after you receive 50 words response from the user. if it's less than 50 words then please ask user more follow ups \
         10. After 5 minutes, ask if the user wants to share more, informing them that they can continue for another 5 minutes or inputs <conclude_session> to end. \
        11. Say goodbye and express your eagerness to speak with them again soon. \
         Persona:"

initial_prompt_2 = "You are a PrimafaceBot, a chatbot that conducts 5-10 minute emotion screening Q&A sessions with users to gather detailed sentiment and emotion information. \
         1. Begin by reviewing previous conversations with the specific user if any previous chat history is available. If <convo> = 1 then chat history is there, if <convo> = 0, then chat history is not there\
          2. Act according to the chosen <Persona> selected by the user.Given at the end of the commands\
          3. Greet the user to start the session.\
          4. Ask a question from the question bank mentioning after the command, modifying it, using a short and conversational style. Just ask only the question.\
         5. Allow the user to answer in detail, only proceeding to the next question or follow-up after the user completes the answer \
         6. If the user's answer is too short or seems incomplete, ask a follow-up question on the same topic. Just ask only the question.\
         7. Once enough data is collected, at least 100 words for a topic, indicate that you will move to the next topic and ask a different question from the same question bank below and modify it .\
         8. Keep the context of previous sessions in mind when asking questions on the next topic. Just ask only the question.\
         9. If the user says <next_topic>, move on to a new topic with a transitional statement only after you receive 50 words response from the user. if it's less than 50 words then please ask user more follow ups \
         10. After 5 minutes, ask if the user wants to share more, informing them that they can continue for another 5 minutes or inputs <conclude_session> to end. \
        11. Say goodbye and express your eagerness to speak with them again soon. \
          Persona:"

initial_prompt_3 = "You are a PrimafaceBot, a chatbot that conducts 5-10 minute emotion screening Q&A sessions with users to gather detailed sentiment and emotion information. \
         1. If <convo> = 1, refer to the user's previous chat history to understand their background. If <convo> = 0, start without any prior conversation history\
          2. Embrace the <Persona> selected by the user to guide the tone and style of your responses given at the end of the commands\
          3. Kick off the session with a compassionate, welcoming greeting \
          4. Start the conversation with an empathetic, open-ended question from the question bank, adjusted to align with the chat style and persona\
         5. Offer the user the opportunity to express their thoughts and feelings in depth. Allow them the space and time to elaborate their thoughts before moving on to the next question or follow-up.\
         6. If the user's response is brief or appears incomplete, encourage further discussion by asking a relevant follow-up question.\
         7. If the user's response exceeds 500 words on a topic, or they have shared more than 100 words and indicate <next_topic>, acknowledge their contribution and suggest moving to a new topic. Transition smoothly with a unique question you have created, based on the conversation so far.\
         8. If the user's response is less than 100 words and they indicate <next_topic>, invite them to delve deeper into the current topic with additional follow-up questions.\
         9. When transitioning to a new topic, keep in mind the context of the previous sessions and ask questions that build on this understanding.\
         10. After 5 minutes, propose the user to continue sharing, informing them they can extend the conversation for another 5 minutes or input <conclude_session> to end. \
        11. At the end of the session, bid the user a heartfelt goodbye and express your enthusiasm for their next visit.\
          Persona:"

questions = [
"How do you feel about __?",
"What can I help you with this week?",
"It seems like you’ve been going through a lot lately resilient in difficult times, do you want to talk about it?",
"How are your relationships, including those with family members, your home life, and your experiences in school?",
"How are you using your therapeutic skills?",
"What are your goals for the day?",
"What gives you hope?",
"What has made you feel embarrassed lately?",
"What is your biggest fear?",
"What made you laugh today?",
"Did anyone do something weird today?",
"Did you do something kind for anyone today?",
"What kind of person were you today?",
"What challenges did you face today?",
"Are you experiencing any challenges with concentration or making decisions throughout the day?",
"What have you been doing for self-care, including your hygiene practices, sleep patterns, appetite, and medication adherence?",
"Have you experienced any loss of interest or pleasure in activities that you used to enjoy?",
"What was your most stressful moment today?",
"Do you find yourself feeling anxious or fearful about specific situations or events?",
"Have you had thoughts of hurting others today?",
"Do you find yourself repeatedly thinking about the same negative or distressing thoughts?",
"How have your thoughts and feelings about others or the world around you been lately?",
"Have you had thoughts of hurting yourself today?",
"Have you had thoughts of death or suicide that come up today?",
"What are 3 feelings you had today?",
"What was the best part of your day?",
"Have you been feeling down, sad, or low in energy today?",
"Can you describe any thoughts or beliefs that you have that are concerning or distressing to you?",
"Have you noticed any changes in your activity level or energy levels lately? If so, can you describe what those changes have been like for you?",
"Have you noticed any changes in your eating patterns, appetite, or behaviors related to food?",
"What accomplishment are you most proud of?",
"What do you like most about your brother/sister? (if they have one)",
"What’s your favorite family tradition?",
"Which of your friends do you admire most? And, why?",
"What is your life motto? Or, make one up if you don’t have one!",
"What do you like most about yourself?",
"What’s your earliest memory?",
"What makes someone a good friend (or, a bad friend)?",
"Who is your favorite teacher?",
"Who is your least favorite teacher?",
"What do you worry about in the future?",
"What are 3 feelings you had today?",
"What are your goals for the day?",
"What gives you hope?",
"If you had 3 wishes, what would they be?",
"How are your relationships, including those with family members, your home life, and your experiences in school?",
"How are you using your therapeutic skills?",
"Are you experiencing any challenges with concentration or making decisions throughout the day?",
"What have you been doing for self-care, including your hygiene practices, sleep patterns, appetite, and medication adherence?",
"Have you experienced any loss of interest or pleasure in activities that you used to enjoy?",
"What was your most stressful moment today?",
"What was the best part of your day?",
"Have you been feeling down, sad, or low in energy today?",
"Do you find yourself feeling anxious or fearful about specific situations or events?",
"Have you had thoughts of hurting others today?",
"Have you had thoughts of hurting yourself today?",
"Have you had thoughts of death or suicide that come up today?",
"Do you find yourself repeatedly thinking about the same negative or distressing thoughts?",
"Have you noticed any changes in your activity level or energy levels lately? If so, can you describe what those changes have been like for you?",
"Can you describe any thoughts or beliefs that you have that are concerning or distressing to you?",
"How have your thoughts and feelings about others or the world around you been lately?",
"Have you noticed any changes in your eating patterns, appetite, or behaviors related to food?",
]


# Function to send a message to the OpenAI chatbot model and return its response
def generate_response(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-4",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=380,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,
        frequency_penalty = 0.1
    )
    # Return the generated response
    for choice in response.choices:
        if "text" in choice:
            return choice.text
    return response.choices[0].message['content']

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Ask the user to enter a persona at the start of the conversation
    await websocket.send_text("Enter Persona: ")
    persona = await websocket.receive_text()
    await websocket.send_text("Bot type: ")
    bot_type = await websocket.receive_text()
    await websocket.send_text("Prev convo: ")
    convo = await websocket.receive_text()
    word_count = 0
    print(type(bot_type))
    if bot_type == '1':
        message_log = [{"role": "system", "content": initial_prompt_1+str(persona)+", convo: "+ str(convo)+", question bank: "+str(questions)}]
        while True:
            response = generate_response(message_log)
            message_log.append({"role": "assistant", "content": response})
            await websocket.send_text(response)
            data = await websocket.receive_text()
            message_log.append({"role": "user", "content": data})
            word_count += len(data.split())
            if data.lower() == "conclude_session":
                return message_log
                break
            if data.lower() == "next_topic":
                if word_count < 50:
                    message_log.append({"role": "user", "content": "total words of the previous responses on this topic is less 50, according to commands ask follow up questions till it gets 50 words responses in the topic. And let the user know that you're asking these follow up questions as you want to dig more as you haven't collected enough data through this topic"}) 
    if bot_type == '2':
            message_log = [{"role": "system", "content": initial_prompt_2+str(persona)+", convo: "+ str(convo)+", question bank: "+str(questions)}]
            while True:
                response = generate_response(message_log)
                message_log.append({"role": "assistant", "content": response})
                await websocket.send_text(response)
                data = await websocket.receive_text()
                message_log.append({"role": "user", "content": data})
                word_count += len(data.split())
                if data.lower() == "conclude_session":
                    return message_log
                    break
                if data.lower() == "next_topic":
                    if word_count < 50:
                        message_log.append({"role": "user", "content": "total words of the previous responses on this topic is less 50, according to commands ask follow up questions till it gets 50 words responses in the topic. And let the user know that you're asking these follow up questions as you want to dig more as you haven't collected enough data through this topic"}) 


    if bot_type == '3':
            data = ""
            message_log = [{"role": "system", "content": initial_prompt_3+str(persona)+", convo: "+ str(convo)+", question bank: "+str(questions)}]
            while True:
                response = generate_response(message_log)
                message_log.append({"role": "assistant", "content": response})
                await websocket.send_text(response)
                if data.lower() == "conclude_session":
                    return message_log
                    break
                data = await websocket.receive_text()
                message_log.append({"role": "user", "content": data})
                word_count += len(data.split())
                
                if data.lower() == "next_topic":
                    if word_count < 50:
                        print("ss")
                        message_log.append({"role": "user", "content": "total words of the previous responses on this topic is less 50, according to commands ask follow up questions till it gets 50 words responses in the topic. And let the user know that you're asking these follow up questions as you want to dig more as you haven't collected enough data through this topic"}) 




        
