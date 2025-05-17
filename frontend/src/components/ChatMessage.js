import React from 'react';

function ChatMessage({ message }) {
  const { role, content } = message;
  
  // Determine message styling based on role
  const getMessageStyles = () => {
    switch (role) {
      case 'user':
        return {
          container: 'flex justify-end mb-4',
          bubble: 'bg-primary-600 text-white rounded-lg py-2 px-4 max-w-md',
          role: 'text-xs text-gray-500 text-right mr-2 mb-1'
        };
      case 'assistant':
        return {
          container: 'flex justify-start mb-4',
          bubble: 'bg-gray-200 text-gray-800 rounded-lg py-2 px-4 max-w-md',
          role: 'text-xs text-gray-500 ml-2 mb-1'
        };
      case 'system':
        return {
          container: 'flex justify-center mb-4',
          bubble: 'bg-red-100 text-red-700 rounded-lg py-2 px-4 max-w-md',
          role: 'hidden'
        };
      default:
        return {
          container: 'flex justify-start mb-4',
          bubble: 'bg-gray-200 text-gray-800 rounded-lg py-2 px-4 max-w-md',
          role: 'text-xs text-gray-500 ml-2 mb-1'
        };
    }
  };

  const styles = getMessageStyles();

  return (
    <div className={styles.container}>
      <div>
        <div className={styles.role}>
          {role === 'user' ? 'You' : role === 'assistant' ? 'NewsChat' : ''}
        </div>
        <div className={styles.bubble}>
          {content.split('\n').map((text, i) => (
            <React.Fragment key={i}>
              {text}
              {i !== content.split('\n').length - 1 && <br />}
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ChatMessage;