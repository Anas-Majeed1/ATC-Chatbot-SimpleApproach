import streamlit as st
from langchain_services.chain_builder import setup_chatbot

def initialize_session_state():
    """
    Initialize Streamlit session state variables
    
    Sets up the chatbot and messages list in the session state if they don't exist
    """
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = setup_chatbot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def main():
    """
    Main function to run the Streamlit web interface
    
    Sets up the page configuration and handles the chat interface
    """
    st.set_page_config(
        page_title="ATC Market Assistant",
        page_icon="🏪",
        layout="centered"
    )

    st.header("🏪 ATC Market Assistant")

    # Initialize session state
    initialize_session_state()

    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get chatbot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.chatbot.invoke({"question": prompt})
                    response = result["answer"]
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_message = f"An error occurred. Please try again or contact support. Error: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

if __name__ == "__main__":
    main()