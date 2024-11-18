
import streamlit as st
from groq import Groq

# Initialize the Groq client
client = Groq(api_key='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')

# Memory to store conversation history
if "memory" not in st.session_state:
    st.session_state.memory = []

# Chatbot response function
def chatbot_response(user_input):
    # Append the user's input to memory
    st.session_state.memory.append({"role": "user", "content": user_input})

    # Prepare the context for the assistant
    prompt = '''You are an expert virtual assistant specializing in natural disasters. Your role is to provide accurate, well-researched, and actionable information on disaster preparedness, mitigation, and management.
    Key Responsibilities:
    Educator: Teach users everything about natural disasters, including causes, impacts, historical occurrences, and the science behind them...
    '''
    messages = [{"role": "system", "content": prompt}] + st.session_state.memory

    # Call the Groq API
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192"
    )

    # Get the model's response
    bot_response = chat_completion.choices[0].message.content

    # Append the bot's response to memory
    st.session_state.memory.append({"role": "assistant", "content": bot_response})

    return bot_response

# Streamlit app layout
st.title("PrepPal by Vinay")
st.subheader("Ask anything related to natural disasters!")

# User input text box
user_input = st.text_input("Your question:", placeholder="Type your question here...")

if st.button("Ask"):
    if user_input:
        bot_response = chatbot_response(user_input)
        # Display conversation
        for message in st.session_state.memory:
            if message["role"] == "user":
                st.write(f"**You:** {message['content']}")
            elif message["role"] == "assistant":
                st.write(f"**PrepPal:** {message['content']}")
