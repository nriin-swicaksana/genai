from src.inference.chat_handler import reply
from config.config import PORT
import os
import streamlit as st


history = []

def main():
    st.title("Nutry Foody Chatbot")
    st.write("Ask anything about nutrition and fitness!")

    inquiry = st.text_input("Your inquiry:")

    if st.button("Send"):
        if history and history[-1]['inquiry'] == inquiry:
            answer = "Your inquiry is the same as before, please change the inquiry."
        else:
            context = {"inquiry": inquiry, "history": history}
            answer = reply(context)
            history.append({"inquiry": inquiry, "answer": answer})
        
        st.write(f"Assistant: {answer}")

if __name__ == '__main__':
    main()
