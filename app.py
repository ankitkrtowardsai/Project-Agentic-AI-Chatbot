from agentic_chatbot_backend import chatbot
from langchain_core.messages import BaseMessage, HumanMessage
import streamlit as st

#test run
# thread_id = "3"
# config = {'configurable': {'thread_id': thread_id}}
# response = chatbot.invoke({'messages': [HumanMessage(content="hi what model are you ?")]}, config=config)


# print(response['messages'][-1].content)
# --------------------------------------------------------

# title daalo
st.title("Agentic Chatbot with LangGraph")

# config to trach
# """
# Agentic Chat Architecture Flow:

# [ User opens chat app ]
#       │
# [ Session ] ── (Handles login, rate limits, and active connection)
#       │
#       ├──> Thread 1: "Code Debugging"
#       │      └──> Checkpoints (Saves State after each tool execution)
#       │
#       └──> Thread 2: "Database Query"
#              └──> Checkpoints (Saves State independently)
#       │
# [ Turn ] ──── (User sends message -> Agent reasons & calls tools -> Final response)
#       │
# [ Memory ] ── (Updates short-term thread history and long-term user facts)
# """

# config kyu :
#   Thread ID & Persistence (Memory Management ke liye) (rmessage kis purane conversation thread mein add karna hai aur kahan se history uthani hai.)
#   Runtime Configuration / Dynamic Variables (jaise user ID, environment, ya API keys)
#   Execution Control & Metadata (agent Recursion Limit, Tags & Metadata )
CONFIG = {'configurable': {'thread_id': 'thread-1'}}


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []



# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])



user_input = st.chat_input('Type here')

if user_input:
    # first add the user message to message_history then show it on UI
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'): #user emoji k liye
        st.text(user_input) #user message dikhao
    

    # stream assistant message and then store
    with st.chat_message('assistant'): #assistant emoji k liye

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= CONFIG,
                stream_mode= 'messages'
            )
        )
    # add the user message to message_history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
