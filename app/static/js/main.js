

document.addEventListener('DOMContentLoaded', () => {
  const chatContainer = document.querySelector('.chat-container');
  const inputContainer = document.querySelector('.input-container');
  const sendButton = document.querySelector('#sendButton');
  const userInput = document.querySelector('#userInput');
  const headerTitle = document.getElementById('title');
  const headerSubtitle = document.getElementById('subtitle');
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
      headerSubtitle.style.display = 'none';
      inputContainer.style.width = '80%';
      inputContainer.style.margin = '0';

      chatContainer.style.justifyContent = 'flex-end';
      inputContainer.style.position = 'fixed';
      // inputContainer.style.bottom = '20px';
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
      chatContainer.appendChild(chatMessages);
    }

    var messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + sender;

    if (sender === 'ai') {
      if (typeof text === 'string') {
        const tableMatch = text.match(/<table[\s\S]*?<\/table>/);
        if (tableMatch) {
          text = tableMatch[0];
          messageDiv.classList.add('table');
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
