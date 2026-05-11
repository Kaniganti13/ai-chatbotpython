// backend/app/static/js/app.js

// Simple client-side chat logic
const messagesEl = document.getElementById('messages');
const inputEl = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const toggleThemeBtn = document.getElementById('toggleTheme');

// Keep chat history in memory (client-side only)
let chatHistory = [];

// Add a welcome message from AI on load
const WELCOME_TEXT = "Hello! I'm Aurora — your AI assistant. Ask me anything or say 'help' to get started.";

function createMessageElement({role, content, isTyping=false}) {
  const wrapper = document.createElement('div');
  wrapper.classList.add('msg', role === 'user' ? 'user' : 'bot');

  // Meta line
  const meta = document.createElement('div');
  meta.className = 'meta';
  meta.textContent = role === 'user' ? 'You' : 'Aurora';
  wrapper.appendChild(meta);

  // Content
  const contentEl = document.createElement('div');
  contentEl.className = 'content';
  if (isTyping) {
    // Typing animation
    const typing = document.createElement('div');
    typing.className = 'typing';
    typing.innerHTML = '<span></span><span></span><span></span>';
    contentEl.appendChild(typing);
  } else {
    contentEl.textContent = content;
  }
  wrapper.appendChild(contentEl);
  return wrapper;
}

function appendMessage(role, content, isTyping=false) {
  const el = createMessageElement({role, content, isTyping});
  messagesEl.appendChild(el);
  autoScroll();
  return el;
}

function autoScroll() {
  // Smooth scroll to bottom
  messagesEl.scrollTo({ top: messagesEl.scrollHeight, behavior: 'smooth' });
}

// Initialize with welcome message
window.addEventListener('load', () => {
  appendMessage('bot', WELCOME_TEXT);
  chatHistory.push({role: 'assistant', content: WELCOME_TEXT});
});

// Send message handler
async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;

  // Append user message
  appendMessage('user', text);
  chatHistory.push({role: 'user', content: text});
  inputEl.value = '';
  inputEl.style.height = 'auto';

  // Append bot typing indicator
  const typingEl = appendMessage('bot', '', true);

  // Show loading state on send button
  sendBtn.disabled = true;
  sendBtn.textContent = '...';

  try {
    // Call backend API
    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ message: text, history: chatHistory })
    });

    if (!resp.ok) {
      const err = await resp.json();
      throw new Error(err.detail || err.error || 'Server error');
    }

    const data = await resp.json();
    const reply = data.reply || 'Sorry, I did not get a response.';

    // Remove typing indicator and replace with actual content
    typingEl.querySelector('.content').textContent = reply;
    // Update chat history
    chatHistory.push({role: 'assistant', content: reply});
    autoScroll();

  } catch (err) {
    // Replace typing with error message
    typingEl.querySelector('.content').textContent = 'Error: ' + err.message;
  } finally {
    sendBtn.disabled = false;
    sendBtn.textContent = 'Send';
  }
}

// Enter key support and auto-resize textarea
inputEl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Auto-resize
inputEl.addEventListener('input', () => {
  inputEl.style.height = 'auto';
  inputEl.style.height = (inputEl.scrollHeight) + 'px';
});

// Send button
sendBtn.addEventListener('click', sendMessage);

// Clear chat
clearBtn.addEventListener('click', () => {
  messagesEl.innerHTML = '';
  chatHistory = [];
  appendMessage('bot', WELCOME_TEXT);
  chatHistory.push({role: 'assistant', content: WELCOME_TEXT});
});

// Theme toggle (dark/light)
toggleThemeBtn.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  document.body.classList.toggle('light');
});
