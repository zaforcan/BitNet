import streamlit as st
import requests

# Set up the FastAPI endpoint
API_URL = "http://127.0.0.1:8000/answer"

# Streamlit application
st.title("Q&A Chatbot")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to send a question to the FastAPI endpoint and get an answer
def ask_question(question):
    payload = {"question": question}
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("answer", "No answer found.")
    else:
        return "Error: Could not get an answer."

# Input box for the user to ask a question
user_input = st.text_input("Ask a question:")

# When the user submits a question
if st.button("Send") and user_input:
    # Add user message to the chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Send the question to the API and get a response
    answer = ask_question(user_input)

    # Add the response from the API to the chat history
    st.session_state["messages"].append({"role": "bot", "content": answer})

# Display the conversation history
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Bot:** {message['content']}")
