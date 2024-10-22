// This file is currently empty, but you can add client-side functionality here if needed.
console.log('main.js loaded');

document.addEventListener('DOMContentLoaded', () => {
  const chatContainer = document.querySelector('.chat-container');
  const inputContainer = document.querySelector('.input-container');
  const sendButton = document.querySelector('#sendButton');
  const userInput = document.querySelector('#userInput');
  const headerTitle = document.querySelector('h1');

  let chatMessages;

  chatContainer.classList.add('empty');

  function sendMessage() {
    let message = userInput.value.trim();
    if (message === '') {
      return;
    }
    if (chatContainer.classList.contains('empty')) {
      chatContainer.classList.remove('empty');
      headerTitle.style.display = 'none';
      inputContainer.style.width = '80%';
      inputContainer.style.margin = '0';
      // Add these lines to move the input container to the bottom
      chatContainer.style.justifyContent = 'flex-end';
      inputContainer.style.position = 'fixed';
      inputContainer.style.bottom = '20px';
      inputContainer.style.left = '50%';
      inputContainer.style.transform = 'translateX(-50%)';
    }
    addMessage('user', message);
    userInput.value = '';
    fetchChatResponse(message);
  }


  sendButton.addEventListener('click', (event) => {
    event.preventDefault();
    sendMessage();
  });

  // Ensure the input is found and add the event listener
  if (userInput) {
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
  } else {
    console.error('User input not found');
  }

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
    if (!chatMessages) {
      chatMessages = document.createElement('div');
      chatMessages.id = 'chatMessages';
      chatContainer.insertBefore(chatMessages, inputContainer);
    }

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

    // Replace the existing scrollTop line with this:
    setTimeout(() => {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 0);
  }
});
