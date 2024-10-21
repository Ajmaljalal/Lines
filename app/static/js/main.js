// This file is currently empty, but you can add client-side functionality here if needed.
console.log('main.js loaded');

document.addEventListener('DOMContentLoaded', () => {
  const sendButton = document.getElementById('sendButton');
  const userInput = document.getElementById('userInput');

  function sendMessage() {
    let message = userInput.value.trim();
    if (message === '') {
      return;
    }
    addMessage('user', message);
    userInput.value = '';
    fetchChatResponse(message);
  }

  sendButton.addEventListener('click', sendMessage);

  userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  });

  userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = userInput.scrollHeight + 'px';
  });

  async function fetchChatResponse(message) {
    try {
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        body: JSON.stringify({ user_input: message }),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();

      if (data.error) {
        addMessage('ai', 'Sorry, I couldn\'t process your request. Please try again.');
      } else if (typeof data.response === 'string') {
        addMessage('ai', data.response);
      } else {
        console.error('Unexpected response type:', data.response);
        addMessage('ai', 'Received an unexpected response format.');
      }
    } catch (error) {
      console.error('Error fetching chat response:', error);
      addMessage('ai', 'There was an error processing your request.');
    }
  }

  function addMessage(sender, text) {
    var chatMessages = document.getElementById('chatMessages');
    var messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + sender;

    if (sender === 'ai') {
      if (typeof text === 'string') {
        const tableMatch = text.match(/<table[\s\S]*?<\/table>/);
        if (tableMatch) {
          text = tableMatch[0];
        }

        if (text.startsWith('```html') && text.endsWith('```')) {
          text = text.slice(7, -3).trim();
        }

        messageDiv.innerHTML = text;
      } else {
        console.error('Expected text to be a string, but received:', text);
        messageDiv.textContent = 'Received an unexpected response format.';
      }
    } else {
      messageDiv.textContent = text;
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});
