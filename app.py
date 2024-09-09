from src.inference.chat_handler import reply
from config.config import PORT
import streamlit.components.v1 as components
import os
import streamlit as st

chat_interface = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Place your CSS here or link to an external CSS file */
        html {
            line-height: 1.5;
            background-color: #f4f4f4;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            display: flex;
            flex-direction: column;
            color: #333;
            background: #e2e2e2;
            height: 100vh;
            margin: 0;
        }
        main#chat {
            padding: 1rem;
            overflow-y: auto;
            flex: auto;
            background: #fff;
            border-bottom: 1px solid #ccc;
            border-top: 1px solid #ccc;
            height: calc(100% - 80px);
        }
        footer {
            display: flex;
            justify-content: center;
            padding: 1rem;
            background-color: #131614;
            border-top: 1px solid #ccc;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
        .input-container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        input, button {
            margin: 0 0.5rem;
        }
        input {
            font-family: inherit;
            color: #333;
            width: 80%;
            height: 2.5rem;
            padding: 0.5rem;
            font-size: 1rem;
            border: 2px solid #007bff;
            background-color: #fff;
            border-radius: 0.5rem;
            box-shadow: 0 0 0.5rem rgba(0, 0, 0, 0.1);
        }
        button {
            height: 2.5rem;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            border: 2px solid #007bff;
            background-color: #007bff;
            color: white;
            border-radius: 0.5rem;
            box-shadow: 0 0 0.5rem rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: background-color 0.2s ease, border-color 0.2s ease;
        }
        button:hover {
            background-color: #0056b3;
            border-color: #00408a;
        }
        .speech {
            display: grid;
            gap: 0.75rem;
            padding: 0.5rem 0;
        }
        .speech-bubble {
            display: inline-block;
            white-space: pre-line;
            position: relative;
            padding: 0.75rem 1.25rem;
            border-radius: 0.5rem;
            max-width: 80%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            background: #f1f1f1;
            border: 1px solid transparent;
        }
        .speech-bubble-assistant {
            background: #f8f9fa;
            border-color: #d3d9d5;
        }
        .speech-bubble-human {
            background: #007bff;
            color: #fff;
            border-color: #0056b3;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            background: linear-gradient(#007bff);
        }
    </style>
</head>
<body>
    <main id="chat"></main>
    <footer>
        <div class="input-container">
            <input type="text" id="prompt" autocomplete="off" autofocus placeholder="Message Nutry Foody">
            <button id="sendButton">Send</button> 
        </div>
    </footer>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const $ = (id) => document.getElementById(id);
            const $div = (cls) => {
                const el = document.createElement('div');
                el.setAttribute('class', cls);
                return el;
            }
            function message(type, text) {
                const el = $div(`speech-bubble-${type}`);
                el.innerText = text || '';
                const wrapper = $div(`speech speech-${type}`);
                wrapper.appendChild(el);
                $('chat').appendChild(wrapper);
                setTimeout(() => {
                    el.scrollIntoView({ behavior: 'smooth' });
                }, 0);
                return el;
            }
            function stream(type, text) {
                const selectors = document.querySelectorAll(`.speech-bubble-${type}`);
                const el = selectors[selectors.length - 1] || message(type, text);
                el.innerText = text || '';
                setTimeout(() => {
                    el.scrollIntoView({ behavior: 'smooth' });
                }, 0);
                return el;
            }
            function unmessage(type) {
                const el = document.querySelector(`.speech-${type}`);
                el && el.remove();
            }
            const isTouchDevice = () => 'ontouchstart' in window;
            function focusInput() {
                if (!isTouchDevice()) {
                    $('prompt').focus();
                }
            }
            async function ask(question, handler) {
                message('human', question);
                $('prompt').blur();
                const url = new URL('/chat', window.location.origin);
                url.searchParams.append('inquiry', encodeURIComponent(question));
                const el = message('loader');
                el.innerHTML = '<div class="loader"></div>';
                setTimeout(get, 100);
                async function get() {
                    try {
                        const response = await fetch(url);
                        if (!response.ok) throw new Error('Network response was not ok');
                        message('assistant');
                        let answer = '';
                        const reader = response.body.getReader();
                        while (true) {
                            const { done, value } = await reader.read();
                            unmessage('loader');
                            if (done) break;
                            const text = new TextDecoder().decode(value, { stream: true });
                            answer += text;
                            stream('assistant', answer);
                        }
                    } catch (e) {
                        message('panic', `Something is wrong: ${e.toString()}`);
                    } finally {
                        unmessage('loader');
                        handler && handler(answer);
                        setTimeout(focusInput, 0);
                    }
                }
            }
            function sendMessage() {
                const el = $('prompt');
                const question = el.value.trim();
                if (question.length > 0) {
                    ask(question);
                    el.value = '';
                }
            }
            $('prompt').addEventListener('keydown', function handleKeyInput(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            });
            $('sendButton').addEventListener('click', function handleButtonClick() {
                sendMessage();
            });
            setTimeout(() => {
                message('assistant', 'Hi, this is Nutry Foody!');
            }, 100);
        });
    </script>
</body>
</html>
"""

history = []

def main():
    st.title("Nutry Foody Chatbot")
    st.write("Ask anything about nutrition and fitness!")
    components.html(chat_interface, height=600, scrolling=True)
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
