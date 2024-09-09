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