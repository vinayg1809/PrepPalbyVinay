import streamlit as st
from groq import Groq, APIError

# Initialize Groq client
api_key = st.secrets["groq"].get("api_key", None)
if not api_key:
    st.error("API Key not found in secrets!")
else:
    client = Groq(api_key=api_key)

# Initialize memory
if "memory" not in st.session_state:
    st.session_state.memory = []

# Chatbot response function
def chatbot_response(user_input):
    try:
        st.session_state.memory.append({"role": "user", "content": user_input})

        prompt = '''You are an expert virtual assistant specializing in natural disasters.'''
        messages = [{"role": "system", "content": prompt}] + st.session_state.memory

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192"
        )
        bot_response = chat_completion.choices[0].message.content
        st.session_state.memory.append({"role": "assistant", "content": bot_response})

        return bot_response
    except APIError as e:
        st.error(f"API error: {e}")
        return "Unable to process your request at the moment."
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return "Something went wrong. Please try again later."

# App layout
st.title("PrepPal by Vinay")
st.subheader("Ask anything related to natural disasters!")

user_input = st.text_input("Your question:", placeholder="Type your question here...")

if st.button("Ask"):
    if user_input.strip():
        with st.spinner("Preparing response..."):
            bot_response = chatbot_response(user_input)

        for message in st.session_state.memory:
            if message["role"] == "user":
                st.write(f"**You:** {message['content']}")
            elif message["role"] == "assistant":
                st.write(f"**PrepPal:** {message['content']}")
    else:
        st.warning("Please enter a valid question.")
