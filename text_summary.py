import openai

# Set up OpenAI API key
api_key = 
openai.api_key = api_key

def str_conver(conversation):
  conversation_dict = {}
  current_question = ""
  for chat in conversation:
    print(chat)
    if chat['role'] == 'assistant':
      current_question = chat['content']
    elif chat['role'] == 'user':
      conversation_dict[current_question] = chat['content']

  return conversation_dict

def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-4",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=380,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7, 
        frequency_penalty = 0.1,
       # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content

def main(conversation_dict):
  x = send_message([{'role':'system','content':'extract emotion class(happy,sad, excited, surprise, angry, neutral) and give % for these 6 emotions at the end of the conversation, check each and every conversation line give how much these classes hold a % in the entire conversation; valence score(with decimal), arousal score(with decimal), conversation topic, summary of the conversation from this entire conversation and please make json summary of that mentioning emotion_class_percentage, valence,arousal, topics, summary  '+str(conversation_dict)}])
  return x

"""
if __name__ == "__main__":
    #main_1()
    #data_2 = main_2(0)
    output = main(prev_convo)
"""
