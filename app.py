import streamlit as st
from groq import Groq, APIError

# Initialize Groq client
api_key = st.secrets["groq"].get("api_key", None)
if not api_key:
    st.error("API Key not found in secrets!")
else:
    client = Groq(api_key=api_key)

# Initialize memory for conversation history
if "memory" not in st.session_state:
    st.session_state.memory = []  # Stores the chat history

# Chatbot response function
def chatbot_response(user_input):
    try:
        # Append the user's input to the conversation memory
        st.session_state.memory.append({"role": "user", "content": user_input})

        # Define the system prompt
        prompt = '''You are an expert virtual assistant specializing in natural disasters. 
        Your role is to provide accurate, well-researched, and actionable information on disaster preparedness, mitigation, and management.
        Key Responsibilities:
        1. Educator: Explain causes, impacts, historical events, and science behind natural disasters.
        2. Advisor: Guide users on how to prepare for and respond to disasters.
        3. Analyst: Provide insights into disaster risk reduction and management strategies.
        4. Supportive: Ensure responses are empathetic and helpful.'''
        
        # Construct the messages for the Groq API
        messages = [{"role": "system", "content": prompt}] + st.session_state.memory

        # Call the Groq API to get a response
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192"
        )
        bot_response = chat_completion.choices[0].message.content

        # Append the assistant's response to the conversation memory
        st.session_state.memory.append({"role": "assistant", "content": bot_response})

        return bot_response
    except APIError as e:
        st.error(f"API error: {e}")
        return "Unable to process your request at the moment."
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return "Something went wrong. Please try again later."

# Streamlit app layout
st.title("PrepPal by Vinay")
st.subheader("Ask me anything about natural disasters!")

# Create the chat-like interface
if user_input := st.chat_input("Type your question here..."):
    # Generate the bot response and display messages
    with st.spinner("Preparing response..."):
        bot_response = chatbot_response(user_input)

# Display the chat history
for message in st.session_state.memory:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])
