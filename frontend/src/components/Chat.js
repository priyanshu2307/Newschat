import React, { useState, useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { getSessionHistory, sendMessage, clearSession } from '../services/api';

function Chat({ sessionId, onResetSession }) {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Load chat history on mount and when sessionId changes
  useEffect(() => {
    const loadChatHistory = async () => {
      try {
        setIsLoading(true);
        const { history } = await getSessionHistory(sessionId);
        setMessages(history);
      } catch (error) {
        console.error('Error loading chat history:', error);
      } finally {
        setIsLoading(false);
      }
    };

    if (sessionId) {
      loadChatHistory();
    }
  }, [sessionId]);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Handle sending a message
  const handleSendMessage = async (message) => {
    try {
      // Optimistically update UI
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: 'user', content: message },
      ]);
      
      setIsLoading(true);
      
      // Send message to API
      const { response } = await sendMessage(sessionId, message);
      
      // Update with assistant response
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: 'assistant', content: response },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Show error in chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { 
          role: 'system', 
          content: 'Sorry, there was an error processing your message. Please try again.' 
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle clearing chat history
  const handleClearChat = async () => {
    try {
      await clearSession(sessionId);
      setMessages([]);
    } catch (error) {
      console.error('Error clearing chat history:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md overflow-hidden">
      <div className="flex justify-between items-center px-4 py-3 bg-gray-50 border-b">
        <h2 className="text-lg font-medium text-gray-700">Chat Session</h2>
        <div className="space-x-2">
          <button
            onClick={handleClearChat}
            className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors"
          >
            Clear Chat
          </button>
          <button
            onClick={onResetSession}
            className="px-3 py-1 text-sm bg-primary-600 text-white rounded hover:bg-primary-700 transition-colors"
          >
            New Session
          </button>
        </div>
      </div>
      
      <div className="h-[60vh] overflow-y-auto p-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-500">
            <p className="text-lg">Welcome to NewsChat!</p>
            <p className="mt-2">Ask me anything about the news articles.</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))
        )}
        {isLoading && (
          <div className="flex justify-center my-4">
            <div className="animate-bounce flex space-x-1">
              <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animation-delay-200"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animation-delay-400"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="border-t">
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
}

export default Chat;