import streamlit as st
from langchain_services.chain_builder import setup_chatbot

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = setup_chatbot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def format_source_documents(source_docs):
    """Format source documents into a readable string"""
    if not source_docs:
        return ""
    
    sources = []
    for doc in source_docs:
        if hasattr(doc, 'metadata') and 'source' in doc.metadata:
            # Extract only the filename without the path
            filename = doc.metadata['source'].split('\\')[-1]
            sources.append(filename)
    
    return ", ".join(set(sources))  # Remove duplicates

def main():
    """Main function to run the Streamlit web interface"""
    st.set_page_config(
        page_title="ATC Market Assistant",
        page_icon="🏪",
        layout="centered"
    )

    st.header("🏪 ATC Market Assistant")
    initialize_session_state()

    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "sources" in message:
                st.markdown(f"<span style='color: #2E86C1'><i>Sources: {message['sources']}</i></span>", 
                          unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get chatbot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.chatbot.invoke({"question": prompt})
                    response = result["answer"]
                    sources = format_source_documents(result.get("source_documents", []))
                    
                    st.markdown(response)
                    if sources:
                        st.markdown(f"<span style='color: #2E86C1'><i>Sources: {sources}</i></span>", 
                                  unsafe_allow_html=True)
                    
                    # Save message with sources
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "sources": sources
                    })
                except Exception as e:
                    error_message = f"An error occurred. Please try again or contact support. Error: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_message
                    })

if __name__ == "__main__":
    main()