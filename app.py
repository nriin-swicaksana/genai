from src.inference.chat_handler import reply
from config.config import PORT
import os
import streamlit as st


history = []

def main():
    st.title("Nutry Foody Chatbot")
    st.write("Ask anything about nutrition and fitness!")
    
    inquiry = st.text_input("Enter your inquiry:")

    if inquiry:
        st.write(f"Human: {inquiry}")

        # Check for duplicate inquiry
        if history and history[-1]['inquiry'] == inquiry:
            answer = "Your inquiry is the same as before, please change the inquiry."
        else:
            # Define stream if necessary (for this example, it's just a placeholder)
            def stream(part):
                yield part

            context = {"inquiry": inquiry, "history": history, "stream": stream}
            answer = reply(context)  # directly return the plain answer
            st.write(f"Assistant: {answer}")
            history.append({"inquiry": inquiry, "answer": answer})

if __name__ == '__main__':
    main()
