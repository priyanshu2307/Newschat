import React, { useState } from 'react';

function ChatInput({ onSendMessage, isLoading }) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() === '' || isLoading) return;
    
    onSendMessage(message);
    setMessage('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex p-3">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        disabled={isLoading}
        placeholder="Type your message..."
        className="flex-grow px-4 py-2 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-primary-300"
      />
      <button
        type="submit"
        disabled={isLoading || message.trim() === ''}
        className={`px-6 py-2 rounded-r-lg font-medium ${
          isLoading || message.trim() === ''
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-primary-600 text-white hover:bg-primary-700'
        } transition-colors`}
      >
        Send
      </button>
    </form>
  );
}

export default ChatInput;